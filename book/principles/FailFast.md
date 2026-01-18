% Fail Fast — Detectar e falhar cedo (nível Sênior / Especialista)

[Anterior](DesignForTestability.md) | [Índice](../../SUMMARY.md) | [Próximo](YAGNI.md)

# Fail Fast

## Resumo
O princípio **Fail Fast** é uma heurística para decisões de design e implementação que reduz risco, custo de mudança e complexidade acidental.

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

[Anterior](DesignForTestability.md) | [Índice](../../SUMMARY.md) | [Próximo](YAGNI.md)
