[Anterior](cloud-native-patterns.md) | [Índice](../../SUMMARY.md) | [Próximo](../mission-critical/high-availability-fault-tolerance.md)

# Security Best Practices for Distributed Systems — Guia Avançado

## Visão Geral e Contexto de Mercado

Segurança em sistemas distribuídos não é um “checklist final”; é um conjunto de controles contínuos ao longo do ciclo de vida (SDLC), com responsabilidade compartilhada entre time e plataforma. Em empresas modernas (CI/CD, microserviços, cloud), segurança precisa ser:

- **Shift-left** (detectar cedo: PR/CI)
- **Defesa em profundidade** (camadas: app, infra, rede, identidade)
- **Observável e auditável** (logs, trilhas, alertas)
- **Pragmática** (proporcional ao risco e ao domínio)

O mercado amadureceu para modelos como Zero Trust, policy-as-code e integração forte com pipelines, porque incidentes são caros (reputação, compliance, paralisação, multas).

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	Segurança em distribuídos evoluiu de perímetro (firewall) para identidade e contexto (Zero Trust). Com cloud, a superfície de ataque inclui IAM, secrets, supply chain e configurações. Hoje o foco é reduzir blast radius, automatizar controles e responder rápido.

- **Padrões e Protocolos Usados no Mercado**
	- **Zero Trust:** nunca confie por rede; valide identidade e contexto.
	- **AuthN/AuthZ:** OAuth2/OIDC, JWT (com cuidado), mTLS.
	- **Criptografia:** TLS em trânsito; KMS/Key Vault em repouso.
	- **Secrets management:** Secret Manager/Key Vault/Vault.
	- **Supply chain:** SBOM (SPDX/CycloneDX), assinatura (cosign), SLSA.
	- **Policy-as-code:** OPA/Gatekeeper, Azure Policy.
	- **OWASP:** Top 10, ASVS (boas referências).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	Em múltiplos serviços, a consistência de controles é difícil: cada time pode implementar auth/logs/segredos de um jeito. Plataformas e templates (golden paths) ajudam.

- **Performance e Manutenção**  
	- Autenticação e criptografia têm custo; precisa de caching e tuning.
	- Rotação de chaves/certificados pode quebrar serviços se não houver automação.
	- Observabilidade de segurança (SIEM) exige padronização de logs.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: permissões amplas (admin), secrets em env sem rotação, tokens long-lived.
	- Coverage: falta de testes para authz (quem pode fazer o quê) é comum.
	- Flakiness: scanners e DAST em pipelines podem ser instáveis sem controle de ambiente.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- SAST e dependency scanning em PR.
	- Secrets scanning no repo.
	- IaC scanning (Terraform/ARM) e policy-as-code.
	- Deploy com attestation/assinatura de artefatos.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit tests para regras de autorização.
	- Integration tests para fluxos de auth (OIDC) em ambiente controlado.
	- DAST seletivo (nightly) para reduzir custo/instabilidade.

- **Métrica de Qualidade**  
	- MTTR de vulnerabilidades (tempo para corrigir)
	- % de serviços com least privilege e rotação de secrets
	- Taxa de incidentes e near-misses
	- Cobertura de controles (SAST/DAST/IaC)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: validação de JWT (conceitual) e checagem de autorização. Em produção, prefira bibliotecas robustas e validação completa (issuer, audience, exp, nbf, kid, rotação de chaves).

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
		subject: str
		roles: set[str]


def can_access_admin(principal: Principal) -> bool:
		return "admin" in principal.roles
```

### C#

```csharp
public sealed record Principal(string Subject, IReadOnlySet<string> Roles);

public static class Authorization
{
		public static bool CanAccessAdmin(Principal p)
				=> p.Roles.Contains("admin");
}
```

### Go

```go
package authz

type Principal struct {
		Subject string
		Roles   map[string]bool
}

func CanAccessAdmin(p Principal) bool {
		return p.Roles["admin"]
}
```

---

## Boas Práticas Sêniores e Armadilhas

- **Least privilege por workload:** IAM por serviço/namespace, não por humano.
- **Segredos fora do repositório:** use Secret Manager/Key Vault e rotação.
- **TLS everywhere:** preferencialmente com mTLS em comunicação serviço-a-serviço.
- **Idempotência e rate limiting:** protegem contra replay e abuso.
- **Logs estruturados e auditáveis:** sem dados sensíveis (PII) indevidos.
- **Threat modeling leve:** por feature crítica (pagamento, auth, dados sensíveis).
- **Supply chain:** fixe versões, SBOM, assinatura de imagens.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** security contexts, network policies, admission control, secrets via CSI.
- **Pipelines CI/CD:** scanners em PR, policy-as-code, deploy com assinatura e provenance.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** SIEM, alertas, detecção de anomalias.
- **Testes e Infra-as-Code:** IaC scanning, drift detection e auditoria.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo para corrigir vulnerabilidades (SLA por severidade)
- Cobertura de serviços com rotação de segredos e least privilege
- Incidentes/near-misses por trimestre
- Alert fatigue (qualidade dos alertas)

---

## Frameworks e Ferramentas do Mercado

- **Python:** bandit, pip-audit, safety, opentelemetry
- **C#:** .NET analyzers, dotnet list package --vulnerable, OpenTelemetry
- **Go:** govulncheck, staticcheck, OpenTelemetry
- **Ferramentas de integração:** Snyk/Dependabot, Trivy, Semgrep, OPA/Gatekeeper, Vault

---

## Recursos Avançados e Leituras Recomendadas

- OWASP ASVS / OWASP Top 10
- NIST (SP 800-53 / Zero Trust)
- Cloud provider security best practices (AWS/Azure/GCP)

---

## FAQ Especialista

**JWT resolve tudo?**  
Não. JWT é um mecanismo. Segurança depende de validação correta, rotação de chaves, expiração curta, revogação quando necessário e autorização consistente.

**Onde colocar autorização (authz)?**  
O ideal é centralizar políticas e padronizar (ex.: middleware + policy engine), mas regras de domínio críticas às vezes precisam estar no core (ex.: “quem pode aprovar X”).

**Como evitar que segurança vire gargalo?**  
Golden paths, automação (policy-as-code), e padrões de plataforma reduzem fricção sem perder controle.

---

## Referências e Práticas do Mercado

- OWASP
- NIST
- Google SRE / práticas de segurança operável

---

[Anterior](cloud-native-patterns.md) | [Índice](../../SUMMARY.md) | [Próximo](../mission-critical/high-availability-fault-tolerance.md)
