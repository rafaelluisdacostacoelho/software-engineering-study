# Sumário

Índice em ordem de leitura (estilo “sumário de livro”). O conteúdo do estudo fica em `book/`, organizado nas mesmas pastas da raiz.

- **01.** [Introdução](book/introduction.md)

- **Princípios**
	- **02.** [DRY](book/principles/dry.md)
	- **03.** [KISS](book/principles/kiss.md)
	- **04.** [SOLID](book/principles/solid.md)
	- **05.** [OCP](book/principles/ocp.md)
	- **06.** [Separation Of Concerns](book/principles/separation-of-concerns.md)
	- **07.** [Tell, Don't Ask](book/principles/tell-dont-ask.md)
	- **08.** [Law Of Demeter](book/principles/law-of-demeter.md)
	- **09.** [Composition Over Inheritance](book/principles/composition-over-inheritance.md)
	- **10.** [Design For Testability](book/principles/design-for-testability.md)
	- **11.** [Fail Fast](book/principles/fail-fast.md)
	- **12.** [YAGNI](book/principles/yagni.md)

- **Arquitetura**
	- **13.** [Hexagonal Architecture](book/archtecture/hexagonal-architecture.md)
	- **14.** [Onion Architecture](book/archtecture/onion-architecture.md)
	- **15.** [Clean Architecture](book/archtecture/clean-architecture.md)
	- **16.** [Atributos de Qualidade (NFRs) e Trade-offs](book/archtecture/quality-attributes-and-trade-offs.md)
	- **17.** [C4 Model & Diagramas](book/archtecture/c4-model-and-diagrams.md)
	- **18.** [Modular Monolith](book/archtecture/modular-monolith.md)
	- **19.** [Arquitetura Evolutiva (Fitness Functions)](book/archtecture/evolutionary-architecture-fitness-functions.md)
	- **20.** [Strangler Fig e Padrões de Migração](book/archtecture/strangler-fig-and-migration-patterns.md)
	- **21.** [ADRs (Architecture Decision Records)](book/archtecture/architecture-decision-records-adrs.md)
	- **22.** [Architecture Reviews & Guardrails](book/archtecture/architecture-reviews-guardrails.md)
	- **23.** [Sistemas Distribuídos na Prática](book/archtecture/distributed-systems-in-practice.md)
	- **24.** [Integrações: Sync vs Async](book/archtecture/integration-architectures-sync-async.md)
	- **25.** [API Design & Versionamento](book/archtecture/api-design-versioning-contracts.md)
	- **26.** [Contratos de Eventos (Schema Evolution)](book/archtecture/event-contracts-schema-evolution.md)
	- **27.** [Arquitetura de Dados (Ownership)](book/archtecture/data-architecture-ownership-and-modeling.md)
	- **28.** [Migrações de Dados (Backfills/CDC)](book/archtecture/data-migrations-backfills-and-cdc.md)
	- **29.** [Confiabilidade (SRE): SLOs e Error Budgets](book/archtecture/reliability-sre-slos-error-budgets.md)
	- **30.** [Observabilidade na Arquitetura](book/archtecture/observability-architecture.md)
	- **31.** [Performance & Capacity Planning](book/archtecture/performance-and-capacity-planning.md)
	- **32.** [Custo em Arquitetura (FinOps)](book/archtecture/cost-architecture-finops.md)
	- **33.** [Arquitetura de Segurança (Threat Modeling)](book/archtecture/security-architecture-threat-modeling.md)
	- **34.** [Identidade & Autorização (Authn/Authz)](book/archtecture/identity-authz-architecture.md)
	- **35.** [Multi-tenancy e Isolamento](book/archtecture/multi-tenancy-and-isolation.md)
	- **36.** [Team Topologies & Conway’s Law](book/archtecture/team-topologies-and-conway-law.md)
	- **37.** [Platform Engineering (Golden Paths)](book/archtecture/platform-engineering-golden-paths.md)
	- **38.** [Liderança Técnica (Staff/Architect)](book/archtecture/technical-leadership-for-architects.md)

- **Domain-Driven Design**
	- **39.** [Domain-Driven Design (DDD)](book/domain/ddd.md)

- **Design Patterns**
	- **40.** [Adapter](book/design-patterns/adapter.md)
	- **41.** [Bridge](book/design-patterns/bridge.md)
	- **42.** [Builder](book/design-patterns/builder.md)
	- **43.** [Chain Of Responsibility](book/design-patterns/chain-of-responsibility.md)
	- **44.** [Command](book/design-patterns/command.md)
	- **45.** [Composite](book/design-patterns/composite.md)
	- **46.** [Decorator](book/design-patterns/decorator.md)
	- **47.** [Facade](book/design-patterns/facade.md)
	- **48.** [Factory](book/design-patterns/factory.md)
	- **49.** [Observer](book/design-patterns/observer.md)
	- **50.** [Proxy](book/design-patterns/proxy.md)
	- **51.** [Singleton](book/design-patterns/singleton.md)
	- **52.** [State](book/design-patterns/state.md)
	- **53.** [Strategy](book/design-patterns/strategy.md)
	- **54.** [Template Method](book/design-patterns/template-method.md)
	- **55.** [Visitor](book/design-patterns/visitor.md)

- **Complexidade & Estruturas de Dados**
	- **56.** [Estruturas de Dados e Big-O](book/complexity/data-structures-and-big-o.md)
	- **57.** [Estruturas de Dados & Algoritmos — Visão Geral Aplicada](book/data-structure/data-structures-algorithms-overview.md)
	- **58.** [Arrays & Strings — Padrões de Algoritmos](book/data-structure/arrays-and-strings.md)
	- **59.** [Listas Encadeadas — Técnicas e Algoritmos](book/data-structure/linked-lists.md)
	- **60.** [Stacks & Queues — Parsing, BFS e Monotonic Stack](book/data-structure/stacks-and-queues.md)
	- **61.** [Hash Tables & Sets — Lookup, Indexação e Caches](book/data-structure/hash-tables-and-sets.md)
	- **62.** [Árvores & BSTs — Traversal, Balanceamento e Decisão Prática](book/data-structure/trees-and-bsts.md)
	- **63.** [Heaps & Priority Queues — Top-K, Scheduling e Medianas](book/data-structure/heaps-and-priority-queues.md)
	- **64.** [Tries & Busca por Prefixo — Autocomplete e Matching](book/data-structure/tries-and-prefix-search.md)
	- **65.** [Grafos — Representação, BFS/DFS, Toposort e SCC](book/data-structure/graphs-representations-and-traversal.md)
	- **66.** [Grafos — Caminhos Mínimos e MST](book/data-structure/shortest-path-and-mst.md)
	- **67.** [Union-Find (DSU) — Conectividade Dinâmica e Kruskal](book/data-structure/union-find-and-connectivity.md)
	- **68.** [Range Queries — Fenwick (BIT), Segment Tree e Sparse Table](book/data-structure/range-queries-fenwick-and-segment-tree.md)
	- **69.** [Caches & Eviction — LRU, LFU, TTL e Cache Stampede](book/data-structure/caches-eviction-lru-lfu.md)
	- **70.** [Consistent Hashing & Sharding — Particionamento com Menos Churn](book/data-structure/consistent-hashing-and-sharding.md)
	- **71.** [Probabilistic Data Structures — Bloom Filter, Sketches e HLL](book/data-structure/probabilistic-data-structures.md)
	- **72.** [Storage Indexes — B Tree, LSM Tree e Inverted Index](book/data-structure/storage-indexes-btree-lsm-inverted.md)
	- **73.** [Queues no Mundo Real — Ring Buffer, Priority Queue e Backpressure](book/data-structure/queues-ring-buffer-backpressure.md)
	- **74.** [Rate Limiting — Token Bucket, Leaky Bucket e Sliding Window](book/data-structure/rate-limiting-algorithms-and-data-structures.md)
	- **75.** [Vector Search — ANN, HNSW e IVF (Relevancia Atual)](book/data-structure/vector-search-ann.md)
	- **76.** [Métricas de Qualidade e Complexidade](book/complexity/code-quality-and-complexity-metrics.md)

- **Concorrência**
	- **77.** [Concorrência e Paralelismo](book/concurrency/concurrency-and-parallelism.md)
	- **78.** [Memory Model & Atomics — Happens-Before e Visibilidade](book/concurrency/memory-model-and-atomics.md)
	- **79.** [Primitivas de Sincronizacao — Locks, Semaforos e Contencao](book/concurrency/synchronization-primitives-and-contention.md)
	- **80.** [Problemas classicos de concorrencia](book/concurrency/classic-concurrency-problems.md)
	- **81.** [Async, Work Queues e Backpressure](book/concurrency/async-concurrency-and-backpressure.md)
	- **82.** [Testes e Debug de Concorrencia](book/concurrency/testing-and-debugging-concurrency.md)

- **Operações Críticas**
	- **83.** [Transações & ACID](book/critical-operations/transactions-acid.md)
	- **84.** [Controle de concorrência em DB](book/critical-operations/db-concurrency-control.md)
	- **85.** [Operacoes Criticas em Pagamentos e Fintech — Visao Geral](book/critical-operations/payments-fintech-overview.md)
	- **86.** [Payment Ledgers — Double Entry, Imutabilidade e Fonte de Verdade](book/critical-operations/payment-ledgers-and-double-entry.md)
	- **87.** [Idempotencia em Pagamentos — Idempotency Key, Dedup e Retries](book/critical-operations/idempotency-keys-and-dedup.md)
	- **88.** [Antifraude em Pagamentos — Risk Checks, Step Up e Revisao Manual](book/critical-operations/antifraud-risk-checks-and-step-up.md)
	- **89.** [Sagas em Pagamentos — Orquestracao, Compensacao e Estados](book/critical-operations/sagas-for-payments.md)
	- **90.** [Transactional Outbox & CDC — Publicacao Confiavel de Eventos](book/critical-operations/transactional-outbox-and-cdc.md)
	- **91.** [Distributed Locks — Leases, Fencing Tokens e Leader Election](book/critical-operations/distributed-locks-leases-fencing.md)
	- **92.** [Reconciliation & Auditabilidade — Fechar Gaps sem Duplicar Efeitos](book/critical-operations/reconciliation-and-auditability.md)

- **Eventos e Filas**
	- **93.** [Filas e Messaging](book/events-and-queues/queues-and-messaging.md)
	- **94.** [Consistência distribuída](book/events-and-queues/distributed-consistency.md)

- **Escalabilidade**
	- **95.** [Caching Strategies](book/scalability/caching-strategies.md)
	- **96.** [Arquitetura orientada a eventos](book/scalability/event-driven-architecture.md)
	- **97.** [CQRS](book/scalability/cqrs.md)
	- **98.** [Event Sourcing](book/scalability/event-sourcing.md)
	- **99.** [Microservices Best Practices](book/scalability/microservices-best-practices.md)

- **Cloud**
	- **100.** [Cloud Native Patterns](book/cloud/cloud-native-patterns.md)
	- **101.** [Security Best Practices](book/cloud/security-best-practices.md)

- **Missão Crítica**
	- **102.** [High Availability & Fault Tolerance](book/mission-critical/high-availability-fault-tolerance.md)

- **Testes**
	- **103.** [TDD](book/tests/tdd.md)
	- **104.** [BDD](book/tests/bdd.md)
	- **105.** [Unit Testing](book/tests/unit-testing.md)

- **Carreira**
	- **106.** [System Design Interview](book/career/system-design-interview.md)
	- **107.** [Code Review & Collaboration](book/career/code-review-collaboration.md)

- **Tecnologias**
	- **108.** [Docker](book/technologies/docker.md)
	- **109.** [Kubernetes](book/technologies/kubernetes.md)
	- **110.** [Terraform](book/technologies/terraform.md)
	- **111.** [Ansible](book/technologies/ansible.md)
	- **112.** [C#](book/technologies/csharp.md)
	- **113.** [Golang](book/technologies/golang.md)
	- **114.** [Linux](book/technologies/linux.md)
	- **115.** [GitHub Actions (CI/CD)](book/technologies/github-actions.md)
	- **116.** [Observability (Prometheus/Grafana)](book/technologies/observability-prometheus-grafana.md)
	- **117.** [Kafka](book/technologies/kafka.md)
	- **118.** [PostgreSQL](book/technologies/postgresql.md)

- **Anexos**
	- **119.** [Template de Documentação (GitHub)](.github/DOCUMENTATION_TEMPLATE.md)
