% Visitor — Padrão Comportamental

[Anterior](TemplateMethod.md) | [Índice](../../SUMMARY.md) | [Próximo](../complexity/data-structures-and-big-o.md)

# Visitor

## Intenção
Separar algoritmos da estrutura de objetos para adicionar operações sem mexer nas classes.

## Quando usar
- Você quer reduzir acoplamento e melhorar testabilidade.
- Você precisa evoluir comportamento com menor impacto.

## Sinais de que ajuda
- Muitos `if/else` escolhendo implementação.
- Mudanças repetidas em vários pontos (shotgun surgery).
- Testes difíceis por dependências fixas.

## Trade-offs
- Mais indireção e mais artefatos.
- Aplicar cedo demais pode piorar a clareza.

## Checklist (PR)
- O cliente depende de abstrações, não de detalhes?
- Dá para testar com fake/mock?
- O padrão está resolvendo um problema real (não “estilo”)?

---

[Anterior](TemplateMethod.md) | [Índice](../../SUMMARY.md) | [Próximo](../complexity/data-structures-and-big-o.md)
