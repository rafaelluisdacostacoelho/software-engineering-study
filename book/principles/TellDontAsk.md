% Tell, Don't Ask — Princípio de Design (nível Sênior / Especialista)

[Anterior](SeparationOfConcerns.md) | [Índice](../../SUMMARY.md) | [Próximo](LawOfDemeter.md)

# Tell, Don't Ask

## Resumo
O princípio **Tell, Don't Ask** é uma heurística para decisões de design e implementação que reduz risco, custo de mudança e complexidade acidental.

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

[Anterior](SeparationOfConcerns.md) | [Índice](../../SUMMARY.md) | [Próximo](LawOfDemeter.md)
