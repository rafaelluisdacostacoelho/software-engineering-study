% Factory — Padrão de Criação (Factory / Factory Method / Abstract Factory)

[Anterior](Facade.md) | [Índice](../../SUMMARY.md) | [Próximo](Observer.md)

# Factory

## Intenção
Centralizar criação de objetos e esconder detalhes de instanciação.

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

[Anterior](Facade.md) | [Índice](../../SUMMARY.md) | [Próximo](Observer.md)
