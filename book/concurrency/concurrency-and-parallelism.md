[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](memory-model-and-atomics.md)

# Concurrency and Parallelism — Fundamentos Avançados (Nível Sênior)

## Visão Geral e Contexto de Mercado

Concorrência e paralelismo são temas centrais em sistemas modernos: backends que atendem milhares de requisições simultâneas, pipelines assíncronas com filas, jobs em batch e serviços distribuídos. No mercado, os problemas de concorrência raramente aparecem como “bug óbvio”; eles se manifestam como:

- Intermitência (heisenbugs) e flakiness em produção
- Corrupção de estado ou duplicidade de efeitos (pagamentos, reservas)
- Deadlocks, contenção e degradação de throughput
- Latência p99 piorando por lock contention, GC e filas internas

**Concorrência** é sobre lidar com múltiplas tarefas que progridem ao mesmo tempo (interleaving). **Paralelismo** é executar realmente ao mesmo tempo (multi-core). Você pode ter concorrência sem paralelismo (um único core alternando tasks) e paralelismo sem concorrência (data parallelism em lote).

Uma forma pratica de pensar:

- Concorrencia e sobre **coordenacao** (ordem, exclusao, cancelamento, limites).
- Paralelismo e sobre **capacidade** (usar mais cores sem piorar corretude).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O mercado saiu do “um thread por request” para modelos mais eficientes e seguros: async/await, event loops, actor model e filas. Ao mesmo tempo, a disciplina de “sistemas resilientes” reforçou padrões como idempotência, timeouts e backpressure.

- **Padrões e Protocolos Usados no Mercado**
	- **Imutabilidade e pure functions:** reduzir estado compartilhado.
	- **Thread confinement:** estado só acessado por uma thread/loop.
	- **Locking disciplinado:** ordem de locks, granularidade, timeouts.
	- **Message passing / queues:** desacoplamento e isolamento de estado.
	- **Actor model:** um ator = mailbox + estado encapsulado.
	- **Idempotência + dedupe:** quando há retries e at-least-once.
	- **Backpressure:** limitar produtores com base na capacidade do consumidor.
	- **Concurrency primitives:** semáforos, mutex, RWLock, channels.

### Modelos de concorrencia (trade-off central)

- **Shared memory + locks**
	- Pratico localmente, mas exige disciplina (invariantes, ordem de locks).
- **Message passing** (channels/queues)
	- Reduz compartilhamento de estado; exige idempotencia e observabilidade.
- **Actor model**
	- Estado encapsulado por ator; cuidado com mailbox ilimitada.

Nenhum modelo evita falhas por magica: ele desloca complexidade (ex.: de deadlock para backpressure).

### CPU-bound vs IO-bound (decisao que evita erros de arquitetura)

- **IO-bound**: async/event loop costuma aumentar throughput e reduzir threads.
- **CPU-bound**: paralelizar faz sentido; async nao cria mais CPU.

Uma regra pratica: se o gargalo e CPU, pense em paralelismo; se e espera de IO, pense em concorrencia controlada.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Testar concorrência é difícil porque o bug depende de timing. Testes precisam ser determinísticos (ou ao menos agressivos e repetíveis), com ferramentas que aumentem a chance de interleavings “ruins”.

- **Performance e Manutenção**  
	- **Contenção:** um lock global vira gargalo conforme QPS cresce.
	- **Oversubscription:** threads demais competindo por CPU pioram throughput.
	- **Starvation:** fairness ruim em locks/filas.
	- **Fila interna invisível:** saturação por work queues não monitoradas.

### Corretude antes de throughput

Em sistemas criticos, a prioridade costuma ser:

1. **Corretude** (invariantes nao podem quebrar)
2. **Previsibilidade** (degradar bem sob pico)
3. **Performance** (otimizar depois com dados)

Otimizacao sem invariantes vira incidente.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: “lock em tudo” como solução padrão; ausência de limites e timeouts.
	- Coverage: não testar cancelamento, timeouts e retries.
	- Flakiness: testes que dependem de sleeps e tempos reais.

---

## Estratégias Avançadas e Decisões Arquiteturais

### Structured concurrency e cancelamento

Um problema recorrente em sistemas async e "task vazando": a request termina, mas o trabalho continua em background sem dono.

Principios:

- Tasks devem ter **escopo** (request, job, batch).
- Cancelamento deve ser propagado (context/cancellation token).
- Sempre defina timeouts para chamadas remotas e operacoes bloqueantes.

Isso melhora p99 e reduz custos.

- **Integração com CI/CD**
	- Rodar suites concorrentes com repetição (stress) em PR/nightly.
	- Habilitar race detectors, linters e analyzers (quando disponíveis).
	- Gates por regressão de p95/p99 e saturação.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: estruturas thread-safe e invariantes.
	- Integração: simular concorrência real (pool, DB locks, filas).
	- E2E: poucos fluxos críticos, validando idempotência.

- **Métrica de Qualidade (explicado como livro)**  

	Metrica de concorrencia nao serve para "ter numero". Ela serve para responder duas perguntas de operacao:

	1) **O sistema esta correto sob concorrencia?** (nao duplica efeito, nao trava)  
	2) **O sistema eh previsivel sob carga?** (p99 controlado, sem backlog infinito)

	Abaixo estao as metricas mais importantes e como interpretar.

	### 1) Taxa de erros por concorrencia (deadlocks, timeouts, cancelamentos)

	**O que eh**
	- Erros causados por competicao por recursos, espera excessiva, ou dependencia circular.
	- Exemplos: deadlock no DB, timeout ao adquirir lock, timeout de request por backlog.

	**Por que importa**
	- Em concorrencia, o sistema falha de forma "coletiva": uma espera bloqueia outras, que bloqueiam outras.
	- Deadlock/timeout costuma ser sinal de **contencao** ou **politica ruim** (ex.: lock order, transacoes longas).

	**Como medir (pratico)**
	- Counters separados por causa: `deadlock_total`, `lock_timeout_total`, `request_timeout_total`.
	- Se houver fila, medir tambem `consumer_timeout_total` e DLQ/quarantine.

	**Como usar**
	- Use taxa (erros por minuto) e tambem proporcao (erros / requests) para evitar alarmes falsos quando o trafego sobe.
	- Correlacione com p99 e backlog: se tudo sobe junto, e overload/contencao.

	### 2) p95/p99 (e por que a cauda eh o que mata)

	**Percentil** e um resumo de distribuicao. `p99` significa: em 99% das requisicoes, a latencia foi **menor ou igual** a esse valor.

	- `p50` (mediana) descreve o "usuario tipico".
	- `p95` descreve usuarios que ja estao perto do limite do aceitavel.
	- `p99` descreve a **cauda**: as piores experiencias que, em concorrencia, tendem a crescer primeiro.

	**Por que concorrencia afeta a cauda**
	- Quando ha contencao, algumas requests entram em espera (lock, fila, DB).  
	- Mesmo que a maioria passe rapido, uma fração fica presa e empurra `p99`.

	**Sob carga vs sob contencao**
	- "Sob carga": o sistema esta ocupado, mas continua fluindo.
	- "Sob contencao": o sistema esta bloqueando (locks, filas, saturacao de downstream).
	- Em geral, contencao aparece como: `p50` razoavel, mas `p99` explode.

	**Como medir corretamente**
	- Percentis em producao devem vir de **histogramas** (ou ferramentas equivalentes) e nao de medias.
	- Media esconde cauda: duas requests de 10ms e uma de 3s podem parecer "ok" na media.
	- Sempre registre unidade (ms, s) e escopo (endpoint, operacao, dependencia).

	**Como usar**
	- Defina SLO (ex.: "p99 < 300ms") para operacoes criticas.
	- Quando `p99` piora, pergunte: "qual fila/lock/downstream virou gargalo?"

	### 3) Tamanho e lag de filas internas (queue depth, queue age, consumer lag)

	**O que eh**
	- `queue_depth`: quantos itens estao esperando.
	- `queue_age`: idade do item mais antigo (tempo desde enqueue).
	- `consumer_lag`: atraso entre producao e consumo (muito comum em streaming/brokers).

	**Por que importa**
	- Backlog cresce quando o **rate de entrada** supera o **rate sustentavel de processamento**.
	- Fila ilimitada e um bug de capacidade: vira latencia, custo e risco de OOM.

	**Interpretacao pratica**
	- `queue_depth` pode oscilar e ainda assim estar ok.
	- `queue_age` subindo continuamente e o sinal mais forte de que o sistema nao esta drenando.
	
	**Como usar**
	- Se `queue_age` sobe e `p99` sobe, o gargalo esta no consumo (workers ou downstream).
	- Se `queue_depth` sobe mas `queue_age` nao, pode ser burst temporario.

	### 4) Retries e duplicacao (idempotency failures)

	**O que eh**
	- Retry: tentativa extra por timeout/erro transiente.
	- Duplicacao: o mesmo comando/evento gerou efeito duas vezes (bug grave em dinheiro).

	**Por que acontece**
	- Muitos sistemas sao at-least-once (fila, webhook, retry client). Duplicidade e esperada.
	- O sistema deve ser idempotente, ou voce transforma falha transiente em efeito duplicado.

	**Como medir**
	- `retries_total` por causa (timeout, 5xx, deadlock).
	- `dedup_hits_total` (quantas vezes a idempotency key evitou duplicacao).
	- `idempotency_failures_total` (quando houve duplicacao ou inconsistencia detectada).

	**Como usar**
	- `dedup_hits_total` alto pode ser normal (webhooks duplicados).
	- `idempotency_failures_total` nao pode existir em fluxo de dinheiro: e bug/incident.
	- Retrys sem jitter e sem limite sao um acelerador de incidentes.

---

## Exemplos Avançados (Python, C# e Go)

Exemplos didáticos de como proteger seção crítica e como limitar concorrência.

### Python

```python
import threading


class Counter:
		def __init__(self):
				self._value = 0
				self._lock = threading.Lock()

		def inc(self) -> int:
				with self._lock:
						self._value += 1
						return self._value
```

### C#

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

public sealed class RateLimitedWorker
{
		private readonly SemaphoreSlim _gate;
		public RateLimitedWorker(int maxConcurrency) => _gate = new SemaphoreSlim(maxConcurrency);

		public async Task RunAsync(Func<Task> job)
		{
				await _gate.WaitAsync();
				try { await job(); }
				finally { _gate.Release(); }
		}
}
```

### Go

```go
package worker

import "sync"

type Counter struct {
		mu sync.Mutex
		v  int
}

func (c *Counter) Inc() int {
		c.mu.Lock()
		defer c.mu.Unlock()
		c.v++
		return c.v
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Evite estado compartilhado por padrão:** prefira imutabilidade e message passing.
- **Timeout em tudo que bloqueia:** locks, IO, chamadas remotas e filas.
- **Retries exigem idempotência:** sem isso, você cria duplicidade.
- **Cuidado com “sleep-based synchronization”:** quase sempre vira flakiness.
- **Não superdimensione threads:** limites e backpressure são parte do design.
- **Observabilidade de filas e locks:** sem métricas, você só descobre em incidente.

### Checklist de review (concurrency)

- Existe limite de concorrencia por recurso (DB, cache, provider)?
- Existe timeout em operacoes bloqueantes?
- Existe idempotencia onde ha retries?
- Existe observabilidade de contencao e fila (queue depth, lock wait)?
- Existe plano de degradacao sob overload?

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** limites de CPU/memória mudam scheduler e latência; teste sob limites reais.
- **Pipelines CI/CD:** race detectors, stress tests e perf tests por endpoint crítico.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing, métricas de fila, alerts de deadlock/timeouts.
- **Testes e Infra-as-Code:** ambientes reproduzíveis para carga e concorrência.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95/p99 sob carga
- Deadlocks/timeouts por dependência
- Tamanho/lag de filas internas
- Retries e taxa de duplicação

---

## Frameworks e Ferramentas do Mercado

- **Python:** threading/asyncio, pytest-xdist (paralelismo), observabilidade via OpenTelemetry
- **C#:** TPL, async/await, dotnet-trace, analyzers
- **Go:** goroutines/channels, race detector (`-race`), pprof

---

## Recursos Avançados e Leituras Recomendadas

- “The Little Book of Semaphores” (problemas clássicos)
- Artigos/talks sobre backpressure e concurrency models
- Kleppmann (DDIA) para impacto em sistemas distribuídos

---

## Proximos capitulos (sequencia recomendada)

- Memory model e happens-before
- Primitivas e contencao
- Classicos e como eles aparecem em producao
- Async e backpressure
- Teste e debug

---

## FAQ Especialista

**Concorrência é sempre melhor?**  
Não. Ela aumenta throughput, mas aumenta complexidade. O objetivo é cumprir SLO com previsibilidade.

**Quando usar locks vs filas?**  
Locks são úteis para seções pequenas e locais. Filas/message passing reduzem acoplamento e ajudam a escalar, mas exigem desenho de idempotência e observabilidade.

**Como reduzir bugs de concorrência?**  
Reduza estado compartilhado, use invariantes claras, adicione timeouts, e tenha testes de stress/race detection.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](memory-model-and-atomics.md)
