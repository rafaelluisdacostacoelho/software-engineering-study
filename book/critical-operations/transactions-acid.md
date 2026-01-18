[Anterior](../concurrency/classic-concurrency-problems.md) | [Índice](../../SUMMARY.md) | [Próximo](db-concurrency-control.md)

# Transactions & ACID — Transações em Sistemas Críticos

## Visão Geral e Contexto de Mercado

Transações são o mecanismo clássico para garantir integridade e consistência quando múltiplas operações precisam ser tratadas como uma unidade atômica de trabalho (ex.: débito + crédito, reserva de estoque + criação de pedido). Em sistemas modernos (microserviços, filas, cloud), o desafio é que nem tudo cabe em uma única transação distribuída — então o mercado combina:

- Transações ACID **locais** (dentro de um banco/serviço)
- Consistência eventual entre serviços (sagas, outbox, idempotência)
- Controles de concorrência (locks/MVCC) para evitar anomalias

Domínios que “pagam caro” por inconsistência (finanças, inventário, billing) precisam de disciplina transacional, observabilidade e estratégias para falhas/retries.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	ACID (Atomicidade, Consistência, Isolamento, Durabilidade) consolidou-se em bancos relacionais como o modelo dominante de integridade. Com sistemas distribuídos, o uso de ACID ficou mais local (por serviço) e complementado por padrões como Sagas e Eventual Consistency.

- **Padrões e Protocolos Usados no Mercado**
	- **ACID:**
		- Atomicidade: tudo ou nada.
		- Consistência: invariantes do domínio não podem ser violados.
		- Isolamento: concorrência sem anomalias “indesejadas”.
		- Durabilidade: commit persiste.
	- **Isolamento (níveis típicos):** Read Committed, Repeatable Read, Serializable.
	- **Padrões complementares:**
		- **Outbox pattern** (publicação confiável de eventos)
		- **Idempotency keys** (retries seguros)
		- **Optimistic concurrency control** (versionamento/ETag)
		- **Deadlock handling** (retries com backoff)
	- **Práticas de mercado:** timeouts, limites de escopo de transação, filas para suavizar picos.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em sistemas grandes, o risco é “transação demais” (locks longos) ou “transação de menos” (inconsistência). Testes precisam cobrir invariantes e cenários concorrentes (race conditions), frequentemente com testes de integração.

- **Performance e Manutenção**  
	- Transações longas reduzem throughput e aumentam contenda.
	- Níveis de isolamento mais fortes podem aumentar latência.
	- Índices e padrões de acesso determinam se lock contention vira gargalo.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: lógica crítica fora de transação, falta de idempotência, ausência de monitoramento de deadlocks/timeouts.
	- Coverage: testes que não exercitam concorrência e isolamento.
	- Flakiness: testes concorrentes sem controle de tempo/ambiente.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Migrations seguras: expand/contract, compatibilidade retroativa.
	- Testes de integração para fluxos transacionais críticos.
	- Observabilidade (métricas de lock waits, deadlocks, retries) como gate operacional.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: invariantes e regras puras.
	- Integração: transações reais no banco (idealmente com ambiente efêmero).
	- E2E: poucos fluxos críticos com dados controlados.
	- Mocks: úteis para portas externas; para transação/isolamento, prefira infra real.

- **Métrica de Qualidade**  
	- Taxa de deadlocks/timeouts
	- Tempo de lock wait e contenda por tabela/chave
	- Taxa de retries e falhas por concorrência
	- Incidentes por inconsistência (ex.: saldo negativo, estoque abaixo de zero)

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos focam em: (1) escopo mínimo de transação, (2) idempotência e (3) concorrência otimista.

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
		id: str
		balance_cents: int
		version: int


class OptimisticConcurrencyError(Exception):
		pass


def transfer(tx, from_id: str, to_id: str, amount_cents: int) -> None:
		# tx: abstração de transação (adapter) — manter o escopo mínimo
		if amount_cents <= 0:
				raise ValueError("amount must be positive")

		a = tx.get_account_for_update(from_id)
		b = tx.get_account_for_update(to_id)
		if a.balance_cents < amount_cents:
				raise ValueError("insufficient funds")

		tx.update_balance(from_id, a.balance_cents - amount_cents)
		tx.update_balance(to_id, b.balance_cents + amount_cents)
		tx.insert_ledger_entry(from_id, -amount_cents)
		tx.insert_ledger_entry(to_id, +amount_cents)
```

### C#

```csharp
public sealed record TransferCommand(string FromId, string ToId, int AmountCents, string IdempotencyKey);

public interface ITransfersRepository
{
		bool ExistsByIdempotencyKey(string key);
		void SaveIdempotencyKey(string key);
}

public sealed class TransferService
{
		private readonly ITransfersRepository _repo;

		public TransferService(ITransfersRepository repo) => _repo = repo;

		public void Execute(TransferCommand cmd)
		{
				if (cmd.AmountCents <= 0) throw new ArgumentOutOfRangeException(nameof(cmd.AmountCents));

				// padrão comum: idempotency key antes/na mesma transação
				if (_repo.ExistsByIdempotencyKey(cmd.IdempotencyKey)) return;
				_repo.SaveIdempotencyKey(cmd.IdempotencyKey);

				// aqui entraria a transação com update de contas + ledger
		}
}
```

### Go

```go
package app

import (
		"context"
		"database/sql"
		"errors"
)

var ErrInsufficientFunds = errors.New("insufficient funds")

func Transfer(ctx context.Context, db *sql.DB, fromID, toID string, amount int) error {
		if amount <= 0 {
				return errors.New("amount must be positive")
		}

		tx, err := db.BeginTx(ctx, nil)
		if err != nil {
				return err
		}
		defer func() { _ = tx.Rollback() }()

		// Exemplo conceitual: SELECT ... FOR UPDATE para travar linhas
		// saldoA := ...
		// if saldoA < amount { return ErrInsufficientFunds }
		// UPDATE accounts SET balance = balance - ? WHERE id = ?
		// UPDATE accounts SET balance = balance + ? WHERE id = ?

		if err := tx.Commit(); err != nil {
				return err
		}
		return nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Escopo mínimo de transação:** faça validações fora quando possível (sem quebrar invariantes), e deixe dentro apenas o que precisa ser atômico.
- **Evite transações longas:** não chame serviços externos dentro da transação.
- **Escolha isolamento conscientemente:** Serializable resolve anomalias, mas pode custar caro; avalie com dados.
- **Idempotência sempre que houver retry:** filas e redes repetem mensagens.
- **Use retries com backoff + jitter** para deadlocks/timeouts.
- **Modelo de dados ajuda:** bons índices e chaves de acesso reduzem contenda.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** considere latência e timeouts; configure readiness/liveness para evitar picos no banco.
- **Pipelines CI/CD:** migrações seguras e testes de integração transacional.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards de deadlocks, lock waits, saturação de conexões.
- **Testes e Infra-as-Code:** ambientes efêmeros para reproduzir contenda e validar configurações.

---

## Métricas, Monitoramento e Melhoria Contínua

- Deadlocks/minuto e timeouts
- Lock wait time
- Retries por operação e taxa de sucesso
- Incidentes por inconsistência

---

## Frameworks e Ferramentas do Mercado

- **Python:** SQLAlchemy, psycopg, pytest + testcontainers
- **C#:** EF Core, Dapper, xUnit, Polly (retries)
- **Go:** database/sql, sqlc, testify
- **Observabilidade:** OpenTelemetry, Prometheus/Grafana

---

## Recursos Avançados e Leituras Recomendadas

- _Designing Data-Intensive Applications_ (Kleppmann)
- _Release It!_ (Nygard)
- Documentação do PostgreSQL/MySQL sobre isolamento e MVCC

---

## FAQ Especialista

**ACID resolve consistência entre microserviços?**  
Não diretamente. ACID é local (por banco/transação). Entre serviços, use padrões como Sagas, Outbox e idempotência.

**Serializable é sempre a resposta?**  
Não. Às vezes Read Committed + locks pontuais + invariantes no modelo é suficiente. Decida com base em risco e carga.

**Por que idempotência é tão crítica?**  
Porque retries acontecem (rede, timeouts, deadlocks). Sem idempotência, você duplica efeitos (double charge, double shipment).

---

## Referências e Práticas do Mercado

- Postgres/MySQL docs (MVCC, isolation levels)
- Martin Fowler (padrões de transação e consistência)
- Google SRE (operabilidade)

---

[Anterior](../concurrency/classic-concurrency-problems.md) | [Índice](../../SUMMARY.md) | [Próximo](db-concurrency-control.md)
