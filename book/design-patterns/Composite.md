[Anterior](Command.md) | [Índice](../../SUMMARY.md) | [Próximo](Decorator.md)

# Composite — Estruturas em Árvore com Interface Uniforme (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Composite permite tratar objetos individuais (*leaf*) e composições (*composite*) de forma uniforme por meio de uma interface comum. Na prática, isso habilita modelar relações “parte-todo” como árvores e escrever código que opera em qualquer nó sem `if/else` de tipo.

Em produtos e plataformas, Composite aparece com frequência em:

- **UI e layout:** árvore de componentes (renderização/medição/eventos).
- **Permissões e políticas:** grupos com membros e subgrupos.
- **Catálogos e bundles:** produtos compostos.
- **Arquivos e configs:** sistemas de arquivos, ASTs, árvores de configuração.
- **Pipelines:** etapas compostas (embora muitas vezes CoR/middleware seja melhor).

O ganho é extensibilidade e consistência. O risco é introduzir uma árvore “genérica demais” e esconder regras importantes.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF definiu Composite para árvores de objetos. Em arquiteturas modernas, ele continua relevante quando a árvore é parte do domínio (ex.: “organizational units”), ou parte do runtime (ex.: UI/component tree).

- **Padrões e Protocolos Usados no Mercado**
	- **Component interface:** operações comuns (`Cost()`, `Render()`, `Evaluate()`).
	- **Leaf vs Composite:** folhas não possuem filhos; composites agregam.
	- **Transparente vs Seguro:**
		- Transparente: `Add/Remove/GetChild` na interface comum (mais simples, menos seguro).
		- Seguro: operações de composição só em `Composite` (mais seguro, mais casting).
	- **Traversal:** recursivo, iterativo, visitors.
	- **Imutabilidade:** árvore imutável quando precisa concorrência/consistência.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Árvores crescem e combinam estados. Você precisa testar:
	- regras de agregação (soma, validação, propagação)
	- travessias (ordem, filtros)
	- invariantes (ex.: sem ciclos, sem duplicidade)

- **Performance e Manutenção**  
	- Recursão pode estourar stack em árvores profundas.
	- Operações agregadas podem virar $O(n)$ por chamada (cache/memoization pode ajudar).
	- Mutabilidade ingênua pode causar bugs de consistência (ex.: múltiplos pais).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: interface “component” inchada (“god interface”) para atender folhas e composites.
	- Coverage: não cobrir casos de borda (árvore vazia, nó único, profundidade extrema).
	- Flakiness: quando travessia depende de ordem não-determinística (ex.: map/dict).

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de propriedades/invariantes (ex.: “árvore nunca tem ciclo”).
	- Benchmarks para operações agregadas usadas em hot paths.
	- Linters/analyzers para evitar recursão não-limitada em caminhos críticos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: folhas e composites isolados.
	- Integração: montar árvores reais com regras e validar agregações.
	- E2E: raro para o padrão em si; relevante quando a árvore é central no produto (ex.: editor/GUI).

- **Métrica de Qualidade**  
	- Tempo de travessia (p95/p99) e tamanho médio da árvore
	- Taxa de invalidações/cache hits (se houver memoization)
	- Número de bugs por inconsistência estrutural (ciclos/duplicidade)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: política de autorização onde um nó pode ser uma regra (leaf) ou um grupo de regras (composite).

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Rule(Protocol):
		def allows(self, ctx: dict) -> bool:
				...


@dataclass(frozen=True)
class HasRole:
		role: str

		def allows(self, ctx: dict) -> bool:
				return self.role in ctx.get("roles", [])


@dataclass(frozen=True)
class AllOf:
		children: tuple[Rule, ...]

		def allows(self, ctx: dict) -> bool:
				return all(child.allows(ctx) for child in self.children)


@dataclass(frozen=True)
class AnyOf:
		children: tuple[Rule, ...]

		def allows(self, ctx: dict) -> bool:
				return any(child.allows(ctx) for child in self.children)
```

### C#

```csharp
public interface IRule
{
		bool Allows(Context ctx);
}

public sealed record HasRole(string Role) : IRule
{
		public bool Allows(Context ctx) => ctx.Roles.Contains(Role);
}

public sealed class AllOf : IRule
{
		private readonly IReadOnlyList<IRule> _children;
		public AllOf(IReadOnlyList<IRule> children) => _children = children;

		public bool Allows(Context ctx) => _children.All(r => r.Allows(ctx));
}

public sealed class AnyOf : IRule
{
		private readonly IReadOnlyList<IRule> _children;
		public AnyOf(IReadOnlyList<IRule> children) => _children = children;

		public bool Allows(Context ctx) => _children.Any(r => r.Allows(ctx));
}
```

### Go

```go
package rules

type Ctx struct{
		Roles map[string]bool
}

type Rule interface {
		Allows(ctx Ctx) bool
}

type HasRole struct{ Role string }

func (r HasRole) Allows(ctx Ctx) bool { return ctx.Roles[r.Role] }

type AllOf struct{ Children []Rule }

func (a AllOf) Allows(ctx Ctx) bool {
		for _, child := range a.Children {
				if !child.Allows(ctx) {
						return false
				}
		}
		return true
}

type AnyOf struct{ Children []Rule }

func (a AnyOf) Allows(ctx Ctx) bool {
		for _, child := range a.Children {
				if child.Allows(ctx) {
						return true
				}
		}
		return false
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Mantenha a interface pequena.** Se a interface do componente começar a crescer demais, considere separar responsabilidades.
- **Evite ciclos:** defina invariantes (um nó não pode ser filho de si mesmo; um nó tem um único pai, etc.).
- **Cuidado com mutabilidade compartilhada:** se múltiplos pais referenciam o mesmo nó, alterações podem vazar.
- **Garanta determinismo em travessias:** especialmente se houver serialização, logs ou hashing.
- **Use caching/memoization com invalidation explícita** quando operações agregadas forem caras.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** quando o Composite modela regras/políticas, ele pode rodar como parte do serviço; foque em limites de CPU/memória para árvores grandes.
- **Pipelines CI/CD:** testes de invariantes e performance; verificação de regressões quando a árvore é construída a partir de config.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** métricas de tamanho/profundidade; tracing em operações de travessia.
- **Testes e Infra-as-Code:** se árvores são derivadas de config (YAML/JSON), valide schema + compatibilidade.

---

## Métricas, Monitoramento e Melhoria Contínua

- Distribuição do tamanho/profundidade das árvores
- Tempo de avaliação/agregação
- Cache hit rate e invalidation rate (se aplicável)
- Erros de validação estrutural (ciclos, nós duplicados)

---

## Frameworks e Ferramentas do Mercado

- **Serialização/Schema:** JSON Schema, Protobuf/Avro (dependendo do domínio)
- **Observabilidade:** OpenTelemetry para medir tempo de travessia e gargalos

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Composite
- Discussões sobre árvores imutáveis e visitors
- Modelagem de políticas (RBAC/ABAC) com composição

---

## FAQ Especialista

**Composite sempre implica recursão?**  
Não. Você pode atravessar iterativamente com uma pilha/fila para evitar stack overflow e controlar melhor a ordem.

**Quando evitar Composite?**  
Quando você não precisa tratar folha e composição da mesma forma, ou quando a “árvore” é um detalhe de armazenamento e não do domínio (a abstração pode ficar artificial).

**Como lidar com operações diferentes em folhas e composites?**  
Tente reduzir a interface comum ao mínimo e, se necessário, use double-dispatch/Visitor ou APIs separadas (transparente vs seguro).

---

[Anterior](Command.md) | [Índice](../../SUMMARY.md) | [Próximo](Decorator.md)
