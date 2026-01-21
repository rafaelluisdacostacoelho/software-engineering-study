[Anterior](strangler-fig-and-migration-patterns.md) | [Índice](../../SUMMARY.md) | [Próximo](architecture-reviews-guardrails.md)

# ADRs (Architecture Decision Records) — Decisão Registrada, Evolução Controlada

## Visão Geral e Contexto de Mercado

ADR é um formato simples para registrar decisões arquiteturais: contexto, decisão, alternativas e consequências. Em times maduros, ADR reduz “tribal knowledge” e acelera onboarding, reviews e auditorias.

Em carreira, ADR é o mecanismo que mostra senioridade: você torna trade-offs explícitos e revisáveis.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Formato mínimo útil**
  - Contexto
  - Decisão
  - Alternativas consideradas
  - Consequências (boas e ruins)
  - Como medir/validar (quando aplicável)

- **Padrões comuns**
  - ADR por PR (a decisão nasce junto do change).
  - Revisão periódica de decisões críticas (ex.: storage, mensageria).

---

## Principais Desafios no Uso Profissional

- **ADR vira burocracia**: texto enorme e sem leitura.
- **Sem owner**: ninguém atualiza quando o sistema muda.
- **Sem ligação com prática**: decisão não vira guardrail/teste.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Quando escrever ADR**
  - Mudança que impacta custo, segurança ou confiabilidade.
  - Mudança irreversível (ou cara de reverter).
  - Definição de contratos e versionamento.

- **ADR + fitness functions**
  - Se a decisão é importante, tente automatizar a “regra” no CI.

---

## Exemplo (ADR ultra curto)

```text
Contexto: precisamos reduzir acoplamento entre Billing e Catalog.
Decisão: publicar eventos de Catalog via outbox.
Alternativas: sync HTTP; shared DB.
Consequências: mais operação (broker), mas menos acoplamento; exige idempotência.
Métricas: lag de consumer, taxa de duplicidade, p95 do fluxo.
```

---

## Referências e Práticas do Mercado

- Michael Nygard — ADR
- Templates leves e revisão em PR
- Relação com SLOs, observabilidade e guardrails
