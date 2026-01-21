[Anterior](c4-model-and-diagrams.md) | [Índice](../../SUMMARY.md) | [Próximo](evolutionary-architecture-fitness-functions.md)

# Modular Monolith — O "Meio do Caminho" que Escala Melhor que Microserviços

## Visão Geral e Contexto de Mercado

Monólito modular é um design onde você mantém **deploy único**, mas com **fronteiras fortes** (módulos) semelhantes a bounded contexts. Para muita empresa, ele é a melhor relação custo/benefício:

- Menos complexidade operacional que microserviços.
- Melhor consistência transacional e simplicidade de debugging.
- Evolução incremental: dá para extrair serviços depois com menos dor.

---

## Fundamentos, Evolução e Padrões de Mercado

- **O que torna modular (de verdade)**
  - Dependências entre módulos restritas e explícitas.
  - APIs internas (interfaces) por módulo.
  - Dados “owned” por módulo (ou ao menos acesso mediado).

- **Padrões comuns**
  - Módulos por domínio (ex.: Billing, Catalog, Identity).
  - Eventos internos para desacoplar sem rede.

---

## Principais Desafios no Uso Profissional

- **Módulos só na pasta**: acoplamento continua alto.
- **Shared database sem disciplina**: qualquer módulo escreve em qualquer tabela.
- **Governança fraca**: sem testes/linters para manter regras.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Regras de dependência automatizadas**
  - CI falha se módulo A importar diretamente módulo B fora da API permitida.

- **Fronteira de dados pragmática**
  - Comece com “write ownership” (somente um módulo escreve).
  - Evolua para “schema por módulo” se necessário.

- **Plano de extração (quando virar microserviço)**
  - Identificar módulo com alta autonomia + alto valor.
  - Extrair junto de observabilidade, idempotência e contratos.

---

## Exemplo (heurística de desenho)

```text
Modulo Identity: autenticação/autorização
Modulo Billing: cobranças e ledger
Regra: Billing não consulta tabelas de Identity; usa API interna ou eventos.
```

---

## Referências e Práticas do Mercado

- DDD: bounded contexts como base de modularização
- Estrangulamento (strangler) como estratégia de extração
- Testes de contrato internos e regras de dependência no CI
