[Anterior](docker.md) | [Índice](../../SUMMARY.md) | [Próximo](terraform.md)

# Kubernetes — Orquestração, Operação e Padrões de Plataforma (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Kubernetes é o padrão de facto para orquestrar workloads containerizados. No mercado, ele aparece quando há necessidade de:

- Escalar horizontalmente com automação.
- Padronizar deploy, networking e observabilidade em múltiplos serviços.
- Reduzir acoplamento com infraestrutura específica (multi-cluster / multi-cloud).

O ponto sênior: Kubernetes não "resolve" complexidade — ele **muda** a complexidade de lugar. Um cluster sem padrões vira um sistema distribuído caótico.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Pod**: menor unidade de execução; um ou mais containers co-localizados.
- **Deployment/ReplicaSet**: desired state + rollout.
- **Service**: abstração estável para discovery/load-balancing.
- **Ingress/Gateway**: entrada HTTP; em setups modernos, Gateway API vem ganhando tração.
- **ConfigMap/Secret**: configuração; secrets exigem disciplina (criptografia, rotação, acesso mínimo).

Padrões comuns:

- Namespaces por domínio/ambiente (com RBAC e quotas).
- Rollouts com readiness/liveness bem definidos.
- Policy-as-code (OPA/Gatekeeper, Kyverno) e padrões de segurança.

---

## Principais Desafios no Uso Profissional

- **Debuggabilidade**
	- Falhas intermitentes (rede, DNS, HPA, throttling) exigem observabilidade.
	- Diferença entre readiness vs liveness mal configurada causa flapping.

- **Custo e capacidade**
	- Requests/limits mal ajustados geram desperdício ou OOM.
	- Autoscaling sem métricas corretas degrada latência.

- **Segurança**
	- RBAC permissivo demais.
	- Exec como root, filesystem writeable, capabilities excessivas.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Defina um "golden path"**
	- Base charts/templates (Helm/Kustomize) para serviços.
	- Sidecars e padrões de observabilidade (ou service mesh) com critério.

- **SLO-first**
	- HPA baseado em sinais ligados ao SLO (p95 latency, queue depth) quando possível.
	- PodDisruptionBudget + topology spread para resiliência.

- **Segurança por padrão**
	- SecurityContext (non-root, drop capabilities, seccomp), NetworkPolicies.
	- Admission policies para impedir manifests perigosos.

---

## Exemplos Avançados (manifest mínimo “production-ish”)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:1.2.3
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
```

---

## Boas Práticas Sêniores e Armadilhas

- `requests/limits`: comece conservador e ajuste com dados reais.
- Evite depender de IPs; dependa de Service/DNS.
- Use `terminationGracePeriodSeconds` e trate SIGTERM corretamente.
- Faça rollback simples (releases versionadas) e mantenha deploys pequenos.

---

## Integração na Arquitetura Real

- CI/CD publica imagem assinada + manifesta/helm chart versionado.
- Observabilidade: métricas (Prometheus), logs centralizados, traces (OTel).
- Segurança: RBAC mínimo, políticas, scanning de imagens e manifests.

---

## Métricas, Monitoramento e Melhoria Contínua

- Taxa de rollout falho/rollback.
- p95/p99 de latência + saturação de CPU/mem.
- CrashLoopBackOff e motivos (OOMKilled, readiness falhando, etc.).
- Custo por namespace/time (showback/chargeback).

---

## Frameworks e Ferramentas do Mercado

- Manifests: Helm, Kustomize.
- Observabilidade: Prometheus/Grafana, Loki/ELK, Jaeger/Tempo.
- Policy: OPA/Gatekeeper, Kyverno.
- GitOps: Argo CD, Flux.

---

## Recursos Avançados e Leituras Recomendadas

- Documentação oficial do Kubernetes (probes, resources, scheduling).
- SRE: SLOs, error budgets e operação de mudanças.

---

## FAQ Especialista

**Service mesh é obrigatório?**  
Não. Ajuda em alguns casos (mTLS, traffic shifting), mas aumenta complexidade. Use quando o problema justificar.

**Por que minha aplicação fica instável em produção e estável local?**  
Normalmente por recursos, probes, DNS/rede, ou dependências externas mais lentas. Observabilidade é essencial.

---

## Referências e Práticas do Mercado

- Kubernetes docs, CNCF landscape
- Padrões SRE (SLOs) aplicados a clusters

---

[Anterior](docker.md) | [Índice](../../SUMMARY.md) | [Próximo](terraform.md)
