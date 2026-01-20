# Template de Documento de Estudo (Manual + Referência)

Este template serve para criar um **documento completo** de estudo sobre um assunto isolado (ex.: uma linguagem específica, um protocolo, uma tecnologia, um conceito).  
A meta é produzir um material que funcione como **manual de estudo e referência**, com **profundidade**, **precisão**, **explicação de termos/siglas**, **utilidade prática**, **exemplos**, **boas práticas**, **armadilhas** e **fontes**.

---

## 0) Como usar este template

### Quando usar arquivo único vs. pasta
- Use **um único arquivo** (ex.: `ASSUNTO.md`) se o tema couber confortavelmente em ~30–60 páginas (dependendo do nível de detalhe).
- Use uma **pasta** (recomendado) se:
  - há muitas áreas (fundamentos, avançado, ferramentas, ecossistema, práticas, etc.)
  - o assunto exige muitos exemplos e seções extensas
  - você pretende evoluir com o tempo

### Padrões de escrita (obrigatórios)
- **Defina termos antes de usar** (ou linke para o glossário).
- Sempre que aparecer uma sigla, escreva na primeira vez: **“Forma Completa (SIGLA)”**.
- Misture **explicação conceitual** + **exemplos práticos** + **“por que isso importa”**.
- Inclua:
  - “**Quando usar** / **Quando evitar**”
  - “**Erros comuns**”
  - “**Pegadinhas**”
  - “**Checklist de revisão**” (no final)
- Use exemplos com:
  - entrada → saída
  - antes → depois
  - ruim → melhor

### Convenções de formatação
- Títulos com numeração (1, 1.1, 1.2…) para facilitar knownledge mapping.
- Blocos de código sempre com linguagem.
- Use tabelas para comparação e “folhas de cola” (cheat sheets).
- Link interno para seções importantes.

---

## 1) Metadados do Documento

- **Assunto:** `<NOME DO ASSUNTO>`
- **Versão do documento:** `vX.Y`
- **Data da última revisão:** `YYYY-MM-DD`
- **Autor(es):** `<NOME(S)>`
- **Objetivo:** (1–3 frases)
- **Público-alvo:** (iniciante / intermediário / avançado)
- **Pré-requisitos:** (conceitos, ferramentas, matemática, etc.)
- **Ambiente/Versões relevantes:** (ex.: versões da linguagem, runtime, SO, etc.)
- **Licença/uso:** (opcional)

---

## 2) Sumário (Table of Contents)

> Gere automaticamente no seu editor, ou mantenha manualmente.

- [3) Visão Geral](#3-visão-geral)
- [4) Fundamentos Essenciais](#4-fundamentos-essenciais)
- [5) Conceitos Intermediários](#5-conceitos-intermediários)
- [6) Tópicos Avançados](#6-tópicos-avançados)
- [7) Ecossistema, Ferramentas e Fluxo de Trabalho](#7-ecossistema-ferramentas-e-fluxo-de-trabalho)
- [8) Boas Práticas, Padrões e Anti-padrões](#8-boas-práticas-padrões-e-anti-padrões)
- [9) Segurança, Performance e Confiabilidade](#9-segurança-performance-e-confiabilidade)
- [10) Debug, Troubleshooting e Observabilidade](#10-debug-troubleshooting-e-observabilidade)
- [11) Comparações e Integrações](#11-comparações-e-integrações)
- [12) Casos de Uso e Projetos Guiados](#12-casos-de-uso-e-projetos-guiados)
- [13) FAQ (Perguntas Frequentes)](#13-faq-perguntas-frequentes)
- [14) Glossário (Termos e Siglas)](#14-glossário-termos-e-siglas)
- [15) Cheatsheet / Folha de Referência Rápida](#15-cheatsheet--folha-de-referência-rápida)
- [16) Referências e Leituras Recomendadas](#16-referências-e-leituras-recomendadas)
- [17) Checklist de Qualidade do Documento](#17-checklist-de-qualidade-do-documento)

---

## 3) Visão Geral

### 3.1 O que é
Explique o assunto em termos simples e depois em termos técnicos.

- Definição curta:
- Definição técnica:
- Problema que resolve:

### 3.2 Por que isso existe (história e motivação)
- Contexto histórico (linha do tempo se útil)
- Principais dores que motivaram
- Alternativas anteriores e limitações

### 3.3 Onde é usado (utilidade)
- Cenários comuns
- Setores/indústrias
- Tipos de projetos

### 3.4 Quando usar vs. quando evitar
**Quando usar:**
- …

**Quando evitar / cuidado:**
- …

### 3.5 Mapa mental do conteúdo (visão macro)
Inclua um diagrama textual (ou links) das áreas do assunto.

---

## 4) Fundamentos Essenciais

> Se alguém ler só esta seção, deve sair com uma base sólida.

Para cada tópico abaixo, use o padrão:

**Definição → Intuição → Como funciona → Exemplo → Erros comuns → Boas práticas → Referências**

### 4.1 Conceitos básicos
- Conceito A
- Conceito B
- Conceito C

### 4.2 Terminologia mínima
Liste termos indispensáveis com links para o glossário.

### 4.3 “Hello World” explicado
Não apenas mostre o exemplo; explique:
- o que cada parte faz
- como executar
- o que esperar de saída
- variações comuns

### 4.4 Estruturas e componentes fundamentais
- Componentes do sistema
- Arquitetura mínima
- Como as partes se conectam

---

## 5) Conceitos Intermediários

### 5.1 Componentes/recursos importantes
- Recurso 1 (o que é + por que importa)
- Recurso 2
- Recurso 3

### 5.2 Modelos mentais (como pensar sobre isso)
- Metáforas úteis
- Invariantes (o que sempre é verdade)
- O que confunde iniciantes

### 5.3 Padrões de uso comuns
- Padrão A
- Padrão B
- Padrão C

### 5.4 Exemplos comentados
Inclua exemplos progressivos (do simples ao robusto).

---

## 6) Tópicos Avançados

> Explique “como funciona por dentro” e implicações.

### 6.1 Internals / implementação (se aplicável)
- Estruturas internas
- Algoritmos relevantes
- Limitações e trade-offs

### 6.2 Concorrência / paralelismo / async (se aplicável)
- Definições (concorrência vs paralelismo)
- Modelos suportados
- Perigos (race conditions, deadlocks, starvation)
- Padrões recomendados

### 6.3 Tipos / memória / runtime (se aplicável)
- Modelo de tipos
- Gerência de memória
- Otimizações e custos ocultos

### 6.4 Compatibilidade e versões
- Breaking changes
- Migração entre versões
- Estratégias de compatibilidade

---

## 7) Ecossistema, Ferramentas e Fluxo de Trabalho

### 7.1 Instalação e setup
- Pré-requisitos
- Instalação em Windows / Linux / macOS
- Verificação de instalação

### 7.2 Ferramentas essenciais
- Compiladores/interpreters/runtimes
- Gerenciadores de pacote
- Formatadores e linters
- Test runners
- IDEs e plugins

### 7.3 Estrutura de projeto recomendada
- Convenções de pastas
- Configurações típicas
- Scripts úteis

### 7.4 Build, deploy e distribuição
- Ambientes (dev/test/prod)
- Empacotamento
- Publicação e versionamento

---

## 8) Boas Práticas, Padrões e Anti-padrões

### 8.1 Boas práticas
- Regra → por quê → exemplo bom

### 8.2 Anti-padrões e cheiros (code smells)
- Sintoma → risco → alternativa

### 8.3 Estilo e convenções
- Nomeação
- Organização
- Comentários e documentação

### 8.4 Testes
- Pirâmide de testes (unit/integration/e2e)
- Estratégias de mock/stub
- Cobertura: o que significa e o que não significa

---

## 9) Segurança, Performance e Confiabilidade

### 9.1 Segurança (Security)
- Modelo de ameaça (threat model) básico
- Vulnerabilidades comuns
- Boas práticas e hardening

### 9.2 Performance
- Onde costuma ficar lento
- Como medir (profiling/benchmark)
- Otimizações típicas
- Trade-offs (memória vs CPU)

### 9.3 Confiabilidade
- Erros e exceções
- Idempotência (se aplicável)
- Retentativas e backoff
- Timeouts e circuit breakers

---

## 10) Debug, Troubleshooting e Observabilidade

### 10.1 Debugging
- Ferramentas e comandos
- Estratégias (reduzir caso, bisectar, logs)

### 10.2 Logs, métricas e traces
- O que logar
- Estrutura de logs
- Métricas chave
- Rastreamento distribuído (se aplicável)

### 10.3 Problemas comuns (com soluções)
Formato recomendado:

- **Sintoma:**
- **Causa provável:**
- **Como confirmar:**
- **Como resolver:**
- **Como prevenir:**

---

## 11) Comparações e Integrações

### 11.1 Comparação com alternativas
Tabela recomendada:
- Curva de aprendizado
- Performance
- Ecossistema
- Segurança
- Produtividade
- Casos de uso ideais

### 11.2 Integração com outras tecnologias
- Integração A
- Integração B

---

## 12) Casos de Uso e Projetos Guiados

> Aqui você ensina fazendo.

### 12.1 Projeto 1 (iniciante)
- Objetivo
- Requisitos
- Passo a passo
- Resultado esperado
- Extensões/exercícios

### 12.2 Projeto 2 (intermediário)
…

### 12.3 Projeto 3 (avançado)
…

---

## 13) FAQ (Perguntas Frequentes)

Liste perguntas reais (ou prováveis) e responda com clareza e exemplos.

- “O que acontece se…?”
- “Qual a diferença entre X e Y?”
- “Por que meu código falha quando…?”

---

## 14) Glossário (Termos e Siglas)

> Cada entrada deve ter: definição, contexto, exemplo e (se útil) “não confundir com”.

**Exemplo de formato:**

- **ABI (Application Binary Interface)**  
  Definição: …  
  Contexto: …  
  Exemplo: …  
  Não confundir com: API

- **API (Application Programming Interface)**  
  Definição: …  
  …

---

## 15) Cheatsheet / Folha de Referência Rápida

Uma seção direta para consulta:

- comandos essenciais
- sintaxe-chave
- atalhos e padrões
- tabelas-resumo

---

## 16) Referências e Leituras Recomendadas

Divida por tipo:
- Documentação oficial
- Livros
- Artigos
- Cursos
- Repositórios e exemplos
- Comunidades (fóruns, Discord, etc.)

Inclua:
- link
- nível (iniciante/intermediário/avançado)
- por que vale a pena

---

## 17) Checklist de Qualidade do Documento

Antes de considerar “pronto”, confirme:

- [ ] Há uma explicação inicial simples e uma técnica
- [ ] Termos e siglas estão definidos na primeira ocorrência
- [ ] Há exemplos executáveis (quando aplicável)
- [ ] Há “quando usar vs evitar”
- [ ] Há seção de erros comuns e troubleshooting
- [ ] Há glossário completo e consistente
- [ ] Há referências confiáveis (preferência oficial)
- [ ] O conteúdo está organizado e linkado
- [ ] Há projetos guiados e exercícios
- [ ] Há uma folha de referência rápida

---

## Apêndice A) Modelo de seção (copiar/colar)

### <TÍTULO DO TÓPICO>
**Definição:**  
**Intuição (explicação simples):**  
**Como funciona (explicação técnica):**  
**Por que isso importa:**  
**Exemplo mínimo:**  
```<linguagem>
<codigo>
```
**Exemplo realista:**  
```<linguagem>
<codigo>
```
**Erros comuns:**  
- …
**Boas práticas:**  
- …
**Pegadinhas:**  
- …
**Leituras:**  
- …