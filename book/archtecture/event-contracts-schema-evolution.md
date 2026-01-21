[Anterior](api-design-versioning-contracts.md) | [Índice](../../SUMMARY.md) | [Próximo](data-architecture-ownership-and-modeling.md)

# Contratos de Eventos — Schema Evolution e Compatibilidade

## Visão Geral e Contexto de Mercado

Em arquitetura orientada a eventos, o contrato é o evento. A falha mais comum é tratar evento como “payload qualquer” e quebrar consumidores na evolução.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Eventos são fatos**: imutáveis e auditáveis.
- **Chaves**: id estável do evento, aggregate id, causalidade/correlation.
- **Compatibilidade**: adicionar campos é fácil; remover/renomear é caro.

---

## Principais Desafios no Uso Profissional

- Consumers assumindo campos obrigatórios sem defaults.
- Reprocessamento sem idempotência.
- Falta de versionamento e governança do schema.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Adotar schema registry (quando fizer sentido) e políticas de compatibilidade.
- Usar envelope padrão (metadata + payload) para rastreabilidade.
- Planejar reprocessamento: dedup, idempotência e replay controlado.

---

## Referências e Práticas do Mercado

- AsyncAPI e/ou schema registry
- Outbox/CDC para publicação confiável
- Observabilidade em pipelines de eventos
