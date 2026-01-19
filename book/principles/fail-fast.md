[Anterior](design-for-testability.md) | [Índice](../../SUMMARY.md) | [Próximo](yagni.md)

# Fail Fast — Falhar Cedo, Falhar Claro (Princípio Operacional)

## Visão Geral e Contexto de Mercado

Fail Fast significa detectar problemas o mais cedo possível e com mensagens claras. Em sistemas modernos, isso reduz MTTR e evita que erros se propaguem como corrupção de dados, efeitos colaterais irreversíveis ou incidentes difíceis.

No mercado, Fail Fast se traduz em:

- validação rigorosa de entrada (API/DTO)
- invariantes explícitas no domínio
- configuração validada no startup (não “descobrir em produção”)
- retries seletivos (não tentar eternamente em erro permanente)

Fail Fast não é “crash sempre”: é **falhar cedo no lugar certo**, com boa observabilidade e, quando necessário, degradação controlada.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Em ambientes com CI/CD e alta frequência de deploy, falhar cedo reduz custo de correção. A prática evoluiu para: validações automáticas, circuit breakers e “guardrails” operacionais.

- **Padrões e Protocolos Usados no Mercado**
	- **Guards/Preconditions:** validar invariantes no início.
	- **Typed errors:** distinguir erro de validação vs infra vs regra.
	- **Circuit breaker:** falhar rápido quando dependência está doente.
	- **Health checks:** readiness/liveness para falhar cedo no rollout.
	- **Schema validation:** contracts (OpenAPI/JSON schema).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Sem padronização de erros, cada time cria uma forma diferente de falhar e debugar vira caos.

- **Performance e Manutenção**  
	Validação excessiva em hot paths pode custar, mas geralmente é marginal comparado a rede/DB. O custo maior é manter mensagens e códigos de erro consistentes.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: “try/catch” genérico que esconde a causa.
	- Coverage: não testar invalidação/erros de config.
	- Flakiness: retries mal definidos causam “retry storms”.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Validar config no build/deploy (schemas + smoke tests).
	- Fail fast em migrações incompatíveis.
	- Alertas para erros de validação (sinal de client fora de contrato).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: invariantes e validações.
	- Integração: erros de dependências e timeouts.
	- E2E: fluxos com falhas simuladas.

- **Métrica de Qualidade**  
	- MTTR e tempo até detectar erro (TTD)
	- Taxa de erro por validação (4xx) vs infra (5xx)
	- Retries por request (sinal de instabilidade)

---

## Exemplos Avançados (Python, C# e Go)

### Python

```python
def create_user(email: str) -> None:
		if "@" not in email:
				raise ValueError("invalid email")
		# seguir fluxo normal
```

### C#

```csharp
public static void GuardPositive(int value, string name)
{
		if (value <= 0) throw new ArgumentOutOfRangeException(name, "must be > 0");
}
```

### Go

```go
package guard

import "fmt"

func Positive(value int, name string) error {
		if value <= 0 {
				return fmt.Errorf("%s must be > 0", name)
		}
		return nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Padronize erros: códigos, mensagens e correlação (trace_id).
- Valide config no startup e exponha readiness corretamente.
- Retry apenas para erros transitórios; use backoff e jitter.
- Evite “catch-all” que devolve `500` sem contexto.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** readiness falha rápido quando config/dependência não está ok.
- **Pipelines CI/CD:** smoke tests e validações de schema/config.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards por erro de validação vs infra.
- **Testes e Infra-as-Code:** simular falhas de dependência para validar circuit breaker.

---

## Métricas, Monitoramento e Melhoria Contínua

- TTD/MTTR
- Erros 4xx (client) vs 5xx (server)
- Retries por endpoint

---

## Frameworks e Ferramentas do Mercado

- OpenTelemetry
- Circuit breaker libs (Polly, etc.)
- Schema validation (OpenAPI)

---

## Recursos Avançados e Leituras Recomendadas

- Release It! (Michael Nygard)
- Resilience patterns: circuit breaker, bulkhead

---

## FAQ Especialista

**Fail Fast é incompatível com alta disponibilidade?**  
Não. Você pode falhar rápido e ainda assim degradar com fallback, desde que isso seja explícito e observável.

**Como evitar retry storm?**  
Retries seletivos, backoff+jitter, budgets e circuit breaker.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](design-for-testability.md) | [Índice](../../SUMMARY.md) | [Próximo](yagni.md)
