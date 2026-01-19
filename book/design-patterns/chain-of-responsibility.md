[Anterior](builder.md) | [Índice](../../SUMMARY.md) | [Próximo](command.md)

# Chain of Responsibility — Encadear Handlers (Padrão Comportamental)

## Visão Geral e Contexto de Mercado

Chain of Responsibility (CoR) permite montar uma cadeia de “handlers” onde cada handler decide se:

- processa a requisição e encerra, ou
- delega para o próximo

No mercado, ele aparece como uma forma elegante de substituir grandes blocos `if/else` e pipelines rígidas, especialmente em:

- Middlewares HTTP (auth, rate limit, logging, validação)
- Processamento de eventos (enriquecimento, filtros, roteamento)
- Pipelines de regras (fraude, pricing, eligibility)
- Aprovação por etapas (políticas)

O ganho é extensibilidade e composição. O risco é virar uma cadeia “mágica” difícil de depurar.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	CoR é um padrão GoF clássico e continua muito usado em frameworks modernos (pipelines/middlewares). Em stacks atuais, ele frequentemente se materializa como “handlers” que retornam `next()` ou como uma lista de interceptors.

- **Padrões e Protocolos Usados no Mercado**
	- **Middleware pipeline:** cada etapa executa algo e chama `next`.
	- **Responsabilidade única por handler:** cada etapa faz uma coisa.
	- **Short-circuit:** parar a cadeia quando a condição é atendida.
	- **Context object:** transportar dados compartilhados com clareza.
	- **Observabilidade:** tracing por etapa e correlação.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Testar a cadeia exige validar ordem, short-circuit e efeitos colaterais. Sem testes, mudanças na ordem quebram comportamento sutilmente.

- **Performance e Manutenção**  
	- Cadeias longas aumentam latência e complexidade.
	- Uma etapa lenta bloqueia tudo (se síncrono).
	- Se cada handler tem side effects, o rollback fica difícil.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: handlers com responsabilidades múltiplas e estado escondido.
	- Coverage: não testar caminhos de short-circuit e erros.
	- Flakiness: handlers que dependem de tempo/IO sem controle em testes.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes focados em “ordem e efeitos” (snapshots de pipeline) e em cenários críticos.
	- Observabilidade como gate: tracing/metrics por etapa.
	- Feature flags para introduzir um handler novo sem risco.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: handlers isolados (funções puras quando possível).
	- Integração: cadeia completa com dependências fakes.
	- E2E: poucos fluxos com dependências reais.

- **Métrica de Qualidade**  
	- Latência por etapa (p95/p99)
	- Taxa de short-circuit (ex.: bloqueios por política)
	- Erros por etapa
	- Complexidade/tamanho da cadeia

---

## Exemplos Avançados (Python, C# e Go)

Exemplo simples: pipeline de validação onde cada etapa pode encerrar o fluxo.

### Python

```python
from typing import Callable


Handler = Callable[[dict, Callable[[], dict]], dict]


def auth(ctx: dict, next_: Callable[[], dict]) -> dict:
		if not ctx.get("user"):
				return {"status": 401}
		return next_()


def rate_limit(ctx: dict, next_: Callable[[], dict]) -> dict:
		if ctx.get("blocked"):
				return {"status": 429}
		return next_()


def build_pipeline(handlers: list[Handler], terminal: Callable[[], dict]) -> Callable[[dict], dict]:
		def run(ctx: dict) -> dict:
				i = 0

				def next_() -> dict:
						nonlocal i
						if i >= len(handlers):
								return terminal()
						h = handlers[i]
						i += 1
						return h(ctx, next_)

				return next_()

		return run
```

### C#

```csharp
public delegate Task<Response> Handler(Context ctx, Func<Task<Response>> next);

public static Handler Auth() => async (ctx, next) =>
{
		if (ctx.User is null) return new Response(401);
		return await next();
};
```

### Go

```go
package pipeline

type Ctx struct{ User string; Blocked bool }
type Res struct{ Status int }

type Next func() Res
type Handler func(*Ctx, Next) Res

func Build(handlers []Handler, terminal func() Res) func(*Ctx) Res {
		return func(ctx *Ctx) Res {
				i := 0
				var next Next
				next = func() Res {
						if i >= len(handlers) {
								return terminal()
						}
						h := handlers[i]
						i++
						return h(ctx, next)
				}
				return next()
		}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Ordem é contrato:** documente e teste (alterar ordem pode mudar semântica).
- **Cada handler deve ser pequeno e previsível.**
- **Evite estado implícito:** prefira `ctx` explícito.
- **Observabilidade por etapa:** tracing/metrics/logs com correlação.
- **Cuidado com side effects:** se handlers fazem escrita, pense em idempotência/compensação.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** pipelines internas podem precisar de limites (timeout/CPU) e backpressure.
- **Pipelines CI/CD:** testes de ordem e regressão; feature flags para handlers novos.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing por handler; alertas de etapa lenta.
- **Testes e Infra-as-Code:** stubs/ambientes para validações que dependem de serviços externos.

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência por etapa
- Taxa de bloqueio/short-circuit
- Erros por handler
- Tamanho da cadeia (tendência)

---

## Frameworks e Ferramentas do Mercado

- **Observabilidade:** OpenTelemetry
- **HTTP pipelines:** middlewares (FastAPI/Starlette, ASP.NET Core, net/http)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Chain of Responsibility
- Middlewares e pipelines em frameworks web

---

## FAQ Especialista

**CoR não vira um “fluxo escondido”?**  
Pode. Resolva com naming claro, ordem documentada e tracing por etapa.

**Quando preferir regras em tabela/engine?**  
Quando as regras mudam com frequência e você precisa governança/explicabilidade. CoR é ótimo para pipelines de engenharia, mas pode ficar rígido para regras de negócio altamente mutáveis.

**Como evitar cadeia gigante?**  
Agrupe por responsabilidade, remova etapas redundantes e meça latência por handler (otimize o que dói).

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](builder.md) | [Índice](../../SUMMARY.md) | [Próximo](command.md)
