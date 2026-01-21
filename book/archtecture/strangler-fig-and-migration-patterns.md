[Anterior](evolutionary-architecture-fitness-functions.md) | [Índice](../../SUMMARY.md) | [Próximo](architecture-decision-records-adrs.md)

# Migração e Modernização — Strangler Fig e Padrões de Decomposição

## Visão Geral e Contexto de Mercado

Quase toda carreira “absoluta” em TI passa por legado. O padrão Strangler Fig (Estrangulamento) é a abordagem mais usada para modernizar sistemas sem reescrita total:

- Criar uma nova borda (gateway/roteador) e mover funcionalidades por fatias.
- Reduzir risco, manter entrega contínua e permitir rollback.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Estratégias típicas**
  - *Route by feature*: roteia por endpoints/casos de uso.
  - *Extract by domain*: extrai um bounded context.
  - *Parallel run*: roda novo e velho em paralelo e compara.

- **Mecanismos de controle de risco**
  - Feature flags
  - Shadow traffic (com cuidado)
  - Migração de dados incremental

---

## Principais Desafios no Uso Profissional

- **Data coupling**: o novo módulo/serviço ainda depende do banco antigo.
- **Observabilidade insuficiente**: sem métricas/traces, migração vira “tiro no escuro”.
- **Inconsistência e duplicidade**: efeitos duplicados sem idempotência.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Ordem que reduz dor**
  - Comece por bordas: auth, gateway, contratos.
  - Extraia módulos com alta coesão e poucos acoplamentos.

- **Planeje dados cedo**
  - Defina fonte de verdade por entidade.
  - Defina estratégia de sincronização (CDC/outbox, jobs, eventos).

---

## Exemplo (plano mínimo)

```text
1) Colocar gateway na frente
2) Extrair um caso de uso com baixo risco
3) Instrumentar e comparar resultados
4) Migrar dados e desligar a rota antiga
```

---

## Referências e Práticas do Mercado

- Strangler Fig (Martin Fowler)
- Migrações incrementais e backfills
- Observabilidade e rollout (canary, blue/green)
