[Anterior](CompositionOverInheritance.md) | [Índice](../../SUMMARY.md) | [Próximo](FailFast.md)

# Design for Testability

## Resumo
O princípio **Design for Testability** é uma heurística para decisões de design e implementação que reduz risco, custo de mudança e complexidade acidental.

## Como aplicar
- Comece simples, extraia abstrações quando houver repetição real.
- Garanta que a decisão seja testável.
- Documente trade-offs quando a escolha não for óbvia.

## Armadilhas
- Aplicar como dogma e ignorar contexto.
- Abstrair cedo demais e criar indireção sem ganho.

## Checklist
- A intenção está clara?
- Há duplicação de regra importante?
- O design facilita mudanças futuras?
- Existe cobertura de testes adequada?

## Leituras sugeridas
- Refactoring (Martin Fowler)
- A Philosophy of Software Design (John Ousterhout)

---

[Anterior](CompositionOverInheritance.md) | [Índice](../../SUMMARY.md) | [Próximo](FailFast.md)
