[Anterior](Composite.md) | [Índice](../../SUMMARY.md) | [Próximo](Facade.md)

# Decorator — Adicionar Responsabilidades Sem Explodir Herança (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Decorator permite adicionar comportamento a um objeto **envolvendo-o** com outro objeto que implementa a mesma interface. Na prática, você compõe responsabilidades sem criar uma explosão de subclasses (“`CachedLoggedValidatedX`”).

No mercado, Decorator aparece como:

- **Middlewares/Interceptors:** camadas de logging, métricas, auth.
- **Clientes de infraestrutura:** wrappers de HTTP/DB/queue com retry, timeout, tracing.
- **Cross-cutting concerns:** caching, rate limiting, circuit breaker.
- **Feature toggles:** um wrapper que altera comportamento sem tocar no core.

O ganho é composição flexível e testabilidade. O risco é criar pilhas profundas de wrappers difíceis de rastrear/depurar.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  Decorator é GoF clássico. Em frameworks atuais, a ideia aparece como “pipeline” e “interceptor chain”. Em linguagens modernas, também se materializa via funções de alta ordem (Python/Go) e attributes/proxies (C#).

- **Padrões e Protocolos Usados no Mercado**
  - **Interface comum:** o decorator implementa a mesma interface do componente.
  - **Delegação:** o decorator chama o componente interno e adiciona algo antes/depois.
  - **Stacking:** múltiplos decorators encadeados.
  - **Separação de concerns:** cada decorator com responsabilidade única.
  - **Observabilidade:** trace/log com correlação por camada.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  Testes precisam validar comportamento isolado do decorator e também o empilhamento (ordem). Sem testes, muda-se a ordem e quebra-se semântica.

- **Performance e Manutenção**  
  - Cada camada adiciona overhead (chamada extra, alocação, logs).
  - Wrappers podem duplicar responsabilidades (ex.: retry em dois lugares).
  - Debug fica mais difícil se não houver nomes e tracing por camada.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  - Debt: decorators que fazem “tudo” (logs + retries + auth + cache).
  - Coverage: não testar timeout/retry/backoff em cenários realistas.
  - Flakiness: decorators que dependem de tempo, thread scheduling ou IO sem controle.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Testes de contrato do cliente decorado (mesma interface, mesmos invariantes).
  - Testes de “ordem do pipeline” para evitar regressões.
  - Feature flags para introduzir decorators gradualmente.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Unit: decorator puro com dependência fake.
  - Integração: decorator com dependência real em ambiente efêmero (containers) para validar timeout/retry.
  - E2E: apenas para fluxos críticos que dependem de resiliência.

- **Métrica de Qualidade**  
  - Latência adicional por camada
  - Taxa de retries/circuit open
  - Cache hit/miss (se houver cache decorator)
  - Erros por camada (onde falha)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: um client de API que ganha logging e retry via decorators.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class HttpClient(Protocol):
	def get(self, url: str) -> str:
		...


@dataclass
class RequestsClient:
	def get(self, url: str) -> str:
		# placeholder: requests.get(url).text
		return "OK"


@dataclass
class LoggingClient:
	inner: HttpClient

	def get(self, url: str) -> str:
		print(f"http_get url={url}")
		return self.inner.get(url)


@dataclass
class RetryClient:
	inner: HttpClient
	attempts: int = 3

	def get(self, url: str) -> str:
		last_exc: Exception | None = None
		for _ in range(self.attempts):
			try:
				return self.inner.get(url)
			except Exception as e:
				last_exc = e
		assert last_exc is not None
		raise last_exc
```

### C#

```csharp
public interface IHttpClient
{
	Task<string> Get(string url, CancellationToken ct);
}

public sealed class LoggingHttpClient : IHttpClient
{
	private readonly IHttpClient _inner;
	private readonly ILogger<LoggingHttpClient> _logger;

	public LoggingHttpClient(IHttpClient inner, ILogger<LoggingHttpClient> logger)
		=> (_inner, _logger) = (inner, logger);

	public async Task<string> Get(string url, CancellationToken ct)
	{
		_logger.LogInformation("http_get url={Url}", url);
		return await _inner.Get(url, ct);
	}
}
```

### Go

```go
package httpx

import "fmt"

type Client interface {
	Get(url string) (string, error)
}

type Logging struct{ Inner Client }

func (l Logging) Get(url string) (string, error) {
	fmt.Printf("http_get url=%s\n", url)
	return l.Inner.Get(url)
}

type Retry struct {
	Inner    Client
	Attempts int
}

func (r Retry) Get(url string) (string, error) {
	var lastErr error
	attempts := r.Attempts
	if attempts <= 0 {
		attempts = 3
	}
	for i := 0; i < attempts; i++ {
		res, err := r.Inner.Get(url)
		if err == nil {
			return res, nil
		}
		lastErr = err
	}
	return "", lastErr
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Evite duplicar políticas:** se existe retry em um decorator, não replique em outro nível.
- **Ordem importa:** por exemplo, logging fora do retry vs dentro do retry muda volume e semântica.
- **Mantenha cada decorator pequeno** e com responsabilidade única.
- **Observabilidade por camada:** inclua nome da camada, latência e erro.
- **Cuidado com exceções:** defina claramente o que é erro transitório vs permanente.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** retries precisam respeitar budgets (timeouts globais) para não amplificar carga.
- **Pipelines CI/CD:** testes de regressão para ordem e comportamento; config-driven decorators (feature flags) com validação.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** tracing e métricas por wrapper; alertas quando uma camada aumenta latência.
- **Testes e Infra-as-Code:** ambientes controlados para simular falhas (latência, erros 5xx) e validar políticas.

---

## Métricas, Monitoramento e Melhoria Contínua

- Overhead de latência introduzido por camada
- Taxa de retries/backoff e circuit open
- Erros categorizados por camada
- Volume de logs por camada (evitar custo excessivo)

---

## Frameworks e Ferramentas do Mercado

- **Python:** requests/httpx + wrappers; tenacity para retry (muitas vezes substitui decorator manual)
- **C#:** HttpClient + DelegatingHandler/Polly
- **Go:** net/http + RoundTripper wrappers; resilience libs (quando aplicável)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Decorator
- Resiliência (retry/backoff/circuit breaker) e “retry storms”
- Observabilidade por camadas (OpenTelemetry)

---

## FAQ Especialista

**Decorator e Chain of Responsibility são iguais?**  
São parecidos na forma (encadeamento), mas diferentes no objetivo: Decorator preserva a interface e adiciona responsabilidades; CoR decide *quem* trata a requisição (pode encerrar no meio).

**Quando preferir middleware/framework ao decorator manual?**  
Quando existe suporte nativo (ex.: `DelegatingHandler` + Polly em C#). Use o que o ecossistema já otimiza e padroniza.

**Como evitar “wrapper hell”?**  
Limite profundidade, componha via configuração explícita, e mantenha tracing/nomes claros para debug.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Composite.md) | [Índice](../../SUMMARY.md) | [Próximo](Facade.md)
