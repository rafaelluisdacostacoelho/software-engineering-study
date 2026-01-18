[Anterior](system-design-interview.md) | [Índice](../../SUMMARY.md)

# Code Review & Collaboration — Boas Práticas Internacionais

## Visão Geral e Contexto de Mercado

Code review é um dos mecanismos mais eficientes para elevar qualidade técnica, reduzir risco e disseminar conhecimento em times de engenharia. Em organizações modernas (squads, CI/CD, DevOps), code review bem feito não é burocracia: é uma combinação de **controle de risco**, **mentoria** e **padronização**, com impacto direto em:

- Change failure rate (menos incidentes por mudança).
- Lead time (mudanças menores, revisões rápidas, feedback contínuo).
- Sustentabilidade do time (onboarding, alinhamento, redução de “ilhas”).

Em empresas de alto desempenho, code review funciona como um “sistema imunológico”: identifica problemas antes de chegar em produção e cria um histórico de decisões (trade-offs, padrões, exceções).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Revisão de código evoluiu de inspeções formais para fluxos assíncronos (PRs) com automação forte (linters, testes, análise estática). Em ambientes de deploy frequente, o “modelo vencedor” é: PR pequeno, checks automatizados, revisão humana focada em design/risco.

- **Padrões e Protocolos Usados no Mercado**
	- **Small PRs:** mudanças pequenas e frequentes.
	- **Ownership compartilhado:** qualquer pessoa pode revisar/alterar módulos (com regras).
	- **CODEOWNERS/approvals:** governança de áreas sensíveis.
	- **Trunk-based development:** integrações frequentes, feature flags.
	- **Definition of Done:** inclui testes, observabilidade, migrações seguras.
	- **Conventional Commits / semantic versioning:** quando necessário.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Com crescimento do time, code review pode virar gargalo. Sem disciplina (PRs enormes, ausência de automação, critérios subjetivos), o throughput cai e o time começa a “pular review”.

- **Performance e Manutenção**  
	- Review de PRs grandes é caro e falho (o revisor perde contexto).
	- Feedback tardio gera retrabalho e frustração.
	- Padrões inconsistentes criam dívida (estilo, arquitetura, tratamento de erros).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Sem gates automatizados, revisor vira linter humano.
	- Flakiness em CI derruba confiança e incentiva bypass.
	- Debt cresce quando “aceita só para não atrasar” vira padrão.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Checks obrigatórios: lint/format, typecheck, unit tests, coverage (quando faz sentido), SAST.
	- Políticas: branch protection, required reviewers, status checks.
	- Deploy seguro: canary/blue-green, feature flags, rollback.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Revisor foca em: design, edge cases, segurança, observabilidade.
	- CI cobre: estilo, formatação, testes, análise estática.
	- Para mudanças em integração: contract tests e testes de integração adequados.

- **Métrica de Qualidade**  
	- Tempo de primeira resposta no PR (TTFR)
	- Tempo até merge
	- Tamanho médio de PR
	- Change failure rate e rollback rate
	- Defeitos escapados por área

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo mostram padrões comuns de comentários e melhorias “de review” (robustez, legibilidade e redução de risco).

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
		ok: bool
		value: str | None = None
		error: str | None = None


def parse_user_id(raw: str) -> Result:
		s = raw.strip()
		if not s:
				return Result(ok=False, error="empty")
		if not s.isdigit():
				return Result(ok=False, error="not_numeric")
		return Result(ok=True, value=s)
```

Pontos típicos de review:

- validar inputs (fail-fast)
- retorno explícito de erro (evita exceções “soltas” em borda)
- funções pequenas e determinísticas (fáceis de testar)

### C#

```csharp
public static class Guard
{
		public static void NotNull(object? value, string name)
		{
				if (value is null) throw new ArgumentNullException(name);
		}
}

public sealed class Handler
{
		public string Handle(string input)
		{
				Guard.NotNull(input, nameof(input));
				var normalized = input.Trim();
				if (normalized.Length == 0) throw new ArgumentException("empty");
				return normalized;
		}
}
```

Pontos típicos de review:

- `ArgumentNullException`/`ArgumentException` consistentes
- `Trim()`/normalização em um ponto
- contratos claros (pré-condições)

### Go

```go
package core

import "errors"

var ErrEmpty = errors.New("empty")

func Normalize(input string) (string, error) {
		// em Go, depende do caso: strings.TrimSpace + validação
		if input == "" {
				return "", ErrEmpty
		}
		return input, nil
}
```

Pontos típicos de review:

- erros sentinela para comparação
- retorno `(value, error)` em vez de panics
- simplicidade e previsibilidade

---

## Boas Práticas Sêniores e Armadilhas

- **PRs pequenos e focados:** idealmente 100–300 linhas de diff (ordem de grandeza).
- **Descrição do PR orientada a intenção:** o que muda, por quê, como testar, riscos.
- **Revisão por risco:** segurança, dados, compatibilidade, migração, idempotência.
- **Comentários acionáveis e respeitosos:** critique o código, não a pessoa.
- **Evite bikeshedding:** automatize formatação/linters.
- **Use labels e checklist:** DB migration? feature flag? métricas/logs? rollback plan?
- **Não normalize bypass:** exceções devem ser raras e auditáveis.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** mudanças que impactam runtime (resources, readiness, env vars) precisam de checklist de operação.
- **Pipelines CI/CD:** status checks obrigatórios, políticas de merge, preview environments.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** Sonar/SAST, observabilidade e alertas por mudança.
- **Testes e Infra-as-Code:** PRs de infra com validação (plan/apply), revisão e DR drills.

---

## Métricas, Monitoramento e Melhoria Contínua

- TTFR (tempo até primeira resposta)
- Tempo até merge
- Tamanho médio de PR
- Change failure rate / rollback rate
- Tendência de bugs por componente

---

## Frameworks e Ferramentas do Mercado

- **Python:** ruff/flake8, black, mypy, pytest
- **C#:** dotnet format, analyzers (Roslyn), xUnit
- **Go:** gofmt, golangci-lint, go test
- **Ferramentas de integração:** GitHub Actions, Azure DevOps, SonarQube/SonarCloud, Dependabot/Renovate

---

## Recursos Avançados e Leituras Recomendadas

- _Accelerate_ (Forsgren/Humble/Kim)
- Google Engineering Practices (code review)
- Artigos do Martin Fowler sobre refactoring e qualidade

---

## FAQ Especialista

**Review deve aprovar design ou só qualidade?**  
Os dois, mas em níveis diferentes: design deve ser revisado principalmente em mudanças maiores (RFC/ADR), e o PR deve refletir a decisão. Para mudanças pequenas, foque em risco e consistência.

**Como evitar gargalo de reviewer?**  
PRs menores, rotação de reviewers, pairing em mudanças complexas, automação forte e limites claros de ownership.

**Como lidar com conflitos de estilo/opinião?**  
Padronize com ferramentas (formatter/linter) e registre decisões (ADR). Evite discussões repetidas em cada PR.

---

## Referências e Práticas do Mercado

- Google Engineering Practices — Code Review
- DORA metrics (Accelerate)
- ThoughtWorks Tech Radar

---

[Anterior](system-design-interview.md) | [Índice](../../SUMMARY.md)
