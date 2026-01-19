[Anterior](Factory.md) | [Índice](../../SUMMARY.md) | [Próximo](Proxy.md)

# Observer — Pub/Sub In-Process para Mudanças de Estado (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Observer define uma relação “um-para-muitos” onde *observadores* (subscribers) são notificados quando um *sujeito* (publisher/subject) muda. É pub/sub **dentro do mesmo processo** (em geral síncrono), muito comum em UIs, caches locais, componentes e domínios com eventos.

No mercado, Observer se manifesta como:

- **Eventos de domínio in-process** (antes de ir para filas).
- **UI frameworks** e sistemas reativos.
- **Invalidation local** (ex.: cache em memória reagindo a mudanças).
- **Event aggregators/event bus** internos.

É importante separar Observer de event-driven distribuído (Kafka/SQS). A ideia é parecida, mas os problemas e garantias são bem diferentes.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Observer é GoF clássico. Em stacks modernas ele evoluiu para modelos reativos (`IObservable`, Rx) e para sistemas de eventos in-process com handlers e pipelines.

- **Padrões e Protocolos Usados no Mercado**
	- **Subscribe/Unsubscribe explícitos:** evita vazamentos.
	- **Handlers tipados por evento:** `On(OrderPaid)`.
	- **Síncrono vs Assíncrono:** síncrono é simples, mas pode travar o fluxo.
	- **Weak references:** mitigam memory leaks em UIs.
	- **Event bus interno:** centraliza publicação e políticas (logging, tracing).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Eventos podem causar efeitos indiretos. Testes precisam garantir:
	- quais observers são chamados
	- ordem (se for relevante)
	- comportamento em erro (um observer falha e os outros?)

- **Performance e Manutenção**  
	- Notificação síncrona em cascata pode aumentar latência e criar acoplamento temporal.
	- Observers “pesados” criam gargalos.
	- Encadeamentos e reentrância podem gerar loops de evento.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: “event spaghetti” (publica em todo lugar, sem contrato).
	- Coverage: não testar efeitos indiretos e cenários de erro.
	- Flakiness: observers assíncronos sem sincronização determinística em testes.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes por evento: dado um evento, validar quais handlers executam.
	- Linters/regras: não permitir publicação em camadas erradas.
	- Observabilidade: tracing/log por evento e handler.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: handler isolado.
	- Integração: event bus + conjunto de handlers.
	- E2E: normalmente para eventos distribuídos; para Observer in-process, menos comum.

- **Métrica de Qualidade**  
	- Latência de publicação por evento
	- Número de handlers por evento (sinal de acoplamento)
	- Taxa de erro por handler
	- Backlog/queue interno (se assíncrono)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: um event bus in-process com subscribe/unsubscribe.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, DefaultDict
from collections import defaultdict


Handler = Callable[[object], None]


@dataclass
class EventBus:
		_handlers: DefaultDict[type, list[Handler]]

		def __init__(self):
				self._handlers = defaultdict(list)

		def subscribe(self, event_type: type, handler: Handler) -> None:
				self._handlers[event_type].append(handler)

		def unsubscribe(self, event_type: type, handler: Handler) -> None:
				self._handlers[event_type] = [h for h in self._handlers[event_type] if h is not handler]

		def publish(self, event: object) -> None:
				for handler in list(self._handlers[type(event)]):
						handler(event)
```

### C#

```csharp
public interface IEventBus
{
		void Subscribe<T>(Action<T> handler);
		void Publish<T>(T evt);
}

public sealed class InMemoryEventBus : IEventBus
{
		private readonly Dictionary<Type, List<Delegate>> _handlers = new();

		public void Subscribe<T>(Action<T> handler)
		{
				var t = typeof(T);
				if (!_handlers.TryGetValue(t, out var list)) _handlers[t] = list = new();
				list.Add(handler);
		}

		public void Publish<T>(T evt)
		{
				if (_handlers.TryGetValue(typeof(T), out var list))
						foreach (var d in list.Cast<Action<T>>()) d(evt);
		}
}
```

### Go

```go
package events

import "sync"

type Handler func(evt any)

type Bus struct {
		mu       sync.RWMutex
		handlers map[string][]Handler
}

func NewBus() *Bus {
		return &Bus{handlers: map[string][]Handler{}}
}

func (b *Bus) Subscribe(key string, h Handler) {
		b.mu.Lock()
		defer b.mu.Unlock()
		b.handlers[key] = append(b.handlers[key], h)
}

func (b *Bus) Publish(key string, evt any) {
		b.mu.RLock()
		hs := append([]Handler(nil), b.handlers[key]...)
		b.mu.RUnlock()
		for _, h := range hs {
				h(evt)
		}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Defina política de erro:** se um handler falha, você interrompe ou continua?
- **Evite handlers pesados em publicação síncrona.** Se necessário, faça async com limites.
- **Cuidado com memory leaks:** sempre tenha `unsubscribe` ou use weak refs em contextos de UI.
- **Evite ordem implícita:** se ordem é requisito, torne explícito (prioridades) e teste.
- **Observabilidade por handler:** tracing e métricas ajudam a debugar “efeitos invisíveis”.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** eventos in-process impactam latência e recursos do pod; aplique budgets e timeouts.
- **Pipelines CI/CD:** testes de regressão para handlers e contratos de eventos; validação de dependências.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing por evento/handler; alertas para handlers lentos.
- **Testes e Infra-as-Code:** quando Observer for ponte para eventos distribuídos, teste a transição (outbox).

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência de publicação e execução total
- Erros por handler
- Número de subscribers por evento
- Volume de eventos por tipo

---

## Frameworks e Ferramentas do Mercado

- **C#:** events, `IObservable<T>`, Rx.NET
- **Python:** callbacks, signals (framework-specific), RxPY (quando aplicável)
- **Go:** channels, fan-out patterns
- **Observabilidade:** OpenTelemetry

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Observer
- Reactive extensions (Rx) e event-driven in-process
- Boas práticas de eventos de domínio (in-process vs distribuído)

---

## FAQ Especialista

**Observer é adequado para regras de negócio críticas?**  
Com cuidado. Ele pode ocultar fluxos e efeitos. Para casos críticos, prefira orquestração explícita (application services) e use eventos para side effects bem definidos.

**Síncrono ou assíncrono?**  
Síncrono é mais simples e consistente; assíncrono melhora latência, mas exige controles (queue, retries, ordenação, shutdown).

**Como evitar acoplamento temporal?**  
Evite colocar dependências críticas em handlers síncronos; use event bus para side effects e monitore tempo por handler.

---

[Anterior](Factory.md) | [Índice](../../SUMMARY.md) | [Próximo](Proxy.md)
