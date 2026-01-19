[Anterior](Strategy.md) | [Índice](../../SUMMARY.md) | [Próximo](Visitor.md)

# Template Method — Esqueleto de Algoritmo com Pontos de Extensão (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Template Method define o esqueleto de um algoritmo (passos fixos) e permite que subclasses/implementações forneçam variações em etapas específicas (hooks). O objetivo é padronizar o fluxo e evitar duplicação, mantendo pontos de extensão controlados.

No mercado, é comum ver esse padrão em:

- **Pipelines de processamento:** importar/validar/transformar/persistir.
- **Frameworks:** lifecycle hooks (startup, before/after).
- **Integrações:** fluxo fixo com variações por provider.
- **Processos de negócio:** etapas invariantes com regras parametrizáveis.

Em stacks modernas, Template Method muitas vezes vira composição (Strategy + pipeline), mas continua útil quando o fluxo é invariável e você quer evitar que variações “quebrem” a sequência.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF popularizou Template Method em OO clássico. Hoje, composição e funções de alta ordem frequentemente substituem herança, mas a ideia de “fluxo fixo com hooks” permanece (middlewares, pipelines e callbacks).

- **Padrões e Protocolos Usados no Mercado**
	- **Método template:** define a sequência e chama hooks.
	- **Hooks/steps protegidos:** subclasses implementam etapas.
	- **Invariantes:** o template garante ordem e validações.
	- **NVI (Non-Virtual Interface):** método público não-virtual chama métodos internos virtuais.
	- **Composição alternativa:** Template Method pode ser implementado com funções/strategies.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Herança cria acoplamento implícito. Testes precisam validar:
	- o fluxo completo
	- cada hook isoladamente
	- garantias (o hook não pode pular validações)

- **Performance e Manutenção**  
	- Muitos templates/subclasses podem virar uma hierarquia difícil.
	- Mudanças no template impactam todas as subclasses.
	- Excesso de hooks vira “framework interno” confuso.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: override que altera invariantes silenciosamente.
	- Coverage: não testar subclasses raras.
	- Flakiness: hooks com IO/tempo sem isolamento.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de contrato: toda implementação de hook deve passar a mesma suite.
	- Regras de lint para evitar overrides perigosos.
	- Documentar invariantes e “não mexer” no template.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: hooks isolados.
	- Integração: fluxo completo com dependências reais/efêmeras.
	- E2E: apenas fluxos críticos do produto.

- **Métrica de Qualidade**  
	- Duplicação reduzida vs. complexidade da hierarquia
	- Incidentes por variações fora do contrato
	- Tempo de manutenção para adicionar uma nova variante

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: pipeline de importação onde o fluxo é fixo, mas parse/validação variam.

### Python

```python
from __future__ import annotations

from abc import ABC, abstractmethod


class ImportTemplate(ABC):
		def run(self, raw: str) -> dict:
				parsed = self.parse(raw)
				self.validate(parsed)
				result = self.persist(parsed)
				self.after_persist(result)
				return result

		@abstractmethod
		def parse(self, raw: str) -> dict:
				raise NotImplementedError

		def validate(self, parsed: dict) -> None:
				if "id" not in parsed:
						raise ValueError("missing id")

		@abstractmethod
		def persist(self, parsed: dict) -> dict:
				raise NotImplementedError

		def after_persist(self, result: dict) -> None:
				return
```

### C#

```csharp
public abstract class ImportTemplate
{
		public async Task<Result> Run(string raw, CancellationToken ct)
		{
				var parsed = Parse(raw);
				Validate(parsed);
				var result = await Persist(parsed, ct);
				AfterPersist(result);
				return result;
		}

		protected abstract Parsed Parse(string raw);
		protected virtual void Validate(Parsed parsed) { /* invariantes */ }
		protected abstract Task<Result> Persist(Parsed parsed, CancellationToken ct);
		protected virtual void AfterPersist(Result result) { }
}
```

### Go

```go
package pipeline

type Parse func(raw string) (map[string]any, error)
type Validate func(parsed map[string]any) error
type Persist func(parsed map[string]any) (map[string]any, error)
type After func(result map[string]any)

type Template struct {
		Parse    Parse
		Validate Validate
		Persist  Persist
		After    After
}

func (t Template) Run(raw string) (map[string]any, error) {
		parsed, err := t.Parse(raw)
		if err != nil { return nil, err }
		if t.Validate != nil {
				if err := t.Validate(parsed); err != nil { return nil, err }
		}
		result, err := t.Persist(parsed)
		if err != nil { return nil, err }
		if t.After != nil { t.After(result) }
		return result, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Defina invariantes no template** e evite permitir que hooks as burlem.
- **Prefira composição** quando herança começar a crescer (muitas variantes).
- **Nomeie hooks pelo objetivo** (ex.: `after_persist`) e mantenha-os pequenos.
- **Use NVI** quando quiser proteger o fluxo (método público não-virtual).
- **Evite “framework interno”:** se há hooks demais, repense o design.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** templates de pipeline podem precisar de timeouts e backpressure quando fazem IO.
- **Pipelines CI/CD:** suites de contrato para variantes; regressão quando o template muda.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing por etapa/hook; métricas por passo.
- **Testes e Infra-as-Code:** ambientes efêmeros para validar persistência e integrações.

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência por etapa do template
- Erros por etapa/hook
- Número de variantes e custo de manutenção
- Duplicação evitada vs complexidade adicional

---

## Frameworks e Ferramentas do Mercado

- **C#:** base classes + NVI, pipelines e middlewares (alternativas)
- **Python:** classes abstratas, hooks; frameworks com signals
- **Go:** composição por funções, pipelines e middlewares

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Template Method
- Discussões sobre herança vs composição
- NVI (Non-Virtual Interface) em C++/OO (conceito aplicável)

---

## FAQ Especialista

**Template Method não incentiva herança (que queremos evitar)?**  
Sim. Use quando o fluxo é realmente invariável e há poucas variantes. Caso contrário, prefira Strategy/composição.

**Como evitar que uma subclass quebre o fluxo?**  
Use NVI: método público final chama hooks protegidos. Documente invariantes e teste com suíte de contrato.

**Quando migrar para composição?**  
Quando o número de variantes cresce, hooks se multiplicam e a hierarquia vira difícil de entender/manter.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Strategy.md) | [Índice](../../SUMMARY.md) | [Próximo](Visitor.md)
