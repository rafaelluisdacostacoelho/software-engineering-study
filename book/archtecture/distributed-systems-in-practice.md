[Anterior](architecture-reviews-guardrails.md) | [Índice](../../SUMMARY.md) | [Próximo](integration-architectures-sync-async.md)

# Sistemas Distribuídos na Prática — Falhas Parciais, Latência e Consistência

## Visão Geral e Contexto de Mercado

A maioria dos sistemas “de verdade” vira distribuída por motivos legítimos: múltiplos times, escalabilidade independente, requisitos de disponibilidade, integrações externas e separação por domínio. O custo inevitável é lidar com:

- **Falhas parciais** (um componente falha, outros não)
- **Latência variável** (p95/p99 importam mais que a média)
- **Resultados desconhecidos** (timeout ≠ falha confirmada)
- **Consistência eventual** e reconciliação

Esse capítulo é o mapa de sobrevivência: como pensar e projetar com esses fatos.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Falhas parciais** são o padrão: rede, DNS, rate limit, overload.
- **Timeout é uma decisão de produto**: qual UX quando o estado é “unknown”.
- **Backpressure** é obrigatório: sem isso, você derruba tudo por cascata.
- **Consistência** precisa ser explicitada por fluxo: o que pode ser eventual e o que não pode.

---

## Principais Desafios no Uso Profissional

- Tratar retry como “solução mágica” e criar duplicidades.
- Misturar semânticas: uma operação sem idempotência com retries automáticos.
- Falta de observabilidade: sem tracing e ids, não dá para depurar.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Contrato de semântica de chamadas**
  - Idempotência: quais endpoints/comandos são idempotentes.
  - Timeouts: onde aplicar e com que budgets.
  - Retries: quando, quantos, com jitter e limites.

- **Cascata e isolamento**
  - Bulkheads (isolamento de pools)
  - Circuit breaker
  - Load shedding (degradar com intenção)

- **Consistência por fluxo**
  - Use transação + outbox quando publicar eventos confiavelmente.
  - Tenha reconciliação para estados “unknown”.

---

## Referências e Práticas do Mercado

- Padrões de resiliência (timeouts, retries, circuit breaker)
- Observabilidade e correlação (trace/span ids)
- Consistência distribuída e design orientado a falhas
