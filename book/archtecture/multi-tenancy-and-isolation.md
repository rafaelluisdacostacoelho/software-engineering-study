[Anterior](identity-authz-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](team-topologies-and-conway-law.md)

# Multi-tenancy — Isolamento, Ruído e Segurança por Tenant

## Visão Geral e Contexto de Mercado

Multi-tenancy aparece cedo em SaaS e plataformas internas. O desafio é oferecer isolamento e segurança sem multiplicar custo operacional.

---

## Fundamentos, Evolução e Padrões de Mercado

- Modelos comuns:
  - Shared everything (com isolamento lógico)
  - Shared DB, schema por tenant
  - DB por tenant (isolamento forte)

- Dimensões:
  - Isolamento de dados
  - Isolamento de performance (noisy neighbor)
  - Isolamento de segurança

---

## Principais Desafios no Uso Profissional

- Vazamento de dados entre tenants.
- Noisy neighbor derrubando performance.
- Migrações e backfills afetando tenants de forma desigual.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Enforçar tenant id em toda borda (queries, caches, eventos).
- Quotas e rate limits por tenant.
- Separar tenants de alto valor/risk em infraestrutura dedicada quando necessário.

---

## Referências e Práticas do Mercado

- Modelos de multi-tenancy
- Rate limiting e isolamento
- Auditoria e controles de acesso
