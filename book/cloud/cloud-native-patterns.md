[Anterior](../scalability/microservices-best-practices.md) | [Índice](../../SUMMARY.md) | [Próximo](security-best-practices.md)

# Cloud-Native Patterns — Padrões e Nuances entre AWS, Azure e GCP

## Visão Geral e Contexto de Mercado

“Cloud-native” é menos sobre usar Kubernetes e mais sobre construir sistemas com **elasticidade, resiliência, automação e observabilidade** como padrões. Em empresas modernas (squads ágeis, microserviços, DevOps), cloud-native patterns são o conjunto de práticas que tornam o sistema:

- **Operável** (monitorável, depurável, com runbooks)
- **Resiliente** (falha parcial, timeouts, retries, degradação)
- **Escalável** (horizontal, com limites claros)
- **Seguro** (least privilege, segredos, auditoria)

No mercado, esses padrões aparecem tanto em arquiteturas com Kubernetes quanto em stacks “managed” (AWS Lambda, Azure Functions, Cloud Run) e em serviços gerenciados (RDS, Cosmos DB, Cloud SQL, Pub/Sub, SQS).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Cloud-native consolidou-se com a maturidade de containers, orquestração, IaC e SRE. O foco passou de “rodar na nuvem” para “operar bem na nuvem”: automação, imutabilidade, observabilidade e resiliência.

- **Padrões e Protocolos Usados no Mercado**
	- **12-Factor App** (config por env, stateless, logs como stream)
	- **Health checks** (liveness/readiness), autoscaling
	- **Circuit breaker, retries com backoff, timeouts**
	- **Bulkheads / isolamento de recursos**
	- **Idempotência** em handlers (especialmente com filas)
	- **Blue/Green, Canary, Feature Flags**
	- **OpenTelemetry** para tracing/metrics/logs
	- **IAM** (least privilege), KMS/Key Vault/Secret Manager

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em múltiplos ambientes (dev/stage/prod) e múltiplas contas/subscriptions/projects, o desafio é evitar drift e manter padrões consistentes com automação.

- **Performance e Manutenção**  
	- Latência p95/p99 pode piorar com redes, service meshes e camadas extras.
	- Custos podem explodir sem FinOps (logs demais, autoscaling mal calibrado, egress).
	- Configuração e secrets mal geridos geram incidentes e vazamentos.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: infra “clicada” no console, sem IaC.
	- Flakiness em testes de integração por dependência de ambientes instáveis.
	- Cobertura insuficiente de cenários de falha (timeouts, retries, partial outage).

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- IaC em pipeline: `plan`/`apply` com revisões e políticas.
	- Deploy progressivo (canary/blue-green) + rollback automatizado.
	- Migrações seguras (expand/contract) e compatibilidade retroativa.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit tests para core.
	- Integration tests em ambientes efêmeros (testcontainers) ou provisionados por pipeline.
	- Chaos testing/fault injection (quando o risco justifica).

- **Métrica de Qualidade**  
	- SLOs (latência p95/p99, disponibilidade)
	- Error budget
	- MTTR, change failure rate
	- Custo por requisição (FinOps)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: “retry com backoff + jitter” e “timeout” são padrões cloud-native fundamentais para resiliência.

### Python

```python
import random
import time


def retry_with_backoff(action, max_attempts: int = 5, base_delay: float = 0.2):
    for attempt in range(1, max_attempts + 1):
        try:
            return action()
        except Exception:
            if attempt == max_attempts:
                raise
            jitter = random.random() * base_delay
            delay = (2 ** (attempt - 1)) * base_delay + jitter
            time.sleep(delay)
```

### C#

```csharp
using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

public static class Http
{
		public static async Task<string> GetWithTimeoutAsync(HttpClient client, string url, TimeSpan timeout)
		{
				using var cts = new CancellationTokenSource(timeout);
				using var res = await client.GetAsync(url, cts.Token);
				res.EnsureSuccessStatusCode();
				return await res.Content.ReadAsStringAsync(cts.Token);
		}
}
```

### Go

```go
package resilient

import (
		"context"
		"net/http"
		"time"
)

func GetWithTimeout(url string, timeout time.Duration) (*http.Response, error) {
		ctx, cancel := context.WithTimeout(context.Background(), timeout)
		defer cancel()

		req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
		if err != nil {
				return nil, err
		}
		return http.DefaultClient.Do(req)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Timeouts em toda chamada remota** (HTTP, DB, fila) + retries com backoff.
- **Idempotência** em consumers/handlers para suportar reprocessamento.
- **Separação de configuração e segredos:** secrets em Secret Manager/Key Vault/KMS, nunca no repo.
- **Least privilege**: IAM por workload, não “admin por padrão”.
- **Observabilidade antes de escala:** sem tracing/metrics/logs, você não sabe onde está o gargalo.
- **Evite custo oculto:** logs excessivos, métricas cardinalidade alta, egress.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** readiness/liveness, HPA, requests/limits, PDBs, rollout progressivo.
- **Pipelines CI/CD:** IaC + deploy progressivo + validações (smoke, SLO checks).
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** SAST/DAST, policy-as-code, SIEM.
- **Testes e Infra-as-Code:** ambientes efêmeros, drift detection, backups e DR.

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência p95/p99, throughput, error rate
- SLO/error budget
- MTTR, change failure rate
- Custo por serviço/ambiente (FinOps)

---

## Frameworks e Ferramentas do Mercado

- **Python:** FastAPI, opentelemetry, tenacity
- **C#:** ASP.NET Core, OpenTelemetry, Polly
- **Go:** net/http, OpenTelemetry, retry libs
- **Infra:** Kubernetes, Terraform/Pulumi, Helm, Argo CD/Flux
- **Observabilidade:** Prometheus/Grafana, Datadog, ELK

---

## Recursos Avançados e Leituras Recomendadas

- CNCF Landscape (stack cloud-native)
- Google SRE / DORA
- _Designing Data-Intensive Applications_ (Kleppmann)

---

## FAQ Especialista

**Cloud-native exige Kubernetes?**  
Não. Você pode ser cloud-native com serviços gerenciados (serverless/managed DB/MQ) desde que pratique automação, observabilidade e resiliência.

**Como equilibrar resiliência vs custo?**  
Comece com SLOs e risco. Invista em padrões (timeouts, retries, bulkheads) antes de multi-região. Use error budget e FinOps para calibrar.

**Retries não pioram incidentes?**  
Podem piorar se mal configurados. Use backoff + jitter, limites, circuit breaker e respeite `Retry-After` quando existir.

---

## Referências e Práticas do Mercado

- CNCF / Cloud Native Definition
- Google SRE
- ThoughtWorks Tech Radar

---

[Anterior](../scalability/microservices-best-practices.md) | [Índice](../../SUMMARY.md) | [Próximo](security-best-practices.md)
