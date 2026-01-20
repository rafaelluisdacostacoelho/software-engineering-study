[Anterior](union-find-and-connectivity.md) | [Índice](../../SUMMARY.md) | [Próximo](caches-eviction-lru-lfu.md)

# Range Queries — Fenwick (BIT), Segment Tree e Sparse Table

## Visão Geral e Contexto de Mercado

Range queries aparecem em:

- Métricas e séries temporais (somas/contagens por intervalo)
- Ranking e agregações (soma, mínimo/máximo, gcd)
- Sistemas de recomendação e analytics

No dia a dia, muitas vezes um **prefix sum** resolve. Quando há **muitas atualizações** e **muitas queries**, Fenwick/segment tree são a próxima camada.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Prefix sum**
	- Build $O(n)$, query $O(1)$, update $O(n)$

- **Fenwick Tree (Binary Indexed Tree)**
	- Update $O(\log n)$
	- Prefix sum $O(\log n)$
	- Range sum: $sum(l,r)=pref(r)-pref(l-1)$
	- Mais simples e com menor constante que segment tree para soma.

- **Segment Tree**
	- Query e update em $O(\log n)$
	- Suporta várias operações (min, max, soma, etc.)
	- Permite lazy propagation (atualizações em range)

- **Sparse Table**
	- Para queries idempotentes (ex.: min/max/gcd) com array estático
	- Build $O(n\log n)$, query $O(1)$
	- Não é boa para updates.

---

## Principais Desafios no Uso Profissional

- Implementação e manutenção: é fácil errar índices e bordas.
- Escolha errada: usar segment tree quando prefix sum bastava.
- Observabilidade: é comum essas estruturas viverem em “core” de performance; teste e monitore.

---

## Exemplos Avançados (Python, C# e Go)

### Python — Fenwick (BIT) para soma

```python
class Fenwick:
	def __init__(self, n: int) -> None:
		self.n = n
		self.bit = [0] * (n + 1)

	def add(self, idx0: int, delta: int) -> None:
		# idx0 é 0-based
		i = idx0 + 1
		while i <= self.n:
			self.bit[i] += delta
			i += i & -i

	def sum_prefix(self, idx0: int) -> int:
		# soma [0..idx0]
		i = idx0 + 1
		s = 0
		while i > 0:
			s += self.bit[i]
			i -= i & -i
		return s

	def sum_range(self, l0: int, r0: int) -> int:
		if l0 > r0:
			return 0
		return self.sum_prefix(r0) - (self.sum_prefix(l0 - 1) if l0 > 0 else 0)
```

### C# — Fenwick para soma (long)

```csharp
public sealed class Fenwick
{
	private readonly long[] _bit;
	public int N { get; }

	public Fenwick(int n)
	{
		N = n;
		_bit = new long[n + 1];
	}

	public void Add(int idx0, long delta)
	{
		for (int i = idx0 + 1; i <= N; i += i & -i) _bit[i] += delta;
	}

	public long SumPrefix(int idx0)
	{
		long s = 0;
		for (int i = idx0 + 1; i > 0; i -= i & -i) s += _bit[i];
		return s;
	}

	public long SumRange(int l0, int r0)
	{
		if (l0 > r0) return 0;
		return SumPrefix(r0) - (l0 > 0 ? SumPrefix(l0 - 1) : 0);
	}
}
```

### Go — Fenwick

```go
type Fenwick struct {
	n   int
	bit []int
}

func NewFenwick(n int) *Fenwick {
	return &Fenwick{n: n, bit: make([]int, n+1)}
}

func (f *Fenwick) Add(idx0 int, delta int) {
	for i := idx0 + 1; i <= f.n; i += i & -i {
		f.bit[i] += delta
	}
}

func (f *Fenwick) SumPrefix(idx0 int) int {
	s := 0
	for i := idx0 + 1; i > 0; i -= i & -i {
		s += f.bit[i]
	}
	return s
}

func (f *Fenwick) SumRange(l0, r0 int) int {
	if l0 > r0 {
		return 0
	}
	left := 0
	if l0 > 0 {
		left = f.SumPrefix(l0 - 1)
	}
	return f.SumPrefix(r0) - left
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Se o array é estático e só há queries: prefix sum ou sparse table podem ser melhores.
- Se há updates pontuais + range sums: Fenwick é excelente.
- Se há updates em range e queries em range: segment tree com lazy propagation.

---

## FAQ Especialista

**Fenwick e segment tree fazem a mesma coisa?**  
Se o problema é soma e updates pontuais, Fenwick é mais simples. Segment tree é mais geral.

**Sparse table vale a pena?**  
Para min/max/gcd em array estático com muitas queries, sim.

[Anterior](union-find-and-connectivity.md) | [Índice](../../SUMMARY.md) | [Próximo](caches-eviction-lru-lfu.md)
