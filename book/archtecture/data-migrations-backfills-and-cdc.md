[Anterior](data-architecture-ownership-and-modeling.md) | [Índice](../../SUMMARY.md) | [Próximo](reliability-sre-slos-error-budgets.md)

# Migrações de Dados — Backfills, Rollback e CDC

## Visão Geral e Contexto de Mercado

Mudanças de dados são onde muitos incidentes nascem: schema changes, backfills longos, reprocessamentos, correções retroativas. Staff/architect precisa dominar migração **sem downtime** e com segurança.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Expand/Contract**
  - Expandir schema (add column, dual write)
  - Migrar dados (backfill)
  - Contrair (remover antigo)

- **Backfill**
  - Processar em lotes, com checkpoints.
  - Respeitar rate limit e impacto no OLTP.

- **CDC**
  - Capturar mudanças do banco para alimentar projeções/integrações.

---

## Principais Desafios no Uso Profissional

- Migração bloqueando tabela → downtime.
- Backfill sem idempotência → duplicidade/inconsistência.
- Falta de plano de rollback (e “stop the bleeding”).

---

## Estratégias Avançadas e Decisões Arquiteturais

- Rodar migrações com feature flags e rollout controlado.
- Instrumentar migração (progresso, erros, impacto em DB).
- Preparar “runbook” antes de executar.

---

## Referências e Práticas do Mercado

- Padrão expand/contract
- Outbox/CDC e reconciliacão
- Observabilidade e execução segura de backfills
