# Estrutura (pasta) — Template de Manual Completo (Senior / Specialist)

Use esta estrutura para qualquer assunto extenso. Ela separa:
- **Ensino (manual)**: conceitos → modelos mentais → implementação → operação
- **Auditoria (review)**: checklists, ADR-lite, playbooks

```
ASSUNTO/
  README.md

  00-meta/
    01-objetivos-de-aprendizado.md
    02-escopo-e-nao-objetivos.md
    03-como-ler-e-como-praticar.md
    04-glossario.md
    05-cheatsheet.md
    06-referencias.md

  01-visao-geral/
    01-o-que-e-e-por-que-existe.md
    02-quando-usar-vs-quando-evitar.md
    03-mapa-mental-do-assunto.md

  02-modelos-mentais-e-fundamentos/
    01-modelo-mental-intuicao.md
    02-modelo-formal-entidades-estados-contratos.md
    03-invariantes-e-propriedades.md
    04-teoria-essencial-e-pegadinhas.md
    05-evolucao-e-padroes-do-mercado.md

  03-arquitetura-de-referencia/
    01-componentes-e-dependencias.md
    02-fluxos-criticos-sync-async.md
    03-fonte-de-verdade-e-projecoes.md
    04-topologias-variantes-e-quando-usar.md

  04-contratos-e-modelo-de-dados/
    01-entidades-eventos-commands.md
    02-schemas-e-exemplos-minimos.md
    03-versionamento-e-compatibilidade.md
    04-validacao-e-constraints.md

  05-algoritmos-e-implementacao/
    01-fluxos-criticos-e-pseudocodigo.md
    02-concorrencia-ordem-dedup-idempotencia.md
    03-consistencia-reconciliacao-e-unknown-state.md
    04-exemplos-end-to-end.md

  06-falhas-resiliencia-recuperacao/
    01-matriz-de-falhas-e-sintomas.md
    02-retries-timeouts-backoff-circuit-breaker.md
    03-backpressure-overload-e-degradacao.md
    04-replay-reprocessamento-e-migracoes.md
    05-playbooks-de-incidente.md

  07-observabilidade-e-operacao/
    01-logging.md
    02-metricas-fichas-e-interpretacao.md
    03-tracing-e-propagacao-de-contexto.md
    04-slos-slis-e-alertas-acionaveis.md
    05-dashboards-e-investigacao.md

  08-seguranca-privacidade-compliance/
    01-threat-model.md
    02-autenticacao-autorizacao-auditoria.md
    03-protecao-de-dados-pii-secrets-crypto.md
    04-abusos-replay-fraude-e-mitigacoes.md

  09-performance-capacidade-custos/
    01-caminho-critico-e-gargalos.md
    02-limites-rate-limits-payload-cardinalidade.md
    03-caching-e-invalidation.md
    04-capacity-planning-e-custos.md

  10-testabilidade-e-qualidade/
    01-estrategia-de-testes.md
    02-testes-de-invariantes-e-propriedades.md
    03-testes-de-concorrencia-e-idempotencia.md
    04-fault-injection-chaos-e-game-days.md

  11-trade-offs-alternativas-e-decisoes/
    01-alternativas-e-comparacoes.md
    02-adr-lite.md
    03-riscos-e-o-que-monitorar.md

  12-estudos-de-caso-e-exercicios/
    01-casos-reais.md
    02-exercicios-guiados.md
    03-perguntas-de-review.md
```

## Regras de profundidade (mínimos)
Para considerar o material “completo”, cada documento deve ter pelo menos:
- 1 seção **Definição + Intuição + Modelo formal**
- 1 **diagrama Mermaid** (se aplicável)
- 2–3 **exemplos progressivos** (mínimo → realista → produção)
- 1 seção “**Armadilhas / erros comuns**”
- 1 seção “**O que monitorar em produção**”
- links para termos no glossário