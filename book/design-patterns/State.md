[Anterior](Singleton.md) | [Índice](../../SUMMARY.md) | [Próximo](Strategy.md)

# State — Comportamento Variável por Estado (State Machine) (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

State permite modelar um objeto cujo comportamento muda conforme seu estado interno, evitando grandes `switch/case` ou `if/else` espalhados. Em vez de condicionar a lógica por um enum, você encapsula o comportamento em classes/estruturas de estado.

Na prática de mercado, State é muito comum em:

- **Workflows:** pedido (created → paid → shipped → delivered/canceled).
- **Pagamentos:** autorização, captura, chargeback.
- **Onboarding/eligibility:** etapas e transições controladas.
- **UI/UX:** estados de tela (loading, loaded, error).
- **Protocolos:** conexões (handshake, open, closing).

Quando o estado é parte crítica do domínio, State melhora legibilidade, reduz bugs e torna transições explícitas.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF trouxe State como forma OO de state machine. Hoje, além de classes de estado, o mercado usa abordagens **table-driven** (tabela de transições), **statecharts** (hierárquico) e persistência via event sourcing.

- **Padrões e Protocolos Usados no Mercado**
	- **State interface:** operações que variam por estado.
	- **Context:** objeto principal que delega ao estado atual.
	- **Transições explícitas:** validação de transições permitidas.
	- **Persistência do estado:** salvar o estado atual e/ou eventos.
	- **Idempotência:** operações repetidas no mesmo estado não quebram invariantes.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	É fácil cair em “explosão de estados” e “explosão de transições”. Testes precisam cobrir:
	- transições permitidas e proibidas
	- invariantes por estado
	- comportamentos idempotentes

- **Performance e Manutenção**  
	- Muitos estados podem gerar boilerplate.
	- Mudanças de workflow exigem migração de dados/estados persistidos.
	- Concorrência: duas transições simultâneas podem corromper o estado.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: estados viram classes enormes e duplicadas.
	- Coverage: não testar “transições inválidas” e concorrência.
	- Flakiness: testes dependentes de relógio e side effects de infra.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de matriz de transições (gerados a partir de tabela).
	- Property-based tests: “estado nunca volta no tempo sem evento X”.
	- Migration tests para mudanças em estados persistidos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: estados isolados e validações de transição.
	- Integração: persistência (DB) e concorrência (optimistic lock).
	- E2E: fluxos do usuário (checkout completo).

- **Métrica de Qualidade**  
	- Taxa de erros “invalid transition”
	- Tempo médio em cada estado (SLA de workflow)
	- Reprocessamentos/retentativas por estado

---

## Exemplos Avançados (Python, C# e Go)

Exemplo mínimo: um pedido que pode ser pago e enviado dependendo do estado.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class OrderState(Protocol):
		def pay(self, order: "Order") -> None: ...
		def ship(self, order: "Order") -> None: ...


@dataclass
class Order:
		state: OrderState

		def pay(self) -> None:
				self.state.pay(self)

		def ship(self) -> None:
				self.state.ship(self)


class Created:
		def pay(self, order: Order) -> None:
				order.state = Paid()

		def ship(self, order: Order) -> None:
				raise ValueError("cannot ship before payment")


class Paid:
		def pay(self, order: Order) -> None:
				return  # idempotente

		def ship(self, order: Order) -> None:
				order.state = Shipped()


class Shipped:
		def pay(self, order: Order) -> None:
				return

		def ship(self, order: Order) -> None:
				return
```

### C#

```csharp
public interface IOrderState
{
		void Pay(Order order);
		void Ship(Order order);
}

public sealed class Order
{
		public IOrderState State { get; internal set; } = new Created();
		public void Pay() => State.Pay(this);
		public void Ship() => State.Ship(this);
}

public sealed class Created : IOrderState
{
		public void Pay(Order order) => order.State = new Paid();
		public void Ship(Order order) => throw new InvalidOperationException("cannot ship before payment");
}

public sealed class Paid : IOrderState
{
		public void Pay(Order order) { /* idempotente */ }
		public void Ship(Order order) => order.State = new Shipped();
}

public sealed class Shipped : IOrderState
{
		public void Pay(Order order) { }
		public void Ship(Order order) { }
}
```

### Go

```go
package order

import "errors"

type State interface {
		Pay(o *Order) error
		Ship(o *Order) error
}

type Order struct{ State State }

func New() *Order { return &Order{State: Created{}} }

func (o *Order) Pay() error  { return o.State.Pay(o) }
func (o *Order) Ship() error { return o.State.Ship(o) }

type Created struct{}
func (Created) Pay(o *Order) error  { o.State = Paid{}; return nil }
func (Created) Ship(o *Order) error { return errors.New("cannot ship before payment") }

type Paid struct{}
func (Paid) Pay(o *Order) error  { return nil }
func (Paid) Ship(o *Order) error { o.State = Shipped{}; return nil }

type Shipped struct{}
func (Shipped) Pay(o *Order) error  { return nil }
func (Shipped) Ship(o *Order) error { return nil }
```

---

## Boas Práticas Sêniores e Armadilhas

- **Transições devem ser explícitas e validadas.** Evite “setar enum” sem regra.
- **Idempotência por estado** evita bugs em retries.
- **Persistência e concorrência:** use optimistic locking/versionamento para evitar double transitions.
- **Evite explosão de classes:** quando muitos estados/ações, use tabela de transições + handlers.
- **Observabilidade do workflow:** logs e métricas por transição.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** workflows longos exigem persistência e reprocessamento seguro (at-least-once).
- **Pipelines CI/CD:** migration tests para mudanças de workflow; testes de regressão de transições.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards por estado (tempo médio, gargalos).
- **Testes e Infra-as-Code:** simulação de falhas e reprocessamento para estados críticos.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo médio por estado e tempo total do workflow
- Erros por transição
- Reprocessamentos/retentativas por estado
- Taxa de transição inválida (sinal de bugs/clients fora de contrato)

---

## Frameworks e Ferramentas do Mercado

- **State machines:** libs específicas (quando workflow é complexo)
- **Persistência:** event sourcing / outbox (quando aplicável)
- **Observabilidade:** OpenTelemetry

---

## Recursos Avançados e Leituras Recomendadas

- GoF — State
- Statecharts e modelagem de workflows
- Idempotência e concorrência em workflows

---

## FAQ Especialista

**State vs Strategy: qual a diferença?**  
Strategy escolhe algoritmo intercambiável; State muda comportamento conforme estado interno e normalmente envolve transições.

**Quando um enum + switch é melhor?**  
Quando há poucos estados e poucas operações, e o fluxo é simples. State vale quando a lógica cresce e o `switch` vira fonte de bugs.

**Como persistir estados sem quebrar compatibilidade?**  
Versione estados, migre dados e mantenha transições compatíveis. Para workflows críticos, considere event sourcing para auditabilidade.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Singleton.md) | [Índice](../../SUMMARY.md) | [Próximo](Strategy.md)
