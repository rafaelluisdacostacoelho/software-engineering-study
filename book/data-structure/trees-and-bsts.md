[Anterior](hash-tables-and-sets.md) | [Índice](../../SUMMARY.md) | [Próximo](heaps-and-priority-queues.md)

# Árvores & BSTs — Traversal, Balanceamento e Decisão Prática

## Visão Geral e Contexto de Mercado

Árvores são a base de:

- Índices (B-Tree/LSM no banco), sistemas de arquivos, tries, heaps.
- Estruturas ordenadas (trees/balanced maps) para range queries e ordenação incremental.
- Representação hierárquica (DOM/AST, permissões, catálogo, org chart).

O ponto sênior é saber quando a complexidade de árvore vale a pena versus “array ordenado + busca binária” ou “hash map”.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Termos**: raiz, folha, altura, profundidade, balanceamento.

- **BST (Binary Search Tree)**
	- Invariante: esquerda < nó < direita.
	- Operações: busca/insert/delete em $O(h)$ (altura).
	- Se a árvore degrada (desbalanceada), $h \approx n$ → vira lista.

- **Árvores balanceadas (mercado)**
	- Red-Black Tree (muito comum em libs)
	- AVL (mais rígida)
	- B-Tree (disco/SSD, bancos)

---

## Algoritmos Essenciais

### 1) Traversal

- Preorder (raiz-esq-dir)
- Inorder (esq-raiz-dir) → em BST, produz ordenado
- Postorder (esq-dir-raiz)
- Level order (BFS)

**Complexidade:** $O(n)$

### 2) Lowest Common Ancestor (LCA)

Útil em hierarquias e árvores.

### 3) Serialização/Deserialização

Prático para persistir estruturas e debug.

---

## Exemplos Avançados (Python, C# e Go)

### Python — inorder iterativo (evita recursion depth)

```python
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
	val: int
	left: Node | None = None
	right: Node | None = None


def inorder(root: Node | None) -> list[int]:
	out: list[int] = []
	stack: list[Node] = []
	cur = root
	while cur is not None or stack:
		while cur is not None:
			stack.append(cur)
			cur = cur.left
		node = stack.pop()
		out.append(node.val)
		cur = node.right
	return out
```

### C# — BFS por níveis

```csharp
using System.Collections.Generic;

public sealed class Node
{
	public int Value { get; }
	public Node? Left { get; set; }
	public Node? Right { get; set; }
	public Node(int value) => Value = value;
}

public static class TreeTraversal
{
	public static List<int> LevelOrder(Node? root)
	{
		var res = new List<int>();
		if (root is null) return res;

		var q = new Queue<Node>();
		q.Enqueue(root);
		while (q.Count > 0)
		{
			var node = q.Dequeue();
			res.Add(node.Value);
			if (node.Left != null) q.Enqueue(node.Left);
			if (node.Right != null) q.Enqueue(node.Right);
		}
		return res;
	}
}
```

### Go — LCA em BST (explora ordenação)

```go
type Node struct {
	Val         int
	Left, Right *Node
}

func LcaBst(root *Node, a, b int) *Node {
	cur := root
	for cur != nil {
		if a < cur.Val && b < cur.Val {
			cur = cur.Left
			continue
		}
		if a > cur.Val && b > cur.Val {
			cur = cur.Right
			continue
		}
		return cur
	}
	return nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Se você só precisa de busca em coleção estática: **array ordenado + binary search** pode ser mais simples e rápido.
- Para range queries e ordenação incremental com inserções frequentes: árvore balanceada é ótima.
- Evite recursão profunda em árvores desbalanceadas (risco de stack overflow).

---

## Integração na Arquitetura Real

- Índices de banco são árvores: entender isso ajuda a projetar queries e chaves.
- Árvores em domínio: valide invariantes (sem ciclos) e considere caching de agregações por nó.

[Anterior](hash-tables-and-sets.md) | [Índice](../../SUMMARY.md) | [Próximo](heaps-and-priority-queues.md)
