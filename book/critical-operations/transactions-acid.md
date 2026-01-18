[Anterior](../concurrency/classic-concurrency-problems.md) | [Índice](../../SUMMARY.md) | [Próximo](db-concurrency-control.md)

# transactions-acid

## Resumo
Práticas para integridade e consistência em operações críticas: transações, isolamento, conflitos e retries.

## Pontos-chave
- ACID e anomalias de isolamento.
- Locking vs MVCC; impacto em throughput/latência.
- Idempotência para lidar com retries.

## Checklist
- Transação tem escopo mínimo?
- Retries são idempotentes?
- Há métricas para timeouts/deadlocks?

---

[Anterior](../concurrency/classic-concurrency-problems.md) | [Índice](../../SUMMARY.md) | [Próximo](db-concurrency-control.md)
