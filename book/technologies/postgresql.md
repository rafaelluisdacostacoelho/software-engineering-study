[Anterior](kafka.md) | [Índice](../../SUMMARY.md)

# PostgreSQL — Modelagem, Performance e Operação (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

PostgreSQL é um banco relacional muito usado por sua robustez, extensibilidade e excelente ecossistema. Em times seniores, Postgres é tanto um banco quanto um componente operacional: índices, locks, autovacuum, backups e migrações.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Transações e isolamento**: locks, MVCC.
- **Índices**: B-tree como padrão; use GIN/GiST quando fizer sentido.
- **Vacuum/Autovacuum**: essencial para saúde do banco.
- **Conexões**: pooler, limites e saturação.

---

## Principais Desafios no Uso Profissional

- **Migrações**: mudanças online vs downtime, locks de DDL.
- **Performance**: queries sem índices, planos ruins, estatísticas desatualizadas.
- **Concorrência**: deadlocks, long transactions, lock contention.
- **Operação**: backups, restore testado, replicação.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Modelagem guiada por queries**
	- Modele o que você consulta; índices são parte do design.
	- Denormalize quando necessário (com critério e invariantes).

- **Migrações seguras**
	- Evite operações bloqueantes em tabelas grandes.
	- Use migrations em fases (add column nullable -> backfill -> add constraint).

- **Confiabilidade**
	- Backups + restore testado.
	- Observabilidade: slow queries, locks, bloat.

---

## Exemplos Avançados (checklist de performance)

- `EXPLAIN (ANALYZE, BUFFERS)` para entender plano real.
- Índices alinhados a filtros e ordenações.
- Evite N+1 no app; use joins/queries melhores.

---

## Boas Práticas Sêniores e Armadilhas

- Transações longas são “inimigas” do vacuum e causam bloat.
- Índices demais degradam writes; índices de menos degradam reads.
- Pool de conexões: muitas conexões não significam mais throughput.

---

## Integração na Arquitetura Real

- Apps: idempotência, migrations, health checks.
- Eventos: outbox e padrões de consistência.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95 de queries, taxa de slow queries.
- Lock waits e deadlocks.
- Bloat e autovacuum lag.
- Replication lag e sucesso de backups.

---

## Frameworks e Ferramentas do Mercado

- `pg_stat_statements`, `auto_explain`.
- Migrações: Flyway, Liquibase, Alembic.
- Poolers: PgBouncer.

---

## Recursos Avançados e Leituras Recomendadas

- Postgres docs (MVCC, indexes, vacuum).
- Guias de migrations online e tuning.

---

## FAQ Especialista

**Por que minha tabela cresce sem parar?**  
Normalmente por bloat (updates/deletes) e vacuum/autovacuum insuficiente ou transações longas impedindo cleanup.

---

## Referências e Práticas do Mercado

- PostgreSQL docs, práticas de operação e tuning

---

[Anterior](kafka.md) | [Índice](../../SUMMARY.md)
