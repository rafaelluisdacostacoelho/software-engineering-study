# Canvas Mestre — Livro Completo para Senior/Especialista “Nível DEUS”
**Versão:** v0.1  
**Última revisão:** 2026-01-20  
**Objetivo:** servir como *sumário/índice-mestre* para um conjunto de manuais que formem um especialista de elite: teoria → implementação → operação → segurança → custo → governança → AI.

> Regra do projeto: cada capítulo “importante” deve ter:
> - Definição + intuição + modelo formal
> - Invariantes e contratos
> - Exemplos progressivos (mínimo → realista → produção)
> - Falhas, observabilidade, segurança, trade-offs
> - Checklist de review + exercícios

---

## 0) Como usar este canvas (metodologia de estudo)
0.1. Como ler: camadas (iniciante → senior → especialista)  
0.2. Como praticar: “learning loops” (ler → implementar → operar → incidentes simulados)  
0.3. Como documentar: padrão anti-doc-rasa (definição/contratos/invariantes/falhas)  
0.4. Como revisar: spaced repetition + flashcards para definições/siglas  
0.5. Como medir domínio: rubricas por capítulo (consegue explicar, implementar, operar, ensinar)  
0.6. Como criar labs: ambientes locais, cloud sandbox, datasets sintéticos  
0.7. Como registrar decisões: ADR-lite e postmortems  
0.8. Como manter atualizado: changelog do conhecimento, “deprecations” e revisão anual  

---

## 1) Meta-habilidades (o multiplicador do nível DEUS)
1.1. Modelos mentais universais (abstração, invariantes, limites, contratos)  
1.2. Decomposição e boundaries (acoplamento, coesão, dependências)  
1.3. Raciocínio por trade-offs (custo, risco, tempo, complexidade)  
1.4. Raciocínio sob incerteza (Bayes mental, experimentos, métricas)  
1.5. Comunicação escrita (design docs, RFCs, ADRs, runbooks, postmortems)  
1.6. Comunicação em incidentes (clareza, priorização, mitigação vs correção)  
1.7. Revisão técnica de alto nível (checklists, padrões, riscos)  
1.8. Mentoria e ensino (currículo, feedback, calibragem de senioridade)  
1.9. Debugging científico (hipóteses, evidências, isolamentos, bisect)  
1.10. Engenharia econômica (FinOps mental, custo por unidade, custo marginal)  
1.11. Qualidade e confiabilidade como cultura (SLOs, error budget, ownership)  
1.12. Ética e responsabilidade (impacto, privacidade, riscos sociais)  

---

## 2) Matemática “para computação + AI” (profunda, aplicada)
### 2.1 Álgebra linear (aplicações diretas em ML e sistemas)
2.1.1 Vetores, bases, subespaços, projeções  
2.1.2 Normas (L1/L2/L∞), ângulos, similaridade (cosine)  
2.1.3 Produto matricial e interpretação geométrica  
2.1.4 Autovalores/autovetores: intuição e usos (estabilidade, PCA)  
2.1.5 Decomposições: SVD (principal), QR, Cholesky (quando/por quê)  
2.1.6 Matrizes esparsas e computação eficiente  
2.1.7 Condicionamento, número de condição, estabilidade numérica  
2.1.8 Diferenciação matricial (gradientes em redes)  
2.1.9 Low-rank approximations, compressão, embeddings  
2.1.10 Random projections (noções) e Johnson–Lindenstrauss (intuição)  

### 2.2 Cálculo (multivariável) e otimização
2.2.1 Derivadas, gradiente, Jacobiano, Hessiana (interpretações)  
2.2.2 Regra da cadeia em grafos computacionais (backprop)  
2.2.3 Otimização convexa vs não convexa: o que muda na prática  
2.2.4 Métodos de gradiente: GD, SGD, mini-batch, momentum, Adam/AdamW  
2.2.5 Schedules: warmup, cosine decay, step decay  
2.2.6 Regularização: L1/L2, weight decay, dropout (efeitos e limites)  
2.2.7 Constraints e Lagrange multipliers (noções aplicadas)  
2.2.8 Otimização sob ruído: variance, gradient noise scale (noções)  
2.2.9 Exploding/vanishing gradients e mitigação  
2.2.10 Segundo-ordem: Newton, quasi-Newton (quando aparece, limitações)  

### 2.3 Probabilidade (para inferência, A/B e AI)
2.3.1 Variáveis aleatórias, esperança, variância, covariância  
2.3.2 Distribuições comuns: Bernoulli, Binomial, Poisson, Normal, Exponencial, LogNormal  
2.3.3 Condicional, independência, Bayes, odds/likelihood  
2.3.4 Lei dos grandes números e CLT (interpretação correta)  
2.3.5 Processos: Poisson process, Markov chains (noções)  
2.3.6 Informação: entropia, cross-entropy, KL divergence, mutual information  
2.3.7 Inferência Bayesiana (noções), priors e posterior  
2.3.8 Monte Carlo e amostragem (noções), MCMC (alto nível)  

### 2.4 Estatística e inferência (evitar autoengano)
2.4.1 Estimadores: viés, variância, consistência  
2.4.2 Intervalos de confiança (interpretação)  
2.4.3 Testes de hipótese, p-values, erros tipo I/II  
2.4.4 Poder estatístico, tamanho de amostra  
2.4.5 Regressão linear: suposições, heterocedasticidade, outliers  
2.4.6 Regressão logística: calibração, thresholding  
2.4.7 Cross-validation, leakage, overfitting, seleção de modelo  
2.4.8 Métricas: AUC, F1, log loss, calibration error  
2.4.9 Causalidade (mínimo sério): DAGs, confounders, Simpson’s paradox  
2.4.10 A/B testing: CUPED (noções), sequential testing, multiple testing  
2.4.11 Séries temporais: estacionariedade (noções), autocorrelação, backtesting (noções)  

### 2.5 Matemática discreta e lógica (para corretude)
2.5.1 Lógica proposicional e de predicados (básico)  
2.5.2 Provas por indução (usos em invariantes)  
2.5.3 Combinatória e contagem (estimativas de complexidade)  
2.5.4 Teoria de grafos (base para redes, dependências, compiladores)  

### 2.6 Numérica e computação científica (prático)
2.6.1 Ponto flutuante (IEEE 754), erros, underflow/overflow  
2.6.2 Estabilidade numérica em somas, softmax, log-sum-exp  
2.6.3 Métodos iterativos e convergência (noções)  
2.6.4 Reprodutibilidade numérica (determinismo em GPU/threads)  

---

## 3) Estruturas de dados e algoritmos (nível produção)
3.1 Análise de complexidade (tempo, espaço, cache locality)  
3.2 Arrays, listas, stacks, queues, deques (trade-offs reais)  
3.3 Hash tables (colisões, resizing, adversarial keys, DoS)  
3.4 Trees: BST, AVL, Red-Black (por que importam)  
3.5 Tries e radix trees (roteamento, autocomplete)  
3.6 Heaps e priority queues (schedulers, rate limiting)  
3.7 B-trees / LSM trees (como bancos realmente funcionam)  
3.8 Grafos: BFS/DFS, SCC, shortest path, MST, topological sort  
3.9 Strings: suffix arrays/trees (noções), regex engines (alto nível)  
3.10 Probabilísticas: Bloom filter, HyperLogLog, Count-Min Sketch  
3.11 Algoritmos de streaming e sketches (heavy hitters, quantiles)  
3.12 Algoritmos concorrentes (locks, lock-free, wait-free — conceitos)  
3.13 Alocadores e estruturas low-level (arena allocators, pooling)  
3.14 Criptografia aplicada (estruturas para hash/MAC/signatures)  
3.15 Benchmarks: como medir sem mentir (warmup, p95/p99, GC)  

---

## 4) Fundamentos de computação (OS, redes, runtime, compiladores)
### 4.1 Sistemas operacionais (profundo)
4.1.1 Processos vs threads vs fibers  
4.1.2 Scheduling, preemption, context switching  
4.1.3 Memória: virtual memory, paging, COW  
4.1.4 Cache (L1/L2/L3), NUMA, false sharing  
4.1.5 IO: buffers, page cache, direct IO, async IO, epoll/kqueue  
4.1.6 Filesystems: ext4/xfs (noções), fsync, durability, journaling  
4.1.7 Time: clocks, NTP, monotonic clock, clock skew  
4.1.8 Containers: namespaces/cgroups, limites e pegadinhas  
4.1.9 Observabilidade do OS: perf, eBPF (noções), strace, lsof  
4.1.10 Segurança no OS: capabilities, seccomp, SELinux/AppArmor  
4.1.11 Kernel vs userland (impactos práticos)  

### 4.2 Redes (profundo e operacional)
4.2.1 TCP: handshake, congestion control, retransmit, TIME_WAIT  
4.2.2 UDP e QUIC (conceito e casos)  
4.2.3 DNS: caching, TTL, negative caching, resolvers  
4.2.4 TLS: handshake, certificados, chain of trust, mTLS  
4.2.5 HTTP semantics: idempotência, caching, headers, content negotiation  
4.2.6 HTTP/2: multiplexing, head-of-line (o que resolve e o que não)  
4.2.7 HTTP/3/QUIC: por que existe e trade-offs  
4.2.8 Load balancing: L4 vs L7, sticky sessions, consistent hashing  
4.2.9 Proxies, service mesh (conceitos), circuit breaking  
4.2.10 NAT, firewalls, WAF, rate limiting na borda  
4.2.11 CDNs: caching, invalidation, edge compute (noções)  

### 4.3 Compiladores e runtimes (entender performance e bugs)
4.3.1 AST, parsing (alto nível), IR, otimizações (noções)  
4.3.2 JIT vs AOT, warmup, deopt, inline caches (noções)  
4.3.3 Memória e GC: tracing, generational GC, pauses  
4.3.4 Escape analysis, stack allocation (noções)  
4.3.5 Concurrency runtimes: event loop, goroutines, async/await  
4.3.6 FFI e ABI: riscos, alignment, calling conventions  
4.3.7 Profiling: CPU, heap, contention, IO  
4.3.8 Debugging avançado: core dumps, heap dumps, symbolication  

---

## 5) Engenharia de Software (design, arquitetura, evolução)
5.1 APIs e contratos: estabilidade, compatibilidade, versionamento  
5.2 Modularidade: camadas, boundaries, dependências e ownership  
5.3 DDD: bounded contexts, aggregates, invariantes de domínio  
5.4 Arquiteturas: hexagonal/clean, modular monolith, microservices  
5.5 Event-driven: eventos, comandos, contratos, schema registry  
5.6 CQRS e Event Sourcing: quando vale, riscos, migrações  
5.7 Patterns distribuídos: outbox/inbox, sagas, idempotency keys  
5.8 Migrações sem downtime: strangler, dual reads/writes (com cautela)  
5.9 Gestão de dívida: métricas, refactors, limites e roadmap  
5.10 Documentação viva: ADRs, RFCs, runbooks, playbooks  
5.11 Code review “sênior”: design, testes, segurança, operação, custo  

---

## 6) Bancos de dados e storage (especialista)
6.1 Relacionais (Postgres como referência)
- 6.1.1 Modelagem, constraints, transações, isolamento e anomalias  
- 6.1.2 Índices (B-tree), seletividade, cardinalidade  
- 6.1.3 Planner/optimizer, EXPLAIN, join strategies  
- 6.1.4 Locks, MVCC, vacuum, bloat  
- 6.1.5 Replication, failover, read replicas, lag  
- 6.1.6 Particionamento, sharding (quando/como)  
- 6.1.7 Backups, PITR, DR, testes de restore  
- 6.1.8 Performance: hotspots, connection pooling, prepared statements  

6.2 LSM e NoSQL
- 6.2.1 LSM trees: compaction, write amplification  
- 6.2.2 Dynamo model: quorum, consistent hashing, hot partitions  
- 6.2.3 Cassandra/Mongo (conceitos): modelagem e tuning  
- 6.2.4 Redis: eviction, persistence, cluster, pitfalls de consistência  

6.3 Busca e analytics
- 6.3.1 Inverted index, scoring, mappings  
- 6.3.2 Aggregations e custos  
- 6.3.3 OLAP/columnar, particionamento, lakehouse (noções)  

6.4 Storage distribuído e arquivos
- 6.4.1 Object storage (S3): consistência, versioning, lifecycle  
- 6.4.2 Block storage vs object vs file  
- 6.4.3 CDN e cache distribuído (integração com storage)  

---

## 7) Mensageria, streaming e integração (especialista)
7.1 Filas vs streams vs pub/sub (modelos e garantias)  
7.2 Kafka/Pulsar/Rabbit/SQS: arquitetura e trade-offs  
7.3 Semânticas: at-least-once, at-most-once, “exactly-once” real  
7.4 Partitioning, ordering keys, consumer groups, rebalance  
7.5 DLQ, retries, backoff, poison messages  
7.6 Schema evolution, versionamento de eventos, compatibilidade  
7.7 Outbox/inbox, transactional messaging  
7.8 Processamento de streams: windowing, watermarking (noções)  
7.9 Reprocessamento, replay, idempotência e dedup  
7.10 Observabilidade em pipelines (lag, throughput, erro)  

---

## 8) Backend e APIs (production grade)
8.1 REST: semântica, cache, idempotência, paginação, rate limits  
8.2 gRPC: contracts, streaming, deadlines, interceptors  
8.3 GraphQL (quando faz sentido e riscos operacionais)  
8.4 Autenticação/autorização em APIs (OAuth2/OIDC, scopes, RBAC/ABAC)  
8.5 Resiliência: timeouts por hop, circuit breaker, bulkheads  
8.6 Consistência e workflows: sagas, orquestração/coreografia  
8.7 Multi-tenancy (isolamento, quotas, “noisy neighbor”)  
8.8 Migrações de API sem quebrar clientes  
8.9 Compatibilidade e versionamento semântico de contratos  

---

## 9) Observabilidade e SRE (operação nível elite)
9.1 Logs estruturados: correlação, sampling, PII redaction  
9.2 Métricas: histogramas, percentis, cardinalidade, custo  
9.3 Tracing: propagação de contexto, baggage, exemplars  
9.4 SLIs/SLOs: error budget, burn rate, alertas acionáveis  
9.5 Dashboards: golden signals, saúde de dependências  
9.6 Incidentes: mitigação, comunicação, postmortems  
9.7 Capacity planning: filas, saturação, Little’s Law  
9.8 Chaos engineering e game days (responsável)  
9.9 Observabilidade de dados (data quality, freshness, lineage)  
9.10 Observabilidade de AI (qualidade, drift, custo, segurança)  

---

## 10) Segurança (do básico ao avançado, incluindo AI)
10.1 Threat modeling: STRIDE/LINDDUN, abuse cases  
10.2 Web/app security: OWASP Top 10 aplicado  
10.3 AuthN/AuthZ: sessões, JWT pitfalls, OAuth2/OIDC, mTLS  
10.4 Criptografia aplicada: hashing, MAC, signatures, key management  
10.5 Gestão de segredos: vaults, rotação, least privilege  
10.6 Segurança em cloud: IAM, policies, boundaries, network segmentation  
10.7 Segurança em CI/CD: supply chain, SBOM, assinaturas  
10.8 Detecção e resposta: logs de auditoria, SIEM (noções), alertas  
10.9 Segurança de dados: PII, LGPD, retenção, auditoria  
10.10 Segurança em Kubernetes: RBAC, policies, pod security, admission  
10.11 Segurança em AI:
- prompt injection (direta/indireta), tool abuse, exfiltration  
- data poisoning (RAG/treino), model extraction (noções)  
- jailbreaks, eval de segurança, red teaming  
- isolamento e sandbox de ferramentas  

---

## 11) Performance, capacidade e custos (engenharia econômica)
11.1 Performance no app: CPU, memória, IO, locks, p99  
11.2 Perf no DB: índices, queries, pool, cache, locks  
11.3 Perf em rede: timeouts, retransmits, TLS overhead  
11.4 Caching: estratégias, invalidação, stampede, consistency  
11.5 Load testing: cenários, ramp-up, limites, regressões  
11.6 FinOps: custo por request, custo por tenant, otimizações  
11.7 GPUs: throughput vs latência, batch, quantização (para AI)  
11.8 Modelos de fila e saturação (Little’s Law aplicado)  

---

## 12) Infra, cloud, plataformas e CI/CD
12.1 Containers: build, imagens, registries, SBOM  
12.2 Kubernetes: deploy, service discovery, autoscaling, rollouts  
12.3 Service mesh (conceitos): mTLS, retries, observabilidade  
12.4 IaC: Terraform/Pulumi, state, drift, módulos  
12.5 Networking cloud: VPC, subnets, routing, LB, WAF  
12.6 Storage cloud: S3, lifecycle, versioning, replication  
12.7 CI/CD: pipelines, gates, progressive delivery, feature flags  
12.8 Multi-region e DR: RTO/RPO, active-active vs active-passive  
12.9 Gestão de configs e segredos  
12.10 Plataforma interna (platform engineering): self-service, templates, golden paths  

---

## 13) AI / ML / LLM (tudo: fundamentos → produção → segurança)
### 13.1 Fundamentos de ML
13.1.1 Supervisionado/não supervisionado/self-supervised  
13.1.2 Loss functions e otimização  
13.1.3 Feature engineering, leakage, drift  
13.1.4 Métricas e avaliação (classification, ranking, regression)  
13.1.5 Interpretação e explicabilidade (noções)  

### 13.2 Deep Learning
13.2.1 Backprop de verdade (grafo computacional)  
13.2.2 CNNs, RNNs (histórico), attention  
13.2.3 Transformers: attention, heads, residuals, LayerNorm  
13.2.4 Treinamento: mixed precision, gradient accumulation, clipping  
13.2.5 Regularização e generalização  
13.2.6 Embeddings e representação  

### 13.3 LLMs
13.3.1 Tokenização, contexto, limitações  
13.3.2 Pré-treino, instruction tuning, alinhamento (SFT/RLHF/DPO)  
13.3.3 Prompting avançado (e limites): few-shot, tool use  
13.3.4 RAG: chunking, embeddings, re-ranking, avaliação  
13.3.5 Fine-tuning/LoRA vs RAG vs prompt (critérios)  
13.3.6 Alucinação: mecanismos e mitigação  
13.3.7 Avaliação: human eval, automatic eval, judge pitfalls  
13.3.8 Governança: model cards, policy, red teaming  

### 13.4 MLOps/LLMOps
13.4.1 Dataset versioning, lineage, data contracts  
13.4.2 Pipelines de treino, reproducibility, artifacts  
13.4.3 Model registry, deploy e rollback  
13.4.4 Serving: batch vs online, caching, quantização, distillation  
13.4.5 Observabilidade: qualidade, drift, custo, latência  
13.4.6 Segurança: prompt injection, tool sandbox, PII  
13.4.7 Operação: incidentes de AI e mitigação  

### 13.5 Engenharia de dados para AI
13.5.1 Coleta, rotulagem, qualidade, vieses  
13.5.2 Dedup, limpeza, normalização, PII redaction  
13.5.3 Dados sintéticos (quando ajuda e riscos)  
13.5.4 Catálogo e governança de dados (mínimo)  

---

## 14) Engenharia de dados e analytics (fora de AI também)
14.1 OLTP vs OLAP (decisões e trade-offs)  
14.2 Data warehouses (conceitos), modelagem dimensional  
14.3 Data lakes e lakehouse (conceitos), formatos colunares  
14.4 ETL/ELT: idempotência, reprocessamento, backfills  
14.5 Qualidade de dados: freshness, completeness, validity  
14.6 Orquestração e dependências, SLAs de dados  
14.7 Observabilidade de dados e lineage (conceitos)  

---

## 15) Produto, experimentação e tomada de decisão
15.1 Métricas de produto: funil, retenção, churn, LTV (noções)  
15.2 A/B testing em produção: guardrails, segmentação, riscos  
15.3 Experimentação com AI: avaliação online, feedback loops  
15.4 Decisões orientadas a métricas (evitar métricas vaidosas)  
15.5 Ética e risco (principalmente com AI)  

---

## 16) Liderança técnica, organização e carreira (staff+)
16.1 Escopo e impacto (time → org → companhia)  
16.2 Platform engineering e governança  
16.3 Gestão de risco e compliance em engenharia  
16.4 Mentoria e desenvolvimento de pessoas  
16.5 Hiring e entrevistas (calibração)  
16.6 Roadmaps técnicos e alinhamento com negócio  
16.7 Cultura de incidentes, qualidade e aprendizado  

---

## 17) Apêndices (referência rápida)
17.1 Glossário mestre (siglas e termos)  
17.2 Cheatsheets (Linux, Git, redes, SQL, observabilidade, segurança, AI)  
17.3 Checklists: design review, PR review, readiness, incident response  
17.4 Bibliografia “canônica” por tema (oficial, papers, livros)  
17.5 Laboratórios sugeridos (projetos) por capítulo  
17.6 “Exame final” (rubrica de proficiência) por domínio  