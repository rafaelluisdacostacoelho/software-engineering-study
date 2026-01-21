[Anterior](modular-monolith.md) | [Índice](../../SUMMARY.md) | [Próximo](strangler-fig-and-migration-patterns.md)

# Arquitetura Evolutiva — Fitness Functions e Guardrails

## Visão Geral e Contexto de Mercado

Arquitetura evolutiva trata arquitetura como algo que **muda com o produto**, mas sem virar caos. A ideia prática: definir *fitness functions* (checagens automatizadas) para garantir atributos desejados (segurança, modularidade, latência, acoplamento) enquanto o sistema evolui.

Isso é extremamente relevante para carreira: é o “como” de manter arquitetura saudável em organizações com muitos times e alta cadência.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Fitness function (definição prática)**
  - Um teste/checagem automatizada que valida uma propriedade arquitetural.
  - Ex.: “módulo X não depende do módulo Y”, “todas as rotas têm auth”, “p95 não regressou”.

- **Exemplos comuns**
  - Lint/CI para dependências (imports proibidos).
  - Checagens de segurança (SAST, dependências).
  - SLO gates (regressão de performance falha o build).

---

## Principais Desafios no Uso Profissional

- **Fitness functions fracas**: checam estilo, mas não arquitetura.
- **Alarm fatigue**: checagens ruidosas viram ignoradas.
- **Sem ownership**: ninguém mantém os guardrails.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Comece com 2–3 guardrails de alto ROI**
  - Dependência (acoplamento)
  - Segurança (auth, segredos, vulnerabilidades)
  - Observabilidade (correlation id, tracing)

- **Pareamento com ADR**
  - Fitness functions “implementam” uma decisão arquitetural.

---

## Exemplo (fitness function conceitual)

```text
Regra: Camada domain não importa infra.
Implementação: teste de dependências no CI (falha ao detectar import proibido).
```

---

## Referências e Práticas do Mercado

- Evolutionary Architecture (Neal Ford, Rebecca Parsons, Patrick Kua)
- SRE/SLO como guardrail de confiabilidade
- Supply chain security (SBOM, dependabot) como guardrail de segurança
