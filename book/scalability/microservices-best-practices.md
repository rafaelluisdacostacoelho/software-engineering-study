[Anterior](event-sourcing.md) | [Índice](../../SUMMARY.md) | [Próximo](../cloud/cloud-native-patterns.md)

# Microservices — Práticas Avançadas e Padrões para Escala

## Visão Geral e Contexto de Mercado

Microservices é um estilo arquitetural em que o sistema é composto por **serviços pequenos e independentes**, alinhados a **capacidades de negócio**, com deploy e evolução relativamente autônomos. No mercado, microserviços costumam aparecer quando:

- Há múltiplas squads com autonomia e cadências distintas
- O domínio é amplo e precisa de fronteiras claras (bounded contexts)
- A escalabilidade exige desacoplamento de times e de componentes
- A disponibilidade/resiliência são metas explícitas (SLOs)

Microservices não é um objetivo em si; é um conjunto de trade-offs. Ele troca simplicidade de um monólito por **complexidade distribuída**: rede falha, latência aumenta, consistência é mais difícil, e operação/observabilidade tornam-se disciplina obrigatória.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	A adoção moderna cresceu com cloud, containerização e práticas DevOps. O foco migrou de “dividir por camadas técnicas” para “dividir por domínio” (DDD), e de “chamar HTTP entre serviços” para misturar **sincronia** e **assíncronia** (eventos/filas) com estratégias de consistência.

- **Padrões e Protocolos Usados no Mercado**
	- **Bounded Contexts (DDD):** fronteiras de modelo e linguagem.
	- **API Gateway / BFF:** agregação e proteção de APIs.
	- **Service Mesh:** mTLS, roteamento, retries, observabilidade (quando faz sentido).
	- **Sagas (orquestração/coreografia):** consistência entre serviços.
	- **Outbox/Inbox:** integração confiável DB↔eventos.
	- **Strangler Fig:** migração incremental a partir de monólitos.
	- **Contract testing:** Pact/consumer-driven contracts.
	- **Health checks:** liveness/readiness/startup.
	- **Resiliência:** timeouts, retries, circuit breaker, bulkheads.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O número de combinações de integração cresce rapidamente: versões distintas, contratos quebrando, eventos reprocessados, dependências instáveis. Sem contract tests e ambientes de integração confiáveis, os bugs viram incidentes de produção.

- **Performance e Manutenção**  
	- Latência: cada hop de rede adiciona custo; p99 vira um problema.
	- Chatty services: excesso de chamadas e payloads grandes.
	- Custos: observabilidade, egress, bancos duplicados e pipelines.
	- Dados: ownership e consistência ficam mais difíceis.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: serviços “mini-monólitos” sem domínio claro; acoplamento por shared DB.
	- Coverage: falta de testes para falhas de rede, retries e idempotência.
	- Flakiness: testes end-to-end demais, lentos e instáveis.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Pipelines por serviço com checks mínimos: lint, unit, segurança, build de imagem.
	- Deploy progressivo: canary/blue-green e feature flags.
	- Gates por SLO: erro, latência e saturação (RED/USE).
	- Versionamento de API/eventos: compatibilidade e depreciação com prazo.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: lógica de domínio sem I/O.
	- Integração: DB/Redis/broker reais (testcontainers quando possível).
	- Contract: validação de consumidor/provedor.
	- E2E: poucos fluxos críticos (pagamento, criação de pedido) com foco em risco.

- **Métrica de Qualidade**  
	- SLO: disponibilidade, latência p95/p99, taxa de erro
	- MTTR e tempo de detecção
	- Change failure rate (DORA)
	- Lead time e frequência de deploy
	- Taxa de quebras de contrato e eventos incompatíveis

---

## Exemplos Avançados (Python, C# e Go)

Os exemplos abaixo mostram padrões práticos de resiliência (timeout/retry/idempotência) comuns em microserviços.

### Python

```python
import time
import random
import requests


class TransientError(Exception):
		pass


def call_with_timeout_and_retry(url: str, timeout_s: float = 1.0, max_attempts: int = 3):
		base_sleep = 0.1
		for attempt in range(1, max_attempts + 1):
				try:
						r = requests.get(url, timeout=timeout_s)
						if r.status_code >= 500:
								raise TransientError(f"server error {r.status_code}")
						return r.json()
				except (requests.Timeout, requests.ConnectionError, TransientError) as e:
						if attempt == max_attempts:
								raise
						# backoff com jitter
						sleep = base_sleep * (2 ** (attempt - 1))
						time.sleep(sleep + random.random() * 0.05)
```

### C#

```csharp
// Exemplo conceitual com Polly (padrão de mercado): timeout + retry com backoff.
// (O foco aqui é o desenho: trate timeouts, retries e logs/tracing.)

// using Polly;
// using Polly.Timeout;

// var policy = Policy
//     .TimeoutAsync<HttpResponseMessage>(TimeSpan.FromSeconds(1))
//     .WrapAsync(
//         Policy
//             .Handle<HttpRequestException>()
//             .Or<TimeoutRejectedException>()
//             .WaitAndRetryAsync(3, i => TimeSpan.FromMilliseconds(100 * Math.Pow(2, i)))
//     );
// var response = await policy.ExecuteAsync(() => httpClient.GetAsync(url));
```

### Go

```go
package httpx

import (
		"context"
		"errors"
		"net/http"
		"time"
)

func GetWithTimeout(ctx context.Context, client *http.Client, url string) (*http.Response, error) {
		ctx, cancel := context.WithTimeout(ctx, 1*time.Second)
		defer cancel()

		req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
		if err != nil {
				return nil, err
		}
		res, err := client.Do(req)
		if err != nil {
				if errors.Is(err, context.DeadlineExceeded) {
						return nil, err
				}
				return nil, err
		}
		return res, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Comece com o monólito modular** quando possível; migre com Strangler Fig.
- **Defina fronteiras por domínio**, não por camadas técnicas (evite “UserService” genérico que vira tudo).
- **Banco por serviço** é o ideal para autonomia; evite shared DB (acoplamento invisível).
- **Retries sem idempotência geram bugs graves** (duplicação). Use idempotency keys e dedupe.
- **Timeout é obrigatório:** sem timeout, “dependência lenta = queda em cascata”.
- **Circuit breaker/bulkhead** em chamadas críticas; degrade com fallback.
- **Observabilidade desde o dia 1:** logs estruturados, métricas e tracing com correlation-id.
- **Evite excesso de sincronia:** use eventos quando o acoplamento temporal for alto.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** readiness/liveness, HPA, limites de recursos e políticas de rollout.
- **Pipelines CI/CD:** builds por serviço, SBOM, scans de vulnerabilidade, deploy canary.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** OpenTelemetry + dashboards; alertas por SLO.
- **Testes e Infra-as-Code:** provisionar filas/tópicos/bancos, secrets, permissões mínimas e ambientes efêmeros.

---

## Métricas, Monitoramento e Melhoria Contínua

- **RED (Rate, Errors, Duration)** por endpoint
- **USE (Utilization, Saturation, Errors)** por recurso
- SLOs por serviço e por jornada (end-to-end)
- MTTR, incident count, change failure rate (DORA)
- Lag de consumidores, DLQ rate (quando houver EDA)

---

## Frameworks e Ferramentas do Mercado

- **Gateways:** Kong, Apigee, NGINX
- **Service Mesh:** Istio, Linkerd (quando necessário)
- **Observabilidade:** OpenTelemetry, Prometheus, Grafana, Jaeger/Tempo
- **Python:** FastAPI, Celery, opentelemetry-sdk
- **C#:** ASP.NET Core, MassTransit, OpenTelemetry
- **Go:** net/http, chi/gin, OpenTelemetry

---

## Recursos Avançados e Leituras Recomendadas

- Sam Newman — _Building Microservices_
- Martin Fowler (Strangler Fig, Microservices)
- Google SRE (SLOs, incident management)
- Documentações de plataforma (Kubernetes, service meshes)

---

## FAQ Especialista

**Microservices sempre escalam melhor?**  
Escalam times e domínios quando há fronteiras claras, mas podem piorar performance e confiabilidade se o sistema virar uma malha de dependências síncronas sem resiliência.

**Quando NÃO usar microservices?**  
Quando o domínio é pequeno, o time é pequeno, ou a complexidade operacional vai superar o benefício. Monólito modular costuma ser melhor ponto de partida.

**Como evitar “deploy independente” virar “inferno de versões”?**  
Contratos versionados, compatibilidade retroativa, depreciação com prazo, contract tests e observabilidade para detectar regressões rapidamente.

---

## Referências e Práticas do Mercado

- Martin Fowler
- Sam Newman
- Google SRE
- ThoughtWorks Tech Radar

---

[Anterior](event-sourcing.md) | [Índice](../../SUMMARY.md) | [Próximo](../cloud/cloud-native-patterns.md)
