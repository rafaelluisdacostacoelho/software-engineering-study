[Anterior](SOLID.md) | [Índice](../../SUMMARY.md) | [Próximo](SeparationOfConcerns.md)

# OCP — Open/Closed Principle (Aberto para Extensão, Fechado para Modificação) (Princípio)

## Visão Geral e Contexto de Mercado

OCP diz que módulos devem ser **abertos para extensão** e **fechados para modificação**. Na prática: você deve conseguir adicionar novos comportamentos com mudanças localizadas, sem editar repetidamente código estável e crítico.

Em sistemas de mercado, OCP reduz risco porque:

- mudanças em áreas estáveis geram regressões
- squads paralelos precisam evoluir sem conflitos constantes
- modularidade facilita testes e rollout gradual

OCP não é “nunca alterar código”: é projetar pontos de extensão com contratos claros quando a variação é real e recorrente.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	OCP surgiu com OO e foi popularizado no SOLID. Hoje, aparece como plugin architectures, policies/strategies, event handlers e adapters.

- **Padrões e Protocolos Usados no Mercado**
	- **Strategy/Policy:** extensão por composição.
	- **Observer/Event handlers:** extensão por novos handlers.
	- **Ports & Adapters:** extensão por novos adapters de infra.
	- **Feature flags:** extensão/variação controlada.
	- **Configuration-driven:** extensão por configuração (com cautela).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Pontos de extensão mal desenhados multiplicam testes e criam contratos ambíguos.

- **Performance e Manutenção**  
	OCP excessivo vira “framework interno”: indireção e plugins desnecessários.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: abstrações precoces.
	- Coverage: não testar extensões raras.
	- Flakiness: extensões que dependem de ordem/config global.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de contrato para pontos de extensão.
	- Governança: “como registrar uma extensão” e ownership.
	- Canary/flags para extensões novas.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: extensões isoladas.
	- Integração: wiring do registry/dispatcher.
	- E2E: fluxos críticos.

- **Métrica de Qualidade**  
	- Mudanças repetidas no mesmo arquivo/módulo (hotspot)
	- Número de conflitos em PR em áreas centrais
	- Tempo para adicionar uma nova variação com segurança

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: extensão por strategy para descontos.

### Python

```python
from dataclasses import dataclass
from typing import Protocol


class Discount(Protocol):
		def apply(self, total_cents: int) -> int: ...


@dataclass(frozen=True)
class NoDiscount:
		def apply(self, total_cents: int) -> int:
				return total_cents


@dataclass
class Checkout:
		discount: Discount

		def total(self, total_cents: int) -> int:
				return self.discount.apply(total_cents)
```

### C#

```csharp
public interface IDiscount { int Apply(int totalCents); }
public sealed class NoDiscount : IDiscount { public int Apply(int totalCents) => totalCents; }

public sealed class Checkout
{
		private readonly IDiscount _discount;
		public Checkout(IDiscount discount) => _discount = discount;
		public int Total(int totalCents) => _discount.Apply(totalCents);
}
```

### Go

```go
package checkout

type Discount func(totalCents int) int

func NoDiscount(totalCents int) int { return totalCents }

type Checkout struct{ Discount Discount }

func (c Checkout) Total(totalCents int) int { return c.Discount(totalCents) }
```

---

## Boas Práticas Sêniores e Armadilhas

- Abra pontos de extensão só onde a variação é real.
- Prefira composição (Strategy/Observer) a herança profunda.
- Documente contratos e forneça uma implementação default.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** extensões por config/flags exigem governança e observabilidade.
- **Pipelines CI/CD:** contract tests para plugins/strategies.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** monitorar uso/erro por extensão.
- **Testes e Infra-as-Code:** validar wiring e compatibilidade em ambientes efêmeros.

---

## Métricas, Monitoramento e Melhoria Contínua

- Hotspots (arquivos mais alterados) e conflitos
- Erros por extensão
- Tempo de rollout de extensões novas

---

## Frameworks e Ferramentas do Mercado

- Feature flags
- DI containers e registries
- Observabilidade (OpenTelemetry)

---

## Recursos Avançados e Leituras Recomendadas

- SOLID (Robert C. Martin)
- Martin Fowler: patterns de extensão

---

## FAQ Especialista

**OCP é sobre interfaces?**  
Frequentemente, mas não só. Também pode ser extensão via eventos, composição, configuração e pipelines.

**Como evitar overengineering?**  
Abra pontos de extensão depois que a variação se provar real (ou quando o risco de mudança é muito alto e previsível).

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](SOLID.md) | [Índice](../../SUMMARY.md) | [Próximo](SeparationOfConcerns.md)
