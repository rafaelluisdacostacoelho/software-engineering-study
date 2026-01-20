[Anterior](transactions-acid.md) | [Índice](../../SUMMARY.md) | [Próximo](payments-fintech-overview.md)

# DB Concurrency Control — Controle de Concorrência em Bancos

## Visão Geral e Contexto de Mercado

Controle de concorrência é o conjunto de mecanismos que permite múltiplas transações simultâneas sem corromper invariantes do domínio. Em produção, ele aparece como a diferença entre:

- um sistema que escala com previsibilidade
- e um sistema que entra em colapso sob contenda (locks, deadlocks, timeouts, filas internas)

No mercado, os dois modelos mais comuns são:

- **Locking (pessimista):** travas explícitas (ex.: `SELECT ... FOR UPDATE`).
- **MVCC (Multiversion Concurrency Control):** leitores não bloqueiam escritores (ex.: PostgreSQL), com conflitos resolvidos em commit/locks específicos.

Em sistemas críticos, concorrência é parte do design: modelo de dados, índices, padrões de acesso e decisões de isolamento.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Bancos relacionais tradicionalmente usaram locks para garantir isolamento; MVCC ganhou adoção por melhorar concorrência de leitura e reduzir bloqueios. Hoje, sistemas combinam MVCC + locks pontuais + técnicas de concorrência otimista.

- **Padrões e Protocolos Usados no Mercado**
	- **Pessimistic locking:** locks em linhas/tabelas; útil para recursos altamente contenciosos.
	- **Optimistic concurrency:** coluna `version`/`rowversion`/ETag; falha e retry em conflito.
	- **Idempotência:** obrigatória com retries.
	- **Evitar hot spots:** particionamento/sharding lógico, chaves bem distribuídas.
	- **Sequenciamento:** filas ou “single writer per key” quando o domínio permite.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Concorrência é difícil de testar. Parte precisa de integração (banco real) e parte de simulação. Em escala, contenda muda (hot keys aparecem) e padrões “ok em dev” quebram em prod.

- **Performance e Manutenção**  
	- Índices ruins e queries não seletivas amplificam locks.
	- Transações longas seguram locks por tempo demais.
	- Níveis de isolamento fortes aumentam aborts/retries sob carga.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: falta de visibilidade (não medir lock waits/deadlocks).
	- Coverage: não testar invariantes sob concorrência.
	- Flakiness: testes concorrentes sem controle de tempo e sem ambiente dedicado.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de integração para cenários contenciosos relevantes.
	- Benchmarks/replays em pipeline (quando o risco justifica).
	- Observabilidade como gate operacional (ex.: alertas de deadlock).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: regras (sem concorrência real).
	- Integração: invariantes com concorrência real (threads/processos).
	- Testes de carga: identificar hot keys e lock contention.

- **Métrica de Qualidade**  
	- Deadlocks/timeouts por minuto
	- Lock wait time e número de bloqueios
	- Taxa de aborts/retries (conflitos)
	- p95/p99 latência por endpoint/operação

---

## Exemplos Avançados (Python, C# e Go)

Exemplos de concorrência otimista (versionamento) e retry controlado.

### Python

```python
class ConcurrencyConflict(Exception):
		pass


def update_with_version(repo, account_id: str, new_balance: int, expected_version: int) -> None:
		# Repo deve executar algo como:
		# UPDATE accounts SET balance=?, version=version+1 WHERE id=? AND version=?
		updated = repo.update_account_balance(account_id, new_balance, expected_version)
		if updated == 0:
				raise ConcurrencyConflict("version mismatch")
```

### C#

```csharp
public sealed record Account(string Id, int BalanceCents, int Version);

public interface IAccountsRepository
{
		int UpdateBalance(string id, int newBalance, int expectedVersion);
}

public static class Concurrency
{
		public static void UpdateWithVersion(IAccountsRepository repo, Account a, int newBalance)
		{
				var updated = repo.UpdateBalance(a.Id, newBalance, a.Version);
				if (updated == 0) throw new InvalidOperationException("version conflict");
		}
}
```

### Go

```go
package store

import "errors"

var ErrVersionConflict = errors.New("version conflict")

type Repo interface {
		UpdateBalance(id string, newBalance int, expectedVersion int) (int64, error)
}

func UpdateWithVersion(r Repo, id string, newBalance int, expectedVersion int) error {
		n, err := r.UpdateBalance(id, newBalance, expectedVersion)
		if err != nil {
				return err
		}
		if n == 0 {
				return ErrVersionConflict
		}
		return nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Escolha pessimista vs otimista pelo perfil de contenda:** alta contenda → pessimista ou serialização por chave; baixa contenda → otimista.
- **Sempre tenha estratégia de retry:** com limites, backoff+jitter e idempotência.
- **Reduza hot keys:** shard lógico por chave, particione tabelas, distribua carga.
- **Monitore e alerte:** deadlocks, lock waits, saturação de conexões.
- **Evite transações longas:** especialmente com IO externo.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** pool de conexões, limites de recursos e proteção contra overload.
- **Pipelines CI/CD:** testes de integração concorrente e migrações seguras.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing para identificar latência em DB + métricas de locks.
- **Testes e Infra-as-Code:** ambientes efêmeros e replays de carga.

---

## Métricas, Monitoramento e Melhoria Contínua

- Deadlocks/timeouts
- Lock wait time
- Aborts/retries
- p95/p99 de operações críticas

---

## Frameworks e Ferramentas do Mercado

- **Python:** SQLAlchemy/psycopg, pytest, testcontainers
- **C#:** EF Core (concurrency tokens), Dapper, Polly
- **Go:** database/sql, sqlc, pgx, testify
- **Observabilidade:** OpenTelemetry, Prometheus/Grafana

---

## Recursos Avançados e Leituras Recomendadas

- Postgres/MySQL docs (locks, MVCC, isolation)
- _Designing Data-Intensive Applications_ (Kleppmann)
- Martin Fowler (consistência e patterns)

---

## FAQ Especialista

**MVCC elimina locks?**  
Não. Ele reduz bloqueios de leitura, mas ainda existem locks (escrita, metadados, índices) e conflitos.

**Otimista sempre é melhor?**  
Não. Com contenda alta, você só aumenta retries e desperdício. Nesses casos, pessimista/serialização por chave pode ser melhor.

**Como diagnosticar contenda em produção?**  
Métricas do banco (lock waits/deadlocks), tracing (spans em DB) e profiling de queries/índices.

---

## Referências e Práticas do Mercado

- PostgreSQL/MySQL docs
- Google SRE (resiliência e operabilidade)
- ThoughtWorks Tech Radar

---

[Anterior](transactions-acid.md) | [Índice](../../SUMMARY.md) | [Próximo](../events-and-queues/queues-and-messaging.md)
