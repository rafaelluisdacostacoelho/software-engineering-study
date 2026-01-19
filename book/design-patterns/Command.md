[Anterior](ChainOfResponsibility.md) | [Índice](../../SUMMARY.md) | [Próximo](Composite.md)

# Command — Encapsular Ações como Objetos (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Command encapsula uma ação (e seus dados) em um objeto/comando executável. Isso permite tratar “operações” como entidades de primeira classe: enfileirar, reagendar, fazer retry, registrar auditoria, aplicar idempotência, desfazer (undo), etc.

No mercado, Command aparece constantemente em:

- **Filas e jobs:** comandos serializáveis processados assíncronamente.
- **APIs e aplicações:** camadas de application service onde cada use case é um “comando”.
- **Auditoria e compliance:** registrar “o que foi solicitado” vs. “o que aconteceu”.
- **Resiliência:** retry com backoff, circuit breaker por tipo de comando.

O valor real é separar *quem pede* (invoker/caller) de *quem executa* (handler/receiver) e padronizar preocupações transversais (logging, tracing, validação, métricas).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  Command é um GoF clássico. Em arquiteturas modernas, ele se mistura com “use-case handlers” (Clean Architecture), “CQRS command handlers” e “job payloads” em plataformas de mensageria.

- **Padrões e Protocolos Usados no Mercado**
  - **Command Handler:** `Command` (dados) + `Handler` (execução), comum em CQRS.
  - **Invoker/Dispatcher:** mecanismo que roteia comandos para handlers.
  - **Middleware/Decorators para comandos:** logging, métricas, validação, idempotência.
  - **Outbox/Inbox:** garantir entrega e idempotência em comandos/eventos.
  - **Sagas/Process managers:** coordenam comandos ao longo de etapas.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  O risco é proliferar dezenas/centenas de comandos sem governança (naming, versionamento, contratos). Testes precisam cobrir:
  - validação de entrada
  - idempotência
  - retries e efeitos colaterais
  - compatibilidade de payload (principalmente quando vai para fila)

- **Performance e Manutenção**  
  - Serialização/deserialização de payload e versionamento custam tempo.
  - A execução pode depender de IO; é comum precisar de timeouts e limites.
  - Comandos muito genéricos (“DoStuffCommand”) viram dívida técnica.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  - Debt: comandos com regras de negócio “espalhadas” no dispatcher/middlewares.
  - Coverage: poucos testes de retry/erro/compensação.
  - Flakiness: handlers dependentes de tempo/serviços externos sem fakes determinísticos.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Contract tests para payloads de fila (schemas/versionamento).
  - Gates de qualidade: lint + testes de idempotência para handlers críticos.
  - Feature flags para introdução gradual de novos comandos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Unit: handler puro (ou quase) + validações.
  - Integração: handler com DB/queue fake ou containers efêmeros.
  - E2E: poucos fluxos, especialmente para comandos que atravessam serviços.

- **Métrica de Qualidade**  
  - Taxa de sucesso/erro por tipo de comando
  - Latência p95/p99 por comando/handler
  - Retentativas por comando (sinal de instabilidade)
  - Idempotency hits (reprocessamentos absorvidos)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: um dispatcher com “middlewares” (logging e retry) e commands com handlers separados.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol


class Command(Protocol):
	pass


@dataclass(frozen=True)
class ChargeCard:
	order_id: str
	amount_cents: int
	idempotency_key: str


Handler = Callable[[Command], Any]
Middleware = Callable[[Command, Handler], Any]


def with_logging(cmd: Command, next_: Handler) -> Any:
	name = cmd.__class__.__name__
	# Em produção: logs estruturados + trace_id
	print(f"command_start name={name}")
	try:
		result = next_(cmd)
		print(f"command_ok name={name}")
		return result
	except Exception:
		print(f"command_error name={name}")
		raise


def with_retry(max_attempts: int) -> Middleware:
	def mw(cmd: Command, next_: Handler) -> Any:
		last_exc: Exception | None = None
		for _ in range(max_attempts):
			try:
				return next_(cmd)
			except Exception as e:  # refine para erros transitórios
				last_exc = e
		assert last_exc is not None
		raise last_exc

	return mw


class Dispatcher:
	def __init__(self):
		self._handlers: dict[type, Handler] = {}
		self._middlewares: list[Middleware] = []

	def register(self, command_type: type, handler: Handler) -> None:
		self._handlers[command_type] = handler

	def use(self, middleware: Middleware) -> None:
		self._middlewares.append(middleware)

	def dispatch(self, cmd: Command) -> Any:
		handler = self._handlers[type(cmd)]

		def call(c: Command) -> Any:
			return handler(c)

		# compõe middlewares (último adicionado roda por fora)
		next_ = call
		for mw in reversed(self._middlewares):
			prev = next_
			next_ = lambda c, mw=mw, prev=prev: mw(c, prev)

		return next_(cmd)
```

### C#

```csharp
public interface ICommand { }
public interface ICommandHandler<in T> where T : ICommand
{
	Task Handle(T command, CancellationToken ct);
}

public sealed record ChargeCard(string OrderId, int AmountCents, string IdempotencyKey) : ICommand;

public sealed class ChargeCardHandler : ICommandHandler<ChargeCard>
{
	public async Task Handle(ChargeCard command, CancellationToken ct)
	{
		if (command.AmountCents <= 0) throw new ArgumentException("AmountCents must be > 0");
		// chamar gateway, persistir estado, etc.
		await Task.CompletedTask;
	}
}

public sealed class Dispatcher
{
	private readonly IServiceProvider _sp;
	public Dispatcher(IServiceProvider sp) => _sp = sp;

	public Task Dispatch<T>(T command, CancellationToken ct) where T : ICommand
		=> _sp.GetRequiredService<ICommandHandler<T>>().Handle(command, ct);
}
```

### Go

```go
package commands

import (
	"context"
	"fmt"
)

type Command interface{ Name() string }

type Handler func(ctx context.Context, cmd Command) error

type Middleware func(next Handler) Handler

type Dispatcher struct {
	handlers map[string]Handler
	chain    []Middleware
}

func NewDispatcher() *Dispatcher {
	return &Dispatcher{handlers: map[string]Handler{}}
}

func (d *Dispatcher) Register(name string, h Handler) { d.handlers[name] = h }
func (d *Dispatcher) Use(m Middleware)               { d.chain = append(d.chain, m) }

func (d *Dispatcher) Dispatch(ctx context.Context, cmd Command) error {
	h, ok := d.handlers[cmd.Name()]
	if !ok {
		return fmt.Errorf("no handler for %s", cmd.Name())
	}

	// aplica middlewares
	for i := len(d.chain) - 1; i >= 0; i-- {
		h = d.chain[i](h)
	}
	return h(ctx, cmd)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Distinga “comando” (dados) de “handler” (efeito).** Evita objetos gigantes.
- **Padronize nomenclatura e fronteiras:** um comando deve representar um caso de uso coeso.
- **Idempotência é requisito real** quando há retries/filas; trate como first-class.
- **Versione payloads de fila:** mudanças breaking são fonte comum de incidentes.
- **Evite comandos genéricos demais:** perdem rastreabilidade e dificultam autorização/auditoria.
- **Tenha política de retry clara:** erros transitórios vs permanentes, DLQ e alertas.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** timeouts, retries e backoff precisam respeitar limites do cluster; handlers devem ser idempotentes.
- **Pipelines CI/CD:** contract tests para mensagens; migrations coordenadas para mudanças de payload.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing por comando, dashboards por tipo e alarmes em DLQ.
- **Testes e Infra-as-Code:** ambientes efêmeros para validar handlers com dependências (DB/queue) de forma repetível.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95/p99 por comando/handler
- Retries por comando e taxa de DLQ
- Idempotency hits e duplicatas absorvidas
- Erros por categoria (validação, dependência externa, concorrência)

---

## Frameworks e Ferramentas do Mercado

- **Filas/Jobs:** RabbitMQ, Kafka, SQS, Celery, Hangfire
- **Observabilidade:** OpenTelemetry, Prometheus/Grafana
- **Validação/Schema:** JSON Schema, Protobuf/Avro (quando aplicável)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Command
- CQRS (Command handlers) e padrões de mensageria (Outbox/Inbox)
- Idempotência e processamento “at-least-once”

---

## FAQ Especialista

**Command é a mesma coisa que “use case” na Clean Architecture?**  
Frequentemente, sim: um “use case” pode ser modelado como um command + handler. A diferença é mais organizacional (contratos, dispatching, cross-cutting) do que conceitual.

**Quando Command vira overengineering?**  
Quando a operação é simples e local, sem necessidade de enfileiramento/retry/auditoria e a indireção só atrapalha. Use com parcimônia.

**Como lidar com mudanças de payload em comandos em fila?**  
Versione a mensagem (ou suporte backward compatibility), implemente migrations graduais e monitore consumo por versão.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](ChainOfResponsibility.md) | [Índice](../../SUMMARY.md) | [Próximo](Composite.md)
