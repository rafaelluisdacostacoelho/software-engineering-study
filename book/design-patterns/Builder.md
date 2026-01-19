[Anterior](Bridge.md) | [Índice](../../SUMMARY.md) | [Próximo](ChainOfResponsibility.md)

# Builder — Construção Passo a Passo de Objetos Complexos (Padrão de Criação)

## Visão Geral e Contexto de Mercado

Builder é um padrão para construir objetos complexos **passo a passo**, separando a construção da representação final. Na prática de mercado, ele aparece quando:

- Você tem objetos com muitos campos opcionais/validações e o construtor vira ilegível.
- Você precisa garantir invariantes na criação (ex.: “se `payment_method=card`, então `token` é obrigatório”).
- Você quer reduzir “telescoping constructors” e `if/else` espalhado.

Em sistemas modernos (microserviços, APIs, CI/CD), Builder também é um aliado para testabilidade: ele simplifica a criação de fixtures de teste sem expor detalhes internos ou criar factories gigantes.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O Builder é um GoF clássico. Em linguagens com recursos modernos (named parameters, records, dataclasses), o papel do Builder mudou: ele não é sempre necessário, mas continua valioso quando existe lógica de construção, invariantes e composição de partes.

- **Padrões e Protocolos Usados no Mercado**
	- **Fluent builder:** API encadeável (`WithX().WithY().Build()`).
	- **Step builder:** força ordem/obrigatoriedade de campos (compila se estiver completo).
	- **Factory vs Builder:** factory cria “de uma vez”; builder constrói incrementalmente.
	- **Immutability:** builder mutável que gera objeto final imutável.
	- **Validation centralizada:** validações na etapa `Build()`.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Builder mal desenhado vira “DSL” confusa e passa a esconder lógica crítica. O objetivo é tornar criação **clara** e **determinística**.

- **Performance e Manutenção**  
	Overhead é pequeno, mas existe: alocações extras, cópias, e complexidade de API. Em código de domínio, o custo é geralmente aceitável; em hot paths, avalie.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: builder que permite estados inválidos e só falha em runtime tarde demais.
	- Coverage: não testar validações e combinações de campos.
	- Flakiness: fixtures de teste dependentes de defaults implícitos e variáveis globais.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Builders usados em testes devem ser estáveis (evitar defaults “mágicos”).
	- Linters/analyzers para evitar builders que expõem campos internos indevidos.
	- Contract tests: se Builder constrói DTOs públicos, garanta compatibilidade.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: validações e invariantes do `Build()`.
	- Integração: quando Builder monta payloads para APIs/DB.
	- E2E: menos comum; foco em fluxos de negócio, não no Builder.

- **Métrica de Qualidade**  
	- Redução de complexidade em construtores
	- Menos bugs de “campo obrigatório faltando”
	- Melhor legibilidade de testes (fixtures)

---

## Exemplos Avançados (Python, C# e Go)

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
		order_id: str
		total_cents: int
		currency: str
		customer_id: str | None


class OrderBuilder:
		def __init__(self, order_id: str):
				self._order_id = order_id
				self._total_cents = 0
				self._currency = "BRL"
				self._customer_id = None

		def total(self, cents: int):
				self._total_cents = cents
				return self

		def currency(self, code: str):
				self._currency = code
				return self

		def customer(self, customer_id: str):
				self._customer_id = customer_id
				return self

		def build(self) -> Order:
				if self._total_cents <= 0:
						raise ValueError("total_cents must be > 0")
				return Order(
						order_id=self._order_id,
						total_cents=self._total_cents,
						currency=self._currency,
						customer_id=self._customer_id,
				)
```

### C#

```csharp
public sealed record Order(string OrderId, int TotalCents, string Currency, string? CustomerId);

public sealed class OrderBuilder
{
		private readonly string _orderId;
		private int _totalCents;
		private string _currency = "BRL";
		private string? _customerId;

		public OrderBuilder(string orderId) => _orderId = orderId;

		public OrderBuilder Total(int cents) { _totalCents = cents; return this; }
		public OrderBuilder Currency(string code) { _currency = code; return this; }
		public OrderBuilder Customer(string id) { _customerId = id; return this; }

		public Order Build()
		{
				if (_totalCents <= 0) throw new ArgumentException("TotalCents must be > 0");
				return new Order(_orderId, _totalCents, _currency, _customerId);
		}
}
```

### Go

```go
package orders

import "fmt"

type Order struct {
		OrderID     string
		TotalCents  int
		Currency    string
		CustomerID  *string
}

type Builder struct {
		orderID    string
		totalCents int
		currency   string
		customerID *string
}

func NewBuilder(orderID string) *Builder {
		return &Builder{orderID: orderID, currency: "BRL"}
}

func (b *Builder) Total(cents int) *Builder { b.totalCents = cents; return b }
func (b *Builder) Currency(code string) *Builder { b.currency = code; return b }
func (b *Builder) Customer(id string) *Builder { b.customerID = &id; return b }

func (b *Builder) Build() (Order, error) {
		if b.totalCents <= 0 {
				return Order{}, fmt.Errorf("TotalCents must be > 0")
		}
		return Order{OrderID: b.orderID, TotalCents: b.totalCents, Currency: b.currency, CustomerID: b.customerID}, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Use Builder quando existir lógica/invariantes de construção.** Para simples DTOs, prefira named params/records.
- **Não esconda regra de negócio crítica** em defaults silenciosos.
- **Valide em `Build()`** e mantenha o objeto final imutável quando possível.
- **Mantenha a API pequena:** se o builder virar um “mini framework”, você perdeu clareza.
- **Em testes, prefira builders explícitos** (`OrderBuilder().Total(…)`) a factories mágicas.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** sem impacto direto; a integração é mais sobre consistência de construção de payloads (requests/outbox/events).
- **Pipelines CI/CD:** validações e testes garantindo invariantes; evitar breaking changes em DTOs.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** logs/telemetria sobre falhas de validação no build.
- **Testes e Infra-as-Code:** builders ajudam a gerar massa de dados determinística para integrações.

---

## Métricas, Monitoramento e Melhoria Contínua

- Redução de bugs por “objeto inválido”
- Menos complexidade em construtores e mapeamentos
- Melhor legibilidade/manutenção de testes

---

## Frameworks e Ferramentas do Mercado

- **Python:** dataclasses/pydantic (pode substituir Builder em muitos casos)
- **C#:** records, required members (pode reduzir necessidade)
- **Go:** functional options (alternativa comum)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Builder
- Effective patterns de construção (functional options, step builders)

---

## FAQ Especialista

**Builder é sempre melhor que construtor?**  
Não. Se o objeto é simples, construtor/record/dataclass é mais claro.

**Quando usar Step Builder?**  
Quando você precisa forçar obrigatoriedade/ordem de campos e quer isso garantido pelo compilador (muito comum em C#).

**Functional options em Go é Builder?**  
É uma alternativa do mesmo problema (configuração incremental), com trade-offs diferentes e geralmente menos boilerplate.

---

[Anterior](Bridge.md) | [Índice](../../SUMMARY.md) | [Próximo](ChainOfResponsibility.md)
