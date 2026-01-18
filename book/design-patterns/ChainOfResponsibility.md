% Chain of Responsibility — Padrão Comportamental

[Anterior](Builder.md) | [Índice](../../SUMMARY.md) | [Próximo](Command.md)

# Chain of Responsibility

## Intenção
Encadear handlers e permitir que a requisição seja tratada por um deles.

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

[Anterior](Builder.md) | [Índice](../../SUMMARY.md) | [Próximo](Command.md)
