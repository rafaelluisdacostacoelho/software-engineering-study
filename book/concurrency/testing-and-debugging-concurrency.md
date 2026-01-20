[Anterior](async-concurrency-and-backpressure.md) | [Índice](../../SUMMARY.md) | [Próximo](../critical-operations/transactions-acid.md)

# Testes, Debug e Reproducao — Tornando Concurrency Operavel (Nível Sênior)

## Visão Geral e Contexto de Mercado

Bugs de concorrencia custam caro porque:

- sao intermitentes
- sao dificeis de reproduzir
- aparecem em pico (pior momento)

O objetivo aqui e transformar um problema "magico" em um problema **observavel e repetivel**.

---

## Testes: estrategia que funciona

### 1) Teste invariantes, nao timing

Ao inves de testar "depois de 200ms, X acontece", teste propriedades:

- "nunca processa o mesmo id duas vezes"
- "saldo nunca fica negativo"
- "o maximo de concorrencia e N"

### 2) Stress e repeticao

- Rodar o mesmo teste centenas/milhares de vezes.
- Aumentar concorrencia (mais workers, mais tasks).
- Introduzir jitter artificial (atrasos pequenos aleatorios) para variar interleavings.

### 3) Race detection / analyzers

- Go: `go test -race`
- .NET: profilers e traces (eventos de lock, contention)
- JVM: thread dumps, profilers

---

## Debug em producao (runbook)

Capture, antes de tentar "consertar":

- p95/p99, saturacao (CPU, filas)
- dumps de threads/goroutines (quando possivel)
- tamanho/lag de filas
- contencao de locks (tempo bloqueado)

---

## Tecnicas avancadas (quando vale o investimento)

- **Model checking / especificacao** (ex.: TLA+ para state machines criticas)
- **Linearizability testing** para estruturas concorrentes
- **Fault injection** (timeouts, delays) em staging

---

## Anti-patterns

- "Adicionar sleep ate parar de falhar"
- "Aumentar threads para resolver backlog" sem backpressure
- "Tirar lock para ganhar performance" sem invariantes e testes

---

## Checklist

- Existe uma fonte de verdade?
- Existe um limite de concorrencia?
- Existe idempotencia onde ha retries?
- Existem metricas de fila/lag e tempo bloqueado?

---

[Anterior](async-concurrency-and-backpressure.md) | [Índice](../../SUMMARY.md) | [Próximo](../critical-operations/transactions-acid.md)
