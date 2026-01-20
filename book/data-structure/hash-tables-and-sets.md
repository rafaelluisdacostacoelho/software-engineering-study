[Anterior](stacks-and-queues.md) | [Índice](../../SUMMARY.md) | [Próximo](trees-and-bsts.md)

# Hash Tables & Sets — Lookup, Indexação e Caches (Nível Sênior)

## Visão Geral e Contexto de Mercado

Hash tables (map/dict) e sets são o “martelo” do lookup rápido. Em produção, eles aparecem em:

- Cache de resultados, feature flags, rate limiting.
- Deduplicação (idempotência) e detecção de repetição.
- Índices in-memory (por ID/chave) para reduzir roundtrips ao banco.

O diferencial é entender **limites e pior caso**, e projetar com **TTL/eviction**, concorrência e observabilidade.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Como funciona (alto nível)**
	- Função hash → bucket → resolução de colisão.
	- Colisões são inevitáveis; o design é “colidir pouco e resolver bem”.

- **Resolução de colisão**
	- **Chaining** (lista/estrutura por bucket): comum e simples.
	- **Open addressing** (linear/quadratic probing): evita ponteiros, mas sofre com clustering.

- **Load factor e rehash**
	Quando a tabela enche, ela precisa crescer e redistribuir (rehash), gerando custo amortizado.

- **Complexidade**
	- Lookup/insert/delete: $O(1)$ médio; $O(n)$ pior caso.
	- Espaço: geralmente maior que arrays por overhead.

---

## Principais Desafios no Uso Profissional

- **Crescimento infinito**: caches sem TTL/eviction viram vazamento lógico.
- **Hot keys**: chaves muito acessadas causam lock contention.
- **Hashing inconsistente**: bugs quando `equals/hashCode` (C#) não são coerentes.
- **Entradas adversas**: em cenários públicos, ataques de colisão podem degradar performance.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Cache com eviction**
	- LRU (recência) é um padrão comum.
	- LFU (frequência) é mais caro, mas útil para workloads específicas.
	- Sempre defina limites: tamanho máximo, TTL, e estratégia de remoção.

- **Consistent hashing (distribuição)**
	Quando você distribui chaves por shards/nós, consistent hashing reduz remapeamento quando nós entram/saem.

- **Bloom filter (pré-teste probabilístico)**
	- Útil para reduzir acessos caros (ex.: “provavelmente não existe”).
	- Tem falso positivo, mas não falso negativo.

---

## Exemplos Avançados (Python, C# e Go)

### Python — contagem por chave (map) + top-k (heap)

```python
from collections import Counter
import heapq


def top_k(words: list[str], k: int) -> list[tuple[int, str]]:
	cnt = Counter(words)
	return heapq.nlargest(k, ((c, w) for w, c in cnt.items()))
```

### C# — cuidado com hash/equality (record ajuda)

```csharp
public sealed record UserKey(string TenantId, string UserId);

// record já implementa equality/hashing estrutural corretamente.
// Use como chave em Dictionary/HashSet.
```

### Go — set via map

```go
type Void struct{}

func Dedup(ids []string) []string {
	seen := make(map[string]Void, len(ids))
	out := make([]string, 0, len(ids))
	for _, id := range ids {
		if _, ok := seen[id]; ok {
			continue
		}
		seen[id] = Void{}
		out = append(out, id)
	}
	return out
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Defina **limite** e **política de descarte** para qualquer map que cresce com tráfego.
- Monitore cardinalidade e distribuição de chaves (hot keys).
- Cuidado com concorrência: `Dictionary` (C#) não é thread-safe; use estruturas concorrentes ou locks.
- Em Go, `map` não é seguro para acesso concorrente sem sincronização.

---

## Integração na Arquitetura Real

- **Idempotência**: set/map para armazenar IDs já processados, com TTL (ex.: 24h).
- **Rate limiting**: contadores por chave + janela de tempo.
- **Caching**: combine TTL, tamanho máximo, métricas e fallback (stale-while-revalidate).

---

## FAQ Especialista

**Por que hash map pode ficar lento de repente?**  
Crescimento e rehash; aumento de colisões; hot keys e contenção; ou ataques de colisão.

**Quando preferir árvore ordenada (\log n) a hash (1 médio)?**  
Quando você precisa de ordenação, predecessor/sucessor, ou range queries por chave.

[Anterior](stacks-and-queues.md) | [Índice](../../SUMMARY.md) | [Próximo](trees-and-bsts.md)
