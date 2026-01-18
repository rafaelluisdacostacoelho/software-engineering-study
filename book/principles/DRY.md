% DRY — Don't Repeat Yourself (nível Sênior / Especialista)

[Anterior](../introducao.md) | [Índice](../../SUMMARY.md) | [Próximo](KISS.md)

# DRY — Don't Repeat Yourself

## Visão Geral e Contexto de Mercado

DRY (Don't Repeat Yourself) é um princípio que, em ambientes modernos de desenvolvimento (squads ágeis, CI/CD, microserviços, múltiplos canais e integrações), funciona como **mecanismo de redução de risco**: reduz divergência de regras, diminui custo de manutenção e melhora previsibilidade de mudanças.

Em organizações com times paralelos e alta cadência de deploy, o problema mais caro não é “duplicação de linhas”, mas sim **duplicação de conhecimento**:

- A mesma regra de negócio (ex.: cálculo de juros, elegibilidade, validação de status) implementada em múltiplos pontos.
- A mesma política de segurança aplicada de formas levemente diferentes (ex.: validação de token em dois serviços).
- O mesmo contrato (payload/evento) interpretado com suposições diferentes por consumidores.

Na prática de mercado, DRY se conecta diretamente a:

- **Confiabilidade** (menos bugs por divergência)
- **Produtividade** (menos “shotgun surgery”)
- **Escalabilidade organizacional** (times conseguem mudar regras sem coordenar dezenas de arquivos/serviços)

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  DRY surge como reação ao custo real de mudanças em software. Em sistemas monolíticos clássicos, o impacto aparecia como duplicação de blocos; em arquiteturas modernas, o impacto aparece mais como **duplicação semântica** (mesma intenção espalhada em serviços, jobs, pipelines e camadas).

- **Padrões e Protocolos Usados no Mercado**
  - **Padrões de design** que ajudam DRY sem virar “abstração demais”: Strategy, Template Method, Adapter, Facade.
  - **Contratos**: OpenAPI/Swagger, AsyncAPI, Protobuf/IDL para evitar “duplicação de entendimento” entre times.
  - **Metodologias**: Contract testing (Pact), consumer-driven contracts, e testes de regressão focados em invariantes de domínio.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  Em sistemas distribuídos, “um único lugar” nem sempre significa “um único arquivo”: pode significar **uma biblioteca versionada**, um serviço dono da regra, ou um contrato central.

- **Performance e Manutenção**  
  DRY mal aplicado pode gerar “acoplamento invisível”: uma abstração genérica demais que passa a ser um gargalo de evolução. O custo aparece como:
  - PRs grandes e arriscados para mudanças simples
  - aumento de indireção e dificuldade de entendimento
  - necessidade de coordenação entre times

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  Deduplicar sem testes é receita para regressão. Em produção, isso normalmente estoura como:
  - “refactor broke behavior”
  - regressões em casos de borda
  - testes frágeis cobrindo detalhes em vez de comportamento

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Use linters e verificações automáticas para clones (quando fizer sentido), mas trate como sinal — não como verdade.
  - Tenha pipelines que garantem **contratos** e **testes** antes de permitir deduplicações estruturais grandes.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Para DRY semântico (regras de negócio), prefira **testes de contrato de comportamento** (ex.: golden tests, snapshots de regras) em vez de “testar cada função extraída”.
  - Para DRY cross-serviço, contract tests e validações de schema previnem divergência.

- **Métrica de Qualidade**
  - Code coverage ajuda, mas o mais útil aqui é medir **churn** (arquivos tocados por mudança), **defeitos por mudança** e **tempo de ciclo**.
  - Monitore PRs com muitos arquivos alterados para mudanças “simples”: sinal de duplicação semântica.

---

## Exemplos Avançados (Python, C# e Go)

### Python
Exemplo: regra de cálculo duplicada em múltiplos lugares → centralizar em um módulo de domínio e testar invariantes.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PricingInput:
	subtotal_cents: int
	customer_tier: str


def calculate_discount_cents(inp: PricingInput) -> int:
	# Fonte única de verdade da regra
	if inp.customer_tier == "gold":
		return int(inp.subtotal_cents * 0.10)
	if inp.customer_tier == "silver":
		return int(inp.subtotal_cents * 0.05)
	return 0


def final_price_cents(inp: PricingInput) -> int:
	return inp.subtotal_cents - calculate_discount_cents(inp)
```

```python
import pytest


@pytest.mark.parametrize(
	"subtotal,tier,expected",
	[
		(10000, "gold", 9000),
		(10000, "silver", 9500),
		(10000, "none", 10000),
	],
)
def test_price_invariants(subtotal, tier, expected):
	from pricing import PricingInput, final_price_cents

	assert final_price_cents(PricingInput(subtotal, tier)) == expected
```

- Sênior: repare que o teste protege comportamento e evita divergência quando a regra mudar.

### C#
Exemplo: validar regra de domínio sem duplicar validações em múltiplas camadas.

```csharp
public static class CouponRules
{
	public static bool IsEligible(string tier, decimal amount)
	{
		if (amount <= 0) return false;
		return tier switch
		{
			"gold" => amount >= 100m,
			"silver" => amount >= 200m,
			_ => false
		};
	}
}
```

```csharp
using Xunit;

public class CouponRulesTests
{
	[Theory]
	[InlineData("gold", 100, true)]
	[InlineData("gold", 99.99, false)]
	[InlineData("silver", 200, true)]
	[InlineData("none", 500, false)]
	public void Eligibility_ShouldMatchBusinessRule(string tier, decimal amount, bool expected)
	{
		Assert.Equal(expected, CouponRules.IsEligible(tier, amount));
	}
}
```

### Go
Exemplo: deduplicar mapeamento/transformação de dados com validação e testes, mantendo a regra em um pacote.

```go
package pricing

type Input struct {
	SubtotalCents int
	Tier          string
}

func DiscountCents(in Input) int {
	switch in.Tier {
	case "gold":
		return int(float64(in.SubtotalCents) * 0.10)
	case "silver":
		return int(float64(in.SubtotalCents) * 0.05)
	default:
		return 0
	}
}
```

```go
package pricing_test

import (
	"testing"
	"yourmodule/pricing"
)

func TestDiscountCents(t *testing.T) {
	got := pricing.DiscountCents(pricing.Input{SubtotalCents: 10000, Tier: "gold"})
	if got != 1000 {
		t.Fatalf("expected 1000, got %d", got)
	}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **DRY é sobre conhecimento, não sobre linhas.** Dois blocos parecidos podem representar intenções diferentes (não deduplique sem entender o domínio).
- **Prefira duplicação local a acoplamento global** quando a estabilidade do contrato entre módulos/times não é garantida.
- **Evite abstrações “framework internas”** criadas cedo demais: viram gargalo e criam dependências difíceis de evoluir.
- **Guarde invariantes em testes** (e não em comentários): quando a regra mudar, os testes apontam o que precisa ser revisado.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** DRY não significa “uma config para todos”. Significa automatizar e padronizar com templates (Helm/Kustomize) e políticas (OPA/Gatekeeper) sem duplicar intent.
- **Pipelines CI/CD:** proteja refactors com suites rápidas + checks de contrato (OpenAPI/AsyncAPI), e aplique deduplicação incremental.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** use Sentry/Datadog para medir regressões após refactors.
- **Testes e Infra-as-Code:** centralize módulos/constructs (Terraform modules) com versionamento e compatibilidade.

---

## Métricas, Monitoramento e Melhoria Contínua

- Métricas úteis para DRY:
  - **Churn** por domínio (quantos arquivos mudam por alteração de regra)
  - **Lead time** para mudança de regra
  - **Incidentes por divergência** (ex.: regra aplicada diferente em endpoints)
  - **Taxa de rollback** após refactors

- Dashboards práticos:
  - tempo médio de PR
  - número de arquivos tocados por PR
  - hotspots de mudanças

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest, hypothesis (property-based), ruff/flake8, mypy
- **C#:** xUnit, NUnit, FluentAssertions, Moq, SonarQube
- **Go:** testing, testify, golangci-lint
- **Ferramentas de integração:** SonarQube (duplicação), jscpd (clones), Pact (contratos), OpenAPI/AsyncAPI tooling

---

## Recursos Avançados e Leituras Recomendadas

- _Refactoring_ (Martin Fowler)
- _A Philosophy of Software Design_ (John Ousterhout)
- _Clean Architecture_ (Robert C. Martin)
- Martin Fowler — “Duplication” e “Shotgun Surgery” (padrões de code smells)

---

## FAQ Especialista

**DRY significa sempre extrair uma função quando vejo repetição?**  
Não. Primeiro valide se é duplicação de **conhecimento**. Se for duplicação apenas incidental (ex.: boilerplate), avalie ferramentas (geração de código, templates) ou aceite duplicação local se o acoplamento seria pior.

**Como lidar com DRY em microserviços sem criar uma “shared library” gigante?**  
Priorize contratos (OpenAPI/AsyncAPI/Protobuf) e testes de contrato. Se uma regra precisa ser centralizada, faça isso com **ownership claro** (um serviço dono da regra ou uma lib pequena e versionada), evitando “pacotes utilitários” genéricos.

**Qual o sinal mais forte de duplicação semântica?**  
Mudanças de requisito que exigem editar muitos lugares e ainda assim geram regressões — típico “shotgun surgery”.

---

## Referências e Práticas do Mercado

- Google Testing Blog (testes como proteção de refactors)
- ThoughtWorks Tech Radar (contratos, governança e práticas de qualidade)
- Catálogos de code smells (Fowler)

---

[Anterior](../introducao.md) | [Índice](../../SUMMARY.md) | [Próximo](KISS.md)
