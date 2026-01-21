[Anterior](performance-and-capacity-planning.md) | [Índice](../../SUMMARY.md) | [Próximo](security-architecture-threat-modeling.md)

# Custo em Arquitetura (FinOps) — Performance, Confiabilidade e Dinheiro

## Visão Geral e Contexto de Mercado

Em níveis staff, custo vira requisito. A arquitetura precisa equilibrar latência, disponibilidade e gasto (cloud, licenças, operação humana).

---

## Fundamentos, Evolução e Padrões de Mercado

- Custo por request/transação
- Dimensionamento e autoscaling
- Storage: retenção, índices, hot vs cold

---

## Principais Desafios no Uso Profissional

- “Escalar por padrão” sem medir ROI.
- Overprovisioning por medo.
- Custos invisíveis: logs, métricas, egress, replicas.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Definir unit economics (custo por unidade de negócio).
- Ligar custo a SLO (quanto custa ganhar 10ms de p95?).
- Políticas de retenção e sampling de observabilidade.

---

## Referências e Práticas do Mercado

- FinOps (práticas e métricas)
- SLOs e trade-offs de custo
- Observabilidade e custos de cardinalidade/retencão
