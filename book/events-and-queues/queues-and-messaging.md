[Anterior](../critical-operations/db-concurrency-control.md) | [Índice](../../SUMMARY.md) | [Próximo](distributed-consistency.md)

# queues-and-messaging

## Resumo
Como desenhar eventos e filas com segurança: contratos, idempotência, DLQ e consistência distribuída.

## Pontos-chave
- Entrega at-least-once exige consumidor idempotente.
- Versionamento de schema/contratos.
- DLQ e reprocessamento controlado.

## Checklist
- Mensagens têm ID de deduplicação?
- Há retry/backoff e DLQ?
- Contratos estão versionados?

---

[Anterior](../critical-operations/db-concurrency-control.md) | [Índice](../../SUMMARY.md) | [Próximo](distributed-consistency.md)
