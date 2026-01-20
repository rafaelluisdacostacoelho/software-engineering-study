[Índice](../../SUMMARY.md) | [Próximo](kubernetes.md)

# Docker — Imagens, Containers e Ambientes Reprodutíveis (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Docker popularizou um modelo simples e poderoso: **empacotar uma aplicação + dependências** em uma imagem imutável e rodá-la de forma consistente em qualquer host compatível. No mercado, Docker é usado para:

- Padronizar ambientes de dev/CI ("works on my machine" vira raro).
- Simplificar deploy (artefato único, versionado).
- Viabilizar orquestração (Kubernetes roda containers; o artefato é a imagem).

O ponto sênior: Docker não é só comando; é **produto operacional**. Um Dockerfile ruim gera imagens enormes, builds lentos, CVEs, segredos vazados e incidentes difíceis de diagnosticar.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Imagem vs container**: imagem é o artefato imutável; container é a execução com filesystem copy-on-write.
- **Layering e cache**: cada instrução do Dockerfile vira layer; ordem importa para cache e tempo de build.
- **OCI**: padrão de runtime/imagem; Docker hoje é mais uma implementação do ecossistema.
- **BuildKit**: builds mais rápidos, cache avançado e suporte a secrets no build.

Padrões práticos comuns:

- Multi-stage build para separar build-time de runtime.
- Imagens mínimas (distroless/alpine com cuidado) + usuários não-root.
- Tags imutáveis por SHA (evitar depender de `latest`).

---

## Principais Desafios no Uso Profissional

- **Segurança e supply chain**
	- Base image desatualizada e com CVEs.
	- Segredos no build (tokens em `RUN`, `.npmrc`, `.pypirc`) indo para layers.
	- Dependência de registries sem assinatura/verificação.

- **Reprodutibilidade**
	- Builds não determinísticos (downloads sem pinning, `apt-get` sem versões).
	- Dependência de `latest` e tags móveis.

- **Performance e custo**
	- Imagens grandes aumentam tempo de pull e custo de storage/egress.
	- Cache ruim explode o tempo de CI.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Defina o que é "runtime"**
	- O runtime deve conter só o necessário para executar.
	- Ferramentas de build e dev ficam no stage de build.

- **Padronize via golden images / templates**
	- Um template por stack (Go, .NET, Node, Python) reduz variação e risco.
	- Centralize hardening (user não-root, healthcheck, labels, SBOM).

- **Separação de config**
	- Config via env vars/volumes/secrets (não bake em imagem).
	- Para Kubernetes, evite acoplar o container ao ambiente (paths e permissões consistentes).

---

## Exemplos Avançados (Dockerfile e Compose)

### Multi-stage (exemplo em Go)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12
WORKDIR /
COPY --from=build /out/app /app
USER 65532:65532
ENTRYPOINT ["/app"]
```

### Compose (dev local)

```yaml
services:
  app:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/app
    ports:
      - "8080:8080"
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
```

---

## Boas Práticas Sêniores e Armadilhas

- Evite `ADD` (prefira `COPY`) e evite `curl | bash` sem pinning.
- Junte `apt-get update` e `apt-get install` no mesmo `RUN` e limpe cache.
- Use `.dockerignore` (reduz contexto, build mais rápido, menos vazamento acidental).
- Nunca rode como root por padrão (a menos que exista razão operacional forte).
- Healthcheck: pense em readiness/liveness no Kubernetes; no Docker isolado, `HEALTHCHECK` pode ajudar.

---

## Integração na Arquitetura Real

- **CI/CD**: build (com cache), scan (CVE/SBOM), assinatura, push, deploy.
- **Observabilidade**: logs em stdout/stderr; métricas via endpoint; traces com propagação de contexto.
- **Runtime**: limites de CPU/memória e comportamento em OOM (especialmente em Kubernetes).

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo médio de build e taxa de cache hit.
- Tamanho de imagem (MB) e tempo de pull (p95).
- CVEs abertas por severidade e tempo para remediação.
- Falhas por permissão (rodar como não-root) e por filesystem read-only.

---

## Frameworks e Ferramentas do Mercado

- Build: BuildKit, `docker buildx`, caching remoto.
- Security: Trivy/Grype, SBOM (Syft), assinatura (cosign), SLSA.
- Registry: GHCR, ECR, GCR/Artifact Registry, ACR.

---

## Recursos Avançados e Leituras Recomendadas

- OCI Image Spec (conceitos de camadas e manifest).
- Dockerfile best practices (hardening, caching, multi-stage).
- Supply chain security: SBOM + assinatura + verificação no deploy.

---

## FAQ Especialista

**Alpine é sempre melhor?**  
Não. Pode reduzir tamanho, mas pode introduzir diferenças (musl vs glibc), e debugging pode ficar difícil. Use quando fizer sentido e com padronização.

**`latest` é problema?**  
Sim, porque é uma tag móvel. Use tags imutáveis (ou SHA) em produção.

---

## Referências e Práticas do Mercado

- Docker / OCI specs e guias de hardening
- Práticas de supply chain (SBOM, assinatura, verificação)

---

[Índice](../../SUMMARY.md) | [Próximo](kubernetes.md)
