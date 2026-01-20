[Anterior](tries-and-prefix-search.md) | [Índice](../../SUMMARY.md) | [Próximo](shortest-path-and-mst.md)

# Grafos — Representação, BFS/DFS, Toposort e SCC

## Visão Geral e Contexto de Mercado

Grafos modelam relacionamentos: serviços e dependências, redes, recomendações, permissões, roteamento, DAGs de pipelines e workflows.
No mercado, o diferencial é:

- Representar bem (memória/custo) e escolher o algoritmo correto.
- Tratar escala (V/E grandes), concorrência e observabilidade.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Representação**
	- **Adjacency list**: $O(V+E)$ espaço, padrão para grafos esparsos.
	- **Adjacency matrix**: $O(V^2)$ espaço, útil para grafos densos pequenos.

- **Grafo dirigido vs não-dirigido**
- **Ponderado vs não-ponderado**

---

## Algoritmos Essenciais

### 1) BFS (Breadth-First Search)

- Menor número de arestas (grafo não ponderado)
- Camadas/níveis

**Complexidade:** $O(V+E)$

### 2) DFS (Depth-First Search)

- Detectar ciclos
- Componentes conexos
- Ordenação topológica (em DAG)

**Complexidade:** $O(V+E)$

### 3) Topological Sort (DAG)

- Kahn (fila + indegree)
- DFS (postorder)

**Complexidade:** $O(V+E)$

### 4) SCC (Strongly Connected Components)

- Kosaraju ou Tarjan

**Complexidade:** $O(V+E)$

---

## Principais Desafios no Uso Profissional

- **Recursão profunda** em DFS (stack overflow). Prefira DFS iterativa em grafos grandes.
- **Explosão de memória**: armazenar todo o grafo pode ser inviável; considere streaming/iteradores.
- **Dados sujos**: self-loops, múltiplas arestas, nós órfãos.

---

## Exemplos Avançados (Python, C# e Go)

### Python — topological sort (Kahn)

```python
from collections import defaultdict, deque


def topo_sort(nodes: list[str], edges: list[tuple[str, str]]) -> list[str]:
	# edge u->v significa u antes de v
	g: dict[str, list[str]] = defaultdict(list)
	indeg: dict[str, int] = {n: 0 for n in nodes}
	for u, v in edges:
		g[u].append(v)
		indeg[v] += 1

	q = deque([n for n in nodes if indeg[n] == 0])
	out: list[str] = []
	while q:
		u = q.popleft()
		out.append(u)
		for v in g[u]:
			indeg[v] -= 1
			if indeg[v] == 0:
				q.append(v)

	if len(out) != len(nodes):
		raise ValueError("graph has a cycle")
	return out
```

### C# — DFS iterativa (evita recursão)

```csharp
using System.Collections.Generic;

public static class GraphDfs
{
	public static List<int> DfsIterative(Dictionary<int, List<int>> g, int start)
	{
		var visited = new HashSet<int>();
		var stack = new Stack<int>();
		var order = new List<int>();

		stack.Push(start);
		while (stack.Count > 0)
		{
			var u = stack.Pop();
			if (!visited.Add(u)) continue;
			order.Add(u);
			if (!g.TryGetValue(u, out var neigh)) continue;
			for (int i = neigh.Count - 1; i >= 0; i--) stack.Push(neigh[i]);
		}
		return order;
	}
}
```

### Go — BFS em adjacency list

```go
func Bfs(g map[int][]int, start int) []int {
	q := make([]int, 0)
	head := 0
	seen := make(map[int]struct{})
	order := make([]int, 0)

	q = append(q, start)
	seen[start] = struct{}{}

	for head < len(q) {
		u := q[head]
		head++
		order = append(order, u)
		for _, v := range g[u] {
			if _, ok := seen[v]; ok {
				continue
			}
			seen[v] = struct{}{}
			q = append(q, v)
		}
	}
	return order
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Prefira adjacency list para grafos grandes e esparsos.
- Em toposort, se sobrar nó com indegree>0, você tem ciclo (bom para validação de DAG).
- Para grafos gigantes, pense em “computar sob demanda” e em reduzir cardinalidade (compressão de IDs).

---

## Integração na Arquitetura Real

- **DAG de pipelines**: toposort para ordem de execução.
- **Dependências entre serviços**: detectar ciclos e blast radius.
- **Permissões**: grafos dirigidos com herança/implicação.

[Anterior](tries-and-prefix-search.md) | [Índice](../../SUMMARY.md) | [Próximo](shortest-path-and-mst.md)
