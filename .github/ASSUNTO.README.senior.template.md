# <ASSUNTO> — Manual de Estudo e Referência (Senior / Specialist)

- **Versão:** v0.1
- **Última revisão:** YYYY-MM-DD
- **Público-alvo:** Dev senior / staff / especialista
- **Objetivo:** formar critério técnico + capacidade de implementar e operar em produção

## Como este manual está organizado
1. **Visão geral** (por quê existe, quando usar, mapa mental)
2. **Modelos mentais + teoria** (invariantes, contratos, pegadinhas)
3. **Arquitetura de referência** (como vive em sistemas reais)
4. **Contratos e dados** (schemas, versionamento)
5. **Implementação** (fluxos críticos, idempotência, concorrência)
6. **Operação** (falhas, observabilidade, SLOs, playbooks)
7. **Segurança, performance, custos e testes**
8. **Trade-offs/ADRs + exercícios**

## Regras deste material (anti-superficial)
- Cada capítulo crítico deve usar o template de seção: `SECTION.contract.template.md`
- Todo termo novo: definir na primeira ocorrência e registrar no glossário
- Todo mecanismo: mostrar pelo menos 1 exemplo mínimo + 1 realista + 1 produção
- Toda decisão: explicitar trade-offs e o que monitorar em produção

## Índice (links)
- `00-meta/`
- `01-visao-geral/`
- `02-modelos-mentais-e-fundamentos/`
- `03-arquitetura-de-referencia/`
- `04-contratos-e-modelo-de-dados/`
- `05-algoritmos-e-implementacao/`
- `06-falhas-resiliencia-recuperacao/`
- `07-observabilidade-e-operacao/`
- `08-seguranca-privacidade-compliance/`
- `09-performance-capacidade-custos/`
- `10-testabilidade-e-qualidade/`
- `11-trade-offs-alternativas-e-decisoes/`
- `12-estudos-de-caso-e-exercicios/`