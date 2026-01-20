# Mapa de migração: template atual -> nova estrutura

Use isto para migrar sem perder nada e sem duplicar.

## Seu template atual → Novo lugar

### "Objetivos de Aprendizado (para senior)"
→ `00-meta/01-objetivos-de-aprendizado.md`

### "Contexto, Escopo e Nao-Objetivos"
→ `00-meta/02-escopo-e-nao-objetivos.md`  
e também reforçar em `01-visao-geral/02-quando-usar-vs-quando-evitar.md`

### "Glossario (padronize linguagem)"
→ `00-meta/04-glossario.md`

### "Modelo Mental (intuicao + formalizacao)"
→ `02-modelos-mentais-e-fundamentos/01-modelo-mental-intuicao.md`  
→ `02-modelos-mentais-e-fundamentos/02-modelo-formal-entidades-estados-contratos.md`  
→ `02-modelos-mentais-e-fundamentos/03-invariantes-e-propriedades.md`

### "Fundamentos Teoricos e Evolucao"
→ `02-modelos-mentais-e-fundamentos/04-teoria-essencial-e-pegadinhas.md`  
→ `02-modelos-mentais-e-fundamentos/05-evolucao-e-padroes-do-mercado.md`

### "Diagramas e Intuicao Visual"
→ incluir como subseções em:
- `03-arquitetura-de-referencia/*`
- `05-algoritmos-e-implementacao/*`
- `06-falhas-resiliencia-recuperacao/*`

### "Arquitetura de Referencia"
→ `03-arquitetura-de-referencia/*`

### "Modelo de Dados e Contratos"
→ `04-contratos-e-modelo-de-dados/*`

### "Algoritmos, Fluxos Criticos e Invariantes"
→ `05-algoritmos-e-implementacao/*`

### "Falhas, Resiliencia e Recuperacao"
→ `06-falhas-resiliencia-recuperacao/*`

### "Observabilidade e Operacao"
→ `07-observabilidade-e-operacao/*`

### "Seguranca, Privacidade e Compliance"
→ `08-seguranca-privacidade-compliance/*`

### "Performance, Capacidade e Custos"
→ `09-performance-capacidade-custos/*`

### "Testabilidade"
→ `10-testabilidade-e-qualidade/*`

### "Trade-offs, Alternativas e Decisoes"
→ `11-trade-offs-alternativas-e-decisoes/*`

### "Checklist de Review"
→ manter em dois níveis:
- checklists por tópico: ao final de cada arquivo (usando `SECTION.contract.template.md`)
- checklist global: `README.md` ou `00-meta/05-cheatsheet.md`

### "Estudos de Caso e Exercicios"
→ `12-estudos-de-caso-e-exercicios/*`

### "Referencias"
→ `00-meta/06-referencias.md`