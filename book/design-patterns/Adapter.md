[Anterior](../domain/ddd.md) | [Índice](../../SUMMARY.md) | [Próximo](Bridge.md)

# Adapter — Integração Sem Acoplamento (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Adapter resolve um problema extremamente comum em sistemas reais: você precisa consumir/encapsular uma dependência externa (SDK, API HTTP, driver, biblioteca legada) cuja interface **não** se encaixa no que sua aplicação/domínio espera.

No mercado, Adapter aparece em:

- Integração com gateways de pagamento, provedores de SMS/e-mail, antifraude
- Encapsulamento de bibliotecas legadas
- Padronização de múltiplos provedores (multi-cloud, multi-PSP)
- Testabilidade: trocar implementação real por fake/in-memory em testes

A ideia sênior não é “criar classes a mais”: é **proteger o domínio** e evitar acoplamento direto com detalhes voláteis.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Adapter é um padrão clássico do GoF e continuou relevante porque integrações externas são inevitáveis. Em arquiteturas modernas (Hexagonal/Clean), o adapter frequentemente é “o lado de fora”: implementa uma porta (interface) do domínio.

- **Padrões e Protocolos Usados no Mercado**
	- **Ports & Adapters (Hexagonal):** o domínio define a porta; o adapter implementa.
	- **Anti-Corruption Layer (DDD):** adaptação para evitar “contaminar” o modelo interno.
	- **Facade vs Adapter:** facade simplifica uma API; adapter muda a forma para encaixar.
	- **DTO mapping:** traduzir payloads externos para tipos internos.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Sem adapter, testes tendem a depender de rede/SDK real e ficam lentos/instáveis. Com adapter, você consegue substituir por fake e testar o domínio com determinismo.

- **Performance e Manutenção**  
	Adapters podem introduzir overhead (serialização, mapeamento, retries) — mas o maior ganho é permitir evoluir sem “refactor em cascata” quando o provedor muda.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: criar adapters “finos” que vazam tipos externos para dentro.
	- Coverage: não testar erros comuns (timeout, 5xx, payload inválido).
	- Flakiness: não controlar retries/backoff em testes.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Contract tests (quando existir contrato formal) e testes de integração em job separado.
	- Feature flags para migração de provedor (rodar dois adapters em paralelo).
	- Observabilidade por adapter: taxa de erro, latência, timeouts.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: domínio chama a porta; fake adapter simula cenários.
	- Integração: adapter real contra sandbox/stub controlado.
	- E2E: poucos fluxos de negócio críticos.

- **Métrica de Qualidade**  
	- Taxa de sucesso por provedor/adapter
	- Latência p95/p99 por operação
	- Retries e timeouts
	- Incidentes por mudança de SDK/API

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: domínio depende de uma porta `Payments`, e o adapter traduz para um SDK externo.

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ChargeResult:
		id: str
		authorized: bool


class PaymentsPort:
		def charge(self, cents: int, token: str) -> ChargeResult:
				raise NotImplementedError


class StripeSdk:
		def create_charge(self, amount_cents: int, card_token: str) -> dict:
				return {"id": "ch_123", "status": "authorized"}


class StripePaymentsAdapter(PaymentsPort):
		def __init__(self, sdk: StripeSdk):
				self._sdk = sdk

		def charge(self, cents: int, token: str) -> ChargeResult:
				raw = self._sdk.create_charge(amount_cents=cents, card_token=token)
				return ChargeResult(id=raw["id"], authorized=(raw["status"] == "authorized"))
```

### C#

```csharp
public sealed record ChargeResult(string Id, bool Authorized);

public interface IPaymentsPort
{
		ChargeResult Charge(int cents, string token);
}

public sealed class ExternalSdk
{
		public (string id, string status) CreateCharge(int amountCents, string cardToken)
				=> ("ch_123", "authorized");
}

public sealed class SdkPaymentsAdapter : IPaymentsPort
{
		private readonly ExternalSdk _sdk;
		public SdkPaymentsAdapter(ExternalSdk sdk) => _sdk = sdk;

		public ChargeResult Charge(int cents, string token)
		{
				var (id, status) = _sdk.CreateCharge(cents, token);
				return new ChargeResult(id, status == "authorized");
		}
}
```

### Go

```go
package payments

type ChargeResult struct {
		ID         string
		Authorized bool
}

type PaymentsPort interface {
		Charge(cents int, token string) (ChargeResult, error)
}

type ExternalSDK interface {
		CreateCharge(amountCents int, cardToken string) (id string, status string, err error)
}

type Adapter struct{ sdk ExternalSDK }

func (a Adapter) Charge(cents int, token string) (ChargeResult, error) {
		id, status, err := a.sdk.CreateCharge(cents, token)
		if err != nil {
				return ChargeResult{}, err
		}
		return ChargeResult{ID: id, Authorized: status == "authorized"}, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Não vaze tipos externos para o domínio:** traduza para tipos internos.
- **Nomeie portas pelo domínio** (ex.: `PaymentsPort`, `NotificationsPort`).
- **Erros com semântica:** mapeie erros do SDK para erros úteis no domínio (timeout, inválido, indisponível).
- **Instrumente o adapter:** métricas e tracing por operação.
- **Evite “adapter pass-through” demais:** se ele só repassa chamadas, talvez a abstração não esteja ajudando.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** configure timeouts, retries e circuit breakers no cliente/mesh com cuidado.
- **Pipelines CI/CD:** testes contra sandbox; e2e mínimo; deploy progressivo ao trocar provedores.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards por adapter; alertas de taxa de erro.
- **Testes e Infra-as-Code:** stubs/sandboxes provisionados; secrets via vault.

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência p95/p99 por operação
- Taxa de erro por tipo (timeout/5xx/4xx)
- Retries e circuit breaker opens
- Disponibilidade do provedor externo

---

## Frameworks e Ferramentas do Mercado

- **Observabilidade:** OpenTelemetry
- **Resiliência:** timeouts/retry/backoff; circuit breaker (bibliotecas por linguagem)
- **Testes:** pact/contract tests quando aplicável; sandboxes dos provedores

---

## Recursos Avançados e Leituras Recomendadas

- Ports & Adapters (Hexagonal)
- DDD — Anti-Corruption Layer
- Documentação de provedores (sandboxes e guidelines de retry)

---

## FAQ Especialista

**Adapter e Facade são a mesma coisa?**  
Não. Facade simplifica uma API; Adapter converte uma interface em outra esperada.

**Quando não vale criar um adapter?**  
Quando a dependência é estável e usada em um único ponto, e a abstração só adicionaria indireção sem benefícios de teste/migração.

**Como migrar de um provedor para outro?**  
Defina uma porta estável, implemente dois adapters, faça shadow/canary, compare métricas e corte gradualmente.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](../domain/ddd.md) | [Índice](../../SUMMARY.md) | [Próximo](Bridge.md)
