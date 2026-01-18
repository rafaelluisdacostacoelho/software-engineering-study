[Anterior](../events-and-queues/distributed-consistency.md) | [Índice](../../SUMMARY.md) | [Próximo](event-driven-architecture.md)

# Caching Strategies — Práticas Avançadas e Impacto em Performance

## Visão Geral e Contexto de Mercado

Cache é uma das alavancas mais eficazes para melhorar latência e reduzir carga em recursos caros (banco, APIs externas). Em sistemas modernos (cloud, microserviços, CI/CD), caching não é só “colocar Redis”: envolve escolhas conscientes de **consistência**, **invalidação**, **observabilidade** e **custo**.

Na prática do mercado, cache é usado para:

- Atingir SLO de latência (p95/p99)
- Reduzir custo (menos queries/egress)
- Proteger dependências (rate limiting indireto)
- Suportar picos (burst)

Mas o trade-off central permanece: **cache é uma forma de inconsistência controlada**. Sem estratégia, ele vira fonte de bugs difíceis (“stale reads”, invalidação incompleta).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	De caches locais em memória, o mercado evoluiu para caches distribuídos (Redis/Memcached), CDNs (edge) e caches no cliente/SDK. Em sistemas distribuídos, surgiram padrões para evitar thundering herd, cache stampede e inconsistência.

- **Padrões e Protocolos Usados no Mercado**
	- **Cache-aside (lazy loading):** app lê do cache, busca no origin se miss e popula.
	- **Read-through/Write-through:** cache gerencia leitura/escrita com origem.
	- **Write-back:** escrita no cache e persistência assíncrona (alto risco; use com cuidado).
	- **TTL + jitter:** expiração com distribuição para evitar “stampede”.
	- **Stale-While-Revalidate:** serve stale e revalida em background.
	- **Negative caching:** cache de “não encontrado” com TTL curto.
	- **Single-flight / request coalescing:** um fetch por chave, outros aguardam.
	- **CDN caching:** cache de conteúdo estático/semidinâmico com headers.
	- **Invalidação por evento:** outbox/eventos para remover/atualizar chaves.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Cache introduz estados e timing (TTL) que complicam testes. É comum precisar de testes de integração e simulações de expiração/concorrência.

- **Performance e Manutenção**  
	- **Cache stampede:** muitos misses simultâneos derrubam o origin.
	- **Hot keys:** uma chave muito acessada vira gargalo.
	- **Cardinalidade alta:** cache cresce e custo explode.
	- **Invalidação:** “o problema dos dois hard things” (invalidar e nomear).

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: TTL arbitrário sem SLO/medição; chaves sem namespace; ausência de limites.
	- Coverage: não testar stale/invalidação/retry.
	- Flakiness: testes dependentes de tempo real (sleep) em vez de clock controlado.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Testes para comportamento de cache (miss/hit/stale) sem depender de tempo real.
	- Observabilidade como gate: alertas de hit ratio, latência e erros do cache.
	- Rollout gradual quando mudar estratégia (TTL, keys, compressão).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: lógica de composição de chaves e política (TTL/jitter).
	- Integração: Redis real (testcontainers) para validar comportamento.
	- E2E: validar SLO e degradação sob falhas do cache.

- **Métrica de Qualidade**  
	- Cache hit ratio (global e por endpoint/chave)
	- Latência p95/p99 com e sem cache
	- Taxa de erros do cache (timeouts, evictions)
	- Volume de evictions e memória usada
	- QPS no origin (deve cair com cache saudável)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo de cache-aside com “single-flight” (coalescing) conceitual.

### Python

```python
import time
from collections import defaultdict
from threading import Lock


class SimpleCache:
		def __init__(self):
				self._data = {}

		def get(self, key: str):
				item = self._data.get(key)
				if not item:
						return None
				value, expires_at = item
				if time.time() >= expires_at:
						return None
				return value

		def set(self, key: str, value, ttl_seconds: int) -> None:
				self._data[key] = (value, time.time() + ttl_seconds)


_locks = defaultdict(Lock)


def get_user(cache: SimpleCache, user_id: str, loader):
		key = f"user:{user_id}"
		v = cache.get(key)
		if v is not None:
				return v
		with _locks[key]:
				v = cache.get(key)
				if v is not None:
						return v
				v = loader(user_id)
				cache.set(key, v, ttl_seconds=60)
				return v
```

### C#

```csharp
using System.Collections.Concurrent;

public sealed class SingleFlight
{
		private readonly ConcurrentDictionary<string, object> _locks = new();

		public T Do<T>(string key, Func<T> loader)
		{
				var gate = _locks.GetOrAdd(key, _ => new object());
				lock (gate)
				{
						return loader();
				}
		}
}
```

### Go

```go
package cache

import "golang.org/x/sync/singleflight"

var g singleflight.Group

func Load(key string, loader func() (any, error)) (any, error) {
		v, err, _ := g.Do(key, loader)
		return v, err
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Defina keys com namespace** (`user:{id}`, `product:{id}`) e versionamento (`v2:`) para migrações.
- **TTL com jitter** para reduzir stampede.
- **Planeje invalidação:** eventos/outbox, ou TTL curto com revalidação.
- **Cache de erro com cuidado:** negative caching com TTL pequeno.
- **Evite cache em dados críticos sem estratégia:** dados financeiros/estado de pagamento exigem desenho específico.
- **Tenha fallback:** cache down não pode derrubar o sistema (use degradação).

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** limites de memória, eviction policy, readiness do cache, timeouts.
- **Pipelines CI/CD:** validações de compatibilidade de keys, testes de integração com Redis.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** dashboards de hit ratio, latência e evictions.
- **Testes e Infra-as-Code:** provisionamento de Redis/Memcached/CDN, políticas de retenção.

---

## Métricas, Monitoramento e Melhoria Contínua

- Hit ratio (por endpoint e por chave)
- Latência p95/p99
- QPS no origin
- Evictions/memória
- Erros/timeouts no cache

---

## Frameworks e Ferramentas do Mercado

- **Python:** redis-py, cachetools
- **C#:** IMemoryCache/IDistributedCache, StackExchange.Redis
- **Go:** go-redis, ristretto
- **Infra:** Redis/Memcached, CloudFront/Akamai/Cloud CDN

---

## Recursos Avançados e Leituras Recomendadas

- _Caching at Scale_ (posts de engenharia de grandes empresas)
- Martin Fowler (cache patterns)
- Documentação Redis (eviction, replication)

---

## FAQ Especialista

**Qual é a melhor estratégia: TTL ou invalidação?**  
Depende. TTL é simples e robusto, mas pode servir stale. Invalidação é mais precisa, mas mais complexa. Muitas empresas combinam TTL curto + invalidação por eventos.

**Como evitar cache stampede?**  
Single-flight/coalescing, TTL com jitter, stale-while-revalidate e warming em deploy.

**Cache distribuído substitui banco?**  
Não. Cache é otimização; o origin continua sendo fonte de verdade (ou um modelo de leitura materializado em CQRS).

---

## Referências e Práticas do Mercado

- Redis docs
- AWS/Azure/GCP caching guidance
- ThoughtWorks Tech Radar

---

[Anterior](../events-and-queues/distributed-consistency.md) | [Índice](../../SUMMARY.md) | [Próximo](event-driven-architecture.md)
