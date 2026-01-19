[Anterior](concurrency-and-parallelism.md) | [Índice](../../SUMMARY.md) | [Próximo](../critical-operations/transactions-acid.md)

# Classic Concurrency Problems — Guia Prático (Nível Sênior)

## Visão Geral e Contexto de Mercado

Os “problemas clássicos” de concorrência são importantes porque eles aparecem disfarçados em bugs reais: processamento duplicado, ordens inconsistentes, filas travadas e serviços que entram em degradação sob pico.

No mercado, você não “resolve dining philosophers”; você resolve:

- Dois workers processando a mesma mensagem
- Uma atualização concorrente perdendo estado (lost update)
- Um deadlock de DB em pico
- Um lock global causando p99 alto

O valor desses clássicos é oferecer um vocabulário e um conjunto de padrões para diagnosticar e corrigir.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Os problemas clássicos surgiram para explicar limites e perigos de sincronização. Em sistemas modernos, os mesmos padrões reaparecem em bancos (locks), filas (competing consumers), caches (stampede) e serviços distribuídos (sagas/retries).

- **Padrões e Protocolos Usados no Mercado**
	- **Mutual exclusion:** mutex/lock, critical section.
	- **Semáforos:** limitar concorrência e coordenar recursos.
	- **Condition variables / wait-notify:** sincronizar eventos.
	- **Channels/queues:** comunicação segura por mensagens.
	- **Optimistic concurrency:** versões/ETags para evitar lost update.
	- **Idempotência e dedupe:** para reprocessamento e at-least-once.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O bug costuma depender de timing e carga. Se você não força concorrência nos testes (stress/race), ele aparece só em produção.

- **Performance e Manutenção**  
	- Soluções “seguras” podem ser lentas (lock global).
	- Soluções “rápidas” podem ser erradas (lock insuficiente).
	- Diagnóstico exige métricas e visibilidade de bloqueios.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: sincronização espalhada e sem invariantes.
	- Coverage: ausência de testes que exercitam interleavings.
	- Flakiness: testes com `sleep` e tempos reais.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Stress tests e race detection (quando disponível) como parte do pipeline.
	- Testes de idempotência para handlers e jobs.
	- Monitoramento de deadlocks/timeouts e alarmes por p99.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: proteger invariantes e comportamento sob concorrência local.
	- Integração: DB/Redis/broker real para validar locking e competing consumers.
	- E2E: fluxos críticos com repetição e carga.

- **Métrica de Qualidade**  
	- Taxa de deadlocks/timeouts
	- Duplicação (idempotency failures)
	- Tempo de fila/lag
	- Throughput e p95/p99

---

## Exemplos Avançados (Python, C# e Go)

Exemplos didáticos de três problemas clássicos: race condition, deadlock (por ordem de locks) e lost update (com controle otimista).

### Python

```python
import threading


lock_a = threading.Lock()
lock_b = threading.Lock()


def safe_lock_order():
		# Regra de mercado: ordem fixa evita deadlock.
		with lock_a:
				with lock_b:
						return "ok"
```

### C#

```csharp
// Lost update prevention (conceitual) via optimistic concurrency.
public sealed record Account(string Id, int Balance, int Version);

public sealed class ConcurrencyException : Exception { }

public interface IAccountsRepo {
		Account Get(string id);
		void Save(Account account, int expectedVersion);
}

public sealed class Service
{
		private readonly IAccountsRepo _repo;
		public Service(IAccountsRepo repo) => _repo = repo;

		public void Deposit(string id, int amount)
		{
				var acc = _repo.Get(id);
				var updated = acc with { Balance = acc.Balance + amount, Version = acc.Version + 1 };
				_repo.Save(updated, expectedVersion: acc.Version);
		}
}
```

### Go

```go
package locks

import "sync"

var a sync.Mutex
var b sync.Mutex

func SafeOrder() {
		a.Lock()
		defer a.Unlock()
		b.Lock()
		defer b.Unlock()
		// critical section
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Ordem de locks é uma política:** documente e aplique (code review).
- **Evite lock global:** prefira granularidade por chave/aggregate.
- **Use timeouts e degrade:** bloquear indefinidamente é convite para incidentes.
- **Idempotência para processamento assíncrono:** handlers precisam suportar duplicação.
- **Controle otimista em atualizações concorrentes:** ETags/version em APIs e DB.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** picos e autoscaling alteram concorrência efetiva; proteja recursos com limites.
- **Pipelines CI/CD:** testes de stress/race e validação de idempotência.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing e métricas de bloqueio/lag.
- **Testes e Infra-as-Code:** brokers/DB provisionados para testes de concorrência.

---

## Métricas, Monitoramento e Melhoria Contínua

- Deadlocks/timeouts
- Retries e DLQ (se houver fila)
- Lag de consumidor
- p95/p99 e throughput

---

## Frameworks e Ferramentas do Mercado

- **Python:** asyncio, threading, locust (carga)
- **C#:** async/await, TPL, analyzers e tracing
- **Go:** goroutines/channels, `-race`, pprof

---

## Recursos Avançados e Leituras Recomendadas

- “The Little Book of Semaphores”
- Materiais sobre idempotência e retries em sistemas distribuídos
- Kleppmann (DDIA)

---

## FAQ Especialista

**Deadlock sempre acontece por dois locks?**  
Não. Pode envolver múltiplos recursos (DB locks, filas, mutexes). O padrão é: dependência circular + retenção de recursos.

**Como diagnosticar deadlock em produção?**  
Métricas de tempo bloqueado, tracing (spans longos), dumps/diagnostics (quando disponível) e correlação com picos.

**Lost update acontece só em memória?**  
Não. É comum em DB e APIs. Use transações, locks, ou controle otimista com versões.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](concurrency-and-parallelism.md) | [Índice](../../SUMMARY.md) | [Próximo](../critical-operations/transactions-acid.md)
