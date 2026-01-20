[Anterior](github-actions.md) | [Índice](../../SUMMARY.md) | [Próximo](kafka.md)

# Observability (Prometheus/Grafana) — Métricas, Alertas e Operação (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Observabilidade é a capacidade de entender o comportamento de um sistema a partir de sinais: **métricas, logs e traces**. Prometheus/Grafana são muito usados para o pilar de métricas e dashboards.

O ponto sênior: dashboards não são “bonitos”, são **instrumentos de decisão**. Alertas ruins geram fadiga; alertas bons reduzem MTTR.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Métricas**: séries temporais com labels.
- **RED/USE**:
	- RED (Rate, Errors, Duration) para serviços.
	- USE (Utilization, Saturation, Errors) para recursos.
- **SLOs**: metas de confiabilidade que guiam alertas.

---

## Principais Desafios no Uso Profissional

- **Alta cardinalidade**: labels explosivos derrubam o custo e a performance.
- **Alertas barulhentos**: sintomas sem impacto no usuário.
- **Métricas sem contexto**: difícil correlacionar com releases e mudanças.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **SLO-driven alerting**
	- Alertar por consumo de error budget e por sintomas de impacto.
	- Evitar alertar “qualquer spike”.

- **Design de labels**
	- Labels estáveis: `service`, `route`, `status_class`.
	- Evite: `user_id`, `request_id` (isso é trace/log).

- **Dashboards orientados a perguntas**
	- “Está impactando usuário?”
	- “É regressão de release?”
	- “CPU/DB/filas estão saturadas?”

---

## Exemplos Avançados (consultas típicas)

- Erro por serviço (exemplo conceitual): taxa de `5xx` / taxa total.
- Latência: p95/p99 por rota.
- Saturação: CPU throttling, filas (queue depth), conexões DB.

---

## Boas Práticas Sêniores e Armadilhas

- Alerta em “página” só para incidentes reais (pager).
- Tenha runbooks curtos por alerta.
- Versione dashboards e regras (infra-as-code) quando possível.

---

## Integração na Arquitetura Real

- Kubernetes: `kube-state-metrics`, node exporter, métricas de apps.
- CI/CD: anotar releases (deploy markers) para correlacionar com regressões.

---

## Métricas, Monitoramento e Melhoria Contínua

- MTTR, incident count, taxa de alerta acionável.
- Cobertura de SLOs e consumo de error budget.

---

## Frameworks e Ferramentas do Mercado

- Prometheus, Alertmanager, Grafana.
- OpenTelemetry (métricas/traces), Loki/ELK para logs.

---

## Recursos Avançados e Leituras Recomendadas

- Google SRE (SLOs, alerting).
- Boas práticas de cardinalidade e custos em Prometheus.

---

## FAQ Especialista

**Por que alta cardinalidade é tão ruim?**  
Porque cada combinação de labels vira uma série; isso multiplica armazenamento, memória e custo.

---

## Referências e Práticas do Mercado

- SRE book, Prometheus docs, práticas de alerting

---

[Anterior](github-actions.md) | [Índice](../../SUMMARY.md) | [Próximo](kafka.md)
