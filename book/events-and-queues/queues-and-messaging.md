[Anterior](../critical-operations/reconciliation-and-auditability.md) | [Índice](../../SUMMARY.md) | [Próximo](distributed-consistency.md)

# Queues & Messaging — Filas, Eventos e Mensageria

## Visão Geral e Contexto de Mercado

Filas e mensageria são fundamentais para desacoplar sistemas, absorver picos e aumentar resiliência. Em arquiteturas modernas (microserviços, event-driven, cloud), elas são usadas para:

- **Assincronismo** (não bloquear o request principal)
- **Buffering** (suportar burst e picos de tráfego)
- **Integração** (pub/sub entre bounded contexts)
- **Resiliência** (retries controlados, isolamento de falhas)

O ponto crítico no mercado é entender que “mensagem entregue” não significa “efeito aplicado”. A entrega mais comum é **at-least-once**, portanto consumidores precisam ser **idempotentes** e sistemas precisam de padrões de observabilidade e reprocessamento.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Mensageria evoluiu de brokers tradicionais (RabbitMQ/ActiveMQ) para streaming (Kafka/Pub/Sub/Event Hubs) e serviços gerenciados (SQS/SNS). O foco saiu de “transportar mensagem” para “contratos, semânticas de entrega e operação em escala”.

- **Padrões e Protocolos Usados no Mercado**
	- **Semânticas de entrega:** at-most-once, at-least-once, exatamente-uma-vez (rara, geralmente com restrições).
	- **Pub/Sub vs Queue:** broadcast vs work distribution.
	- **Consumer groups / partitions:** paralelismo e ordenação por chave.
	- **DLQ (Dead Letter Queue):** isolamento de mensagens problemáticas.
	- **Backoff + jitter:** retries sem tempestade.
	- **Idempotency keys/dedup:** evitar duplicação de efeitos.
	- **Outbox/Inbox:** consistência entre DB e eventos.
	- **Schema registry e versionamento:** evolução compatível de mensagens.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	É difícil garantir comportamento sob duplicação, reordenação e atrasos. Testes precisam cobrir: idempotência, reprocessamento, ordenação por chave e falhas parciais.

- **Performance e Manutenção**  
	- Aumentar paralelismo sem cuidado pode quebrar ordenação e invariantes.
	- Mensagens grandes geram custo e latência; prefira eventos enxutos + fetch por ID quando necessário.
	- Retenção/compactação (Kafka) e visibilidade (SQS) exigem tuning.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: consumidores sem idempotência, sem DLQ, sem observabilidade.
	- Coverage: falta de testes para duplicação/retry.
	- Flakiness: testes que dependem de timing e brokers instáveis.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests (schema compatível) antes de publicar mudanças.
	- Deploy com compatibilidade: produtores “forward compatible” e consumidores “backward compatible”.
	- Migração de schemas por versões.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: lógica do handler (pura) + idempotência (ex.: store de dedup em memória).
	- Integração: broker real (testcontainers) + DB (outbox/inbox).
	- E2E: poucos fluxos críticos (pedido → pagamento → faturamento).

- **Métrica de Qualidade**  
	- Lag de consumidores
	- Taxa de retries e DLQ
	- Tempo médio de processamento por mensagem
	- Taxa de duplicação detectada (dedup hits)
	- Incidentes por reprocessamento/ordenação

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: handler idempotente com “store” de deduplicação (conceitual).

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
		id: str
		payload: dict


class DedupStore:
		def __init__(self) -> None:
				self._seen: set[str] = set()

		def already_processed(self, message_id: str) -> bool:
				return message_id in self._seen

		def mark_processed(self, message_id: str) -> None:
				self._seen.add(message_id)


def handle_message(msg: Message, dedup: DedupStore) -> None:
		if dedup.already_processed(msg.id):
				return
		# aplicar efeito (ex.: atualizar status)
		dedup.mark_processed(msg.id)
```

### C#

```csharp
public sealed record Message(string Id, IReadOnlyDictionary<string, string> Payload);

public interface IDedupStore
{
		bool AlreadyProcessed(string id);
		void MarkProcessed(string id);
}

public sealed class Handler
{
		private readonly IDedupStore _dedup;
		public Handler(IDedupStore dedup) => _dedup = dedup;

		public void Handle(Message msg)
		{
				if (_dedup.AlreadyProcessed(msg.Id)) return;
				// aplicar efeito
				_dedup.MarkProcessed(msg.Id);
		}
}
```

### Go

```go
package handler

type Message struct {
		ID      string
		Payload map[string]string
}

type DedupStore interface {
		AlreadyProcessed(id string) (bool, error)
		MarkProcessed(id string) error
}

func Handle(msg Message, store DedupStore) error {
		seen, err := store.AlreadyProcessed(msg.ID)
		if err != nil {
				return err
		}
		if seen {
				return nil
		}
		// aplicar efeito
		return store.MarkProcessed(msg.ID)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Assuma at-least-once:** dedup/idempotência são padrão.
- **DLQ com runbook:** por que falhou, como reprocessar, como corrigir payload.
- **Evite eventos “gordos”:** prefira eventos pequenos e versionáveis.
- **Ordenação por chave:** quando necessário, particione por entity-id.
- **Retries controlados:** backoff+jitter + limites.
- **Outbox/Inbox:** para consistência DB↔evento.
- **Observabilidade:** correlation-id/trace-id, métricas de lag, retries e DLQ.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** autoscaling por lag, limites de consumo e proteção contra overload.
- **Pipelines CI/CD:** validação de schemas/contratos, deploy compatível e rollback.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards para lag/DLQ, alertas e runbooks.
- **Testes e Infra-as-Code:** provisionamento de tópicos/filas, políticas de retenção e DLQ.

---

## Métricas, Monitoramento e Melhoria Contínua

- Consumer lag
- DLQ rate
- Retry rate
- Tempo de processamento
- Duplicação detectada

---

## Frameworks e Ferramentas do Mercado

- **Python:** kombu/celery (fila), confluent-kafka, pytest
- **C#:** MassTransit, Confluent.Kafka, xUnit
- **Go:** sarama/segmentio-kafka-go, testify
- **Cloud:** SQS/SNS, Pub/Sub, Event Hubs

---

## Recursos Avançados e Leituras Recomendadas

- _Designing Data-Intensive Applications_ (Kleppmann)
- Documentação Kafka/SQS/PubSub sobre delivery semantics
- Martin Fowler (event-driven, outbox)

---

## FAQ Especialista

**Por que exatamente-uma-vez é raro?**  
Porque exige coordenação forte e custos (transações distribuídas, idempotência implícita). O mercado prefere at-least-once + idempotência.

**DLQ é “lixeira”?**  
Não deveria ser. DLQ precisa de triagem, runbook, métricas e estratégia de reprocessamento.

**Como lidar com evolução de schema?**  
Versione mensagens, mantenha compatibilidade (fields opcionais), e use schema registry/contract tests.

---

## Referências e Práticas do Mercado

- Kafka/SQS/PubSub docs
- ThoughtWorks Tech Radar
- Martin Fowler

---

[Anterior](../critical-operations/reconciliation-and-auditability.md) | [Índice](../../SUMMARY.md) | [Próximo](distributed-consistency.md)
