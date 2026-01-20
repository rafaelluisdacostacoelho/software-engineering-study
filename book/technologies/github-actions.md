[Anterior](linux.md) | [Índice](../../SUMMARY.md) | [Próximo](observability-prometheus-grafana.md)

# GitHub Actions — CI/CD, Qualidade e Guardrails (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

GitHub Actions é uma plataforma de automação para CI/CD e rotinas operacionais (lint, testes, scans, releases). O valor sênior é transformar pipeline em **sistema de controle de risco**:

- Feedback rápido (unit tests/lint) para manter lead time baixo.
- Gates de segurança (SAST, dependency scanning, SBOM).
- Deploys previsíveis (versionamento, rollback, ambientes).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Workflows**: YAML em `.github/workflows/`.
- **Jobs/steps**: execução em runners (hosted ou self-hosted).
- **Artifacts e cache**: reduzir tempo de pipeline.
- **Secrets**: cuidado com logs e com permissões.

Padrões:

- Workflow de PR: lint + testes + scan.
- Workflow de release: tag/version, build, publish, deploy.
- Reuso com `workflow_call` e actions internas.

---

## Principais Desafios no Uso Profissional

- **Tempo de pipeline**: builds lentos reduzem produtividade.
- **Segurança**: permissões excessivas do `GITHUB_TOKEN` e supply chain de actions.
- **Flakiness**: testes não determinísticos e dependência de rede.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Permissões mínimas**
	- Use `permissions:` explícito por workflow/job.
	- Prefira OIDC para cloud (evita secrets long-lived).

- **Gates por criticidade**
	- Branch protection + required checks.
	- Deploys com aprovação para prod.

- **Reprodutibilidade**
	- Pin de versões de actions por SHA.
	- Build determinístico e artefatos versionados.

---

## Exemplos Avançados (workflow mínimo para PR)

```yaml
name: ci
on:
  pull_request:

permissions:
  contents: read

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/validate_links.py
```

---

## Boas Práticas Sêniores e Armadilhas

- Evite jobs gigantes: separe build/test/scan.
- Use cache com parcimônia e invalidation clara.
- Observabilidade do pipeline: métricas de duração, taxa de falha, flaky rate.

---

## Integração na Arquitetura Real

- CI roda qualidade e segurança; CD promove artefatos.
- Integração com Docker/Kubernetes: build/push de imagem e deploy via GitOps.

---

## Métricas, Monitoramento e Melhoria Contínua

- Duração p50/p95 do pipeline.
- Taxa de falha por etapa (lint/test/build/deploy).
- Flaky rate e tempo até green.

---

## Frameworks e Ferramentas do Mercado

- Actions oficiais + actions internas.
- SAST/Dependency scanning, SBOM e assinatura.

---

## Recursos Avançados e Leituras Recomendadas

- GitHub Actions security hardening (permissions, pinning, OIDC).

---

## FAQ Especialista

**Self-hosted runner vale a pena?**  
Às vezes (builds pesados, acesso a rede interna), mas aumenta responsabilidade operacional e superfície de ataque.

---

## Referências e Práticas do Mercado

- GitHub Actions docs e guias de hardening

---

[Anterior](linux.md) | [Índice](../../SUMMARY.md) | [Próximo](observability-prometheus-grafana.md)
