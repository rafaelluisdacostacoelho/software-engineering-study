[Anterior](heaps-and-priority-queues.md) | [Índice](../../SUMMARY.md) | [Próximo](graphs-representations-and-traversal.md)

# Tries & Busca por Prefixo — Autocomplete e Matching

## Visão Geral e Contexto de Mercado

Tries (árvores de prefixo) e variações (radix tree, ternary search tree) são úteis quando você faz muitas operações de:

- Autocomplete / sugestão de termos.
- Matching por prefixo (roteamento, dicionários, tokens).
- Busca incremental (digitação) com baixa latência.

Em muitos sistemas, tries competem com soluções baseadas em índices (banco/search engine). A decisão sênior é sobre **latência**, **memória** e **custos operacionais**.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Trie**
	- Cada nó representa um prefixo.
	- Caminho da raiz até um nó → string/prefixo.
	- Busca por prefixo: $O(L)$ onde $L$ é o tamanho da string/prefixo.

- **Radix tree (compact trie)**
	- Comprime caminhos de nós com um único filho.
	- Geralmente reduz memória.

---

## Principais Desafios no Uso Profissional

- **Memória**: tries podem explodir se o alfabeto é grande e o vocabulário enorme.
- **Unicode**: definir unidade (rune/codepoint) e normalização.
- **Atualizações**: inserções frequentes exigem cuidado com concorrência.

---

## Estratégias Avançadas e Decisões Arquiteturais

- Se o dataset é grande e mutável, considere search engines (Elastic/OpenSearch) ou índices no banco.
- Se o dataset é médio e a latência é crítica (p99 baixo), trie/radix em memória pode vencer.
- Para sugestão: combine trie + ranking (heap/top-k) por nó ou cache de resultados.

---

## Exemplos Avançados (Python, C# e Go)

### Python — trie simples para prefix lookup

```python
from __future__ import annotations


class TrieNode:
	def __init__(self) -> None:
		self.children: dict[str, TrieNode] = {}
		self.is_end = False


class Trie:
	def __init__(self) -> None:
		self.root = TrieNode()

	def insert(self, word: str) -> None:
		node = self.root
		for ch in word:
			node = node.children.setdefault(ch, TrieNode())
		node.is_end = True

	def starts_with(self, prefix: str) -> bool:
		node = self.root
		for ch in prefix:
			if ch not in node.children:
				return False
			node = node.children[ch]
		return True
```

### C# — abordagem pragmática: prefix search em lista ordenada

Quando o conjunto é pequeno/médio e estático, `List<string>` ordenada + busca binária pode ser suficiente.

```csharp
using System;

public static class PrefixSearch
{
	public static int LowerBound(string[] a, string x)
	{
		int lo = 0, hi = a.Length;
		while (lo < hi)
		{
			int mid = lo + (hi - lo) / 2;
			if (string.Compare(a[mid], x, StringComparison.Ordinal) < 0) lo = mid + 1;
			else hi = mid;
		}
		return lo;
	}

	public static bool HasPrefix(string[] sorted, string prefix)
	{
		int i = LowerBound(sorted, prefix);
		return i < sorted.Length && sorted[i].StartsWith(prefix, StringComparison.Ordinal);
	}
}
```

### Go — prefix search com slice ordenado (mesma ideia)

```go
import "sort"

func HasPrefix(sorted []string, prefix string) bool {
	i := sort.SearchStrings(sorted, prefix)
	return i < len(sorted) && len(sorted[i]) >= len(prefix) && sorted[i][:len(prefix)] == prefix
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Trie é ótima para muitas queries por prefixo; para poucas queries, use estrutura simples.
- Evite alfabeto fixo gigante; prefira map/dict por nó ou radix tree.
- Normalize entradas (lowercase, Unicode NFC/NFKC conforme requisito).

---

## FAQ Especialista

**Trie sempre ganha de busca em lista ordenada?**  
Não. Para conjuntos pequenos e estáticos, lista ordenada + busca binária costuma ser mais simples e eficiente.

**Como lidar com ranking de sugestões?**  
Armazene contadores/score por palavra e mantenha top-k por nó (com custo/memória) ou use cache.

[Anterior](heaps-and-priority-queues.md) | [Índice](../../SUMMARY.md) | [Próximo](graphs-representations-and-traversal.md)
