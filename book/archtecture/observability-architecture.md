[Anterior](reliability-sre-slos-error-budgets.md) | [Índice](../../SUMMARY.md) | [Próximo](performance-and-capacity-planning.md)

# Observabilidade na Arquitetura — Logs, Métricas, Traces e Diagnóstico

## Visão Geral e Contexto de Mercado

Observabilidade é parte da arquitetura: sem ela, o sistema não é operável. O objetivo é conseguir responder “o que aconteceu?” com baixo MTTR.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Logs**: eventos com contexto (ids)
- **Métricas**: séries temporais agregadas (p95/p99, counters)
- **Traces**: causalidade ponta a ponta (spans)

---

## Principais Desafios no Uso Profissional

- Cardinalidade alta em métricas.
- Logs sem correlação (sem request/correlation id).
- Tracing parcial (faltam spans em integrações).

---

## Estratégias Avançadas e Decisões Arquiteturais

- Padronizar contexto (correlation id, user/tenant id quando aplicável).
- Instrumentar bordas e pontos críticos (DB, filas, gateways).
- Desenhar dashboards e alertas por SLO (não por “CPU > 80%”).

---

## Referências e Práticas do Mercado

- OpenTelemetry
- Prometheus/Grafana e tracing distribuído
- Runbooks e observabilidade orientada a incidentes
