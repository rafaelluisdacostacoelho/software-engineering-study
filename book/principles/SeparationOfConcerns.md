[Anterior](OCP.md) | [Índice](../../SUMMARY.md) | [Próximo](TellDontAsk.md)

# Separation of Concerns — Separar Responsabilidades para Evoluir com Segurança (Princípio)

## Visão Geral e Contexto de Mercado

Separation of Concerns (SoC) é separar responsabilidades distintas em módulos/camadas, reduzindo acoplamento e tornando mudanças localizadas. Em times grandes, SoC é fundamental para paralelismo: squads conseguem mudar partes do sistema sem quebrar tudo.

SoC aparece em:

- camadas (API, aplicação, domínio, infra)
- limites de contexto (bounded contexts)
- módulos por responsabilidade (auth, billing, shipping)

SoC não é “muitos arquivos”: é ter fronteiras claras e contratos estáveis.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	De sistemas monolíticos a microserviços, a indústria reforçou a importância de boundaries. Mesmo em monólitos, SoC bem feito dá resultados parecidos com microserviços sem os custos operacionais.

- **Padrões e Protocolos Usados no Mercado**
	- **Arquitetura em camadas / Hexagonal / Onion**
	- **Ports & Adapters**
	- **CQRS (quando necessário)**
	- **Seams para testabilidade**

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Sem SoC, testes viram integrações acidentais. Com SoC, você testa domínio isolado e valida integrações com suites menores.

- **Performance e Manutenção**  
	SoC melhora manutenção, mas pode criar overhead de mapeamento (DTOs, adapters). Normalmente vale o custo.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: regras de negócio em controllers, queries SQL espalhadas.
	- Coverage: difícil cobrir porque tudo depende de tudo.
	- Flakiness: testes que dependem de infra sem necessidade.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Enforce boundaries (analyzers/linters por pasta/camada).
	- Suites separadas por camada.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: domínio.
	- Integração: adapters (DB/HTTP/queue).
	- E2E: fluxos críticos.

- **Métrica de Qualidade**  
	- Acoplamento entre módulos/camadas
	- Tempo de build/test por camada
	- Incidentes por mudanças cross-cutting

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: separar domínio (regras) de infraestrutura (persistência).

### Python

```python
from dataclasses import dataclass
from typing import Protocol


class Repo(Protocol):
		def save(self, user: dict) -> None: ...


@dataclass
class CreateUser:
		repo: Repo

		def execute(self, email: str) -> None:
				if "@" not in email:
						raise ValueError("invalid email")
				self.repo.save({"email": email})
```

### C#

```csharp
public interface IUserRepo { Task Save(User user, CancellationToken ct); }

public sealed class CreateUser
{
		private readonly IUserRepo _repo;
		public CreateUser(IUserRepo repo) => _repo = repo;

		public Task Execute(string email, CancellationToken ct)
		{
				if (!email.Contains('@')) throw new ArgumentException("invalid email");
				return _repo.Save(new User(email), ct);
		}
}
```

### Go

```go
package app

import "errors"

type Repo interface{ Save(user map[string]string) error }

type CreateUser struct{ Repo Repo }

func (c CreateUser) Execute(email string) error {
		if len(email) == 0 {
				return errors.New("invalid email")
		}
		return c.Repo.Save(map[string]string{"email": email})
}
```

---

## Boas Práticas Sêniores e Armadilhas

- SoC é sobre fronteiras e contratos, não “organização estética”.
- Evite vazar infraestrutura para o domínio.
- Use nomes e pastas que reflitam responsabilidades.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** SoC facilita trocar infra por ambiente sem tocar no domínio.
- **Pipelines CI/CD:** testes por camada e boundaries enforcement.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** observabilidade no boundary (adapters).
- **Testes e Infra-as-Code:** ambientes efêmeros para adapters críticos.

---

## Métricas, Monitoramento e Melhoria Contínua

- Acoplamento e churn cross-module
- Tempo de build/test por camada
- Defeitos por mudanças cross-cutting

---

## Frameworks e Ferramentas do Mercado

- Analyzers de dependência/camadas
- SonarQube/SonarCloud

---

## Recursos Avançados e Leituras Recomendadas

- Clean Architecture (Robert C. Martin)
- DDD (Evans) — bounded contexts

---

## FAQ Especialista

**SoC significa microserviços?**  
Não. Um monólito bem modular com SoC frequentemente é melhor que microserviços mal definidos.

**Quando SoC vira burocracia?**  
Quando a separação cria atrito (mapeamentos e camadas demais) sem reduzir risco. Ajuste ao tamanho do time e do produto.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](OCP.md) | [Índice](../../SUMMARY.md) | [Próximo](TellDontAsk.md)
