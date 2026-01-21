[Anterior](clean-architecture.md) | [Índice](../../SUMMARY.md) | [Próximo](c4-model-and-diagrams.md)

# Atributos de Qualidade (NFRs) — Trade-offs que Definem Arquitetura

## Visão Geral e Contexto de Mercado

Em empresas, “arquitetura” quase sempre significa tomar decisões guiadas por **atributos de qualidade** (requisitos não funcionais): disponibilidade, latência, escalabilidade, segurança, custo, evolutividade. Esse capítulo é o mapa mental que separa “opinião” de “decisão defendível”.

Arquitetura boa é a que:

- Torna trade-offs explícitos.
- Define métricas e SLOs.
- Cria limites (guardrails) para não “pagar” o custo errado sem perceber.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Atributos de qualidade típicos**
  - **Disponibilidade** (SLO, MTTR, blast radius)
  - **Latência/Performance** (p95/p99, tail latency)
  - **Escalabilidade** (vertical/horizontal, custos)
  - **Confiabilidade** (retries, idempotência, falhas parciais)
  - **Segurança** (authn/z, segredos, supply chain, auditoria)
  - **Evolutividade** (acoplamento, versionamento, compatibilidade)

- **Trade-off clássico**
  - Melhorar p99 pode aumentar custo.
  - Aumentar consistência pode aumentar latência.
  - Desacoplar por eventos pode reduzir acoplamento e aumentar complexidade operacional.

---

## Principais Desafios no Uso Profissional

- **NFRs não escritos**: todo mundo “assume” disponibilidade/latência.
- **Métricas erradas**: média escondendo cauda (p95/p99).
- **Alinhamento fraco com produto**: custo e risco não entram na decisão.
- **Overengineering**: arquitetura para problemas que não existem.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Transforme NFR em contrato operacional**
  - Defina SLI/SLO/alertas e o que é “degradado aceitável”.

- **Relacione decisões a hipóteses**
  - “Vamos usar cache X porque p95 precisa cair para Y”.
  - “Vamos aceitar consistência eventual porque o fluxo tolera reconciliação”.

- **Checklist de decisão (enxuto)**
  - Qual atributo estamos otimizando?
  - Qual atributo piora?
  - Quais métricas provam que melhorou?
  - Qual é o plano de rollback?

---

## Exemplo (mini ADR de trade-off)

```text
Contexto: checkout precisa p95 < 200ms.
Decisão: cachear catálogo por 5 min.
Consequência: risco de preço desatualizado; mitigar com validação final no pagamento.
Métricas: p95 checkout, taxa de inconsistência detectada, hit ratio.
```

---

## Referências e Práticas do Mercado

- SRE: SLI/SLO/Error Budget (Google SRE)
- Latência de cauda (tail latency) e observabilidade
- Threat modeling (STRIDE) como entrada para segurança
