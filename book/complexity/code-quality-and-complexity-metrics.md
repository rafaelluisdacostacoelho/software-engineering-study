[Anterior](data-structures-and-big-o.md) | [Índice](../../SUMMARY.md) | [Próximo](../concurrency/concurrency-and-parallelism.md)

# Code Quality & Complexity Metrics — Medir para Melhorar

## Visão Geral e Contexto de Mercado

Em engenharia moderna (squads, CI/CD, microserviços), “qualidade” não é estética: é **previsibilidade**. Métricas de qualidade e complexidade existem para reduzir risco e custo:

- Menos bugs em produção
- Mudanças mais rápidas (menor lead time)
- Onboarding mais eficiente
- Menos regressões e retrabalho

O ponto sênior aqui é: **métrica não é objetivo; é instrumento**. Uma métrica ruim ou usada como KPI vira incentivo perverso (ex.: “100% coverage” e testes inúteis).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O mercado saiu de “linhas de código” e “coverage” como proxy de qualidade para métricas mais maduras: complexidade cognitiva, hotspots por churn, acoplamento, e análise de risco por área do código.

- **Padrões e Protocolos Usados no Mercado**
	- **Complexidade Ciclomática (McCabe):** número de caminhos independentes; útil para sinalizar funções difíceis de testar.
	- **Complexidade Cognitiva:** quão difícil é entender (penaliza nesting e fluxo mental).
	- **Acoplamento e Coesão:** risco de mudanças “em cascata”.
	- **Hotspots (churn + complexidade):** onde bugs tendem a aparecer.
	- **Coverage (com maturidade):** branch/line; complementado por **mutation testing**.
	- **Linters e analyzers:** regras de estilo + risco (nullability, concurrency, security).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em bases grandes, é comum ter “ilhas” de qualidade: alguns módulos excelentes e outros intocáveis. Métricas ajudam a priorizar refatoração, mas precisam ser alinhadas ao risco do negócio.

- **Performance e Manutenção**  
	- Rodar análise em CI pode ficar lento; é comum separar checks rápidos (PR) e checks profundos (nightly).
	- Métricas sem baseline e tendência viram ruído.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: módulos com alto churn e baixa cobertura.
	- Coverage: alto percentual com baixa efetividade (testes superficiais).
	- Flakiness: testes instáveis destroem confiança na pipeline.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- PR gate com regras simples: lint + unit + cobertura mínima em delta (diff coverage).
	- Nightly/weekly: análise profunda (Sonar, security scan, mutation em módulos críticos).
	- “Quality budgets”: limites por módulo (ex.: complexidade máxima por função, com exceções justificadas).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit tests focados em lógica e invariantes.
	- Integração para limites (DB/queue) e contratos.
	- E2E mínimo e direcionado por risco.

- **Métrica de Qualidade**  
	- Complexidade ciclomática/cognitiva por função
	- Hotspots (churn + complexidade)
	- Cobertura por branch (onde faz sentido)
	- Flaky rate (por suite)
	- Tempo de pipeline e tempo de feedback

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: reduzir complexidade cognitiva com guard clauses e extração de regras.

### Python

```python
def price(total_cents: int, country: str, is_vip: bool) -> int:
		if total_cents <= 0:
				raise ValueError("invalid total")
		if country not in {"BR", "US"}:
				raise ValueError("unsupported country")

		discount = 0
		if is_vip:
				discount += 5
		if total_cents >= 10_000:
				discount += 10
		if country == "BR":
				discount += 2

		return max(0, total_cents - (total_cents * discount // 100))
```

### C#

```csharp
public static int Price(int totalCents, string country, bool isVip)
{
		if (totalCents <= 0) throw new ArgumentException("invalid total");
		if (country is not ("BR" or "US")) throw new ArgumentException("unsupported");

		var discount = 0;
		if (isVip) discount += 5;
		if (totalCents >= 10_000) discount += 10;
		if (country == "BR") discount += 2;

		return Math.Max(0, totalCents - (totalCents * discount / 100));
}
```

### Go

```go
package pricing

import "fmt"

func Price(totalCents int, country string, isVIP bool) (int, error) {
		if totalCents <= 0 {
				return 0, fmt.Errorf("invalid total")
		}
		if country != "BR" && country != "US" {
				return 0, fmt.Errorf("unsupported country")
		}

		discount := 0
		if isVIP { discount += 5 }
		if totalCents >= 10_000 { discount += 10 }
		if country == "BR" { discount += 2 }

		price := totalCents - (totalCents*discount)/100
		if price < 0 { price = 0 }
		return price, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Métricas por tendência, não por foto:** compare com baseline.
- **Evite gamificação:** métricas como KPI de performance individual distorcem.
- **Hotspots primeiro:** combine churn + complexidade para priorizar.
- **Defina limites por contexto:** módulo crítico vs módulo experimental.
- **Qualidade é produto da cultura:** code review + padrões + ownership.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** pipelines de qualidade e segurança fazem parte da plataforma.
- **Pipelines CI/CD:** qualidade como gate (lint/test/scan) e relatórios automáticos.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** correlacionar incidentes com hotspots.
- **Testes e Infra-as-Code:** ambientes reprodutíveis para integrações e análise.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tendência de complexidade por módulo
- Flaky rate e tempo de pipeline
- Incidentes/bugs por área (quando possível)
- Churn e hotspots

---

## Frameworks e Ferramentas do Mercado

- **Python:** ruff, mypy, radon, pytest-cov
- **C#:** Roslyn analyzers, StyleCop, SonarAnalyzer, Coverlet
- **Go:** golangci-lint, govulncheck, go test -cover
- **Plataformas:** SonarQube/SonarCloud, CodeQL

---

## Recursos Avançados e Leituras Recomendadas

- Google Testing Blog (qualidade e práticas)
- Martin Fowler (refactoring, metrics, code smells)
- ThoughtWorks Tech Radar (ferramentas e tendências)

---

## FAQ Especialista

**Qual métrica é “a melhor”?**  
Não existe. Use um conjunto pequeno que gere decisões: hotspots, complexidade, flakiness e SLOs.

**Como usar coverage de forma saudável?**  
Use como sinal: cobertura em código crítico e em mudanças recentes (diff coverage). Combine com reviews e, se fizer sentido, mutation testing.

**Como reduzir complexidade sem reescrever tudo?**  
Refatoração incremental: extração de funções, reduzir nesting, criar abstrações por domínio, e atacar hotspots primeiro.

---

[Anterior](data-structures-and-big-o.md) | [Índice](../../SUMMARY.md) | [Próximo](../concurrency/concurrency-and-parallelism.md)
