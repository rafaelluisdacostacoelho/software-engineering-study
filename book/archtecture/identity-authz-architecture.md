[Anterior](security-architecture-threat-modeling.md) | [Índice](../../SUMMARY.md) | [Próximo](multi-tenancy-and-isolation.md)

# Identidade & Autorização — Arquitetura de Authn/Authz

## Visão Geral e Contexto de Mercado

Quase todo sistema precisa de identidade (quem é) e autorização (o que pode). Erros aqui viram incidentes graves. Arquitetura de auth também impacta experiência, latência e integração entre serviços.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Authn**: autenticação (tokens, sessões)
- **Authz**: autorização (RBAC/ABAC)
- **Tokens**: JWT vs opaque, rotação e expiração

---

## Principais Desafios no Uso Profissional

- Autorização espalhada e inconsistente.
- Falta de auditoria de decisões de acesso.
- Confundir identificação do usuário com permissões (ex.: tenant).

---

## Estratégias Avançadas e Decisões Arquiteturais

- Centralizar políticas (quando faz sentido) e padronizar enforcement.
- Propagar contexto com segurança (claims mínimas, não PII desnecessária).
- Planejar revogação e rotação de credenciais.

---

## Referências e Práticas do Mercado

- OAuth2/OIDC
- RBAC/ABAC e policy engines
- Auditoria e trilhas de acesso
