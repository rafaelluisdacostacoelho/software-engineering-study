[Anterior](../tests/unit-testing.md) | [Índice](../../SUMMARY.md) | [Próximo](code-review-collaboration.md)

# System Design Interview — Guia Prático para Candidatos e Entrevistadores

## Visão Geral e Contexto de Mercado

Entrevistas de System Design avaliam se você consegue transformar um problema aberto em uma solução técnica **coerente, escalável e operável**. No mercado (especialmente para posições mid/sênior/staff), elas testam mais do que “arquitetura bonita”: querem ver como você lida com **trade-offs**, **incerteza**, **requisitos não funcionais** e **operabilidade**.

Em empresas com squads e plataformas complexas, o que diferencia candidatos é:

- Capacidade de fazer perguntas certas (requisitos, restrições, SLAs/SLOs).
- Pensamento por evolução (MVP → escala → hardening).
- Clareza em escolhas (consistência, disponibilidade, custo, simplicidade).
- Mentalidade de produção (observabilidade, resiliência, segurança, incident response).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O formato popularizou-se com grandes empresas de tecnologia para avaliar engenharia sistêmica. Com cloud e microserviços, entrevistas passaram a incluir temas como filas, cache, consistência eventual, multi-região, rate limiting, e modelagem de dados em escala.

- **Padrões e Protocolos Usados no Mercado**
	- **API Design:** REST/gRPC, OpenAPI/Protobuf.
	- **Mensageria:** Kafka/RabbitMQ/SQS; modelos pub/sub e filas.
	- **Caching:** cache-aside, write-through, TTL e invalidação.
	- **Consistência:** transações, sagas, outbox, idempotência.
	- **Observabilidade:** OpenTelemetry, métricas, logs estruturados, tracing.
	- **Segurança:** authn/authz, secrets, criptografia em trânsito/repouso.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O desafio na entrevista é navegar escala sem “overengineering”: mostrar caminho incremental e justificar cada etapa.

- **Performance e Manutenção**  
	- Escolhas de banco/índices/particionamento precisam de racional.
	- Designs muito acoplados dificultam evolução.
	- Latência, throughput e custo devem ser tratados explicitamente.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt arquitetural aparece como integrações frágeis, modelos inconsistentes e ausência de observabilidade.
	- O entrevistador quer ver como você evita regressão (testes, contratos, rollout seguro).

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Estratégias de rollout: canary, blue/green, feature flags.
	- Migrações seguras: expansão/contração de schema, compatibilidade retroativa.
	- Testes: unit + integração + contrato + e2e mínimo.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Contract tests para integrações entre serviços.
	- Ambientes efêmeros para integração.
	- Mocks de infraestrutura apenas onde o custo/instabilidade for alto.

- **Métrica de Qualidade**  
	- SLOs (latência p95/p99, disponibilidade)
	- Error budget
	- Taxa de falhas por deploy, MTTR
	- Custo por requisição/cliente

---

## Exemplos Avançados (Python, C# e Go)

Exemplo de um componente típico em designs: **rate limiting** (proteção e controle de capacidade). Os snippets são ilustrativos.

### Python

```python
import time
from collections import defaultdict, deque


class SlidingWindowRateLimiter:
		def __init__(self, max_requests: int, window_seconds: int) -> None:
				self.max_requests = max_requests
				self.window_seconds = window_seconds
				self._requests: dict[str, deque[float]] = defaultdict(deque)

		def allow(self, key: str) -> bool:
				now = time.time()
				q = self._requests[key]
				while q and q[0] <= now - self.window_seconds:
						q.popleft()
				if len(q) >= self.max_requests:
						return False
				q.append(now)
				return True
```

### C#

```csharp
using System.Collections.Concurrent;

public sealed class TokenBucket
{
		private readonly int _capacity;
		private readonly double _refillPerSecond;
		private double _tokens;
		private long _lastTicks;

		public TokenBucket(int capacity, double refillPerSecond)
		{
				_capacity = capacity;
				_refillPerSecond = refillPerSecond;
				_tokens = capacity;
				_lastTicks = DateTime.UtcNow.Ticks;
		}

		public bool TryConsume(double cost = 1.0)
		{
				var now = DateTime.UtcNow.Ticks;
				var elapsedSeconds = (now - _lastTicks) / (double)TimeSpan.TicksPerSecond;
				_lastTicks = now;

				_tokens = Math.Min(_capacity, _tokens + elapsedSeconds * _refillPerSecond);
				if (_tokens < cost) return false;
				_tokens -= cost;
				return true;
		}
}
```

### Go

```go
package ratelimit

import (
		"sync"
		"time"
)

type FixedWindow struct {
		mu     sync.Mutex
		start  time.Time
		count  int
		limit  int
		window time.Duration
}

func NewFixedWindow(limit int, window time.Duration) *FixedWindow {
		return &FixedWindow{start: time.Now(), limit: limit, window: window}
}

func (w *FixedWindow) Allow() bool {
		w.mu.Lock()
		defer w.mu.Unlock()

		now := time.Now()
		if now.Sub(w.start) >= w.window {
				w.start = now
				w.count = 0
		}
		if w.count >= w.limit {
				return false
		}
		w.count++
		return true
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Comece por requisitos:** QPS, latência, tamanho de dados, SLA/SLO, picos, multi-região.
- **Faça suposições explícitas:** e valide com o entrevistador.
- **Evolua incrementalmente:** MVP simples → cache → fila → particionamento → multi-região.
- **Trate falhas como primeiro cidadão:** retries com backoff, timeouts, circuit breaker, idempotência.
- **Operabilidade:** logging, tracing, dashboards, alertas e runbooks.
- **Evite overdesign:** não desenhe Kafka, sharding e multi-region sem necessidade.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** autoscaling, requests/limits, readiness/liveness, rollout progressivo.
- **Pipelines CI/CD:** deploy seguro, migrações compatíveis, validações automatizadas.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** SLOs, métricas, tracing, SIEM.
- **Testes e Infra-as-Code:** ambientes efêmeros, validação de mudanças de infra, DR drills.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95/p99 latency, throughput, error rate
- SLOs e error budget
- MTTR, change failure rate
- custo por requisição (FinOps)

---

## Frameworks e Ferramentas do Mercado

- **Python:** FastAPI, pytest, locust, opentelemetry
- **C#:** ASP.NET Core, xUnit, BenchmarkDotNet, OpenTelemetry
- **Go:** net/http, testify, vegeta/k6, OpenTelemetry
- **Ferramentas de integração:** Kubernetes, Terraform, Prometheus/Grafana, Datadog, ELK

---

## Recursos Avançados e Leituras Recomendadas

- _Designing Data-Intensive Applications_ (Martin Kleppmann)
- _Building Microservices_ (Sam Newman)
- _Site Reliability Engineering_ (Google)

---

## FAQ Especialista

**O que o entrevistador mais penaliza?**  
Partir direto para uma arquitetura complexa sem requisitos, ignorar trade-offs (consistência vs disponibilidade), e esquecer operabilidade (logs, métricas, alertas, rollback).

**Como lidar com estimativas (QPS, storage)?**  
Faça aproximações rápidas (ordens de grandeza), declare suposições e use isso para justificar cache, particionamento e filas.

**Como “vender” trade-offs com clareza?**  
Explique o porquê, o custo (complexidade/latência/custo) e o plano de evolução. O entrevistador quer ver engenharia pragmática.

---

## Referências e Práticas do Mercado

- Google SRE (métricas e práticas)
- Martin Fowler (padrões e trade-offs)
- ThoughtWorks Tech Radar

---

[Anterior](../tests/unit-testing.md) | [Índice](../../SUMMARY.md) | [Próximo](code-review-collaboration.md)
