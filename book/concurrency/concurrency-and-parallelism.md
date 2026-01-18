[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](classic-concurrency-problems.md)

# Concurrency and Parallelism

## Resumo
Conceitos práticos de concorrência/paralelismo, problemas clássicos e estratégias para evitar bugs difíceis.

## Problemas clássicos
- Race conditions e estado compartilhado.
- Deadlock (ordem de locks), starvation e livelock.

## Estratégias
- Reduza estado compartilhado; prefira mensagens/filas.
- Imutabilidade quando possível.
- Timeouts, backoff e observabilidade para contenção.

## Checklist
- Ordem de locks consistente?
- Se der retry, ele é seguro?
- Existe teste/monitoramento para concorrência?

---

[Anterior](../complexity/code-quality-and-complexity-metrics.md) | [Índice](../../SUMMARY.md) | [Próximo](classic-concurrency-problems.md)
