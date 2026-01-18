[Anterior](KISS.md) | [Índice](../../SUMMARY.md) | [Próximo](OCP.md)

# SOLID — Princípios para Design Orientado a Objetos (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

SOLID é um conjunto de cinco princípios de design orientado a objetos que ajudam a construir software **evolutivo**: mais fácil de manter, testar e estender sem regressões. Em empresas modernas (squads, CI/CD, microserviços), SOLID é relevante porque o custo real não é “escrever código”, e sim **mudar código com segurança**.

No mercado, SOLID costuma aparecer em discussões de:

- Arquiteturas testáveis (Hexagonal/Onion/Clean) e separação de responsabilidades.
- Redução de acoplamento com frameworks/infra.
- Refatoração contínua em codebases vivas.

Importante: SOLID não é dogma; é um “conjunto de lentes” para decisões de design. Aplicado sem contexto, vira indireção e complexidade acidental.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Os princípios foram popularizados por Robert C. Martin. Com o tempo, o mercado aprendeu a aplicá-los de forma pragmática: usando testes, refatoração incremental e observando sinais (mudança frequente, acoplamento, baixa coesão).

- **Padrões e Protocolos Usados no Mercado**
	- **SRP (Single Responsibility):** motivos para mudar.
	- **OCP (Open/Closed):** extensão sem modificar o que está estável (com parcimônia).
	- **LSP (Liskov Substitution):** substituibilidade sem quebrar invariantes.
	- **ISP (Interface Segregation):** interfaces pequenas e orientadas ao consumidor.
	- **DIP (Dependency Inversion):** depender de abstrações (interfaces) e não de concretos.
	- Padrões correlatos: Strategy, Adapter, Template Method, Ports & Adapters.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em sistemas grandes, SOLID só “escala” se o time consegue testar rápido. Sem testes, o custo de mudar aumenta e a tendência é criar abstrações defensivas (complexidade).

- **Performance e Manutenção**  
	- Abstrações demais geram indireção e dificultam debugar.
	- Interfaces genéricas viram “God interfaces”.
	- Performance raramente é o problema; o problema é complexidade e custo de entendimento.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: camadas espelho + interfaces “por padrão”.
	- Coverage: testes que só testam mocks e não comportamento.
	- Flakiness: costuma vir de testes que misturam infra com unit.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Use SOLID para tornar o core testável e acelerar o gate de unit tests.
	- Automatize estilo/linters; use review humano para design.
	- Deploy seguro + refatoração contínua com feature flags quando necessário.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Aplique DIP/ISP para permitir fakes em testes unitários.
	- Teste comportamento observável (Given/When/Then) em vez de interações internas.
	- Integrações reais ficam em testes de integração (adapters).

- **Métrica de Qualidade**  
	- Tempo para refatorar com segurança (lead time de mudanças internas)
	- Tamanho médio de PRs e frequência de regressões
	- Taxa de “mudanças espalhadas” (mudança em N lugares para uma feature)

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo focam em DIP/ISP (mais palpáveis) e em como isso melhora testabilidade.

### Python

```python
from typing import Protocol


class EmailSender(Protocol):
		def send(self, to: str, subject: str, body: str) -> None: ...


class WelcomeUser:
		def __init__(self, sender: EmailSender) -> None:
				self._sender = sender

		def execute(self, email: str) -> None:
				self._sender.send(email, "Welcome", "Hello!")
```

```python
def test_welcome_user_uses_port_not_smtp():
		class SpySender:
				def __init__(self):
						self.calls = []

				def send(self, to: str, subject: str, body: str) -> None:
						self.calls.append((to, subject, body))

		spy = SpySender()
		WelcomeUser(spy).execute("user@example.com")
		assert spy.calls == [("user@example.com", "Welcome", "Hello!")]
```

### C#

```csharp
public interface IEmailSender
{
		void Send(string to, string subject, string body);
}

public sealed class WelcomeUser
{
		private readonly IEmailSender _sender;
		public WelcomeUser(IEmailSender sender) => _sender = sender;

		public void Execute(string email)
				=> _sender.Send(email, "Welcome", "Hello!");
}
```

### Go

```go
package app

type EmailSender interface {
		Send(to, subject, body string) error
}

type WelcomeUser struct {
		sender EmailSender
}

func NewWelcomeUser(s EmailSender) *WelcomeUser {
		return &WelcomeUser{sender: s}
}

func (uc *WelcomeUser) Execute(email string) error {
		return uc.sender.Send(email, "Welcome", "Hello!")
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **SRP não é “1 classe = 1 método”:** é sobre motivos de mudança.
- **OCP na dose certa:** extraia estratégia quando existir variação real (ou previsível) com frequência.
- **LSP:** herança só quando há substituição sem “ifs” e sem quebrar invariantes.
- **ISP:** prefira interfaces pequenas e específicas; evite “IService”.
- **DIP:** mantenha interfaces no core e implementações na borda; injete dependências.
- **Evite abstração prematura:** abstraia quando a dor for real (YAGNI ainda vale).

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** DIP facilita trocar adaptadores (DB/HTTP/MQ) sem mexer no core.
- **Pipelines CI/CD:** unit tests rápidos no core, integration tests nos adaptadores.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** analyzers e linters para padrões; observabilidade nas bordas.
- **Testes e Infra-as-Code:** infra não vaza para o core; testes de infra em pipeline dedicado.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo para implementar variações (novos casos) sem reescrever core
- Número de lugares impactados por uma mudança (acoplamento)
- Taxa de regressões pós-refactor

---

## Frameworks e Ferramentas do Mercado

- **Python:** pytest, mypy, ruff/flake8
- **C#:** xUnit, analyzers, dotnet format
- **Go:** go test, golangci-lint
- **Ferramentas de integração:** SonarQube/SonarCloud, CI (GitHub Actions/Azure DevOps)

---

## Recursos Avançados e Leituras Recomendadas

- _Agile Software Development, Principles, Patterns, and Practices_ (Robert C. Martin)
- _Clean Architecture_ (Robert C. Martin)
- _Refactoring_ (Martin Fowler)
- _A Philosophy of Software Design_ (John Ousterhout)

---

## FAQ Especialista

**SOLID é obrigatório em qualquer projeto?**  
Não. Use quando a complexidade e o ritmo de mudança justificarem. Para scripts e projetos pequenos, pode virar custo sem benefício.

**Como evitar “SOLID overdose”?**  
Comece simples, refatore com testes e extraia abstrações quando houver variação real. Se a abstração não reduz risco nem melhora testabilidade, provavelmente é ruído.

**SOLID funciona fora de OO?**  
Os princípios são formulados em OO, mas ideias como separação de responsabilidades, contratos pequenos e dependência invertida se aplicam em outros paradigmas.

---

## Referências e Práticas do Mercado

- Robert C. Martin (SOLID)
- Martin Fowler (refatoração e design)
- ThoughtWorks Tech Radar (práticas)

---

[Anterior](KISS.md) | [Índice](../../SUMMARY.md) | [Próximo](OCP.md)
