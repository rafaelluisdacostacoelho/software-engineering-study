[Anterior](Adapter.md) | [Índice](../../SUMMARY.md) | [Próximo](Builder.md)

# Bridge — Separar Abstração de Implementação (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Bridge separa uma **abstração** (o que o cliente quer fazer) de uma **implementação** (como isso é feito) para que ambas possam evoluir independentemente.

No mercado, Bridge aparece quando você tem duas dimensões que variam e que, se combinadas via herança/ifs, explodem em combinações (produto cartesiano), por exemplo:

- Tipos de “notificação” (e-mail, SMS, push) × provedores (Twilio, SNS, SendGrid)
- Formas de “renderização” (HTML, PDF) × engines (wkhtmltopdf, Playwright, serviço externo)
- UI widgets × temas/skins, ou plataformas (desktop/mobile)

Bridge ajuda a manter o código testável e evitar “classes para cada combinação”.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	O padrão é do GoF, mas sua motivação continua atual: reduzir acoplamento entre duas hierarquias que mudam por razões diferentes. Em arquiteturas modernas, Bridge frequentemente aparece como composição + interfaces (DIP).

- **Padrões e Protocolos Usados no Mercado**
	- **Composição sobre herança:** a abstração contém um implementador.
	- **DIP/Interfaces:** cliente depende da abstração, não do detalhe.
	- **Strategy vs Bridge:** ambos usam composição; Strategy muda algoritmo; Bridge separa dimensões de abstração/implementação.
	- **Adapter/Facade podem coexistir:** adapter para integrar um SDK; bridge para separar dimensões de variação.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O desafio é manter o “implementor” substituível e com contratos claros. Sem isso, a abstração começa a depender de detalhes específicos.

- **Performance e Manutenção**  
	A indireção pode confundir se não houver naming claro. O ganho é reduzir churn em classes e permitir extensões sem refatorações amplas.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: criar camadas demais sem variação real.
	- Coverage: não testar combinações importantes ou falhas dos implementadores.
	- Flakiness: testes que dependem de implementações externas sem stubs.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Suites de teste por implementador + smoke tests nas abstrações críticas.
	- Canary ao trocar implementadores (provedor A → B).
	- Observabilidade por implementador para comparar SLO/custo.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: abstração testada com fake implementor.
	- Integração: implementor real contra sandbox.
	- E2E: poucos fluxos relevantes de negócio.

- **Métrica de Qualidade**  
	- Complexidade (redução de classes combinatórias)
	- Latência/erro por implementador
	- Tempo para adicionar uma nova variação (extensibilidade)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: abstração “Notifier” varia por tipo; implementor varia por provedor.

### Python

```python
from dataclasses import dataclass


class Provider:
		def send(self, to: str, body: str) -> None:
				raise NotImplementedError


@dataclass
class Notifier:
		provider: Provider

		def notify(self, to: str, message: str) -> None:
				self.provider.send(to, message)


class SmsProvider(Provider):
		def send(self, to: str, body: str) -> None:
				# chamar SDK externo
				pass
```

### C#

```csharp
public interface IProvider { void Send(string to, string body); }

public sealed class Notifier
{
		private readonly IProvider _provider;
		public Notifier(IProvider provider) => _provider = provider;
		public void Notify(string to, string message) => _provider.Send(to, message);
}
```

### Go

```go
package bridge

type Provider interface {
		Send(to string, body string) error
}

type Notifier struct{ Provider Provider }

func (n Notifier) Notify(to, msg string) error {
		return n.Provider.Send(to, msg)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Use Bridge quando existirem dimensões reais de variação.**
- **Nomeie bem abstração e implementor:** o padrão fica invisível se o naming for ruim.
- **Teste a abstração com fake implementor** (rápido e determinístico).
- **Instrumente implementadores**: latência/erro/custo.
- **Evite “herança disfarçada” via downcasts:** se você precisa de `if (provider is X)`, a separação falhou.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** políticas de retry/timeout podem variar por implementador; padronize.
- **Pipelines CI/CD:** deploy progressivo ao trocar implementor; contract tests se existirem.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards por implementor.
- **Testes e Infra-as-Code:** sandboxes e secrets por provedor.

---

## Métricas, Monitoramento e Melhoria Contínua

- Erros/latência por implementor
- Tempo para adicionar uma nova variação
- Incidentes por acoplamento indevido (refactor em cascata)

---

## Frameworks e Ferramentas do Mercado

- OpenTelemetry (tracing/metrics)
- Bibliotecas de resiliência (retry/timeout/circuit breaker)
- Contract testing (quando aplicável)

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Bridge
- DIP e composição sobre herança

---

## FAQ Especialista

**Bridge não é só Strategy?**  
Eles se parecem (composição), mas Bridge foca em separar duas hierarquias/dimensões de variação; Strategy foca em trocar algoritmo/política.

**Quando Bridge vira overengineering?**  
Quando você só tem uma implementação e não há perspectiva real de variação, ou quando uma interface passa a ser “pass-through” sem valor.

**Posso usar com Adapter?**  
Sim. Adapter integra um SDK específico; Bridge permite trocar implementadores/provedores sob a mesma abstração.

---

[Anterior](Adapter.md) | [Índice](../../SUMMARY.md) | [Próximo](Builder.md)
