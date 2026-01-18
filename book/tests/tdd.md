% Test-Driven Development (TDD) — Guia Avançado para Profissionais

[Anterior](../mission-critical/high-availability-fault-tolerance.md) | [Índice](../../SUMMARY.md) | [Próximo](bdd.md)

# Test-Driven Development (TDD) — Guia Avançado para Profissionais

## Visão Geral e Contexto de Mercado

Test-Driven Development (TDD) é uma prática de desenvolvimento onde você escreve um teste automatizado **antes** do código de produção, guiando o design por comportamento e feedback rápido. Em organizações modernas (squads ágeis, CI/CD, DevOps, microserviços), TDD funciona como um acelerador de qualidade quando aplicado com maturidade:

- Reduz retrabalho por regressão (especialmente em domínios críticos).
- Acelera o ciclo “build-measure-learn” ao dar confiança para refatorar.
- Melhora o design: APIs tendem a ficar mais simples, coesas e testáveis.

Quando aplicado em sistemas críticos (pagamentos, saúde, segurança), TDD ajuda a evitar que incidentes virem “custo fixo” do produto — mas ele não substitui testes de integração/contrato/e2e; ele complementa.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  Popularizado por Kent Beck e a comunidade XP, TDD evoluiu de uma prática “apenas unit tests” para um conjunto de técnicas de design e teste que convivem com BDD/ATDD, contract tests e pipelines modernos. Hoje, em times de alto desempenho, TDD é frequentemente combinado com code review rigoroso, linters, análise estática e observabilidade.

- **Padrões e Protocolos Usados no Mercado**
  - **Red-Green-Refactor:** teste falha → faz passar → refatora com segurança.
  - **Given-When-Then / Arrange-Act-Assert:** estrutura de teste para legibilidade.
  - **Test Doubles:** fakes, stubs, mocks e spies (com parcimônia).
  - **Contract Testing:** Pact (quando integrações entre serviços são relevantes).
  - **Mutation testing:** mede se testes realmente pegam defeitos (não só cobertura).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  Em codebases grandes, o risco é a suíte virar lenta e o time parar de rodar testes localmente. Isso mata o feedback loop. É comum precisar separar testes em camadas e rodar em paralelo.

- **Performance e Manutenção**  
  - Testes lentos (IO/DB/rede) travam pipelines; use isolamento.
  - Testes frágeis (asserts em detalhes internos) quebram a cada refactor.
  - Testes duplicados e sem intenção clara geram custo de manutenção.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  - **Flaky tests**: causam desconfiança e “ignore failures”.
  - Coverage alta pode ser placebo; o que importa é risco coberto.
  - Debt em testes aparece como acoplamento excessivo a mocks e fixtures pesadas.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Gate rápido: unit tests (TDD) + lint/typecheck.
  - Gate médio: integration tests por adaptador (DB, fila, HTTP).
  - Gate seletivo: contract tests (produtor/consumidor).
  - Gate mínimo: e2e para fluxos críticos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Prefira fakes in-memory para ports/repositórios em unit.
  - Use testcontainers para DB/Redis/Kafka em integração.
  - Evite “testes que só testam mocks”: faça asserts no comportamento e nos efeitos.

- **Métrica de Qualidade**  
  - Code coverage útil: branch/mutation (quando viável).
  - Flaky rate (quantidade de re-runs / instabilidade).
  - Tempo total de pipeline e tempo de unit tests.
  - Taxa de bugs em produção por área (correlação com cobertura de cenários).

---

## Exemplos Avançados (Python, C# e Go)

### Python

Exemplo com parametrização e isolamento de dependência (sem tocar infraestrutura real em unit tests).

```python
import pytest


def fizzbuzz(n: int) -> str:
	if n % 15 == 0:
		return "FizzBuzz"
	if n % 3 == 0:
		return "Fizz"
	if n % 5 == 0:
		return "Buzz"
	return str(n)


@pytest.mark.parametrize(
	"input, expected",
	[(3, "Fizz"), (5, "Buzz"), (15, "FizzBuzz"), (2, "2")],
)
def test_fizzbuzz(input: int, expected: str) -> None:
	assert fizzbuzz(input) == expected
```

```python
def test_side_effect_isolated_with_fake_repo():
	class FakeRepo:
		def __init__(self):
			self.saved = []

		def save(self, value: str) -> None:
			self.saved.append(value)

	repo = FakeRepo()
	repo.save("ok")
	assert repo.saved == ["ok"]
```

### C#

```csharp
using Xunit;

public static class Discount
{
	public static int Apply(int totalCents)
	{
		if (totalCents <= 0) throw new ArgumentOutOfRangeException(nameof(totalCents));
		return totalCents >= 10_000 ? (int)(totalCents * 0.9) : totalCents;
	}
}

public class DiscountTests
{
	[Fact]
	public void Apply_WhenTotalIsHigh_ShouldGive10PercentOff()
	{
		Assert.Equal(9000, Discount.Apply(10_000));
	}
}
```

### Go

```go
package calc

import "testing"

func Discount(totalCents int) int {
	if totalCents >= 10000 {
		return int(float64(totalCents) * 0.9)
	}
	return totalCents
}

func TestDiscount(t *testing.T) {
	t.Parallel()
	if got := Discount(10000); got != 9000 {
		t.Fatalf("expected 9000, got %d", got)
	}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Testes determinísticos, rápidos, repeatable.**
- Evite assert em detalhes internos (prefira comportamento observável).
- **Não use mocks como default:** use quando o custo do fake é alto ou a interação é o contrato.
- **Teste invariantes e bordas:** nulos, valores extremos, idempotência, reentrância.
- Cuidado com “coverage theatre”: 100% de coverage com testes fracos é pior que 70% bem pensado.
- Trate testes como produto: revisão, refactor e remoção do que não agrega.
- Quando um incidente acontece, converta em teste (onde fizer sentido) para evitar regressão.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** teste infra com ambientes efêmeros; mantenha unit tests independentes de cluster.
- **Pipelines CI/CD:** gates rápidos + paralelização (ex.: pytest-xdist, dotnet test com runsettings, `go test -p`).
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** Sonar, linters, relatórios automáticos, flake detection.
- **Testes e Infra-as-Code:** provisionamento para integração (DB, redis, kafka) com teardown automatizado.

---

## Métricas, Monitoramento e Melhoria Contínua

- Cobertura (branch/mutation quando possível), tempo de execução, flaky rate
- Relatórios automáticos por PR (tendência de falhas)
- Dashboards (CI) com tempo de pipeline e saúde da suíte
- Cultura de melhoria: guidelines, revisão de testes e “test debt backlog”

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest, pytest-cov, pytest-xdist, coverage.py, hypothesis
- **C#:** xUnit, NUnit, MSTest, Moq, NSubstitute, Coverlet
- **Go:** testing, testify, gomock, ginkgo/gomega
- **Ferramentas de integração:** GitHub Actions, Azure DevOps, Jenkins, SonarQube/SonarCloud

---

## Recursos Avançados e Leituras Recomendadas

- Kent Beck — TDD
- Martin Fowler — Test Pyramid / test smells
- Google Testing Blog (práticas escaláveis)
- _Working Effectively with Legacy Code_ (Michael Feathers)

---

## FAQ Especialista

**Como evitar “testes que só testam mocks”?**  
Use fakes para dependências e asserts no estado/efeito observável. Reserve mocks para checar um contrato de interação realmente importante (ex.: publicar evento com schema correto).

**TDD em sistemas legacy altamente acoplados?**  
Comece com characterization tests para capturar comportamento atual, depois refatore em pequenos passos, introduzindo seams e isolando dependências.

**Como vender investimento em TDD para a empresa?**  
Mostre custo de incidentes, redução de lead time de mudanças e previsibilidade do delivery. Use métricas do pipeline (tempo, falhas, regressões) para evidenciar ganho.

---

## Referências e Práticas do Mercado

- Kent Beck (TDD/XP)
- Martin Fowler (práticas e padrões de teste)
- ThoughtWorks Tech Radar (qualidade e engenharia)

---

[Anterior](../mission-critical/high-availability-fault-tolerance.md) | [Índice](../../SUMMARY.md) | [Próximo](bdd.md)
