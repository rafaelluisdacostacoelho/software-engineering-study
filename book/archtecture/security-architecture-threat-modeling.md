[Anterior](cost-architecture-finops.md) | [Índice](../../SUMMARY.md) | [Próximo](identity-authz-architecture.md)

# Arquitetura de Segurança — Threat Modeling e Secure-by-Default

## Visão Geral e Contexto de Mercado

Segurança não é checklist no final: é parte da arquitetura. Staff precisa conseguir mapear ameaças, escolher controles e explicar trade-offs sem virar burocracia.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Threat modeling** (ex.: STRIDE) para descobrir riscos cedo.
- **Defesa em profundidade**: camadas de controle.
- **Least privilege**: permissões mínimas.

---

## Principais Desafios no Uso Profissional

- Tratar segurança como “configuração de cloud”.
- Falhas em gestão de segredos e supply chain.
- Falta de auditoria (quem fez o quê, quando).

---

## Estratégias Avançadas e Decisões Arquiteturais

- Padronizar authn/authz e gestão de segredos.
- Definir limites de exposição (public/private, network policies).
- Automatizar guardrails (SAST, dependências, IaC scanning).

---

## Referências e Práticas do Mercado

- STRIDE e threat modeling
- OWASP ASVS/Top 10
- Supply chain security (SBOM)
