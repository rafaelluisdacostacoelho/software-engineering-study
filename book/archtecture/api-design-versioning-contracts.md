[Anterior](integration-architectures-sync-async.md) | [Índice](../../SUMMARY.md) | [Próximo](event-contracts-schema-evolution.md)

# API Design & Versionamento — Contratos que Escalam com Times

## Visão Geral e Contexto de Mercado

APIs são a principal forma de acoplamento entre times. Um design bom evita deploy coordenado, permite evolução compatível e reduz incidentes. Isso vale para HTTP, gRPC e também para “APIs” assíncronas (eventos).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Contrato como produto**
  - OpenAPI para HTTP.
  - Protobuf/IDL para gRPC.
  - AsyncAPI (ou schema registry) para eventos.

- **Compatibilidade**
  - Mudanças compatíveis (add fields, default values).
  - Mudanças incompatíveis (rename/remove fields, sem defaults).

- **Semânticas**
  - Idempotência por design (idempotency keys quando aplicável).
  - Erros: padronizar códigos e motivos.

---

## Principais Desafios no Uso Profissional

- APIs que vazam detalhes internos (tabelas/ORM).
- Versionamento “na URL” sem estratégia de compatibilidade.
- Falta de limites de payload/timeout → incidentes por overload.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Defina uma política de compatibilidade (semântica e técnica).
- Use contract tests para reduzir regressões.
- Documente idempotência, retries e timeouts como parte do contrato.

---

## Referências e Práticas do Mercado

- OpenAPI/AsyncAPI, consumer-driven contracts (Pact)
- Guidelines de API (REST/gRPC) com versionamento
- Patterns de idempotência e retries
