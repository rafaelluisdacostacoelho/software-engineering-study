% Facade — Padrão Estrutural

[Anterior](Decorator.md) | [Índice](../../SUMMARY.md) | [Próximo](Factory.md)

# Facade

## Intenção
Fornecer uma interface simplificada para um subsistema complexo.

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

[Anterior](Decorator.md) | [Índice](../../SUMMARY.md) | [Próximo](Factory.md)
