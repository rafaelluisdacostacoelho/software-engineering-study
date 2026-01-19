[Anterior](tell-dont-ask.md) | [Índice](../../SUMMARY.md) | [Próximo](composition-over-inheritance.md)

# Law of Demeter — Menos Conhecimento, Menos Acoplamento (Princípio)

## Visão Geral e Contexto de Mercado

Law of Demeter (LoD) recomenda que código interaja apenas com seus colaboradores diretos, evitando “cadeias” de acesso a objetos (ex.: `a.b.c.d()`). O objetivo é reduzir acoplamento e tornar mudanças estruturais menos dolorosas.

Em sistemas profissionais, LoD é valioso porque:

- mudanças em modelos internos (estrutura de objetos/DTOs) não devem quebrar callers
- cadeias profundas incentivam vazamento de detalhes internos entre camadas
- testes ficam frágeis (mocks profundos) e PRs geram conflitos por mudanças transversais

LoD não é proibir `.`; é limitar o quanto uma unidade precisa conhecer sobre a estrutura interna de outra.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	LoD surgiu como heurística em design OO, mas o princípio é universal: reduzir dependências estruturais. Em arquiteturas modernas, ele se materializa em boundaries com APIs coesas.

- **Padrões e Protocolos Usados no Mercado**
	- **Tell, Don’t Ask:** prefira pedir uma ação em vez de navegar em estado.
	- **Facade:** expor uma API de alto nível para subsistemas.
	- **Encapsulamento e invariantes (DDD):** métodos de intenção em entidades/aggregates.
	- **Ports & Adapters:** adapters protegem o domínio de detalhes externos.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Um risco é substituir cadeias por “pass-through methods” (métodos que só repassam getters) em excesso. O ganho vem de expor operações de intenção, não de criar “atalhos” sem coesão.

- **Performance e Manutenção**  
	LoD tende a aumentar qualidade de manutenção. O custo pode ser uma camada a mais de métodos, mas normalmente é marginal comparado ao ganho em acoplamento.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: dependência direta de internals
	- Coverage: callers precisam testar muitas combinações
	- Flakiness: mocks profundos e frágeis

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Diretrizes de review: evitar “train wrecks” (`a.b.c...`) em camadas críticas.
	- Checkers/analyzers para identificar acessos encadeados repetidos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: prefira testar comportamento encapsulado (métodos de intenção).
	- Integração: valide boundaries (mapeamento e contratos).
	- E2E: apenas fluxos essenciais.

- **Métrica de Qualidade**  
	- Densidade de cadeias profundas em módulos críticos
	- Quantidade de mocks profundos em testes
	- Churn do modelo propagando para múltiplas camadas

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: substitua `order.customer.profile.email` por uma operação coesa.

### Python

```python
class Customer:
		def __init__(self, email: str):
				self.email = email


class Order:
		def __init__(self, customer: Customer):
				self._customer = customer

		def customer_email(self) -> str:
				return self._customer.email
```

### C#

```csharp
public sealed class Customer { public string Email { get; } public Customer(string email) => Email = email; }

public sealed class Order
{
		private readonly Customer _customer;
		public Order(Customer customer) => _customer = customer;
		public string CustomerEmail() => _customer.Email;
}
```

### Go

```go
package domain

type Customer struct{ Email string }

type Order struct{ customer Customer }

func (o Order) CustomerEmail() string { return o.customer.Email }
```

---

## Boas Práticas Sêniores e Armadilhas

- Prefira métodos que expressem intenção: `order.CustomerEmail()` ou `order.NotifyCustomer()`.
- Evite objetos anêmicos (só getters) em modelos com invariantes.
- Não use LoD para esconder dados úteis; use para esconder estrutura acidental.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** boundaries com DTOs estáveis reduzem impacto de mudanças.
- **Pipelines CI/CD:** linters + testes de contrato em integrações.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** logs e erros ficam mais localizados.
- **Testes e Infra-as-Code:** ambientes efêmeros validam contratos sem “mocks profundos”.

---

## Métricas, Monitoramento e Melhoria Contínua

- Frequência de cadeias profundas por módulo
- Taxa de regressões por mudanças em modelos internos
- Tempo para refatorar modelo sem quebrar múltiplas camadas

---

## Frameworks e Ferramentas do Mercado

- Analyzers/linters para code smells
- Arquiteturas (hexagonal/onion) para reforçar boundaries

---

## Recursos Avançados e Leituras Recomendadas

- Refactoring (Martin Fowler)
- Domain-Driven Design (Eric Evans)

---

## FAQ Especialista

**LoD é útil em DTOs?**  
Menos. DTOs são estruturas de dados; o valor de LoD aparece quando há encapsulamento e invariantes.

**Como evitar “pass-through methods”?**  
Exponha operações coesas (intenção). Se o método só repassa um getter sem agregar significado, reavalie.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](tell-dont-ask.md) | [Índice](../../SUMMARY.md) | [Próximo](composition-over-inheritance.md)
