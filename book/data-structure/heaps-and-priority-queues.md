[Anterior](trees-and-bsts.md) | [Índice](../../SUMMARY.md) | [Próximo](tries-and-prefix-search.md)

# Heaps & Priority Queues — Top-K, Scheduling e Medianas

## Visão Geral e Contexto de Mercado

Heaps (priority queues) são essenciais quando você precisa repetidamente do **menor/maior elemento**:

- Scheduling de jobs e timeouts.
- Rate limiting e filas por prioridade.
- Top-k (ex.: “top 100 produtos”).
- Menor caminho (Dijkstra usa heap).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Heap binário**
	- Min-heap: pai <= filhos
	- Max-heap: pai >= filhos
	- `push/pop`: $O(\log n)$
	- `peek`: $O(1)$
	- `heapify`: $O(n)$

- **Trade-offs**
	- Heaps não mantêm ordenação total; são para “melhor elemento agora”.

---

## Algoritmos Essenciais

### 1) Top-K

- Mantenha um min-heap de tamanho $k$ para obter top-k maior.
- Complexidade: $O(n \log k)$

### 2) Mediana em streaming (two heaps)

- Max-heap para metade inferior, min-heap para metade superior.
- Rebalanceie tamanhos.
- Complexidade por inserção: $O(\log n)$

---

## Exemplos Avançados (Python, C# e Go)

### Python — top-k maior via heap tamanho k

```python
import heapq


def top_k_largest(nums: list[int], k: int) -> list[int]:
	if k <= 0:
		return []
	h: list[int] = []
	for x in nums:
		if len(h) < k:
			heapq.heappush(h, x)
		elif x > h[0]:
			heapq.heapreplace(h, x)
	return sorted(h, reverse=True)
```

### C# — `PriorityQueue<TElement, TPriority>` (net6+)

```csharp
using System;
using System.Collections.Generic;

public static class TopK
{
	public static List<int> Largest(int[] nums, int k)
	{
		var pq = new PriorityQueue<int, int>(); // element, priority (min)
		foreach (var x in nums)
		{
			if (pq.Count < k) pq.Enqueue(x, x);
			else if (pq.TryPeek(out _, out var min) && x > min)
			{
				pq.Dequeue();
				pq.Enqueue(x, x);
			}
		}
		var res = new List<int>(pq.Count);
		while (pq.Count > 0) res.Add(pq.Dequeue());
		res.Sort((a, b) => b.CompareTo(a));
		return res;
	}
}
```

### Go — heap interface

```go
import "container/heap"

type IntMinHeap []int

func (h IntMinHeap) Len() int            { return len(h) }
func (h IntMinHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h IntMinHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *IntMinHeap) Push(x any)         { *h = append(*h, x.(int)) }
func (h *IntMinHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func TopKLargest(nums []int, k int) []int {
	if k <= 0 {
		return []int{}
	}
	h := &IntMinHeap{}
	heap.Init(h)
	for _, x := range nums {
		if h.Len() < k {
			heap.Push(h, x)
			continue
		}
		if (*h)[0] < x {
			heap.Pop(h)
			heap.Push(h, x)
		}
	}
	out := make([]int, 0, h.Len())
	for h.Len() > 0 {
		out = append(out, heap.Pop(h).(int))
	}
	return out
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Em top-k, prefira heap de tamanho $k$ em vez de ordenar tudo.
- Cuidado com prioridades invertidas (min vs max).
- Em sistemas de jobs, tenha limites e observabilidade: fila por prioridade pode gerar starvation.

[Anterior](trees-and-bsts.md) | [Índice](../../SUMMARY.md) | [Próximo](tries-and-prefix-search.md)
