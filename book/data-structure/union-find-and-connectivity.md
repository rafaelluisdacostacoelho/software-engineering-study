[Anterior](shortest-path-and-mst.md) | [Índice](../../SUMMARY.md) | [Próximo](range-queries-fenwick-and-segment-tree.md)

# Union-Find (DSU) — Conectividade Dinâmica e Kruskal

## Visão Geral e Contexto de Mercado

Union-Find (Disjoint Set Union / DSU) é a estrutura padrão para:

- Conectividade em grafos (componentes) sob operações de união.
- Kruskal (MST) e problemas de clustering.
- Detecção de ciclos em grafo não-dirigido.

O valor está em oferecer operações quase $O(1)$ amortizado com path compression + union by rank/size.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Operações**
	- `find(x)`: retorna representante do conjunto
	- `union(a,b)`: une conjuntos

- **Otimizações**
	- **Path compression**: achata a árvore durante `find`
	- **Union by rank/size**: conecta árvore menor na maior

- **Complexidade**
	Amortizado: $O(\alpha(n))$ (Ackermann inversa), praticamente constante.

---

## Exemplos Avançados (Python, C# e Go)

### Python — DSU com size

```python
class DSU:
	def __init__(self, n: int) -> None:
		self.parent = list(range(n))
		self.size = [1] * n

	def find(self, x: int) -> int:
		while self.parent[x] != x:
			self.parent[x] = self.parent[self.parent[x]]
			x = self.parent[x]
		return x

	def union(self, a: int, b: int) -> bool:
		ra, rb = self.find(a), self.find(b)
		if ra == rb:
			return False
		if self.size[ra] < self.size[rb]:
			ra, rb = rb, ra
		self.parent[rb] = ra
		self.size[ra] += self.size[rb]
		return True
```

### C# — DSU clássico

```csharp
public sealed class Dsu
{
	private readonly int[] _parent;
	private readonly int[] _size;

	public Dsu(int n)
	{
		_parent = new int[n];
		_size = new int[n];
		for (int i = 0; i < n; i++) { _parent[i] = i; _size[i] = 1; }
	}

	public int Find(int x)
	{
		while (_parent[x] != x)
		{
			_parent[x] = _parent[_parent[x]];
			x = _parent[x];
		}
		return x;
	}

	public bool Union(int a, int b)
	{
		int ra = Find(a), rb = Find(b);
		if (ra == rb) return false;
		if (_size[ra] < _size[rb]) (ra, rb) = (rb, ra);
		_parent[rb] = ra;
		_size[ra] += _size[rb];
		return true;
	}
}
```

### Go — DSU

```go
type DSU struct {
	parent []int
	size   []int
}

func NewDSU(n int) *DSU {
	p := make([]int, n)
	s := make([]int, n)
	for i := 0; i < n; i++ {
		p[i] = i
		s[i] = 1
	}
	return &DSU{parent: p, size: s}
}

func (d *DSU) Find(x int) int {
	for d.parent[x] != x {
		d.parent[x] = d.parent[d.parent[x]]
		x = d.parent[x]
	}
	return x
}

func (d *DSU) Union(a, b int) bool {
	ra, rb := d.Find(a), d.Find(b)
	if ra == rb {
		return false
	}
	if d.size[ra] < d.size[rb] {
		ra, rb = rb, ra
	}
	d.parent[rb] = ra
	d.size[ra] += d.size[rb]
	return true
}
```

---

## Boas Práticas Sêniores e Armadilhas

- DSU não responde bem a “remover aresta” (conectividade dinâmica completa é mais complexa).
- Em Kruskal, ordene arestas e aplique `union`; aresta que não une conjuntos cria ciclo.

[Anterior](shortest-path-and-mst.md) | [Índice](../../SUMMARY.md) | [Próximo](range-queries-fenwick-and-segment-tree.md)
