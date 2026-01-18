% Behavior-Driven Development (BDD) — Guia Avançado para Especialistas

[Anterior](tdd.md) | [Índice](../../SUMMARY.md) | [Próximo](unit-testing.md)

# Behavior-Driven Development (BDD) — Guia Avançado para Especialistas

## Visão Geral e Contexto de Mercado

Behavior-Driven Development (BDD) é uma evolução pragmática de TDD que coloca o foco em **comportamento do produto** e em uma linguagem compartilhada entre engenharia, produto e negócio. Em empresas com squads e CI/CD, BDD é especialmente valioso quando há necessidade de:

- Transformar requisitos ambíguos em exemplos executáveis.
- Reduzir gap entre o que foi “combinado” e o que foi “entregue”.
- Melhorar colaboração (refinamento, discovery/delivery) e reduzir retrabalho.

No mercado, BDD costuma ser aplicado junto com:

- Critérios de aceite claros (Given/When/Then).
- Automação de cenários críticos (geralmente em nível de serviço/API, não só UI).
- Estratégias de testes em camadas (unit + integração + contrato + e2e mínimo).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	BDD emergiu como resposta a dois problemas: (1) TDD sendo aplicado de forma “técnica demais” (sem conexão com comportamento de negócio) e (2) especificações textuais que não viravam teste verificável. A ideia central é: requisitos devem ser expressos como exemplos concretos e verificáveis.

- **Padrões e Protocolos Usados no Mercado**
	- **Given/When/Then (Gherkin):** estrutura de cenários.
	- **Specification by Example:** exemplos como contrato.
	- **Três Amigos (3 Amigos):** Produto/Dev/QA refinando juntos.
	- **ATDD:** quando os critérios de aceite dirigem o desenvolvimento.
	- **Contract tests:** Pact (quando o “comportamento” é o contrato entre serviços).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Suítes BDD podem crescer demais se todo requisito virar cenário end-to-end. Em sistemas grandes, o custo explode (tempo de execução, instabilidade). O ideal é escolher o nível correto: cenários no nível de API/serviço costumam ser mais estáveis que UI.

- **Performance e Manutenção**  
	- Cenários duplicados geram manutenção cara.
	- Passos (steps) muito genéricos viram “linguagem de programação disfarçada” e perdem legibilidade.
	- Muitos cenários rodando com UI (Selenium) geram pipelines lentos.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Flakiness vem de UI, timing, ambientes instáveis e dados compartilhados.
	- “Coverage de features” não significa cobertura de risco.
	- Debt aparece quando specs são atualizadas “depois” e param de refletir a realidade.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Execute BDD em paralelo e mantenha o conjunto pequeno (smoke/regressão crítica).
	- Separe cenários por criticidade e por tempo (rápidos vs. lentos).
	- Versione dados/fixtures e use ambientes efêmeros quando possível.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Use BDD como especificação de fluxos de negócio críticos.
	- Prefira BDD no nível de **API/serviço** + contract tests para integrações.
	- Use stubs/mocks para dependências externas em ambientes de teste (quando objetivo é comportamento local).

- **Métrica de Qualidade**  
	- Taxa de falhas por instabilidade (flaky rate) em specs.
	- Tempo de execução e custo de manutenção por cenário.
	- “Defeitos escapados” em fluxos cobertos por specs (indicador de qualidade das specs).

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo focam em estilo BDD: cenários com linguagem de negócio + execução automatizada em nível de serviço.

### Python

```python
# Exemplo ilustrativo com estilo Given/When/Then em pytest

def test_checkout_should_fail_when_stock_is_insufficient():
		# Given
		stock = {"sku-1": 0}

		# When
		def checkout(sku: str) -> str:
				if stock.get(sku, 0) <= 0:
						return "OUT_OF_STOCK"
				return "OK"

		# Then
		assert checkout("sku-1") == "OUT_OF_STOCK"
```

### C#

```csharp
using Xunit;

public class CheckoutSpecs
{
		[Fact]
		public void GivenNoStock_WhenCheckout_ThenReturnsOutOfStock()
		{
				var stock = new Dictionary<string, int> { ["sku-1"] = 0 };

				string Checkout(string sku) => stock.TryGetValue(sku, out var qty) && qty > 0
						? "OK"
						: "OUT_OF_STOCK";

				Assert.Equal("OUT_OF_STOCK", Checkout("sku-1"));
		}
}
```

### Go

```go
package specs

import "testing"

func TestGivenNoStock_WhenCheckout_ThenOutOfStock(t *testing.T) {
		t.Parallel()

		stock := map[string]int{"sku-1": 0}
		checkout := func(sku string) string {
				if stock[sku] <= 0 {
						return "OUT_OF_STOCK"
				}
				return "OK"
		}

		if got := checkout("sku-1"); got != "OUT_OF_STOCK" {
				t.Fatalf("expected OUT_OF_STOCK, got %s", got)
		}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Especificações como contrato vivo:** specs devem refletir o comportamento atual do sistema; se ficam desatualizadas, viram ruído.
- **Evite specs em excesso:** foque em fluxos críticos e regras de negócio de alto risco.
- **Evite UI como default:** prefira API/service-level specs; UI e2e só para smoke.
- **Steps legíveis e específicos:** não transforme step definitions em um “framework” genérico.
- **Dados de teste controlados:** isolamento por cenário, idempotência e teardown.
- **Falhas acionáveis:** quando um cenário falha, a mensagem precisa explicar o comportamento violado.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** rode specs contra ambientes efêmeros; mantenha dados isolados por suíte.
- **Pipelines CI/CD:** smoke specs em PR; regressão maior em nightly; paralelização obrigatória.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** specs viram documentação e input para observabilidade (SLOs por fluxo).
- **Testes e Infra-as-Code:** provisionamento de dependências (DB/filas) com teardown automatizado.

---

## Métricas, Monitoramento e Melhoria Contínua

- Flaky rate por suíte
- Tempo de execução e custo por cenário
- Frequência de mudanças de specs por mudança de produto
- Taxa de incidentes em fluxos “especificados” (indicador de lacunas)

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest-bdd, behave, pytest, requests
- **C#:** SpecFlow, xUnit, NUnit
- **Go:** godog, testify
- **Ferramentas de integração:** GitHub Actions/Azure DevOps/Jenkins, Allure/ReportPortal, Sonar

---

## Recursos Avançados e Leituras Recomendadas

- Dan North (BDD)
- _Specification by Example_ (Gojko Adzic)
- Martin Fowler — artigos sobre testes e contratos

---

## FAQ Especialista

**BDD é só Gherkin?**  
Não. Gherkin é uma forma popular de escrever cenários, mas BDD é principalmente uma prática de colaboração e especificação por exemplos.

**Como evitar specs que viram “testes de UI” lentos?**  
Escolha o nível de teste: valide comportamento no nível de API/serviço e mantenha UI como smoke. Use contract tests para integração entre serviços.

**Como manter specs sem virar manutenção infinita?**  
Trate specs como produto: curadoria, remoção do que não agrega, foco em risco e revisão contínua com produto/QA.

---

## Referências e Práticas do Mercado

- Dan North (BDD)
- Gojko Adzic (Specification by Example)
- ThoughtWorks Tech Radar (qualidade)

---

[Anterior](tdd.md) | [Índice](../../SUMMARY.md) | [Próximo](unit-testing.md)
