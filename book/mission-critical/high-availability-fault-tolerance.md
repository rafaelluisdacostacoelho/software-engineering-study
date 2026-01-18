[Anterior](../cloud/security-best-practices.md) | [Índice](../../SUMMARY.md) | [Próximo](../tests/tdd.md)

# High Availability & Fault Tolerance — Alta Disponibilidade e Tolerância a Falhas

## Visão Geral e Contexto de Mercado

Alta Disponibilidade (HA) e Tolerância a Falhas (Fault Tolerance) são disciplinas essenciais em sistemas onde downtime e degradação têm impacto direto em receita, confiança e compliance (pagamentos, e-commerce, saúde, logística). Em ambientes modernos (microserviços, cloud, CI/CD), o objetivo não é “nunca falhar” — é:

- Falhar de forma **controlada** (graceful degradation).
- Recuperar rápido (**MTTR baixo**).
- Limitar blast radius (isolamento, bulkheads).
- Ter previsibilidade com SLOs, error budget e playbooks.

Na prática de mercado, “ser altamente disponível” envolve tanto design quanto operação: redundância, automação, observabilidade e ensaios de recuperação.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
  A disponibilidade evoluiu do modelo “servidor único + backup” para arquiteturas distribuídas com redundância e automação (autoscaling, multi-AZ, multi-região). Com SRE, a conversa migrou de uptime absoluto para SLOs e error budget.

- **Padrões e Protocolos Usados no Mercado**
  - **Redundância:** N+1, active-active, active-passive.
  - **Failover:** automático com health checks, DNS/traffic shifting.
  - **Timeouts e retries com backoff + jitter.**
  - **Circuit breaker e bulkheads** (isolamento de recursos).
  - **Rate limiting e load shedding** (proteção contra overload).
  - **Idempotência** (essencial para reprocessamento e retries).
  - **DR (Disaster Recovery):** backups, restore testado, runbooks.
  - **Observabilidade:** OpenTelemetry, métricas (SLI), logs estruturados.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
  Em sistemas grandes, o risco é “HA no papel”: documentação bonita sem testes de falha. A escalabilidade exige padrões repetíveis (golden paths) e automação.

- **Performance e Manutenção**  
  - Retries mal configurados amplificam incidentes (retry storms).
  - Health checks ruins causam failover em cascata.
  - Observabilidade insuficiente impede diagnosticar gargalos (p95/p99).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
  - Debt: single points of failure (SPOF), permissões/admin sem controle, falta de runbooks.
  - Coverage: poucos testes de recuperação (restore, failover).
  - Flakiness: testes de caos sem ambiente controlado e sem hipóteses claras.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
  - Rollouts progressivos (canary/blue-green) com métricas como gate.
  - Migração expand/contract e compatibilidade retroativa.
  - Smoke tests e SLO checks pós-deploy.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
  - Unit tests: invariantes e comportamento local.
  - Integration tests: dependências reais (DB/filas) com ambientes efêmeros.
  - DR drills: exercícios periódicos (restore, failover, simulação de perda de AZ).
  - Chaos/fault injection: seletivo e com hipóteses verificáveis.

- **Métrica de Qualidade**  
  - SLO de disponibilidade/latência (p95/p99)
  - MTTR e MTTD
  - Change failure rate e rollback rate
  - Error budget burn rate
  - RTO/RPO atingidos em drills reais

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: circuit breaker simplificado (didático). Em produção, prefira bibliotecas maduras e instrumentação.

### Python

```python
import time


class CircuitBreaker:
	def __init__(self, failure_threshold: int, reset_after_seconds: int) -> None:
		self.failure_threshold = failure_threshold
		self.reset_after_seconds = reset_after_seconds
		self.failures = 0
		self.opened_at: float | None = None

	def allow(self) -> bool:
		if self.opened_at is None:
			return True
		return (time.time() - self.opened_at) >= self.reset_after_seconds

	def on_success(self) -> None:
		self.failures = 0
		self.opened_at = None

	def on_failure(self) -> None:
		self.failures += 1
		if self.failures >= self.failure_threshold:
			self.opened_at = time.time()
```

### C#

```csharp
public sealed class CircuitBreaker
{
	private readonly int _threshold;
	private readonly TimeSpan _resetAfter;
	private int _failures;
	private DateTime? _openedAt;

	public CircuitBreaker(int threshold, TimeSpan resetAfter)
	{
		_threshold = threshold;
		_resetAfter = resetAfter;
	}

	public bool Allow()
		=> _openedAt is null || (DateTime.UtcNow - _openedAt.Value) >= _resetAfter;

	public void OnSuccess() { _failures = 0; _openedAt = null; }

	public void OnFailure()
	{
		_failures++;
		if (_failures >= _threshold) _openedAt = DateTime.UtcNow;
	}
}
```

### Go

```go
package resilience

import "time"

type CircuitBreaker struct {
	threshold  int
	resetAfter time.Duration
	failures   int
	openedAt   time.Time
	open       bool
}

func NewCircuitBreaker(threshold int, resetAfter time.Duration) *CircuitBreaker {
	return &CircuitBreaker{threshold: threshold, resetAfter: resetAfter}
}

func (cb *CircuitBreaker) Allow(now time.Time) bool {
	if !cb.open {
		return true
	}
	return now.Sub(cb.openedAt) >= cb.resetAfter
}

func (cb *CircuitBreaker) OnSuccess() {
	cb.failures = 0
	cb.open = false
}

func (cb *CircuitBreaker) OnFailure(now time.Time) {
	cb.failures++
	if cb.failures >= cb.threshold {
		cb.open = true
		cb.openedAt = now
	}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Defina SLO/SLI antes de “otimizar HA”.**
- **RTO/RPO explícitos** e alinhados com negócio/compliance.
- **Evite retry storms:** timeouts curtos, backoff+jitter, limites e circuit breaker.
- **Degradação graciosa:** fallback (cache, funcionalidade reduzida) quando dependências falham.
- **Isolamento (bulkheads):** pools separados por dependência/feature.
- **Testar restore/failover:** backup sem restore testado é “fé”.
- **Runbooks e automação:** incident response precisa ser ensaiado.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** multi-AZ, autoscaling, PDBs, readiness/liveness, rollout progressivo.
- **Pipelines CI/CD:** deploy com gates por métricas, rollback automatizado, migrations seguras.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** alertas acionáveis, tracing, dashboards.
- **Testes e Infra-as-Code:** DR drills automatizados, validação de backups, chaos engineering seletivo.

---

## Métricas, Monitoramento e Melhoria Contínua

- Disponibilidade e latência (p95/p99)
- Error budget burn rate
- MTTR/MTTD
- Change failure rate
- Frequência e resultado de DR drills (RTO/RPO real)

---

## Frameworks e Ferramentas do Mercado

- **Python:** tenacity (retries), opentelemetry
- **C#:** Polly (resiliência), OpenTelemetry
- **Go:** libs de retry/circuit breaker, OpenTelemetry
- **Infra/Observabilidade:** Kubernetes, Terraform, Prometheus/Grafana, Datadog, ELK

---

## Recursos Avançados e Leituras Recomendadas

- Google SRE (SLOs, error budget)
- _Release It!_ (Michael T. Nygard)
- _Designing Data-Intensive Applications_ (Kleppmann)

---

## FAQ Especialista

**HA é o mesmo que fault tolerance?**  
Não. HA mede “tempo no ar”. Fault tolerance é a capacidade de continuar operando apesar de falhas. Você pode ter HA com failover (recupera rápido) sem ser totalmente tolerante a falhas (sem impacto).

**Multi-região sempre vale a pena?**  
Não. É caro e complexo. Comece com multi-AZ, boas práticas de resiliência e DR bem testado. Suba para multi-região quando o risco/impacto justificar.

**Como evitar cascata em microserviços?**  
Timeouts, circuit breaker, bulkheads, rate limiting, backpressure e degradação graciosa por feature.

---

## Referências e Práticas do Mercado

- Google SRE
- DORA metrics
- ThoughtWorks Tech Radar

---

[Anterior](../cloud/security-best-practices.md) | [Índice](../../SUMMARY.md) | [Próximo](../tests/tdd.md)
