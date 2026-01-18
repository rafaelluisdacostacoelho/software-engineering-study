[Anterior](event-driven-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](event-sourcing.md)

# CQRS — Command Query Responsibility Segregation (Guia Avançado)

## Visão Geral e Contexto de Mercado

CQRS separa responsabilidades de **escrita** (Commands) e **leitura** (Queries). O objetivo não é “ter dois bancos por esporte”, mas permitir que cada lado evolua com requisitos diferentes:

- Escrita: consistência, invariantes, transações, validações.
- Leitura: performance, modelos materializados, cache e UX.

No mercado, CQRS aparece em domínios com leitura pesada, relatórios complexos, múltiplas visões de dados e necessidade de escalar leitura sem comprometer integridade da escrita.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	CQRS foi popularizado como derivação de CQS (Command-Query Separation) e ganhou tração com event-driven e event sourcing. Hoje, muitos sistemas aplicam CQRS de forma parcial: um modelo de escrita e um (ou mais) modelos de leitura.

- **Padrões e Protocolos Usados no Mercado**
	- **Command handlers** (escrita) com validação e transação.
	- **Read models/materialized views** (leitura) otimizados.
	- **Event-driven updates:** projeções atualizadas por eventos.
	- **Outbox pattern:** publicar eventos de forma confiável.
	- **Idempotência nas projeções:** replays e at-least-once.
	- Contratos: OpenAPI/AsyncAPI, schema registry.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Você precisa testar consistência do lado write e corretude/convergência do lado read. Bugs comuns: projeções atrasadas, duplicadas ou inconsistentes.

- **Performance e Manutenção**  
	- Projeções podem ficar caras (rebuild) sem planejamento.
	- “Eventual consistency” precisa ser comunicada e refletida em UX.
	- O custo operacional sobe (mais componentes, pipelines, observabilidade).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: projeções sem versionamento, sem replay seguro, sem idempotência.
	- Coverage: falta de testes para reprocessamento e compatibilidade.
	- Flakiness: testes assíncronos dependentes de timing.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Migração segura de read models (versões de projeção).
	- Deploy compatível (consumidores/projeções antes de produtores quando necessário).
	- Observabilidade do lag como gate.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: command handler (invariantes).
	- Integração: outbox + broker + projeção.
	- E2E: poucos fluxos críticos com verificação de convergência.

- **Métrica de Qualidade**  
	- Lag das projeções
	- Tempo de convergência (write → read)
	- Taxa de falhas e replays
	- Incidentes por inconsistência de leitura

---

## Exemplos Avançados (Python, C# e Go)

Exemplo didático: command handler (write) e projeção (read) atualizada por evento.

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrder:
		order_id: str
		total_cents: int


@dataclass(frozen=True)
class OrderCreated:
		order_id: str
		total_cents: int


def handle_create_order(cmd: CreateOrder, repo, outbox) -> None:
		if cmd.total_cents <= 0:
				raise ValueError("invalid total")
		repo.insert_order(cmd.order_id, cmd.total_cents)
		outbox.add_event(OrderCreated(cmd.order_id, cmd.total_cents))
```

### C#

```csharp
public sealed record CreateOrder(string OrderId, int TotalCents);
public sealed record OrderCreated(string OrderId, int TotalCents);

public sealed class Orders
{
		public void Handle(CreateOrder cmd, IOrdersRepo repo, IOutbox outbox)
		{
				if (cmd.TotalCents <= 0) throw new ArgumentException("invalid total");
				repo.Insert(cmd.OrderId, cmd.TotalCents);
				outbox.Add(new OrderCreated(cmd.OrderId, cmd.TotalCents));
		}
}
```

### Go

```go
package app

import "fmt"

type CreateOrder struct { OrderID string; TotalCents int }
type OrderCreated struct { OrderID string; TotalCents int }

type OrdersRepo interface { Insert(id string, total int) error }
type Outbox interface { Add(event any) error }

func HandleCreateOrder(cmd CreateOrder, repo OrdersRepo, outbox Outbox) error {
		if cmd.TotalCents <= 0 {
				return fmt.Errorf("invalid total")
		}
		if err := repo.Insert(cmd.OrderID, cmd.TotalCents); err != nil {
				return err
		}
		return outbox.Add(OrderCreated{OrderID: cmd.OrderID, TotalCents: cmd.TotalCents})
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Não use CQRS sem necessidade:** aumenta componentes e custo operacional.
- **Mantenha invariantes no write model:** read model é derivado.
- **Trate convergência como requisito:** defina SLA de atualização do read model.
- **Idempotência nas projeções** para suportar replays/at-least-once.
- **Versione projeções** para rebuild/migrações.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** autoscaling por lag; jobs de rebuild.
- **Pipelines CI/CD:** deploy compatível e migrações de read models.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards de lag/tempo de convergência.
- **Testes e Infra-as-Code:** provisionamento de tópicos/filas e bancos de leitura.

---

## Métricas, Monitoramento e Melhoria Contínua

- Lag de projeção
- Tempo de convergência
- Falhas/retries em projeções
- Incidentes por inconsistência

---

## Frameworks e Ferramentas do Mercado

- **Python:** SQLAlchemy, redis, confluent-kafka
- **C#:** MassTransit, EF Core, Dapper
- **Go:** sqlc/database/sql, kafka-go
- **Ferramentas:** OpenTelemetry, Prometheus/Grafana

---

## Recursos Avançados e Leituras Recomendadas

- Martin Fowler (CQRS)
- Kleppmann (DDIA)
- Documentação de brokers e bancos

---

## FAQ Especialista

**CQRS exige dois bancos?**  
Não necessariamente. Você pode ter separação lógica com a mesma base, ou read replicas/materialized views. A separação é de responsabilidades.

**Como lidar com usuário vendo dados “atrasados”?**  
Defina SLA de convergência, use UX com estados (pendente/confirmado) e, quando necessário, faça leitura “forte” do write model para telas críticas.

**Como reprocessar projeções com segurança?**  
Versione projeções, use idempotência e tenha capacidade de replay (event log) ou rebuild a partir do write store.

---

## Referências e Práticas do Mercado

- Martin Fowler
- ThoughtWorks Tech Radar
- Kleppmann

---

[Anterior](event-driven-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](event-sourcing.md)
