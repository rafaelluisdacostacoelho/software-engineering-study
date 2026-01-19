[Anterior](CompositionOverInheritance.md) | [Índice](../../SUMMARY.md) | [Próximo](FailFast.md)

# Design for Testability — Projetar para Ser Testável (Princípio de Engenharia)

## Visão Geral e Contexto de Mercado

Design for Testability significa projetar código de forma que ele possa ser validado de maneira rápida, determinística e barata. Em times modernos, testabilidade é um multiplicador de velocidade: reduz lead time, diminui change failure rate e permite refatorações seguras.

No mercado, sistemas com CI/CD e múltiplos squads exigem:

- feedback rápido (testes unitários confiáveis)
- isolamento de dependências (DB, filas, HTTP)
- capacidade de simular falhas (timeouts, retries, partial failures)

Projetar para testabilidade normalmente implica arquitetura por camadas, composição, dependências invertidas e separação de concerns.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O “testar depois” falha em sistemas grandes. A indústria passou a integrar testes ao pipeline e a projetar para automação (TDD/BDD/ATDD como práticas, não dogmas).

- **Padrões e Protocolos Usados no Mercado**
	- **Dependency Injection / Ports & Adapters:** trocar infra por fakes.
	- **Pure functions / domínio isolado:** regras sem IO.
	- **Deterministic time:** clock injetável.
	- **Idempotência e side effects controlados:** facilita reprocessamento.
	- **Contract tests:** integrações estáveis.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em bases grandes, o maior problema é disciplina: manter testes rápidos e estáveis, e não transformar testes unitários em mini-integrações.

- **Performance e Manutenção**  
	- Test suites lentas travam CI.
	- Testes frágeis (acoplados à implementação) aumentam custo de mudança.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: código acoplado a infra e estado global.
	- Coverage: foco em “número” e não em risco/branch.
	- Flakiness: tempo real, concorrência, rede e dependências externas.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Separar suites: unit (rápido) vs integração (container) vs E2E.
	- Flaky detection e quarantine temporária com dono/SLAs.
	- Gates por risco: testes obrigatórios em PR, mutação/branch coverage onde faz sentido.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: regras e invariantes.
	- Integração: DB/queue/HTTP com docker.
	- E2E: poucos fluxos críticos.

- **Métrica de Qualidade**  
	- Tempo de pipeline e flaky rate
	- Change failure rate e MTTR
	- Cobertura útil (branches críticos, mutação em módulos essenciais)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: injetar clock para testes determinísticos.

### Python

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Callable


Clock = Callable[[], datetime]


@dataclass
class TokenService:
		now: Clock

		def expires_at_iso(self, ttl_seconds: int) -> str:
				if ttl_seconds <= 0:
						raise ValueError("ttl_seconds must be > 0")
				return (self.now()).isoformat()
```

### C#

```csharp
public interface IClock { DateTimeOffset Now(); }

public sealed class TokenService
{
		private readonly IClock _clock;
		public TokenService(IClock clock) => _clock = clock;

		public DateTimeOffset ExpiresAt(int ttlSeconds)
		{
				if (ttlSeconds <= 0) throw new ArgumentException("ttlSeconds must be > 0");
				return _clock.Now().AddSeconds(ttlSeconds);
		}
}
```

### Go

```go
package token

import "time"

type Clock func() time.Time

type Service struct{ Now Clock }

func (s Service) ExpiresAt(ttlSeconds int) time.Time {
		if ttlSeconds <= 0 { panic("ttlSeconds must be > 0") }
		return s.Now().Add(time.Duration(ttlSeconds) * time.Second)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Separe domínio (puro) de infraestrutura (IO) com portas/adapters.
- Faça dependências explícitas (sem singletons/globais) para facilitar substituição.
- Prefira testes determinísticos; controle tempo, aleatoriedade e concorrência.
- Evite testar detalhes internos; teste contratos e invariantes.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** testes de integração sobem dependências efêmeras.
- **Pipelines CI/CD:** separar suites e usar caches; bloquear merge com falhas.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** SAST/linters + observabilidade para incidentes reais.
- **Testes e Infra-as-Code:** IaC para ambientes de teste reprodutíveis.

---

## Métricas, Monitoramento e Melhoria Contínua

- Flaky rate e tempo de suite unitária
- Incidentes por regressão
- Tempo médio para refatorar módulos críticos com segurança

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest, monkeypatch, freezegun
- **C#:** xUnit, Moq, NSubstitute
- **Go:** testing, testify, gomock
- **Integração:** docker compose para dependências

---

## Recursos Avançados e Leituras Recomendadas

- Growing Object-Oriented Software, Guided by Tests
- Google Testing Blog
- Martin Fowler: test pyramid, contract testing

---

## FAQ Especialista

**Testabilidade é só “escrever testes”?**  
Não. É projeto: dependências explícitas, separação de concerns, controle de side effects.

**Como lidar com legacy não-testável?**  
Comece com characterization tests e crie seams (interfaces) incrementalmente.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](CompositionOverInheritance.md) | [Índice](../../SUMMARY.md) | [Próximo](FailFast.md)
