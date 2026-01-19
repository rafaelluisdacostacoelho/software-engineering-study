[Anterior](template-method.md) | [Índice](../../SUMMARY.md) | [Próximo](../complexity/data-structures-and-big-o.md)

# Visitor — Adicionar Operações sem Alterar a Estrutura (Double Dispatch) (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Visitor permite adicionar novas operações sobre uma estrutura de objetos (tipicamente uma árvore/AST) sem modificar as classes dessa estrutura. Ele faz isso via **double dispatch**: o elemento aceita um visitor e delega para o método específico daquele tipo.

No mercado, Visitor aparece principalmente em:

- **Compiladores/ASTs:** pretty-print, type-check, codegen.
- **Árvores de documentos:** renderização, validação, export.
- **Modelos complexos:** aplicar múltiplas operações sobre a mesma estrutura.

Ele não é tão comum em serviços de negócio quanto Strategy/Decorator, mas continua útil em domínios onde a estrutura é estável e as operações mudam com frequência.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Visitor é GoF clássico. Em linguagens modernas, pattern matching/ADTs podem substituir parte do padrão. Em OOP, Visitor ainda é relevante para separar operações e preservar encapsulamento.

- **Padrões e Protocolos Usados no Mercado**
	- **Element.Accept(visitor):** ponto único de entrada.
	- **Visitor.VisitX(element):** operação por tipo.
	- **Double dispatch:** resolve dinamicamente por tipo de visitor e elemento.
	- **Extensibilidade:** fácil adicionar novas operações (novos visitors), difícil adicionar novos tipos de elemento (exige atualizar visitors).
	- **Traversal:** visitor pode controlar travessia (pré/pós-ordem).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Muitas classes + muitos visitors = matriz grande. Testes precisam garantir:
	- cobertura de tipos de elementos
	- comportamento em travessias complexas
	- consistência de resultados (ex.: render determinístico)

- **Performance e Manutenção**  
	- Boilerplate aumenta com o número de tipos.
	- Mudanças na estrutura (novo tipo) “quebram” todos os visitors.
	- Pode ficar verboso e difícil para onboarding.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: visitors gigantes e sem coesão.
	- Coverage: não testar tipos raros (mas críticos).
	- Flakiness: travessia não determinística (ordem de children) afetando saída.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Suites de teste por visitor e por tipo de elemento.
	- Snapshot tests para renderização/pretty-print.
	- Contratos para garantir que todo elemento implementa `Accept` e está coberto.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: cada `VisitX` isolado.
	- Integração: travessia completa em árvores reais.
	- E2E: raramente necessário (a não ser que Visitor esteja em uma pipeline maior).

- **Métrica de Qualidade**  
	- Número de tipos de elemento vs número de visitors
	- Cobertura por tipo/visitor
	- Tempo de execução de travessias (p95/p99)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: AST simples com `Number` e `Add`, e um visitor para avaliação.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Visitor(Protocol):
		def visit_number(self, n: "Number") -> int: ...
		def visit_add(self, a: "Add") -> int: ...


class Expr(Protocol):
		def accept(self, v: Visitor) -> int: ...


@dataclass(frozen=True)
class Number:
		value: int

		def accept(self, v: Visitor) -> int:
				return v.visit_number(self)


@dataclass(frozen=True)
class Add:
		left: Expr
		right: Expr

		def accept(self, v: Visitor) -> int:
				return v.visit_add(self)


class Eval:
		def visit_number(self, n: Number) -> int:
				return n.value

		def visit_add(self, a: Add) -> int:
				return a.left.accept(self) + a.right.accept(self)
```

### C#

```csharp
public interface IExpr
{
		T Accept<T>(IVisitor<T> v);
}

public interface IVisitor<T>
{
		T VisitNumber(Number n);
		T VisitAdd(Add a);
}

public sealed record Number(int Value) : IExpr
{
		public T Accept<T>(IVisitor<T> v) => v.VisitNumber(this);
}

public sealed record Add(IExpr Left, IExpr Right) : IExpr
{
		public T Accept<T>(IVisitor<T> v) => v.VisitAdd(this);
}

public sealed class Eval : IVisitor<int>
{
		public int VisitNumber(Number n) => n.Value;
		public int VisitAdd(Add a) => a.Left.Accept(this) + a.Right.Accept(this);
}
```

### Go

```go
package ast

type Visitor interface {
		VisitNumber(n Number) int
		VisitAdd(a Add) int
}

type Expr interface {
		Accept(v Visitor) int
}

type Number struct{ Value int }
func (n Number) Accept(v Visitor) int { return v.VisitNumber(n) }

type Add struct{ Left, Right Expr }
func (a Add) Accept(v Visitor) int { return v.VisitAdd(a) }

type Eval struct{}
func (Eval) VisitNumber(n Number) int { return n.Value }
func (Eval) VisitAdd(a Add) int { return a.Left.Accept(Eval{}) + a.Right.Accept(Eval{}) }
```

---

## Boas Práticas Sêniores e Armadilhas

- **Visitor é ótimo quando a estrutura é estável e operações variam.** Se você adiciona tipos de elementos com frequência, ele dói.
- **Evite visitors gigantes:** divida por responsabilidade (Eval, PrettyPrint, Validate).
- **Travessia determinística:** preserve ordem de filhos para outputs estáveis.
- **Considere alternativas modernas:** pattern matching/ADTs, dependendo da linguagem.
- **Cuidado com encapsulamento:** visitor pode exigir expor dados internos demais.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** normalmente irrelevante; o impacto é mais sobre performance e memória em pipelines.
- **Pipelines CI/CD:** snapshot tests para outputs; regressões ao adicionar novos tipos.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** métricas de tempo de travessia e tamanho de árvores.
- **Testes e Infra-as-Code:** quando AST/trees vêm de config, valide schema e compatibilidade.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de travessia por tipo de visitor
- Tamanho/profundidade média das árvores
- Cobertura por tipo de elemento

---

## Frameworks e Ferramentas do Mercado

- **C#:** visitors tipados, pattern matching como alternativa parcial
- **Python:** protocols/duck typing; `functools.singledispatch` como alternativa
- **Go:** interfaces e type switches (alternativa), geração de código para reduzir boilerplate

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Visitor
- AST design e compiladores
- Alternativas: pattern matching, ADTs, `singledispatch`

---

## FAQ Especialista

**Visitor é bom para código de domínio de negócios?**  
Raramente. Ele brilha mais em árvores/ASTs e estruturas estáveis. Em domínio de negócio, Strategy/State costumam ser mais naturais.

**Por que é difícil adicionar um novo tipo de elemento?**  
Porque cada visitor precisa aprender a lidar com esse novo tipo. Isso é o trade-off central do padrão.

**O que usar em Python no lugar de Visitor?**  
Muitas vezes `singledispatch` ou pattern matching (quando disponível) dá um resultado mais simples, mantendo operações separadas.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](template-method.md) | [Índice](../../SUMMARY.md) | [Próximo](../complexity/data-structures-and-big-o.md)
