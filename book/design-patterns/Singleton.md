[Anterior](Proxy.md) | [Índice](../../SUMMARY.md) | [Próximo](State.md)

# Singleton — Uma Instância por Processo (com Muitos Cuidados) (Padrão de Criação)

## Visão Geral e Contexto de Mercado

Singleton garante que exista uma única instância de um objeto e fornece um ponto global de acesso. Em ambientes profissionais, ele é frequentemente discutido como **padrão vs anti-pattern**, porque “global state” e dependências implícitas degradam testabilidade e evolutividade.

Ainda assim, o conceito aparece no mercado em formas controladas:

- **Infra compartilhada por processo:** pool de conexões, client HTTP configurado, cache local.
- **Objetos realmente únicos no processo:** registries, clock, config “read-only”.
- **Bibliotecas/frameworks:** loggers, metrics registries (idealmente injetáveis).

Em microserviços (Docker/Kubernetes), “único” significa “único por pod/processo”, não global no cluster.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF trouxe Singleton como solução para instâncias únicas. Com DI containers e composição explícita, o uso recomendado migrou para: “compor uma instância única no composition root e injetar”, evitando acesso global.

- **Padrões e Protocolos Usados no Mercado**
	- **Lazy initialization:** cria sob demanda.
	- **Thread-safe singleton:** sincronização correta (locks/`sync.Once`/`Lazy<T>`).
	- **Composition root:** instanciação única “fora” do domínio.
	- **Module singletons:** variáveis de módulo/estáticas com escopo bem definido.
	- **Test seams:** permitir substituição em testes (ou evitar Singleton).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Singleton cria dependência global: testes interferem entre si, estado vaza, ordem importa.

- **Performance e Manutenção**  
	- Inicialização preguiçosa pode ter bugs de concorrência.
	- Lifecycle é difícil: quando destruir? (quase nunca; vira vazamento)
	- “God singleton”: vira lugar para colocar utilitários e estado.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: acoplamento invisível (qualquer módulo pode acessar).
	- Coverage: difícil simular falhas (ex.: client HTTP) sem poder injetar.
	- Flakiness: estado compartilhado e testes paralelos.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Rodar testes em paralelo para expor vazamento de estado.
	- Regras de lint: restringir uso de singletons globais em camadas de domínio.
	- Instrumentação para detectar uso inesperado (ex.: singleton acessado antes de init).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: evite singleton; prefira injeção de dependência.
	- Integração: se houver singleton de infra (client), isole configuração e reset controlado.
	- E2E: não depende do padrão.

- **Métrica de Qualidade**  
	- Flaky rate em testes paralelos
	- Número de acessos globais (indicador de acoplamento)
	- Tempo de startup (singletons pesados)

---

## Exemplos Avançados (Python, C# e Go)

Exemplos thread-safe por processo (úteis para infra). Em código de domínio, prefira DI.

### Python

```python
from __future__ import annotations

import threading


_lock = threading.Lock()
_client = None


def get_http_client():
		global _client
		if _client is None:
				with _lock:
						if _client is None:
								_client = object()  # placeholder para um client real
		return _client
```

### C#

```csharp
public sealed class HttpClientSingleton
{
		public static Lazy<HttpClient> Instance { get; } = new(() =>
		{
				var client = new HttpClient();
				client.Timeout = TimeSpan.FromSeconds(5);
				return client;
		});
}
```

### Go

```go
package httpclient

import "sync"

var (
		once   sync.Once
		client any
)

func Get() any {
		once.Do(func() {
				client = struct{}{} // placeholder
		})
		return client
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Prefira DI/composição explícita** a acesso global.
- **Se usar, limite o escopo:** singleton de infra em pacote/módulo dedicado.
- **Evite estado mutável global.** Se houver cache, controle invalidação.
- **Garanta thread safety** e inicialização determinística.
- **Teste paralelamente** para detectar vazamento de estado.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** um singleton não é global no cluster; considere múltiplas réplicas e consistência.
- **Pipelines CI/CD:** testes paralelos e regras de lint para evitar global state no domínio.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** monitorar startup e efeitos colaterais de init.
- **Testes e Infra-as-Code:** singletons de infra precisam de config via env/secret e validação no startup.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de startup e inicialização
- Flaky rate em testes paralelos
- Incidentes por estado global/caches inconsistentes

---

## Frameworks e Ferramentas do Mercado

- **C#:** DI container, `Lazy<T>`, `IHttpClientFactory` (alternativa superior ao singleton de HttpClient)
- **Python:** injeção via funções/factories, containers leves (dependency-injector)
- **Go:** wiring manual, `sync.Once`

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Singleton
- Discussões modernas: DI e composition root como alternativa
- Guidelines de HttpClient (C#) e gestão de conexões

---

## FAQ Especialista

**Singleton é sempre anti-pattern?**  
Não. É um trade-off. Para infra compartilhada por processo (client/pool), pode ser pragmático. Para domínio, quase sempre piora testabilidade e acoplamento.

**Como ter “uma instância” sem Singleton?**  
Crie uma instância no composition root e injete onde precisa. Você ainda terá “uma instância”, mas sem dependência global.

**E em Kubernetes, singleton garante exclusividade?**  
Não. Você terá um por réplica/pod. Exclusividade global exige coordenação externa (lock distribuído, leader election).

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Proxy.md) | [Índice](../../SUMMARY.md) | [Próximo](State.md)
