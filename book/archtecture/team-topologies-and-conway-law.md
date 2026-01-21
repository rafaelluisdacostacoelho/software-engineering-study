[Anterior](multi-tenancy-and-isolation.md) | [Índice](../../SUMMARY.md) | [Próximo](platform-engineering-golden-paths.md)

# Arquitetura Sociotécnica — Conway’s Law, Team Topologies e Ownership

## Visão Geral e Contexto de Mercado

Arquitetura não é só técnica: a estrutura do sistema tende a refletir a estrutura do time (Conway’s Law). Staff/architect precisa desenhar fronteiras que funcionam para o código e para o org.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Conway’s Law**: organizações produzem sistemas que espelham sua comunicação.
- **Team Topologies**:
  - Stream-aligned teams
  - Platform team
  - Enabling team
  - Complicated-subsystem team

---

## Principais Desafios no Uso Profissional

- Microserviços virando “micro times” sem plataforma.
- Ownership confuso (quem opera? quem atende incidente?).
- Fronteiras técnicas que exigem coordenação excessiva.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Definir claramente:
  - Ownership de domínio
  - Ownership operacional (SLO/runbook)
  - Contratos e versionamento

---

## Referências e Práticas do Mercado

- Team Topologies
- DDD (bounded contexts) e estrutura de times
- Governança leve via ADRs e guardrails
