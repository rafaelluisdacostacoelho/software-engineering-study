[Anterior](transactions-acid.md) | [Índice](../../SUMMARY.md) | [Próximo](../events-and-queues/queues-and-messaging.md)

# db-concurrency-control

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

[Anterior](transactions-acid.md) | [Índice](../../SUMMARY.md) | [Próximo](../events-and-queues/queues-and-messaging.md)
