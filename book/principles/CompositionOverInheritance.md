[Anterior](LawOfDemeter.md) | [Índice](../../SUMMARY.md) | [Próximo](DesignForTestability.md)

# Composition over Inheritance — Compor Objetos em vez de Herdar (Princípio de Design)

## Visão Geral e Contexto de Mercado

“Composition over Inheritance” recomenda preferir composição (um objeto **tem** outro objeto) em vez de herança (um objeto **é** outro) para reutilizar comportamento. Em sistemas de mercado, isso reduz acoplamento estrutural, facilita testes e evita hierarquias frágeis.

Em arquiteturas modernas (microserviços, squads, CI/CD), mudanças são constantes. Herança tende a:

- criar efeitos colaterais em cadeia (mudou a base, quebrou subclasses)
- incentivar “God base class”
- dificultar refatoração e extração de componentes

Composição, por outro lado, favorece módulos pequenos, com interfaces claras e substituíveis.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	OO clássico promoveu herança como mecanismo principal de reutilização. Com o tempo, a indústria aprendeu que herança profunda é cara para evoluir. O mercado migrou para composição, DI e padrões como Strategy/Decorator.

- **Padrões e Protocolos Usados no Mercado**
	- **Strategy:** compor algoritmos/políticas.
	- **Decorator:** compor responsabilidades (logging, cache, retry).
	- **Ports & Adapters:** compor infraestrutura via interfaces.
	- **Dependency Injection:** compor objetos no composition root.
	- **Functional composition:** funções/handlers encadeados.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Composição exige desenhar interfaces boas. Interfaces ruins criam mocks demais ou dificultam substituição.

- **Performance e Manutenção**  
	- Composição pode adicionar indireção (chamadas extras), mas geralmente é irrelevante frente a IO.
	- Manutenção melhora porque você troca partes sem mexer em toda a hierarquia.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: herança para “reutilizar” acaba virando acoplamento global.
	- Coverage: subclasses raras ficam sem testes.
	- Flakiness: estado compartilhado em base classes e testes paralelos.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Regras de review: evitar herança profunda em camadas de domínio.
	- Testes de contrato para interfaces compostas.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: testar componentes isolados.
	- Integração: validar composição real (wiring) com dependências.
	- E2E: fluxos críticos.

- **Métrica de Qualidade**  
	- Profundidade média de herança
	- Número de overrides por classe
	- Tempo para adicionar uma variação (nova policy)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: em vez de herdar para “adicionar logging”, compor um wrapper.

### Python

```python
from dataclasses import dataclass
from typing import Protocol


class Sender(Protocol):
		def send(self, msg: str) -> None: ...


@dataclass
class SmtpSender:
		def send(self, msg: str) -> None:
				pass


@dataclass
class LoggingSender:
		inner: Sender

		def send(self, msg: str) -> None:
				print(f"send msg_size={len(msg)}")
				self.inner.send(msg)
```

### C#

```csharp
public interface ISender { void Send(string msg); }

public sealed class LoggingSender : ISender
{
		private readonly ISender _inner;
		private readonly ILogger<LoggingSender> _logger;

		public LoggingSender(ISender inner, ILogger<LoggingSender> logger)
				=> (_inner, _logger) = (inner, logger);

		public void Send(string msg)
		{
				_logger.LogInformation("send msg_size={Size}", msg.Length);
				_inner.Send(msg);
		}
}
```

### Go

```go
package sender

import "log"

type Sender interface{ Send(msg string) error }

type Logging struct{ Inner Sender }

func (l Logging) Send(msg string) error {
		log.Printf("send msg_size=%d", len(msg))
		return l.Inner.Send(msg)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Use herança quando existe uma relação “é-um” real e estável (raro no domínio).
- Prefira interfaces pequenas e composição para variar comportamento.
- Evite “base classes utilitárias” que acumulam responsabilidades.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** composição facilita trocar integrações (providers) por ambiente.
- **Pipelines CI/CD:** tests e lint ajudam a conter herança profunda.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** wrappers (decorators) são bons pontos de observabilidade.
- **Testes e Infra-as-Code:** wiring explícito torna ambiente de testes mais fiel.

---

## Métricas, Monitoramento e Melhoria Contínua

- Profundidade de herança e churn em base classes
- Flaky rate (sinal de estado global/compartilhado)
- Tempo para adicionar uma variação com segurança

---

## Frameworks e Ferramentas do Mercado

- DI containers (C#), wiring manual (Go), factories (Python)
- Linters e analyzers para complexidade/acoplamento

---

## Recursos Avançados e Leituras Recomendadas

- Refactoring (Martin Fowler)
- A Philosophy of Software Design (John Ousterhout)
- GoF: Strategy/Decorator como alternativas frequentes

---

## FAQ Especialista

**Herança é sempre ruim?**  
Não. Mas hierarquias profundas e reutilização por herança tendem a ser frágeis. Prefira composição por padrão.

**Quando herança faz sentido?**  
Quando o framework exige (ex.: classes base de UI) ou quando o domínio é realmente polimórfico e estável.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](LawOfDemeter.md) | [Índice](../../SUMMARY.md) | [Próximo](DesignForTestability.md)
