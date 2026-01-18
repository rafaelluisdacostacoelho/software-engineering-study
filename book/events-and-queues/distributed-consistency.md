[Anterior](queues-and-messaging.md) | [Índice](../../SUMMARY.md) | [Próximo](../scalability/caching-strategies.md)

# Distributed Consistency — Consistência em Sistemas Distribuídos

## Visão Geral e Contexto de Mercado

Consistência distribuída é a disciplina de garantir que múltiplos componentes (serviços, bancos, filas) cheguem a um estado correto apesar de falhas, concorrência e latência. Em sistemas modernos, a maioria das integrações é construída com **consistência eventual** — não por “moda”, mas por limites físicos e operacionais.

O mercado equilibra:

- **Disponibilidade** e **latência**
- contra **consistência forte** e **coordenação**

Por isso, padrões como Sagas, Outbox, Idempotência, Versionamento de schema e “single-writer per key” são pilares reais em produção.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O entendimento prático de consistência distribuída foi moldado por sistemas como bancos distribuídos e grandes plataformas. Conceitos como CAP, consenso, replicação e consistência eventual viraram parte do “kit” de engenharia.

- **Padrões e Protocolos Usados no Mercado**
	- **CAP (na prática):** em partição de rede, escolhe-se Consistência ou Disponibilidade.
	- **Consensus:** Raft/Paxos (implementado em sistemas como etcd/consul).
	- **Sagas:** coordenação de transações locais com compensação.
	- **Outbox/Inbox:** publicação/consumo confiável.
	- **Idempotência:** essencial para retries e at-least-once.
	- **Versionamento de eventos:** compatibilidade entre produtores/consumidores.
	- **Read models (CQRS):** separa escrita consistente de leitura escalável.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Reproduzir falhas distribuídas (reordenação, duplicação, delay) é difícil. Sem testes e observabilidade, bugs aparecem como “fantasmas” em produção.

- **Performance e Manutenção**  
	- Coordenação forte (2PC/consenso) tem custo de latência e disponibilidade.
	- Consistência eventual exige design de UX e de processos (ex.: status “pendente”).
	- Reprocessamento é obrigatório e precisa ser seguro.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: ausência de idempotência, ausência de outbox, ausência de versionamento.
	- Coverage: falta de testes para duplicação/reordenação.
	- Flakiness: testes distribuídos sem ambientes controlados.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests e validação de schemas.
	- Deploy compatível (produtor/consumidor) com rollout gradual.
	- Migrações e compatibilidade retroativa.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: regras e invariantes locais.
	- Integração: outbox/inbox e consumo real de eventos.
	- E2E: poucos fluxos críticos.
	- Fault injection: seletivo e com hipóteses.

- **Métrica de Qualidade**  
	- Tempo de convergência (quanto demora para o sistema ficar consistente)
	- Taxa de reprocessamento e DLQ
	- Incidentes por inconsistência (duplicação, perda, ordem)
	- Lag e backlog

---

## Exemplos Avançados (Python, C# e Go)

Exemplo didático: idempotência por “inbox” (tabela/registro de mensagens processadas).

### Python

```python
def process_event(event_id: str, inbox_repo, handler) -> None:
		if inbox_repo.already_processed(event_id):
				return
		handler()
		inbox_repo.mark_processed(event_id)
```

### C#

```csharp
public interface IInbox
{
		bool AlreadyProcessed(string eventId);
		void MarkProcessed(string eventId);
}

public sealed class Consumer
{
		private readonly IInbox _inbox;
		public Consumer(IInbox inbox) => _inbox = inbox;

		public void Handle(string eventId, Action handler)
		{
				if (_inbox.AlreadyProcessed(eventId)) return;
				handler();
				_inbox.MarkProcessed(eventId);
		}
}
```

### Go

```go
package consumer

type Inbox interface {
		AlreadyProcessed(eventID string) (bool, error)
		MarkProcessed(eventID string) error
}

func Handle(inbox Inbox, eventID string, handler func() error) error {
		seen, err := inbox.AlreadyProcessed(eventID)
		if err != nil {
				return err
		}
		if seen {
				return nil
		}
		if err := handler(); err != nil {
				return err
		}
		return inbox.MarkProcessed(eventID)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Escolha consistência por caso de uso:** não existe “um nível certo” global.
- **Idempotência como padrão:** redes e brokers repetem.
- **Outbox/Inbox para confiabilidade:** evita perder/publicar em duplicidade sem controle.
- **Compensação (sagas) com cuidado:** compensar não é “desfazer” perfeito; desenhe estados.
- **Observabilidade:** trace/correlation-id para seguir fluxos distribuídos.
- **Evite 2PC se não for obrigatório:** alto custo e fragilidade.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** resiliência (retries/timeouts), autoscaling por backlog.
- **Pipelines CI/CD:** deploy compatível, contract tests, schema registry.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing distribuído e alertas por backlog.
- **Testes e Infra-as-Code:** ambientes efêmeros e replays de eventos.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de convergência
- Backlog/lag
- DLQ/retries
- Incidentes por inconsistência

---

## Frameworks e Ferramentas do Mercado

- **Python:** confluent-kafka, celery, pytest
- **C#:** MassTransit, Confluent.Kafka, xUnit
- **Go:** kafka-go/sarama, testify
- **Ferramentas de integração:** Pact, OpenTelemetry, Prometheus/Grafana

---

## Recursos Avançados e Leituras Recomendadas

- _Designing Data-Intensive Applications_ (Kleppmann)
- Martin Fowler (eventual consistency, sagas, outbox)
- Documentação de Kafka/PubSub/SQS

---

## FAQ Especialista

**CAP é uma regra absoluta do dia a dia?**  
É um guia. O ponto prático é: partições existem, e coordenação tem custo. Escolha conscientemente por caso.

**Como lidar com duplicação e reordenação?**  
Idempotência + dedup/inbox, ordenação por chave (partições) e handlers tolerantes a replays.

**Como explicar consistência eventual para produto?**  
Traduza em estados do usuário (pendente/confirmado), SLAs de convergência e UX que não promete “instantâneo” quando não é garantido.

---

## Referências e Práticas do Mercado

- Kleppmann (DDIA)
- Martin Fowler
- Google SRE

---

[Anterior](queues-and-messaging.md) | [Índice](../../SUMMARY.md) | [Próximo](../scalability/caching-strategies.md)
