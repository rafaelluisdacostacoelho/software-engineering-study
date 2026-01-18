[Anterior](../archtecture/onion-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](../design-patterns/Adapter.md)

# Domain-Driven Design (DDD) — Guia Avançado para Desenvolvedores Experientes

## Visão Geral e Contexto de Mercado

Domain-Driven Design (DDD) é uma abordagem para construir software onde o **modelo do domínio** (o que a empresa faz, suas regras e linguagem) dirige as decisões de design. Em organizações modernas (squads, microserviços, DevOps), DDD é especialmente valioso quando:

- O domínio é complexo e muda rápido (pagamentos, crédito, logística, precificação, antifraude).
- Existem múltiplos times e sistemas que precisam integrar sem virar um “monolito organizacional”.
- A consistência do negócio é crítica e incidentes têm custo alto.

DDD não é “só arquitetura” — é uma prática sociotécnica: aproxima engenharia e especialistas do negócio para produzir um modelo com **linguagem ubíqua**, limites claros e regras implementadas com alta fidelidade.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  O DDD ficou conhecido com Eric Evans e evoluiu com práticas como Event Storming, Context Mapping e a popularização de arquiteturas centradas em domínio (Clean/Hexagonal/Onion). Hoje ele é usado tanto em monólitos modulares quanto em microserviços, e frequentemente se combina com CQRS e event-driven.

- **Padrões e Protocolos Usados no Mercado**
  - **Ubiquitous Language:** termos do domínio usados no código, docs e conversas.
  - **Bounded Context:** fronteira onde um modelo é consistente; integrações entre contextos via contratos.
  - **Aggregates e Invariantes:** consistência transacional dentro do aggregate.
  - **Domain Events:** eventos representando fatos do domínio (ex.: `OrderPlaced`).
  - **Context Mapping:** relacionamento entre contextos (ACL, conformist, shared kernel).
  - Protocolos/contratos: OpenAPI/AsyncAPI/Protobuf; versionamento semântico.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  Em sistemas distribuídos, o desafio é manter coerência do modelo sem tentar impor um “modelo global”. Testes devem focar invariantes e casos de uso por contexto.

- **Performance e Manutenção**  
  - Modelos ricos com regras mal organizadas viram “bola de lama” de outro tipo.
  - Excesso de abstração (“abstração por moda”) aumenta custo sem reduzir risco.
  - Integrações entre contextos precisam de contratos estáveis e evolução compatível.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  - Debt aparece quando tudo vira “service” e o domínio vira DTO.
  - Coverage que importa cobre invariantes, regras e cenários críticos.
  - Flakiness frequentemente vem de testes de integração mal isolados (DB/filas/rede).

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Use unit tests rápidos no domínio por bounded context.
  - Use contract tests para integrações (HTTP e eventos) entre contextos/serviços.
  - Separe pipelines por serviço/contexto quando possível, com gates proporcionais ao risco.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Domínio: fakes/mocks para ports; testes determinísticos.
  - Persistência/mensageria: integration tests com ambientes efêmeros.
  - Entre contextos: contract tests e cenários de compatibilidade.

- **Métrica de Qualidade**  
  - Mudanças de requisito: quantos pontos do código precisam mudar?
  - Incidentes por inconsistência de modelo/integração.
  - Tempo de onboarding (clareza da linguagem e limites).

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo mostram (a) modelagem de Value Object, (b) invariantes e (c) eventos de domínio. Eles são “recortes” para evidenciar o estilo; em projetos reais, você separaria em módulos/pacotes e adicionaria portas/adapters.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
	currency: str
	cents: int

	def __post_init__(self) -> None:
		if self.cents < 0:
			raise ValueError("money cannot be negative")
		if len(self.currency) != 3:
			raise ValueError("invalid currency")


@dataclass(frozen=True)
class OrderPlaced:
	order_id: str
	total_cents: int


class Order:
	def __init__(self, order_id: str) -> None:
		self._id = order_id
		self._items: list[Money] = []
		self._events: list[object] = []

	def add_item(self, price: Money) -> None:
		self._items.append(price)

	def place(self) -> None:
		total = sum(i.cents for i in self._items)
		if total <= 0:
			raise ValueError("order total must be positive")
		self._events.append(OrderPlaced(order_id=self._id, total_cents=total))

	def pull_events(self) -> list[object]:
		events = list(self._events)
		self._events.clear()
		return events
```

### C#

```csharp
public readonly record struct Money(string Currency, int Cents)
{
	public Money {
		if (Cents < 0) throw new ArgumentOutOfRangeException(nameof(Cents));
		if (Currency is null || Currency.Length != 3) throw new ArgumentException("invalid currency");
	}
}

public sealed record OrderPlaced(string OrderId, int TotalCents);

public sealed class Order
{
	private readonly List<Money> _items = new();
	private readonly List<object> _events = new();

	public string Id { get; }

	public Order(string id) => Id = id;

	public void AddItem(Money price) => _items.Add(price);

	public void Place()
	{
		var total = _items.Sum(x => x.Cents);
		if (total <= 0) throw new InvalidOperationException("order total must be positive");
		_events.Add(new OrderPlaced(Id, total));
	}

	public IReadOnlyList<object> PullEvents()
	{
		var copy = _events.ToArray();
		_events.Clear();
		return copy;
	}
}
```

### Go

```go
package domain

import "fmt"

type Money struct {
	Currency string
	Cents    int
}

func NewMoney(currency string, cents int) (Money, error) {
	if cents < 0 {
		return Money{}, fmt.Errorf("money cannot be negative")
	}
	if len(currency) != 3 {
		return Money{}, fmt.Errorf("invalid currency")
	}
	return Money{Currency: currency, Cents: cents}, nil
}

type OrderPlaced struct {
	OrderID    string
	TotalCents int
}

type Order struct {
	ID     string
	items  []Money
	events []any
}

func NewOrder(id string) *Order {
	return &Order{ID: id}
}

func (o *Order) AddItem(price Money) {
	o.items = append(o.items, price)
}

func (o *Order) Place() error {
	total := 0
	for _, it := range o.items {
		total += it.Cents
	}
	if total <= 0 {
		return fmt.Errorf("order total must be positive")
	}
	o.events = append(o.events, OrderPlaced{OrderID: o.ID, TotalCents: total})
	return nil
}

func (o *Order) PullEvents() []any {
	out := append([]any(nil), o.events...)
	o.events = nil
	return out
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Não force DDD em todo lugar:** use onde há complexidade de negócio e custo alto de erro.
- **Evite “anemic domain model”:** regras importantes não deveriam morar em controllers/services com if-else espalhado.
- **Aggregate pequeno e consistente:** invariantes fortes dentro do aggregate; use eventos/sagas para o resto.
- **Bounded Contexts reais:** prefira limites explícitos a “um modelo único para tudo”.
- **Anti-Corruption Layer (ACL):** proteja seu modelo quando integrar com sistemas externos legados.
- **Eventos de domínio não são eventos de integração automaticamente:** às vezes você publica um “Integration Event” derivado, com schema/versão controlada.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** serviços por bounded context; contratos versionados; migrações coordenadas.
- **Pipelines CI/CD:** unit tests por contexto + contract tests entre produtores/consumidores.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** SLOs por contexto; rastreabilidade de eventos e fluxos de negócio.
- **Testes e Infra-as-Code:** ambientes efêmeros para adapters e contratos; validação automatizada de schemas.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de onboarding (entendimento da linguagem e do mapa de contextos)
- Taxa de incidentes por inconsistência de integração/schema
- Churn concentrado em infra vs. core (sinal de isolamento bom)
- Lead time para mudanças de regra de negócio

---

## Frameworks e Ferramentas do Mercado

- **Python:** pydantic (DTOs), pytest, FastAPI (adapters), SQLAlchemy (infra)
- **C#:** ASP.NET Core, EF Core, xUnit, Moq
- **Go:** net/http, sqlc/database/sql, testify
- **Ferramentas de integração:** OpenAPI/AsyncAPI, Pact, OpenTelemetry, Backstage (catálogo de serviços)

---

## Recursos Avançados e Leituras Recomendadas

- _Domain-Driven Design_ (Eric Evans)
- _Implementing Domain-Driven Design_ (Vaughn Vernon)
- Event Storming (Alberto Brandolini)
- Artigos de Martin Fowler sobre bounded contexts, agregados e integração

---

## FAQ Especialista

**DDD significa microserviços?**  
Não. DDD pode ser aplicado em monólitos modulares, e inclusive pode ajudar a preparar uma separação futura com menos risco.

**Como decidir bounded contexts?**  
Mapeie linguagem e fluxos com o negócio (event storming), identifique conflitos de significado e diferentes ritmos de mudança. Contextos nascem onde o modelo diverge.

**Agregados grandes ou pequenos?**  
Pequenos. Agregados grandes costumam gerar lock/contenda e dificultar escalabilidade; use eventos e consistência eventual entre agregados.

---

## Referências e Práticas do Mercado

- Eric Evans (DDD)
- Vaughn Vernon (práticas de implementação)
- Martin Fowler (patterns e integração)

---

[Anterior](../archtecture/onion-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](../design-patterns/Adapter.md)
