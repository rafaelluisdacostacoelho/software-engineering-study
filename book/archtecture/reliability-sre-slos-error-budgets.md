[Anterior](data-migrations-backfills-and-cdc.md) | [Índice](../../SUMMARY.md) | [Próximo](observability-architecture.md)

# Confiabilidade (SRE) — SLOs, Error Budgets e Arquitetura Operável

## Visão Geral e Contexto de Mercado

Staff/architect é cobrado por “funcionar em produção”. SRE dá o framework para isso: definir SLOs, medir SLIs e tomar decisões com base em error budget.

---

## Fundamentos, Evolução e Padrões de Mercado

- **SLI**: o que medir (latência, disponibilidade, taxa de erro)
- **SLO**: alvo acordado
- **Error budget**: quanto pode falhar sem quebrar o contrato

---

## Principais Desafios no Uso Profissional

- Medir coisa errada (média em vez de p95/p99).
- Alertas barulhentos sem ação.
- “Alta disponibilidade” sem entender dependências e blast radius.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Use SLO como entrada de arquitetura (cache, filas, redundância, degradação).
- Defina runbooks e ownership por serviço.
- Tenha estratégia de rollout (canary/blue-green) e reversão.

---

## Referências e Práticas do Mercado

- Google SRE: SLI/SLO/Error Budget
- Runbooks, incident response e postmortems
- Padrões de HA e tolerância a falhas
