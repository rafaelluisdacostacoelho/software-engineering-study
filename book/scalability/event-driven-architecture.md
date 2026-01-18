[Anterior](caching-strategies.md) | [Índice](../../SUMMARY.md) | [Próximo](cqrs.md)

# Event-Driven Architecture — Guia Avançado

## Visão Geral e Contexto de Mercado

Event-Driven Architecture (EDA) é um estilo onde mudanças relevantes do sistema são publicadas como **eventos**, e outros componentes reagem a esses eventos de forma assíncrona. No mercado, EDA é usada para:

- Escalar desacoplando produtores/consumidores
- Integrar bounded contexts com menor acoplamento temporal
- Suportar workflows complexos (orquestração/coreografia)
- Melhorar resiliência (buffering, retries, backpressure)

O custo é lidar com consistência eventual, duplicação, reordenação e operação de mensageria em escala.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	EDA ganhou força com microserviços e plataformas que precisavam de integração e throughput. A maturidade veio com práticas de schema registry, outbox/inbox, observabilidade e padronização de contratos.

- **Padrões e Protocolos Usados no Mercado**
	- **Event vs Command:** evento é fato ocorrido; comando é intenção.
	- **Pub/Sub e streaming:** Kafka/PubSub/Event Hubs.
	- **Outbox/Inbox:** consistência DB↔evento e idempotência no consumo.
	- **Sagas:** coordenação de transações locais.
	- **Schema versioning:** compatibilidade para evoluir sem quebrar consumidores.
	- **DLQ + reprocessamento:** operação segura.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Testar fluxos assíncronos é mais difícil do que sync. Sem contract tests e ambientes confiáveis, bugs aparecem em produção por incompatibilidade de schema.

- **Performance e Manutenção**  
	- Backlog/lag pode crescer e virar “incidente silencioso”.
	- Mensagens grandes e alta cardinalidade aumentam custo.
	- Ordenação: partições por chave resolvem parte, mas exigem disciplina.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: consumidores sem idempotência; eventos sem versionamento.
	- Coverage: falta de testes para replays e duplicação.
	- Flakiness: testes dependentes de timing/infra instável.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests (schema) no pipeline.
	- Deploy compatível: consumidores primeiro quando necessário.
	- Rollout gradual e observabilidade (lag/DLQ) como gate.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: handlers puros.
	- Integração: broker real + outbox/inbox.
	- E2E: poucos fluxos de negócio.

- **Métrica de Qualidade**  
	- Consumer lag
	- DLQ/retry rate
	- Tempo de convergência do fluxo
	- Taxa de incompatibilidade de schema (quebras)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo de “event handler” idempotente (conceitual) com inbox.

### Python

```python
def on_order_paid(event_id: str, inbox, apply_effect) -> None:
		if inbox.already_processed(event_id):
				return
		apply_effect()
		inbox.mark_processed(event_id)
```

### C#

```csharp
public interface IInbox {
		bool AlreadyProcessed(string id);
		void MarkProcessed(string id);
}

public sealed class OrderPaidHandler
{
		private readonly IInbox _inbox;
		public OrderPaidHandler(IInbox inbox) => _inbox = inbox;

		public void Handle(string eventId, Action apply)
		{
				if (_inbox.AlreadyProcessed(eventId)) return;
				apply();
				_inbox.MarkProcessed(eventId);
		}
}
```

### Go

```go
package handlers

type Inbox interface {
		AlreadyProcessed(id string) (bool, error)
		MarkProcessed(id string) error
}

func Handle(inbox Inbox, eventID string, apply func() error) error {
		seen, err := inbox.AlreadyProcessed(eventID)
		if err != nil { return err }
		if seen { return nil }
		if err := apply(); err != nil { return err }
		return inbox.MarkProcessed(eventID)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Trate eventos como contratos:** versionamento, compatibilidade e ownership.
- **Idempotência é obrigatória** (at-least-once).
- **Evite coreografias complexas sem observabilidade:** sagas exigem visibilidade.
- **Use DLQ com runbook** e estratégia de reprocessamento.
- **Evite “evento gordo” e PII desnecessária** (compliance).

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** autoscaling por lag, limites e backpressure.
- **Pipelines CI/CD:** contract tests + deploy compatível.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing distribuído; dashboards de lag/DLQ.
- **Testes e Infra-as-Code:** tópicos/filas versionados, retention e DLQ provisionadas.

---

## Métricas, Monitoramento e Melhoria Contínua

- Lag/backlog
- DLQ rate
- Tempo de processamento e convergência
- Erros por handler

---

## Frameworks e Ferramentas do Mercado

- **Python:** confluent-kafka, celery, opentelemetry
- **C#:** MassTransit, Confluent.Kafka, OpenTelemetry
- **Go:** kafka-go/sarama, OpenTelemetry
- **Infra:** Kafka, SQS/SNS, Pub/Sub, Event Hubs

---

## Recursos Avançados e Leituras Recomendadas

- Martin Fowler (event-driven, outbox, sagas)
- Kleppmann (DDIA)
- Documentação Kafka/SQS/PubSub

---

## FAQ Especialista

**Event-driven sempre melhora o sistema?**  
Não. Ele troca simplicidade por desacoplamento e escala. Para fluxos simples e sincronização direta, HTTP pode ser melhor.

**Como evitar “bola de eventos”?**  
Tenha ownership, contratos versionados, naming consistente e evite publicar eventos que são apenas detalhes internos.

**Como debugar fluxos assíncronos?**  
Tracing distribuído, correlation-id, replay controlado e dashboards de lag/DLQ.

---

## Referências e Práticas do Mercado

- Martin Fowler
- ThoughtWorks Tech Radar
- Documentação dos brokers

---

[Anterior](caching-strategies.md) | [Índice](../../SUMMARY.md) | [Próximo](cqrs.md)
