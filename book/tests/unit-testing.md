[Anterior](bdd.md) | [Índice](../../SUMMARY.md) | [Próximo](../career/system-design-interview.md)

# Unit Testing — Testes Unitários (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Testes unitários são a base do feedback rápido em engenharia de software: validam comportamento de **unidades pequenas** (funções, classes, casos de uso) de forma determinística e sem dependências externas. Em times profissionais com CI/CD, unit tests bem desenhados:

- Aumentam confiança para refatorar (reduzindo regressões).
- Diminuem custo de incidentes ao capturar falhas antes do deploy.
- Melhoram design (interfaces mais simples, coesão maior, acoplamento menor).

No mercado, o valor aparece quando unit tests não são “checklist”, mas sim uma forma de **proteger invariantes** e documentar comportamentos críticos.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Unit testing ganhou escala com práticas ágeis/XP e se consolidou com automação em pipelines. Com a evolução para microserviços e arquiteturas baseadas em contratos, unit tests continuam essenciais, mas convivem com integration/contract/e2e.

- **Padrões e Protocolos Usados no Mercado**
	- **Arrange-Act-Assert (AAA)** / Given-When-Then.
	- **Test Doubles:** fake, stub, spy, mock (use com intenção).
	- **Property-based testing:** valida propriedades invariantes (Hypothesis/QuickCheck-like).
	- **Arquiteturas testáveis:** Hexagonal/Onion/Clean favorecem unit tests rápidos no core.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em codebases grandes, a suíte pode ficar lenta ou redundante. O desafio é manter testes unitários como “fast lane” e controlar o crescimento (duplicação, fixtures pesadas).

- **Performance e Manutenção**  
	- Testes acoplados à implementação quebram com refactors.
	- Setup complexo reduz legibilidade e aumenta custo.
	- Tests que tocam IO (rede/DB) deixam de ser unit e viram flaky.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Flakiness: frequentemente vem de tempo/aleatoriedade/shared state.
	- Debt: testes com mocks demais (testando interações internas) e pouco comportamento.
	- Coverage: “linha coberta” não garante risco coberto.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Rode unit tests sempre em PR.
	- Paralelize e mantenha tempos baixos (segundos/minutos, não dezenas de minutos).
	- Faça fail-fast e reporte granular (qual teste, qual contexto).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: sem DB, sem rede, sem tempo real (use `Clock`/injeção de tempo).
	- Integração: valida adapters e wiring.
	- Contrato/e2e: cobre fluxos críticos e compatibilidade.

- **Métrica de Qualidade**  
	- Tempo de execução da suíte unitária
	- Taxa de flakiness (ideal: ~0)
	- Mutation score (quando aplicável)
	- Densidade de bugs por módulo (correlação com testes)

---

## Exemplos Avançados (Python, C# e Go)

### Python

```python
import pytest


def normalize_email(email: str) -> str:
		email = email.strip().lower()
		if "@" not in email:
				raise ValueError("invalid email")
		return email


@pytest.mark.parametrize(
		"raw, expected",
		[(" User@Example.com ", "user@example.com"), ("a@b.com", "a@b.com")],
)
def test_normalize_email(raw: str, expected: str) -> None:
		assert normalize_email(raw) == expected


def test_normalize_email_invalid() -> None:
		with pytest.raises(ValueError):
				normalize_email("invalid")
```

### C#

```csharp
using Xunit;

public static class Email
{
		public static string Normalize(string email)
		{
				var normalized = email.Trim().ToLowerInvariant();
				if (!normalized.Contains("@")) throw new ArgumentException("invalid email");
				return normalized;
		}
}

public class EmailTests
{
		[Fact]
		public void Normalize_ShouldTrimAndLower()
				=> Assert.Equal("user@example.com", Email.Normalize(" User@Example.com "));

		[Fact]
		public void Normalize_Invalid_ShouldThrow()
				=> Assert.Throws<ArgumentException>(() => Email.Normalize("invalid"));
}
```

### Go

```go
package email

import (
		"strings"
		"testing"
)

func Normalize(raw string) (string, bool) {
		s := strings.ToLower(strings.TrimSpace(raw))
		if !strings.Contains(s, "@") {
				return "", false
		}
		return s, true
}

func TestNormalize(t *testing.T) {
		t.Parallel()
		got, ok := Normalize(" User@Example.com ")
		if !ok || got != "user@example.com" {
				t.Fatalf("expected user@example.com, got %q (ok=%v)", got, ok)
		}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Teste comportamento observável e invariantes**, não detalhes internos.
- **Evite shared state**: cada teste deve ser independente.
- **Controle tempo e aleatoriedade**: injete `Clock`/seed.
- Use mocks com intenção; fakes costumam ser mais estáveis.
- **Nomes claros**: descreva cenário e expectativa.
- Trate testes como código de produção (refactor, revisão e remoção do que não agrega).

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** unit tests não dependem de cluster; integração sim.
- **Pipelines CI/CD:** unit tests como gate rápido; integração/contrato como gates progressivos.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** qualidade como pipeline (linters + testes + relatórios).
- **Testes e Infra-as-Code:** mantenha provisionamento para integrações fora da suíte unitária.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo da suíte unitária (por PR)
- Flaky rate
- Mutation score (quando aplicável)
- Tendência de falhas por módulo

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest, unittest, hypothesis, coverage.py
- **C#:** xUnit, NUnit, MSTest, Moq/NSubstitute, Coverlet
- **Go:** testing, testify, gomock
- **Ferramentas de integração:** GitHub Actions, Azure DevOps, Jenkins, SonarQube/SonarCloud

---

## Recursos Avançados e Leituras Recomendadas

- _xUnit Test Patterns_ (Gerard Meszaros)
- Martin Fowler — test smells
- Google Testing Blog
- _Working Effectively with Legacy Code_ (Michael Feathers)

---

## FAQ Especialista

**Quando um teste deixa de ser unitário?**  
Quando depende de IO externo (DB, rede, filesystem compartilhado) ou de tempo real. Aí ele passa a ser integração/e2e e precisa de outra estratégia.

**Mocks ou fakes?**  
Fakes tendem a ser mais estáveis e expressivos; mocks são úteis para validar contratos de interação específicos (ex.: publicar um evento), mas em excesso fragilizam refactors.

**Como lidar com legado sem testes?**  
Comece com characterization tests, introduza seams e refatore incrementalmente. Priorize áreas de maior risco/incidente.

---

## Referências e Práticas do Mercado

- Kent Beck (TDD e práticas de teste)
- Martin Fowler (padrões e armadilhas)
- ThoughtWorks Tech Radar (qualidade)

---

[Anterior](bdd.md) | [Índice](../../SUMMARY.md) | [Próximo](../career/system-design-interview.md)
