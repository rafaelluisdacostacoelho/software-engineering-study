[Anterior](State.md) | [Índice](../../SUMMARY.md) | [Próximo](TemplateMethod.md)

# Strategy — Algoritmos Intercambiáveis por Composição (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Strategy define uma família de algoritmos/políticas e permite trocar o comportamento em runtime (ou por configuração) sem alterar o código do “context”. Em vez de um `switch` por tipo, você injeta uma estratégia.

No mercado, Strategy aparece o tempo todo em:

- **Políticas de preço/frete:** regras variáveis por segmento/país/campanha.
- **Autenticação/autorização:** múltiplos provedores (OIDC, SAML, API key).
- **Roteamento e seleção de providers:** escolher gateway de pagamento/antifraude.
- **Algoritmos de cache/backoff/retry:** políticas variáveis por endpoint.
- **Feature flags/experimentos:** trocar comportamento sem redeploy.

O ganho é extensibilidade e testabilidade. O risco é criar “estratégias demais” sem governança e com contratos ambíguos.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Strategy é GoF clássico. Em código moderno, ele também aparece como funções de alta ordem (Python/Go) e delegates (C#). A ideia continua: separar política (variável) do fluxo (estável).

- **Padrões e Protocolos Usados no Mercado**
	- **Context + Strategy interface:** `Context` delega para `Strategy`.
	- **Config-driven strategies:** escolha por config/feature flag.
	- **Default strategy:** comportamento padrão explícito.
	- **Composição de strategies:** wrappers (Decorator) para cross-cutting.
	- **Teste de contrato:** todas as strategies devem obedecer invariantes.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O problema real não é “criar classes”, é manter consistência. Você precisa testar:
	- contrato mínimo da interface
	- matriz de seleção (quando a strategy é escolhida)
	- cenários de borda para cada policy

- **Performance e Manutenção**  
	- Selection logic (factory/registry) pode virar `if/else` gigante.
	- Strategies podem duplicar regras, divergindo com o tempo.
	- Overhead de indireção é pequeno, mas existe em hot paths.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: “strategy” vira nome para qualquer classe e perde significado.
	- Coverage: não testar estratégias raras (mas críticas em incidentes).
	- Flakiness: estratégias dependentes de tempo/serviço externo sem controle em testes.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests por strategy (mesma suite roda para todas).
	- Testes por configuração (matrix testing) para flags/tenant/region.
	- Deploy gradual para strategies novas (canary/flag).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: strategies puras, sem IO.
	- Integração: quando a strategy chama infra (ex.: provider externo).
	- E2E: poucos fluxos críticos para validar seleção e compatibilidade.

- **Métrica de Qualidade**  
	- Frequência de uso por strategy (telemetria)
	- Erros/latência por strategy
	- Cobertura da matriz de seleção

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: política de cálculo de frete.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ShippingStrategy(Protocol):
		def quote_cents(self, weight_grams: int, distance_km: int) -> int:
				...


@dataclass(frozen=True)
class FlatRate:
		cents: int

		def quote_cents(self, weight_grams: int, distance_km: int) -> int:
				return self.cents


@dataclass(frozen=True)
class WeightBased:
		base: int
		per_kg: int

		def quote_cents(self, weight_grams: int, distance_km: int) -> int:
				kg = (weight_grams + 999) // 1000
				return self.base + kg * self.per_kg


@dataclass
class ShippingService:
		strategy: ShippingStrategy

		def quote(self, weight_grams: int, distance_km: int) -> int:
				if weight_grams <= 0:
						raise ValueError("weight_grams must be > 0")
				return self.strategy.quote_cents(weight_grams, distance_km)
```

### C#

```csharp
public interface IShippingStrategy
{
		int QuoteCents(int weightGrams, int distanceKm);
}

public sealed class FlatRate : IShippingStrategy
{
		private readonly int _cents;
		public FlatRate(int cents) => _cents = cents;
		public int QuoteCents(int weightGrams, int distanceKm) => _cents;
}

public sealed class ShippingService
{
		private readonly IShippingStrategy _strategy;
		public ShippingService(IShippingStrategy strategy) => _strategy = strategy;

		public int Quote(int weightGrams, int distanceKm)
		{
				if (weightGrams <= 0) throw new ArgumentException("weightGrams must be > 0");
				return _strategy.QuoteCents(weightGrams, distanceKm);
		}
}
```

### Go

```go
package shipping

import "fmt"

type Strategy interface {
		QuoteCents(weightGrams int, distanceKm int) (int, error)
}

type FlatRate struct{ Cents int }

func (f FlatRate) QuoteCents(weightGrams int, distanceKm int) (int, error) {
		if weightGrams <= 0 {
				return 0, fmt.Errorf("weightGrams must be > 0")
		}
		return f.Cents, nil
}

type Service struct{ Strategy Strategy }

func (s Service) Quote(weightGrams int, distanceKm int) (int, error) {
		return s.Strategy.QuoteCents(weightGrams, distanceKm)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Defina contratos e invariantes.** Strategies devem concordar em regras básicas.
- **Evite selection logic gigante:** mova seleção para factory/registry bem testado.
- **Instrumente:** log/metric por strategy ativa (para debug e custo).
- **Cuidado com “strategy de infra”:** se chama rede, trate timeouts/retries e idempotência.
- **Não crie strategy por modismo:** use quando há variação real e provável.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** strategies com IO precisam budgets (timeouts) para evitar amplificação de carga.
- **Pipelines CI/CD:** matrix testing por config/flag; contract tests por strategy.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards por strategy (erro/latência/custo).
- **Testes e Infra-as-Code:** ambientes efêmeros para providers externos (quando viável) ou stubs determinísticos.

---

## Métricas, Monitoramento e Melhoria Contínua

- Erros/latência por strategy
- Distribuição de tráfego por strategy
- Drift de regras (diferenças detectadas por testes de contrato)

---

## Frameworks e Ferramentas do Mercado

- **Feature flags:** LaunchDarkly/Unleash (para seleção)
- **Observabilidade:** OpenTelemetry
- **DI:** containers (C#) / wiring manual (Go) / factories (Python)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Strategy
- Guidelines de design por composição
- Patterns de seleção por config/flags

---

## FAQ Especialista

**Strategy vs State: quando usar cada um?**  
Use Strategy para algoritmos intercambiáveis sem transições internas. Use State quando há máquina de estados e transições explícitas.

**Como evitar explosão de strategies?**  
Mantenha governança: naming, ownership, testes de contrato e telemetria de uso. Remova strategies não usadas.

**Strategy pode virar “switch escondido”?**  
Sim, se a seleção for confusa. Centralize seleção e torne o critério explícito e testado.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](State.md) | [Índice](../../SUMMARY.md) | [Próximo](TemplateMethod.md)
