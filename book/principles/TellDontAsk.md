[Anterior](SeparationOfConcerns.md) | [Índice](../../SUMMARY.md) | [Próximo](LawOfDemeter.md)

# Tell, Don’t Ask — Peça Ações, Não Estado (Princípio)

## Visão Geral e Contexto de Mercado

Tell, Don’t Ask (TDA) recomenda que você **mande o objeto fazer algo** (“tell”) em vez de obter seu estado (“ask”) e decidir fora dele. Isso mantém regras e invariantes perto dos dados e reduz acoplamento.

No mercado, TDA melhora:

- consistência do domínio (regras em um lugar)
- testabilidade (menos lógica espalhada)
- manutenção (mudanças localizadas)

TDA não significa “nunca retornar valores”. Significa evitar que callers recomponham invariantes e regras internas.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	TDA é associado a encapsulamento e “objetos ricos”. Em arquiteturas modernas, ele também se expressa como “use cases” que orquestram, enquanto entidades preservam invariantes.

- **Padrões e Protocolos Usados no Mercado**
	- **Encapsulamento de invariantes:** `order.pay()` em vez de `if order.status == ...`.
	- **Law of Demeter:** reduzir navegação em grafos.
	- **DDD:** entidades/aggregates protegem invariantes.
	- **Command/Use case:** ações explícitas.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Se o modelo vira anêmico (só getters), TDA é impossível e a lógica se espalha. Por outro lado, objetos “ricos demais” podem virar “god objects”.

- **Performance e Manutenção**  
	Centralizar regras ajuda manutenção. O risco é misturar responsabilidades (domínio vs infra).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: lógica de negócio em controllers.
	- Coverage: testes fragmentados e redundantes.
	- Flakiness: pouca determinismo ao depender de infra.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Code review para evitar regra no caller.
	- Suites de testes focadas em invariantes de domínio.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: entidade/aggregate.
	- Integração: application service com repos.
	- E2E: fluxos críticos.

- **Métrica de Qualidade**  
	- Duplicação de regras em múltiplas camadas
	- Hotspots em controllers/services
	- Bugs por invariantes violadas

---

## Exemplos Avançados (Python, C# e Go)

### Python

```python
class Order:
		def __init__(self):
				self._paid = False

		def pay(self) -> None:
				if self._paid:
						return
				self._paid = True


# Evite:
# if not order.paid: order.paid = True
# Prefira:
# order.pay()
```

### C#

```csharp
public sealed class Order
{
		private bool _paid;
		public void Pay()
		{
				if (_paid) return;
				_paid = true;
		}
}
```

### Go

```go
package domain

type Order struct{ paid bool }

func (o *Order) Pay() { o.paid = true }
```

---

## Boas Práticas Sêniores e Armadilhas

- Mantenha invariantes onde os dados vivem (entidades/aggregates).
- Não misture domínio com infraestrutura (repo/HTTP) dentro da entidade.
- TDA funciona melhor com modelos com intenção (métodos) e não só getters.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** invariantes no domínio reduzem bugs que viram incidentes.
- **Pipelines CI/CD:** testes unitários de domínio rápidos e confiáveis.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** erros de regra vs infra ficam claros.
- **Testes e Infra-as-Code:** integração valida que orquestração não viola invariantes.

---

## Métricas, Monitoramento e Melhoria Contínua

- Bugs por violação de invariantes
- Duplicação de regras em camadas
- Tempo para alterar regra com segurança

---

## Frameworks e Ferramentas do Mercado

- DDD/clean architecture patterns
- Linters/analyzers para code smells

---

## Recursos Avançados e Leituras Recomendadas

- DDD (Evans)
- Refactoring (Fowler)

---

## FAQ Especialista

**TDA é contra DTOs?**  
Não. DTOs são dados. TDA se aplica a objetos que representam comportamento e invariantes.

**Como aplicar em código funcional?**  
Mantenha a regra perto do dado (funções coesas por módulo) e evite “regrinhas” espalhadas.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](SeparationOfConcerns.md) | [Índice](../../SUMMARY.md) | [Próximo](LawOfDemeter.md)
