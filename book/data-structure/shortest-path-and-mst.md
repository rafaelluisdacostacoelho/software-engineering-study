[Anterior](graphs-representations-and-traversal.md) | [Índice](../../SUMMARY.md) | [Próximo](union-find-and-connectivity.md)

# Grafos — Caminhos Mínimos e MST (Dijkstra, Bellman-Ford, Prim, Kruskal)

## Visão Geral e Contexto de Mercado

Esses algoritmos aparecem em roteamento, custo mínimo, otimização de jobs, dependências e planejamento.
Saber escolher corretamente evita bugs clássicos (ex.: usar Dijkstra com arestas negativas).

---

## Fundamentos e Escolha do Algoritmo

- **BFS**: não ponderado (ou peso uniforme)
- **Dijkstra**: pesos não-negativos
- **Bellman-Ford**: permite pesos negativos; detecta ciclo negativo
- **Floyd-Warshall**: all-pairs em grafos menores ($O(V^3)$)
- **A\***: quando há heurística admissível

- **MST (Minimum Spanning Tree)** em grafo não-dirigido
	- **Kruskal**: ordena arestas + DSU
	- **Prim**: cresce usando heap

---

## Complexidades (referência rápida)

- Dijkstra (heap): $O((V+E)\log V)$
- Bellman-Ford: $O(VE)$
- Kruskal: $O(E\log E)$
- Prim (heap): $O((V+E)\log V)$

---

## Exemplos Avançados (Python, C# e Go)

### Python — Dijkstra (adjacency list)

```python
import heapq


def dijkstra(g: dict[int, list[tuple[int, int]]], src: int) -> dict[int, int]:
	INF = 10**18
	dist = {src: 0}
	pq: list[tuple[int, int]] = [(0, src)]

	while pq:
		d, u = heapq.heappop(pq)
		if d != dist.get(u, INF):
			continue
		for v, w in g.get(u, []):
			nd = d + w
			if nd < dist.get(v, INF):
				dist[v] = nd
				heapq.heappush(pq, (nd, v))
	return dist
```

### C# — Bellman-Ford (detecção de ciclo negativo)

```csharp
using System;
using System.Collections.Generic;

public static class BellmanFord
{
	public sealed record Edge(int U, int V, int W);

	public static (long[] dist, bool hasNegCycle) Run(int n, List<Edge> edges, int src)
	{
		const long INF = (long)1e18;
		var dist = new long[n];
		Array.Fill(dist, INF);
		dist[src] = 0;

		for (int i = 0; i < n - 1; i++)
		{
			bool changed = false;
			foreach (var e in edges)
			{
				if (dist[e.U] == INF) continue;
				long nd = dist[e.U] + e.W;
				if (nd < dist[e.V])
				{
					dist[e.V] = nd;
					changed = true;
				}
			}
			if (!changed) break;
		}

		foreach (var e in edges)
		{
			if (dist[e.U] == INF) continue;
			if (dist[e.U] + e.W < dist[e.V]) return (dist, true);
		}
		return (dist, false);
	}
}
```

### Go — Prim (MST) com heap

```go
import "container/heap"

type Edge struct{ To, W int }

type Item struct{ W, To int }

type MinHeap []Item

func (h MinHeap) Len() int            { return len(h) }
func (h MinHeap) Less(i, j int) bool  { return h[i].W < h[j].W }
func (h MinHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any)         { *h = append(*h, x.(Item)) }
func (h *MinHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func PrimMST(g map[int][]Edge, start int) int {
	seen := make(map[int]struct{})
	h := &MinHeap{}
	heap.Init(h)
	heap.Push(h, Item{W: 0, To: start})
	cost := 0

	for h.Len() > 0 {
		it := heap.Pop(h).(Item)
		if _, ok := seen[it.To]; ok {
			continue
		}
		seen[it.To] = struct{}{}
		cost += it.W
		for _, e := range g[it.To] {
			if _, ok := seen[e.To]; ok {
				continue
			}
			heap.Push(h, Item{W: e.W, To: e.To})
		}
	}
	return cost
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Dijkstra não serve com arestas negativas.
- Em grafos grandes, evite estruturas que duplicam memória (ex.: matriz).
- Em MST, garanta que o grafo é não-dirigido e (se necessário) conexo; caso contrário, você tem floresta.

[Anterior](graphs-representations-and-traversal.md) | [Índice](../../SUMMARY.md) | [Próximo](union-find-and-connectivity.md)
