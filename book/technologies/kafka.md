[Anterior](observability-prometheus-grafana.md) | [Índice](../../SUMMARY.md) | [Próximo](postgresql.md)

# Kafka — Streaming, Throughput e Operação de Filas (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Kafka é uma plataforma de streaming/log distribuído usada para eventos, integrações e pipelines de dados. Ele é muito escolhido quando você precisa de:

- Alto throughput e retenção de eventos.
- Escalabilidade por partições.
- Integração assíncrona entre serviços.

O ponto sênior: Kafka é uma peça operacional pesada — você precisa de governança (schemas, compatibilidade), observabilidade e disciplina de consumidores.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Topic/partition**: particionamento define paralelismo e ordenação.
- **Consumer groups**: escalabilidade horizontal do consumo.
- **Offsets**: checkpoint do consumer; semânticas (at-least-once, etc.).
- **Retention**: tempo/tamanho; Kafka é log, não “fila que apaga”.

---

## Principais Desafios no Uso Profissional

- **Ordenação vs paralelismo**: por chave/partição.
- **Reprocessamento**: mudanças de lógica exigem replay.
- **Garantias**: duplicidade e idempotência no consumer.
- **Operação**: lag, rebalances, throttling, tuning.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Keying e particionamento**
	- Escolha chave alinhada à ordenação desejada.
	- Evite hot partitions.

- **Contratos (schemas)**
	- Schema registry e compatibilidade (backward/forward).
	- Versionamento explícito de eventos.

- **Consumidores resilientes**
	- Idempotência, retries com backoff, DLQ quando aplicável.
	- Controle de concorrência e backpressure.

---

## Exemplos Avançados (checklist de consumer)

- Processar mensagem como transação lógica.
- Persistir efeito idempotente.
- Commit offset só após efeito durável.
- Tratar duplicidade e out-of-order.

---

## Boas Práticas Sêniores e Armadilhas

- Não dependa de “exactly once” como mágica: modele idempotência.
- Monitore lag e tempo de processamento.
- Cuidado com payloads grandes; prefira referências (object storage).

---

## Integração na Arquitetura Real

- Outbox + CDC para publicação confiável.
- Consumers para projeções (CQRS), integrações e workflows.

---

## Métricas, Monitoramento e Melhoria Contínua

- Consumer lag (por grupo/partição).
- Taxa de rebalances.
- p95 de processamento e taxa de erro.

---

## Frameworks e Ferramentas do Mercado

- Kafka, Confluent Platform.
- Schema registry.
- Ferramentas de monitoramento (exporters, dashboards).

---

## Recursos Avançados e Leituras Recomendadas

- Documentação Kafka (partitions, consumer groups).
- Padrões de idempotência e outbox.

---

## FAQ Especialista

**Kafka substitui banco de dados?**  
Não. Ele é um log/event stream. Persistência de estado e queries ainda pedem storage apropriado.

---

## Referências e Práticas do Mercado

- Kafka docs, padrões de event streaming

---

[Anterior](observability-prometheus-grafana.md) | [Índice](../../SUMMARY.md) | [Próximo](postgresql.md)
