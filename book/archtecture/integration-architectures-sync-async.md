[Anterior](distributed-systems-in-practice.md) | [Índice](../../SUMMARY.md) | [Próximo](api-design-versioning-contracts.md)

# Integrações — Sync vs Async, Orquestração vs Coreografia

## Visão Geral e Contexto de Mercado

Boa parte da arquitetura de software é arquitetura de integração: como serviços e sistemas conversam sem virar um emaranhado frágil. As principais escolhas:

- Sincrono (HTTP/gRPC) vs Assíncrono (filas/eventos)
- Orquestração vs Coreografia
- Contratos e versionamento

---

## Fundamentos, Evolução e Padrões de Mercado

- **Sync (request/response)**
  - Mais simples de entender, mas aumenta acoplamento temporal.
  - Exige budgets de latência e estratégias de fallback.

- **Async (eventos/filas)**
  - Reduz acoplamento temporal, mas aumenta custo operacional.
  - Exige idempotência, dedup e tratamento de reprocessamento.

- **Orquestração vs coreografia**
  - Orquestração concentra lógica (mais controle, mais “centralização”).
  - Coreografia distribui reações (mais autonomia, mais risco de efeitos emergentes).

---

## Principais Desafios no Uso Profissional

- “Tudo evento” sem necessidade → complexidade desnecessária.
- “Tudo sync” → cascata, latência alta, disponibilidade baixa.
- Contratos mal versionados → deploy coordenado (dor organizacional).

---

## Estratégias Avançadas e Decisões Arquiteturais

- Defina “o que é fato” (eventos) vs “o que é comando” (intenção).
- Versione mensagens com compatibilidade (producer/consumer).
- Faça contratos explícitos (OpenAPI/AsyncAPI/Protobuf).

---

## Referências e Práticas do Mercado

- Event-driven architecture e padrões de mensageria
- Sagas/Outbox/CDC (para consistência e publicação confiável)
- Contract tests e evolução compatível
