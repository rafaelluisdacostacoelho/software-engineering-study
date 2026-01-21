[Anterior](observability-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](cost-architecture-finops.md)

# Performance & Capacity Planning — Latência de Cauda, Throughput e Limites

## Visão Geral e Contexto de Mercado

Arquitetura define performance por escolhas de dependências, IO, concorrência e limites. Staff precisa dominar como estimar capacidade, identificar gargalos e evitar regressões.

---

## Fundamentos, Evolução e Padrões de Mercado

- p95/p99 e tail latency
- Lei de Little (intuição de filas)
- Limites: conexões DB, pools, filas, threads

---

## Principais Desafios no Uso Profissional

- Otimizar microdetalhes ignorando IO remoto.
- Sem budgets de latência por dependência.
- Falta de testes de carga e de degradação.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Definir budgets por hop (API → Service → DB/SDK).
- Usar caching/filas quando resolve o gargalo correto.
- Planejar degradação (load shedding, limites, quotas).

---

## Referências e Práticas do Mercado

- SRE/capacity planning
- Backpressure e filas
- Técnicas de profiling e testes de carga
