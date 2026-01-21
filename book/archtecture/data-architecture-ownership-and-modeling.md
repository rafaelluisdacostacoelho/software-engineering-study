[Anterior](event-contracts-schema-evolution.md) | [Índice](../../SUMMARY.md) | [Próximo](data-migrations-backfills-and-cdc.md)

# Arquitetura de Dados — Ownership, Modelagem e Fonte de Verdade

## Visão Geral e Contexto de Mercado

Arquitetura de dados define confiabilidade do produto: consistência, auditoria, relatórios e evolução segura. Para nível staff, é essencial conseguir responder:

- Quem é a **fonte de verdade** de cada entidade?
- Quem pode **escrever**? Quem pode **ler**?
- Como evoluir schema e dados sem downtime?

---

## Fundamentos, Evolução e Padrões de Mercado

- **Data ownership** por domínio/módulo.
- **Write ownership** como primeira barreira contra acoplamento.
- **Projeções**: read models, caches, índices, views.

---

## Principais Desafios no Uso Profissional

- Shared database sem disciplina (qualquer serviço escreve em tudo).
- Relatórios em cima de OLTP (impacto de performance e concorrência).
- Migrações sem plano de rollback.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Separar OLTP vs analytics quando necessário.
- Definir contratos de dados (schemas, eventos, SLAs de dados).
- Usar outbox/CDC para alimentar projeções com consistência operacional.

---

## Referências e Práticas do Mercado

- DDD e bounded contexts como base de ownership
- Modelagem pragmática (invariantes, auditoria)
- Padrões de CDC/outbox e pipelines de dados
