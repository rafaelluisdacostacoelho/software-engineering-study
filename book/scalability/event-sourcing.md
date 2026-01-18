[Anterior](cqrs.md) | [Índice](../../SUMMARY.md) | [Próximo](microservices-best-practices.md)

# Event Sourcing — Guia Avançado

## Visão Geral e Contexto de Mercado

Event Sourcing é um estilo arquitetural em que o **estado** de uma entidade/sistema não é persistido como “linha atual no banco”, mas como uma sequência **append-only** de **eventos imutáveis** (fatos que aconteceram). O estado atual é derivado ao **reaplicar** os eventos.

No mercado, Event Sourcing aparece em contextos onde:

- Auditoria e rastreabilidade são mandatórias (fintech, logística, compliance)
- Fluxos de negócio têm regras complexas e evoluem com frequência
- Há valor em reconstruir estado, fazer replay, simular cenários e manter histórico

Ele frequentemente é combinado com **CQRS** (write model por eventos + read models por projeções), e pode ser implementado sobre bancos/streams (Kafka) ou event stores dedicados.

Trade-off central: ganha-se auditabilidade e flexibilidade de projeções, mas paga-se com **complexidade**, **consistência eventual** (em leituras) e um custo operacional maior.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	A motivação original é simples: “o que aconteceu” é mais estável do que “como represento agora”. Com sistemas distribuídos e demandas regulatórias, registrar fatos e derivar visões virou uma vantagem competitiva. A maturidade moderna inclui: versionamento de eventos, snapshotting, idempotência, outbox/inbox e observabilidade.

- **Padrões e Protocolos Usados no Mercado**
	- **Evento (fato) vs Comando (intenção):** eventos são imutáveis; comandos podem falhar.
	- **Aggregate + invariantes:** decisões no write model; eventos descrevem o resultado.
	- **Optimistic concurrency (expected version):** evita lost updates no append.
	- **Snapshots:** reduzir tempo de rehidratação (replay) para streams longos.
	- **Projeções (read models):** visões derivadas para consulta/UX.
	- **Rebuild e replay controlado:** capacidade de reconstruir projeções.
	- **Schema evolution:** compatibilidade retroativa/adiantada (upcasters).
	- **Outbox/Inbox:** quando a fonte de eventos não é o event store dedicado.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Testar Event Sourcing exige validar invariantes no aggregate e também a correção/consistência das projeções sob duplicação, reordenação e replays. Sem testes determinísticos e contratos bem definidos, o sistema “passa” em unit tests e falha em produção com edge cases de eventos.

- **Performance e Manutenção**  
	- **Streams longos:** rehidratar milhares de eventos por request pode ser caro.
	- **Hot aggregates:** alta concorrência em um stream gera conflitos frequentes.
	- **Projeções:** podem atrasar (lag) e impactar UX.
	- **Eventos grandes:** payloads volumosos aumentam custo e latência.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: eventos sem versionamento; “eventos detalhes internos” vazando.
	- Coverage: falta de testes para replay, upcasters, migrações de projeção.
	- Flakiness: testes que dependem de tempo/infra e não controlam ordering.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Versione contratos de eventos (schema registry) e valide compatibilidade no pipeline.
	- Deploy compatível: consumidores/upcasters antes quando necessário.
	- Migrações de projeções: abordagem “side-by-side” (v1 e v2) com cutover.
	- Gate de release por métricas: lag de projeções, DLQ, taxa de conflitos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: aggregate puro (Given-When-Then de eventos).
	- Integração: event store/broker real (ou container) + projeções.
	- E2E: poucos fluxos críticos, com verificação de convergência.

- **Métrica de Qualidade**  
	- Tempo de rehidratação (p95/p99)
	- Conflitos de concorrência (expected-version failures)
	- Lag de projeções e tempo de convergência (evento → read model)
	- Taxa de reprocessamento (replays) e sucesso
	- Quebras de compatibilidade de schema

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo são didáticos (sem dependências externas) e ilustram a ideia de **append com controle de versão** e rehidratação.

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
		type: str
		data: dict


class ConcurrencyError(Exception):
		pass


class InMemoryEventStore:
		def __init__(self):
				self._streams: dict[str, list[Event]] = {}

		def load(self, stream_id: str) -> list[Event]:
				return list(self._streams.get(stream_id, []))

		def append(self, stream_id: str, expected_version: int, events: list[Event]) -> None:
				current = self._streams.get(stream_id, [])
				if len(current) != expected_version:
						raise ConcurrencyError(f"expected={expected_version} actual={len(current)}")
				self._streams[stream_id] = current + events


def rehydrate_balance(events: list[Event]) -> int:
		balance = 0
		for e in events:
				if e.type == "Deposited":
						balance += int(e.data["amount"])
				elif e.type == "Withdrawn":
						balance -= int(e.data["amount"])
		return balance
```

### C#

```csharp
public interface IEvent { }
public sealed record Deposited(int Amount) : IEvent;
public sealed record Withdrawn(int Amount) : IEvent;

public sealed class Account
{
		public int Balance { get; private set; }
		public int Version { get; private set; }

		public void Apply(IEvent e)
		{
				switch (e)
				{
						case Deposited d: Balance += d.Amount; break;
						case Withdrawn w: Balance -= w.Amount; break;
				}
				Version++;
		}
}
```

### Go

```go
package es

import "errors"

type Event struct {
		Type string
		Data map[string]any
}

var ErrConcurrency = errors.New("concurrency error")

type Store interface {
		Load(streamID string) ([]Event, error)
		Append(streamID string, expectedVersion int, events []Event) error
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Nomeie eventos como fatos de negócio**, não como chamadas de método (`OrderPaid`, não `PayOrderCommand`).
- **Imutabilidade real:** nunca “edite evento antigo”; use novos eventos e projeções.
- **Evolução de schema:** planeje compatibilidade; use upcasters quando necessário.
- **Snapshotting com critério:** snapshot demais vira outro state store; snapshot de menos vira latência.
- **Idempotência em projeções:** at-least-once é o default prático.
- **Evite PII nos eventos** quando possível; trate criptografia/retention/compliance.
- **Runbooks para replay:** replay pode causar efeitos colaterais se handlers não forem seguros.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** jobs de rebuild, autoscaling por lag, limites de memória/CPU para replays.
- **Pipelines CI/CD:** contract tests de eventos; deploy compatível; migração de projeções com versionamento.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing com correlation-id; dashboards de lag/conflitos.
- **Testes e Infra-as-Code:** provisionar tópicos/streams, políticas de retenção, DLQ e permissões.

---

## Métricas, Monitoramento e Melhoria Contínua

- Lag de projeções e tempo de convergência
- Taxa de conflitos de concorrência (expected version)
- Latência de rehidratação (p95/p99)
- Volume de eventos por aggregate e crescimento ao longo do tempo
- Erros de compatibilidade de schema e falhas de upcasting

---

## Frameworks e Ferramentas do Mercado

- **Event Stores:** EventStoreDB, Kafka (como log), DynamoDB streams (contextual)
- **Observabilidade:** OpenTelemetry, Prometheus/Grafana
- **Schemas:** Avro/Protobuf + schema registry (Confluent, etc.)
- **Python:** confluent-kafka, pydantic (schemas)
- **C#:** Marten (Postgres), MassTransit (mensageria), OpenTelemetry
- **Go:** sarama/kafka-go, OpenTelemetry

---

## Recursos Avançados e Leituras Recomendadas

- Martin Fowler (Event Sourcing)
- Greg Young (talks e artigos)
- Martin Kleppmann — _Designing Data-Intensive Applications_

---

## FAQ Especialista

**Event Sourcing é sempre Event Sourcing + CQRS?**  
Não. Eles se combinam muito bem, mas é possível ter Event Sourcing com leitura derivada “on the fly” em sistemas pequenos, ou usar CQRS sem Event Sourcing (read model separado sem log de eventos).

**Como lidar com mudanças de regra de negócio em eventos antigos?**  
Você não altera o passado. Normalmente você introduz novos eventos/versões e atualiza projeções (ou upcasters) para interpretar versões antigas.

**Quando usar snapshot?**  
Quando o custo de rehidratar começa a afetar SLO (p95/p99) ou throughput. Snapshots devem ser reconstituíveis a partir do log e versionados.

---

## Referências e Práticas do Mercado

- Martin Fowler
- Greg Young
- Kleppmann (DDIA)
- Documentação do EventStoreDB / Kafka

---

[Anterior](cqrs.md) | [Índice](../../SUMMARY.md) | [Próximo](microservices-best-practices.md)
