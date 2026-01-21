[Anterior](onion-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](quality-attributes-and-trade-offs.md)

# Clean Architecture — Comparativo e Implementação Prática

## Visão Geral e Contexto de Mercado

Clean Architecture (popularizada por Robert C. Martin) é uma forma pragmática de organizar sistemas para manter o **core do negócio** independente de frameworks, UI, banco e integrações. Em empresas, ela aparece como:

- Base para monólitos “bem estruturados” e para serviços em arquitetura orientada a eventos.
- Linguagem comum em entrevistas (principalmente para níveis sênior) para discutir **dependências**, **testabilidade** e **trade-offs**.

A regra mais importante é a mesma que você já viu em Onion/Hexagonal:

- Dependências (imports/compilação) apontam para dentro: **Entities → Use Cases → Interface Adapters → Frameworks/Drivers**.

---

## Fundamentos, Evolução e Padrões de Mercado

- **O que muda vs Onion/Hexagonal**
  - Clean descreve “anéis” semelhantes à Onion, mas explicita melhor a função de *interface adapters*.
  - Na prática, os três estilos convergem: o que importa é a **regra de dependência** e fronteiras claras.

- **Camadas típicas (interpretação prática)**
  - **Domain/Entities:** regras e invariantes “puras”.
  - **Application/Use Cases:** orquestra fluxos, transações, políticas, idempotência.
  - **Adapters (inbound/outbound):** HTTP controllers, consumers, repos, gateways.
  - **Infra:** framework web, ORM, clients, SDKs, detalhes.

---

## Principais Desafios no Uso Profissional

- **Cerimônia e excesso de abstração**: interfaces demais, DTOs demais, pouca clareza.
- **Fronteiras falsas**: pastas bonitas, mas o domínio importando ORM/HTTP.
- **Mapeamento e duplicação**: DTO ↔ domínio ↔ persistência (custo real de manutenção).
- **“Clean” sem produto**: arquitetura perfeita que não entrega valor e atrasa feedback.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Comece por casos de uso e invariantes**
  - Defina o que é “efeito” (persistência, publish, chamada externa) e onde isso acontece.
  - Garanta que o core seja testável sem infraestrutura.

- **Defina contratos nas bordas**
  - Inbound: OpenAPI/Protobuf/AsyncAPI.
  - Outbound: ports com *shape* do domínio (não do SDK).

- **Testes que sustentam a arquitetura**
  - Unit tests para domínio/casos de uso.
  - Integration tests para adapters (DB, broker, HTTP) com ambientes efêmeros.
  - E2E só para fluxos críticos.

---

## Exemplos (estrutura mínima)

Estrutura comum (exemplo genérico):

```text
src/
  domain/
  application/
  adapters/
    inbound/
    outbound/
  infra/
```

Heurística de review rápida:

- Domínio importa apenas linguagem padrão (sem infra).
- Use cases dependem de ports/interfaces.
- Infra implementa ports e é montada no composition root.

---

## Referências e Práticas do Mercado

- Robert C. Martin — Clean Architecture (conceitos e exemplos)
- Ports & Adapters / Hexagonal e Onion (comparação de dependências)
- Contract testing e versionamento (OpenAPI/AsyncAPI/Protobuf)
