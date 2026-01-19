[Anterior](observer.md) | [Índice](../../SUMMARY.md) | [Próximo](singleton.md)

# Proxy — Controlar Acesso a um Objeto (Cache, Segurança, Remoto) (Padrão Estrutural)

## Visão Geral e Contexto de Mercado

Proxy é um objeto que implementa a mesma interface do “real subject” e controla o acesso a ele. Ele pode:

- atrasar criação (*virtual proxy* / lazy)
- proteger acesso (*protection proxy*)
- representar um objeto remoto (*remote proxy*)
- adicionar cache (*caching proxy*)
- registrar/auditar (*logging proxy*)

No mercado, proxies aparecem como wrappers de clients (HTTP/DB), ORMs com lazy-loading, SDKs, interceptors e mecanismos AOP.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Proxy é GoF clássico e hoje aparece fortemente em infra (clients e gateways). Em C#, por exemplo, interceptors e `DispatchProxy` são formas comuns de proxy dinâmico.

- **Padrões e Protocolos Usados no Mercado**
	- **Virtual Proxy:** cria o objeto real sob demanda.
	- **Remote Proxy:** traduz chamadas locais em chamadas remotas.
	- **Protection Proxy:** checa autorização.
	- **Caching Proxy:** memoiza resultados com invalidação.
	- **Observabilidade proxy:** tracing/logs/metrics.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Proxies precisam ser testados como “mesma interface, mesma semântica”. Testes devem cobrir:
	- cache hits/misses
	- comportamento em erro do real subject
	- concorrência (cache stampede)

- **Performance e Manutenção**  
	- Proxy pode mascarar latência remota (parece local, mas não é).
	- Cache incorreto causa bugs difíceis (stale data, invalidação errada).
	- Proxies empilhados (proxy sobre proxy) complicam debug.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: proxies que misturam muitas responsabilidades.
	- Coverage: não testar cenários de concorrência e TTL.
	- Flakiness: testes com tempo real/TTL sem controle determinístico.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes de contrato para garantir compatibilidade com a interface.
	- Benchmarks para medir overhead de proxy (principalmente logging/tracing).
	- Testes determinísticos para TTL (clock fake).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: proxy com real subject fake.
	- Integração: proxy com dependência real (ex.: Redis) para validar comportamento.
	- E2E: fluxos críticos onde caching/remote proxy muda SLA.

- **Métrica de Qualidade**  
	- Cache hit rate e latência p95/p99
	- Taxa de erros do real subject vs erros do proxy
	- Concurrency issues (stampede, lock contention)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: proxy de cache para um repositório.

### Python

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class UserRepo(Protocol):
		def get_user(self, user_id: str) -> dict: ...


@dataclass
class CachedUserRepo:
		inner: UserRepo
		cache: dict[str, dict]

		def get_user(self, user_id: str) -> dict:
				if user_id in self.cache:
						return self.cache[user_id]
				user = self.inner.get_user(user_id)
				self.cache[user_id] = user
				return user
```

### C#

```csharp
public interface IUserRepo
{
		Task<User> GetUser(string userId, CancellationToken ct);
}

public sealed class CachedUserRepo : IUserRepo
{
		private readonly IUserRepo _inner;
		private readonly IMemoryCache _cache;

		public CachedUserRepo(IUserRepo inner, IMemoryCache cache)
				=> (_inner, _cache) = (inner, cache);

		public Task<User> GetUser(string userId, CancellationToken ct)
				=> _cache.GetOrCreateAsync(userId, _ => _inner.GetUser(userId, ct))!;
}
```

### Go

```go
package users

import "sync"

type Repo interface{ GetUser(userID string) (User, error) }

type CachedRepo struct {
		inner Repo
		mu    sync.RWMutex
		cache map[string]User
}

func NewCachedRepo(inner Repo) *CachedRepo {
		return &CachedRepo{inner: inner, cache: map[string]User{}}
}

func (c *CachedRepo) GetUser(userID string) (User, error) {
		c.mu.RLock()
		if u, ok := c.cache[userID]; ok {
				c.mu.RUnlock()
				return u, nil
		}
		c.mu.RUnlock()

		u, err := c.inner.GetUser(userID)
		if err != nil {
				return User{}, err
		}
		c.mu.Lock()
		c.cache[userID] = u
		c.mu.Unlock()
		return u, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Nomeie claramente:** `CachedX`, `AuthorizedX`, `RemoteX` — o caller precisa saber o que está usando.
- **Se for cache, trate invalidação e concorrência** (stampede) — simples “map” pode não bastar.
- **Não mascare latência remota:** tenha timeouts, retries e métricas explícitas.
- **Evite múltiplas responsabilidades por proxy.** Prefira compor proxies (Decorator) quando fizer sentido.
- **Cuidado com transparência excessiva:** proxies “mágicos” dificultam debug.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** proxies de cache precisam de limites e políticas (TTL, tamanho) para não estourar memória.
- **Pipelines CI/CD:** testes determinísticos para TTL, concorrência e compatibilidade de interface.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards de hit rate/latência e alertas para degradação.
- **Testes e Infra-as-Code:** para proxies remotos/caches distribuídos, testes com ambiente efêmero (Redis) e caos (latência).

---

## Métricas, Monitoramento e Melhoria Contínua

- Cache hit/miss e latência por operação
- Taxa de timeouts/retries (se proxy remoto)
- Tamanho do cache e evictions
- Erros por categoria (inner vs proxy)

---

## Frameworks e Ferramentas do Mercado

- **C#:** `DispatchProxy`, `DelegatingHandler`, Polly
- **Python:** wrappers + tenacity, clients httpx/requests
- **Go:** interfaces + wrappers, `net/http` RoundTripper
- **Caches:** Redis, Memcached, in-memory caches

---

## Recursos Avançados e Leituras Recomendadas

- GoF — Proxy
- Caching strategies e cache invalidation
- Patterns de resiliência (timeouts, retries, circuit breaker)

---

## FAQ Especialista

**Proxy vs Decorator: qual a diferença prática?**  
Decorator adiciona responsabilidades mantendo interface e intenção de “enriquecer” o objeto. Proxy controla acesso (lazy, remoto, proteção, cache). Na implementação podem ser parecidos, mas a intenção e os trade-offs são diferentes.

**Quando cache em proxy vira risco alto?**  
Quando consistência é crítica e invalidação é difícil. Em cenários assim, prefira caches com contratos claros (TTL curto, versionamento, write-through) e observabilidade forte.

**Como evitar cache stampede?**  
Use locks por chave, singleflight, ou caches que suportam “request coalescing”, além de jitter em TTL.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](observer.md) | [Índice](../../SUMMARY.md) | [Próximo](singleton.md)
