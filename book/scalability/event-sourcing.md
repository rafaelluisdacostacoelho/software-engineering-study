[Anterior](cqrs.md) | [Índice](../../SUMMARY.md) | [Próximo](microservices-best-practices.md)

# Event Sourcing — Guia Avançado

## Visão Geral e Contexto de Mercado

Event Sourcing é um estilo arquitetural em que a **fonte de verdade** do sistema não é o “estado atual” gravado no banco, e sim o **histórico de mudanças**: uma sequência **append-only** de **eventos imutáveis** (fatos do domínio que aconteceram).

O **estado atual** de uma entidade é obtido ao **reconstruir** (rehydrate) a partir desse histórico — isto é, **reaplicando os eventos na ordem em que ocorreram** — ou consultando uma **projeção/read model** materializada a partir deles.

### Intuição (por que isso existe?)
Em vez de salvar “como está agora”, você salva “o que aconteceu”. Isso tende a ser mais estável ao longo do tempo, porque:
- regras e telas mudam, mas os **fatos do domínio** (“PedidoPago”, “ItemAdicionado”) permanecem úteis;
- você ganha **trilha de auditoria** natural;
- é possível reconstruir e comparar **diferentes visões** do mesmo passado (novos relatórios, novos read models, correções).

Uma analogia útil é pensar em um **extrato bancário**: o saldo é derivado da soma das movimentações; o extrato (eventos) é a fonte de verdade.

### Como “estado” vira eventos na prática
Normalmente há uma separação clara entre:
- **Comandos** (*intenções*): “PagarPedido”, “AdicionarItem”
- **Eventos** (*fatos*): “PedidoPago”, “ItemAdicionado”

O fluxo típico no write model:
1. Carrega eventos do stream do aggregate (rehydrate).
2. Valida regras/invariantes com base no estado derivado.
3. Emite novos eventos (resultado).
4. Persiste via **append** com controle de concorrência (expected version).

O read model (consultas) vem de **projeções** que consomem eventos e materializam visões para leitura (tabelas, documentos, índices).

### Onde o mercado usa (quando faz sentido)
Event Sourcing aparece mais quando há **alto valor no histórico** e/ou na capacidade de **reconstrução**:
- Auditoria e rastreabilidade mandatórias (fintech, seguros, logística, compliance)
- Domínios com regras complexas e evolução frequente (precificar, antifraude, limites, crédito)
- Necessidade de **replay/backfill** (corrigir bug em projeção, criar uma visão nova, reprocessar um período)
- Integrações e workflows assíncronos (muitos consumidores do mesmo fato)

Em sistemas simples (CRUD clássico, baixo risco, poucas regras), o custo costuma superar os ganhos.

### Benefícios reais (quando bem feito)
- **Auditabilidade por padrão** (quem/quando/o quê aconteceu)
- **Rebuild de read models** (novas consultas sem “migrar histórico” manualmente)
- **Depuração e análises** (replay para reproduzir bugs e entender comportamento)
- **Integração orientada a eventos** (múltiplos consumidores, evolução de features por projeções)

### Trade-offs e complexidades (o que geralmente pega)
- **Modelo mental**: pensar em fatos e efeitos ao longo do tempo (não em “update”)
- **Consistência eventual** nas leituras (read model pode atrasar)
- **Evolução de schema** (eventos “duram para sempre”, exigem compatibilidade/upcasters)
- **Idempotência** e tolerância a duplicação/reordenação em consumidores
- **Custo operacional** (replay controlado, snapshotting, observabilidade, DLQ)

### Relação com CQRS (por que andam juntos)
Event Sourcing *não exige* CQRS, mas a combinação é comum porque:
- o write model foca em **decisão** (invariantes e emissão de eventos);
- o read model foca em **consulta** (projeções otimizadas);
- isso reduz acoplamento e permite evoluir leituras independentemente.

### Implementação: event store dedicado vs log (Kafka)
- **Event store dedicado** (ex.: EventStoreDB): stream por aggregate, controle de versão, APIs de leitura/append.
- **Log distribuído** (ex.: Kafka): excelente para distribuição e replay, mas você ainda precisa decidir como tratar concorrência, particionamento por aggregate e garantias de gravação/leitura.

Regra prática: se o sistema precisa de **streams por entidade + expected version + leitura eficiente por stream**, um event store facilita. Se a prioridade é **distribuição e integração** em escala, Kafka é forte (muitas vezes com outbox/inbox).

Em resumo: Event Sourcing troca “atualizar estado” por “registrar fatos”. Você ganha histórico, auditoria e poder de reconstrução, mas precisa assumir disciplina de modelagem, compatibilidade e operação para manter o sistema previsível em produção.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	A motivação original é simples: “o que aconteceu” é mais estável do que “como represento agora”. Com sistemas distribuídos e demandas regulatórias, registrar fatos e derivar visões virou uma vantagem competitiva. A maturidade moderna inclui: versionamento de eventos, snapshotting, idempotência, outbox/inbox e observabilidade.

- **Padrões e Protocolos Usados no Mercado**
	- **Evento (fato) vs Comando (intenção)**
		- **Comando** representa uma *intenção* (“Quero pagar o pedido”) e é validado no momento da decisão. Pode falhar por regra de negócio, autorização, limites, etc.
		- **Evento** representa um *fato que já aconteceu* (“PedidoPago”) e, uma vez persistido/publicado, **não deve ser alterado**.
		- **Implicações práticas:**
			- Comandos são normalmente *endereçados* a um aggregate (um “destino”) e executados de forma síncrona/assíncrona.
			- Eventos são *distribuídos* e *consumidos* (publish/subscribe) por múltiplas projeções/serviços.
			- Eventos devem carregar contexto suficiente para reconstrução/auditoria, mas sem vazar detalhes internos desnecessários.
		- **Regra de ouro:** comando é “pode acontecer”; evento é “aconteceu”.

	- **Aggregate + invariantes (write model orientado a decisão)**
		- O **aggregate** é o limite transacional onde você garante **invariantes** (regras que nunca podem ser violadas), por exemplo: “saldo não pode ficar negativo”, “pedido não pode ser pago duas vezes”.
		- Fluxo típico:
			1) Carregar eventos do stream do aggregate (rehydrate).  
			2) Executar o comando validando invariantes.  
			3) Emitir novos eventos descrevendo o resultado.  
			4) Persistir (append) com controle de concorrência.
		- **Boas práticas:**
			- Mantenha aggregates **pequenos** (menos eventos por decisão) e coesos (uma única responsabilidade).
			- Evite invariantes “globais” que exigem múltiplos aggregates; quando inevitável, use processos (sagas/process managers) e aceite consistência eventual.

	- **Optimistic concurrency (expected version)**
		- Como múltiplos writers podem tentar gravar no mesmo stream, o append geralmente usa **expected version** (ou ETag) para evitar *lost updates*.
		- Se a versão esperada não bate com a versão atual do stream, ocorre **conflito** (expected-version failure) e o writer precisa:
			- Recarregar eventos, reavaliar o comando e tentar novamente (retry), ou
			- Rejeitar se a intenção ficou inválida (ex.: o estado mudou).
		- **Pontos de atenção:**
			- Hot aggregates geram muitos conflitos; pode ser sinal para rever a modelagem (particionamento, sharding lógico, split de aggregate).
			- Retentativas precisam ser limitadas e observáveis (métrica de conflitos).

	- **Snapshots (redução do custo de rehidratação)**
		- Snapshot é um “checkpoint” do estado derivado até uma versão do stream, para evitar reaplicar milhares de eventos em cada carregamento.
		- Estratégias comuns:
			- A cada **N eventos** (ex.: 200/500), ou
			- Por **tempo** (ex.: a cada X horas), ou
			- Por **SLO** (quando p95/p99 de rehidratação excede um limite).
		- **Cuidados:**
			- Snapshot é um **cache** reconstruível; não substitui o log de eventos.
			- Versione snapshots (mudanças no modelo exigem migração/rebuild).
			- Snapshotting excessivo adiciona complexidade e custo de armazenamento.

	- **Projeções (read models)**
		- Projeções transformam eventos em visões otimizadas para leitura (tabelas, documentos, índices), normalmente com **consistência eventual**.
		- Padrões frequentes:
			- Projeção “por tela” (read model focado em UX).
			- Projeção “por relatório” (agregações e métricas).
			- Materialização em bancos diferentes (Postgres, Elastic, Redis, etc.).
		- **Requisitos de robustez:**
			- **Idempotência** (reprocessar o mesmo evento não pode corromper o read model).
			- Tolerância a **duplicação** e **reordenação** (conforme a entrega do broker/infra).
			- Checkpoint/offset bem controlado (saber “até onde processei”).

	- **Rebuild e replay controlado**
		- A capacidade de **reconstruir projeções** a partir do log é um dos maiores benefícios do Event Sourcing (correção de bugs, novas visões, auditorias, backfills).
		- Práticas de mercado:
			- Rebuild “side-by-side”: projeção v2 roda em paralelo com v1 e depois ocorre o cutover.
			- Replay com *throttling* (controle de taxa) para não derrubar bancos/serviços.
			- Isolamento de efeitos colaterais: handlers de projeção não devem enviar e-mails/pagamentos; isso pertence a fluxos transacionais/compensáveis separados.
		- **Operação:** trate rebuild como um job com observabilidade (tempo estimado, taxa, erros, DLQ).

	- **Schema evolution (compatibilidade e versionamento)**
		- Eventos vivem “para sempre”, então você precisa de regras claras de evolução:
			- Preferir mudanças **aditivas** (novos campos opcionais).
			- Evitar renomes/remoções sem estratégia (quebra de consumidores antigos).
			- Definir compatibilidade **backward/forward** e validar em CI (ex.: schema registry).
		- **Upcasters** (ou adapters) convertem eventos antigos para um formato novo em tempo de leitura/replay, permitindo que código atual lide com versões anteriores.
		- **Prática recomendada:** versionar explicitamente o schema do evento (ex.: `eventVersion`) e manter testes de compatibilidade.

	- **Outbox/Inbox (integração quando o “event store” não é o broker)**
		- Quando seu sistema persiste estado em um banco transacional e publica eventos em um broker, surge o risco do “salvou no banco mas não publicou” (ou o inverso).
		- **Outbox pattern:** gravar a mensagem/evento em uma tabela outbox **na mesma transação** do write; um worker publica no broker e marca como enviado.
		- **Inbox pattern:** do lado consumidor, registrar o `messageId/eventId` já processado para garantir **deduplicação** (idempotência) em entregas at-least-once.
		- **Quando usar:** integrações entre serviços, CDC, Kafka, e cenários onde o commit do banco precisa ser consistente com a publicação.
		- **Observabilidade:** DLQ, retries, backoff, e métricas de backlog (outbox pendente / inbox duplicadas).

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
