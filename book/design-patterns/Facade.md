[Anterior](Decorator.md) | [Índice](../../SUMMARY.md) | [Próximo](Factory.md)

# Facade — Interface Simples para Subsistemas Complexos (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Facade oferece uma interface de alto nível, focada em casos de uso, para um subsistema com múltiplas dependências e detalhes. Ele reduz acoplamento e melhora legibilidade ao evitar que clientes precisem conhecer a “coreografia” interna.

No mercado, Facade é extremamente comum em:

- **SDKs e clients:** um “client” que encapsula autenticação, retries, paginação, parsing.
- **Camada de aplicação (service layer):** orquestração de repositórios/serviços.
- **Integrações complexas:** gateways de pagamento, antifraude, logística.
- **Módulos legados:** “anti-corruption layer” que protege o domínio.

Facade não é “esconder tudo”: é oferecer uma API coerente e intencional, com contratos claros e tratamento consistente de erros.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF descreveu Facade para reduzir dependências diretas de subsistemas. Em arquiteturas modernas, ele aparece como “application services”, “clients” e “ports” que encapsulam detalhes de infraestrutura.

- **Padrões e Protocolos Usados no Mercado**
	- **API orientada a casos de uso:** métodos que representam intenções do negócio.
	- **Anti-corruption layer (ACL):** tradução de modelos e isolamento de mudanças.
	- **Boundary + DTOs:** contratos estáveis para entrada/saída.
	- **Error model consistente:** erros tipados e mapeamento coerente.
	- **Observabilidade:** tracing e logs em um ponto central.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Se a facade vira “super classe” com dezenas de métodos, você perde coesão e testabilidade. Prefira facades menores por contexto/caso de uso.

- **Performance e Manutenção**  
	- Facades podem esconder chamadas múltiplas e aumentar latência sem visibilidade.
	- Se a facade engole exceções e retorna “false”, incidentes ficam opacos.
	- “Leaky abstraction”: detalhes ainda vazam (timeouts, partial failures).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: facade vira lugar de “colocar lógica rápido” e acumula regras.
	- Coverage: não cobrir caminhos de erro (timeouts, retries, degradação).
	- Flakiness: testes integrados na facade sem isolamento de dependências.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests do contrato exposto (input/output + erros).
	- Testes de integração com dependências via containers efêmeros.
	- Feature flags e “canary” para mudanças de coreografia.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: facade com dependências fakes (interfaces/ports).
	- Integração: facade contra ambientes efêmeros (DB/queue/service stub).
	- E2E: poucos fluxos críticos (pagamento, criação de pedido).

- **Métrica de Qualidade**  
	- Latência e taxa de erro por operação da facade
	- Número de dependências por método (sinal de acoplamento)
	- Incidentes relacionados a coreografias ocultas

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: uma facade de checkout que orquestra estoque e pagamento.

### Python

```python
from dataclasses import dataclass
from typing import Protocol


class Inventory(Protocol):
		def reserve(self, sku: str, qty: int) -> None: ...


class Payments(Protocol):
		def charge(self, order_id: str, amount_cents: int) -> None: ...


@dataclass
class CheckoutFacade:
		inventory: Inventory
		payments: Payments

		def checkout(self, order_id: str, sku: str, qty: int, amount_cents: int) -> None:
				if qty <= 0 or amount_cents <= 0:
						raise ValueError("invalid input")
				self.inventory.reserve(sku, qty)
				self.payments.charge(order_id, amount_cents)
```

### C#

```csharp
public interface IInventory { Task Reserve(string sku, int qty, CancellationToken ct); }
public interface IPayments { Task Charge(string orderId, int amountCents, CancellationToken ct); }

public sealed class CheckoutFacade
{
		private readonly IInventory _inventory;
		private readonly IPayments _payments;

		public CheckoutFacade(IInventory inventory, IPayments payments)
				=> (_inventory, _payments) = (inventory, payments);

		public async Task Checkout(string orderId, string sku, int qty, int amountCents, CancellationToken ct)
		{
				if (qty <= 0 || amountCents <= 0) throw new ArgumentException("invalid input");
				await _inventory.Reserve(sku, qty, ct);
				await _payments.Charge(orderId, amountCents, ct);
		}
}
```

### Go

```go
package checkout

import "context"

type Inventory interface { Reserve(ctx context.Context, sku string, qty int) error }
type Payments interface { Charge(ctx context.Context, orderID string, amountCents int) error }

type Facade struct {
		Inventory Inventory
		Payments  Payments
}

func (f Facade) Checkout(ctx context.Context, orderID, sku string, qty, amountCents int) error {
		if qty <= 0 || amountCents <= 0 {
				return ErrInvalidInput
		}
		if err := f.Inventory.Reserve(ctx, sku, qty); err != nil {
				return err
		}
		return f.Payments.Charge(ctx, orderID, amountCents)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Não faça “God Facade”.** Prefira facades pequenas por contexto.
- **Erros e observabilidade são parte do contrato.** Não “engula” erros.
- **Não esconda efeitos colaterais perigosos:** se a operação chama 5 serviços, isso precisa ser conhecido.
- **Use interfaces/ports** para facilitar testes e evitar acoplamento a infra.
- **Defina limites e timeouts** na camada de facade para proteger o sistema.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** a facade costuma ser o ponto certo para aplicar budgets (timeout global) e limites.
- **Pipelines CI/CD:** contract tests por método; testes de integração com stubs/containers.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing por operação, logs estruturados, SLO por operação.
- **Testes e Infra-as-Code:** simulação de falhas (chaos) para validar coreografias e compensações.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95/p99 por operação da facade
- Taxa de erro por dependência envolvida
- Rate de timeouts e retries
- Incidentes por “leaky abstraction”

---

## Frameworks e Ferramentas do Mercado

- **Observabilidade:** OpenTelemetry
- **Resiliência:** Polly (C#), tenacity (Python), padrões de retry/backoff
- **API Design:** OpenAPI/Swagger para contratos estáveis

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Facade
- Martin Fowler — patterns de integração e ACL
- Clean Architecture — application services/use cases

---

## FAQ Especialista

**Facade é a mesma coisa que Service Layer?**  
Muitas vezes sim no efeito prático: uma API coesa que orquestra subsistemas. A diferença é contexto/ênfase, mas a técnica é a mesma.

**Quando a facade vira leaky abstraction inevitável?**  
Quando o subsistema tem semânticas que precisam ser expostas (ex.: consistência eventual, retries, limites). Nesse caso, documente explicitamente e modele erros/estados.

**Como evitar duplicação de regras entre facade e domínio?**  
Mantenha regras de negócio no domínio; a facade deve orquestrar e adaptar. Se a facade contém regra, reavalie limites do domínio.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Decorator.md) | [Índice](../../SUMMARY.md) | [Próximo](Factory.md)
