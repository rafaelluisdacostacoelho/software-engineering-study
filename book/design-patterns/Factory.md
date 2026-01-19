[Anterior](Facade.md) | [Índice](../../SUMMARY.md) | [Próximo](Observer.md)

# Factory — Centralizar Criação e Selecionar Implementações (Padrão de Criação)

## Visão Geral e Contexto de Mercado

Factory (no sentido amplo) organiza a criação de objetos para:

- esconder detalhes de instanciação
- aplicar regras de seleção (qual implementação usar)
- padronizar configuração (timeouts, credenciais, endpoints)
- facilitar testes (substituir implementações)

Em sistemas profissionais, “Factory” aparece tanto como:

- **Simple Factory:** função/classe que cria implementações.
- **Factory Method:** subclasses definem qual produto criar.
- **Abstract Factory:** cria famílias de objetos relacionados.

O principal valor de mercado é **manter o código do domínio/aplicação livre de detalhes de infraestrutura** e evitar criação “espalhada” que gera inconsistência e bugs.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	GoF introduziu Factory Method e Abstract Factory para reduzir acoplamento a classes concretas. Hoje, DI containers e configuração (12-factor apps) resolveram parte do problema, mas factories continuam úteis quando existe lógica de seleção/configuração (ex.: multi-tenant, multi-cloud, fallback).

- **Padrões e Protocolos Usados no Mercado**
	- **Config-driven creation:** escolher implementação por config/feature flag.
	- **Registry + map:** registrar implementações por chave (cuidado com “stringly-typed”).
	- **Dependency Injection:** factory como composição no “composition root”.
	- **Builder vs Factory:** builder constrói passo a passo; factory instancia de uma vez.
	- **Abstract Factory:** famílias coerentes (ex.: storage + cache + locks do mesmo vendor).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Factories não podem virar um “switch gigante” sem testes. É comum quebrar produção ao introduzir uma implementação nova sem testes de contrato.

- **Performance e Manutenção**  
	- Inicialização cara (clients, pools) precisa ser cacheada/reutilizada.
	- Factories que criam recursos por request causam vazamento e latência.
	- Lógica de seleção complexa vira dívida (“se region=X e tier=Y e flag=Z…”).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: factory com dependências globais/estado oculto.
	- Coverage: não testar matriz de seleção (todas as combinações críticas).
	- Flakiness: testes que dependem de env vars mutáveis e ordem de execução.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de contrato por interface (mesmo comportamento mínimo garantido).
	- Matriz de build/test por “provider” (ex.: `redis`, `memory`).
	- Deploy gradual para novas implementações (canary/flag).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: factory retorna a implementação correta para configs.
	- Integração: cada implementação em ambiente efêmero (containers).
	- E2E: fluxos críticos para validar seleção e comportamento.

- **Métrica de Qualidade**  
	- Tempo de inicialização e número de instâncias criadas
	- Incidentes por seleção errada de provider
	- Cobertura da matriz de seleção

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: escolher um cache provider por configuração (in-memory vs Redis).

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Cache(Protocol):
		def get(self, key: str) -> str | None: ...
		def set(self, key: str, value: str) -> None: ...


@dataclass
class MemoryCache:
		_data: dict[str, str]

		def get(self, key: str) -> str | None:
				return self._data.get(key)

		def set(self, key: str, value: str) -> None:
				self._data[key] = value


def cache_factory(provider: str) -> Cache:
		if provider == "memory":
				return MemoryCache(_data={})
		if provider == "redis":
				# placeholder: return RedisCache(...)
				raise NotImplementedError("redis not wired")
		raise ValueError(f"unknown provider: {provider}")
```

### C#

```csharp
public interface ICache
{
		string? Get(string key);
		void Set(string key, string value);
}

public sealed class MemoryCache : ICache
{
		private readonly Dictionary<string, string> _data = new();
		public string? Get(string key) => _data.TryGetValue(key, out var v) ? v : null;
		public void Set(string key, string value) => _data[key] = value;
}

public static class CacheFactory
{
		public static ICache Create(string provider)
				=> provider switch
				{
						"memory" => new MemoryCache(),
						// "redis" => new RedisCache(...)
						_ => throw new ArgumentException($"unknown provider: {provider}")
				};
}
```

### Go

```go
package cache

import "fmt"

type Cache interface {
		Get(key string) (string, bool)
		Set(key, value string)
}

type Memory struct{ data map[string]string }

func NewMemory() *Memory { return &Memory{data: map[string]string{}} }
func (m *Memory) Get(key string) (string, bool) { v, ok := m.data[key]; return v, ok }
func (m *Memory) Set(key, value string)         { m.data[key] = value }

func Factory(provider string) (Cache, error) {
		switch provider {
		case "memory":
				return NewMemory(), nil
		case "redis":
				return nil, fmt.Errorf("redis not wired")
		default:
				return nil, fmt.Errorf("unknown provider: %s", provider)
		}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Prefira compor no “composition root”.** Factory demais dentro do domínio indica acoplamento.
- **Cacheie/reutilize recursos caros** (clients, pools). Não crie por request.
- **Evite stringly-typed registries** sem validação; prefira enums/consts e validação de config.
- **Teste a matriz de seleção** e o contrato mínimo da interface.
- **Não esconda falhas de configuração:** falhe rápido com mensagens claras.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** factories frequentemente leem config/env; valide e exponha readiness quando dependências não estão prontas.
- **Pipelines CI/CD:** testes por provider; flags/canary para novas implementações.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** monitorar seleção por provider e taxas de erro específicas.
- **Testes e Infra-as-Code:** provisionar dependências de integração (Redis) em ambientes efêmeros.

---

## Métricas, Monitoramento e Melhoria Contínua

- Número de instâncias criadas por tipo
- Tempo de inicialização de clients
- Incidentes por configuração inválida
- Distribuição real de uso por provider

---

## Frameworks e Ferramentas do Mercado

- **DI/Composition:** containers de DI (C#), wiring manual (Go), frameworks leves (Python)
- **Config:** 12-factor; validação de config e schemas

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Factory Method, Abstract Factory
- Patterns de DI e composition root

---

## FAQ Especialista

**Factory e DI container competem?**  
Não. Muitas vezes o container usa factories ou “provider functions”. Use DI para composição e factory quando existir lógica de seleção/configuração relevante.

**Quando Abstract Factory faz sentido?**  
Quando você precisa trocar famílias inteiras de implementações de forma coerente (ex.: “AWS vs GCP” para storage + queue + locks), mantendo compatibilidade de interfaces.

**Como evitar factory virar switch infinito?**  
Use registry tipado, módulos por provider, e testes de contrato por implementação. Quando crescer demais, avalie plugins/strategies.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](Facade.md) | [Índice](../../SUMMARY.md) | [Próximo](Observer.md)
