[Anterior](architecture-decision-records-adrs.md) | [Índice](../../SUMMARY.md) | [Próximo](distributed-systems-in-practice.md)

# Architecture Reviews & Guardrails — Governança Leve que Evita Caos

## Visão Geral e Contexto de Mercado

Em organizações com múltiplos times, arquitetura morre sem governança mínima. O objetivo aqui não é “comitê”, é criar um sistema de reviews e guardrails para:

- Reduzir incidentes por decisões repetidas e mal avaliadas.
- Evitar fragmentação tecnológica sem necessidade.
- Acelerar entregas com padrões aprovados (golden paths).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Architecture review**
  - Revisão de uma mudança com foco em riscos: segurança, dados, consistência, operação.

- **Guardrails**
  - Regras automatizadas no CI (linters, scanners, testes de contrato)
  - Padrões de referência (templates, libs internas, exemplos)

---

## Principais Desafios no Uso Profissional

- **Virar gatekeeping**: review lento e centralizador.
- **Regras rígidas demais**: bloqueiam inovação.
- **Regras frouxas demais**: não protegem nada.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Checklist de review (produção)**
  - Dados: fonte de verdade, migração, compatibilidade.
  - Resiliência: timeouts, retries, idempotência.
  - Observabilidade: logs com ids, métricas, traces.
  - Segurança: authz, segredos, least privilege.
  - Custo: impacto em infra e operação.

- **Golden paths**
  - Templates de serviço (health, tracing, logging, deploy).
  - Bibliotecas internas para padrões críticos.

---

## Exemplo (guardrail simples)

```text
Regra: toda rota externa exige autenticação.
Implementação: teste automatizado que falha se rota pública não tiver middleware.
```

---

## Referências e Práticas do Mercado

- SRE / error budgets como mecanismo de governança
- Threat modeling (STRIDE) e secure-by-default
- Evolutionary architecture: guardrails via fitness functions
