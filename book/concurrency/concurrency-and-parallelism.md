[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](classic-concurrency-problems.md)

# Concurrency and Parallelism — Fundamentos Avançados (Nível Sênior)

## Visão Geral e Contexto de Mercado

Concorrência e paralelismo são temas centrais em sistemas modernos: backends que atendem milhares de requisições simultâneas, pipelines assíncronas com filas, jobs em batch e serviços distribuídos. No mercado, os problemas de concorrência raramente aparecem como “bug óbvio”; eles se manifestam como:

- Intermitência (heisenbugs) e flakiness em produção
- Corrupção de estado ou duplicidade de efeitos (pagamentos, reservas)
- Deadlocks, contenção e degradação de throughput
- Latência p99 piorando por lock contention, GC e filas internas

**Concorrência** é sobre lidar com múltiplas tarefas que progridem ao mesmo tempo (interleaving). **Paralelismo** é executar realmente ao mesmo tempo (multi-core). Você pode ter concorrência sem paralelismo (um único core alternando tasks) e paralelismo sem concorrência (data parallelism em lote).

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

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Testar concorrência é difícil porque o bug depende de timing. Testes precisam ser determinísticos (ou ao menos agressivos e repetíveis), com ferramentas que aumentem a chance de interleavings “ruins”.

- **Performance e Manutenção**  
	- **Contenção:** um lock global vira gargalo conforme QPS cresce.
	- **Oversubscription:** threads demais competindo por CPU pioram throughput.
	- **Starvation:** fairness ruim em locks/filas.
	- **Fila interna invisível:** saturação por work queues não monitoradas.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: “lock em tudo” como solução padrão; ausência de limites e timeouts.
	- Coverage: não testar cancelamento, timeouts e retries.
	- Flakiness: testes que dependem de sleeps e tempos reais.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Rodar suites concorrentes com repetição (stress) em PR/nightly.
	- Habilitar race detectors, linters e analyzers (quando disponíveis).
	- Gates por regressão de p95/p99 e saturação.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: estruturas thread-safe e invariantes.
	- Integração: simular concorrência real (pool, DB locks, filas).
	- E2E: poucos fluxos críticos, validando idempotência.

- **Métrica de Qualidade**  
	- Taxa de erros por concorrência (deadlocks/timeouts)
	- p95/p99 sob carga e sob contenção
	- Tamanho/lag de filas internas
	- Retries e duplicação (idempotency failures)

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

## FAQ Especialista

**Concorrência é sempre melhor?**  
Não. Ela aumenta throughput, mas aumenta complexidade. O objetivo é cumprir SLO com previsibilidade.

**Quando usar locks vs filas?**  
Locks são úteis para seções pequenas e locais. Filas/message passing reduzem acoplamento e ajudam a escalar, mas exigem desenho de idempotência e observabilidade.

**Como reduzir bugs de concorrência?**  
Reduza estado compartilhado, use invariantes claras, adicione timeouts, e tenha testes de stress/race detection.

---

[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](classic-concurrency-problems.md)
