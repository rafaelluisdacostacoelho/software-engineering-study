[Anterior](kubernetes.md) | [Índice](../../SUMMARY.md) | [Próximo](ansible.md)

# Terraform — Infra-as-Code com State, Módulos e Governança (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Terraform é uma ferramenta de **infra-as-code declarativa** para provisionar recursos em cloud e em provedores diversos. No mercado, o valor real está em:

- Reprodutibilidade de ambientes (dev/stage/prod).
- Revisões via PR e rastreabilidade de mudanças.
- Padronização por módulos (evita “infra artesanal”).

O ponto sênior: o risco principal é o **state** (e a governança em torno dele). Sem disciplina, mudanças viram incidentes.

---

## Fundamentos, Evolução e Padrões de Mercado

- **State**: fonte de verdade do que foi provisionado; precisa ser remoto, versionado e com locking.
- **Plan/Apply**: fluxo de mudança; `plan` deve ser revisado como artefato.
- **Módulos**: encapsulam padrões; reduzem duplicação e variabilidade.
- **Providers**: integração com APIs; upgrades exigem cuidado.

Padrões:

- Backend remoto (S3+DynamoDB, GCS, Azure Storage) + locking.
- Workspaces ou (preferível em escala) stacks separadas por env.
- `terraform fmt` + validação/scan em CI.

---

## Principais Desafios no Uso Profissional

- **Drift**: mudanças manuais no console geram diferença entre real e código.
- **Blast radius**: um apply “inocente” pode destruir recursos se o estado/modelagem estiver errado.
- **Segredos**: variáveis sensíveis e outputs podem vazar no state.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Estruture por camadas/stacks**
	- Separar rede/fundação de apps diminui blast radius.
	- Outputs explícitos entre stacks (com cuidado) e contratos claros.

- **Módulos com interface pequena**
	- Poucos inputs bem definidos.
	- Defaults seguros + validação (`validation` blocks).

- **Pipelines com guardrails**
	- `plan` como artefato anexado ao PR.
	- `apply` restrito, com aprovação e ambiente controlado.

---

## Exemplos Avançados (módulo mínimo)

```hcl
terraform {
  required_version = ">= 1.6.0"
}

variable "env" {
  type        = string
  description = "Environment name (dev/stage/prod)"
  validation {
    condition     = contains(["dev", "stage", "prod"], var.env)
    error_message = "env must be dev, stage, or prod"
  }
}

locals {
  tags = {
    env   = var.env
    owner = "platform"
  }
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Nunca use state local em time; use backend remoto e locking.
- Evite `-target` (quebra invariantes de dependência); use só em incidentes e com entendimento.
- Evite dependências cíclicas entre módulos; trate outputs como contrato.
- Proteja recursos críticos com `prevent_destroy` quando fizer sentido.

---

## Integração na Arquitetura Real

- GitOps/PR: alterações de infra passam por review.
- CI roda `fmt`, `validate`, `plan`; CD (ou job manual) faz `apply`.
- Integração com Kubernetes via providers (ou via Argo/Flux para manifests).

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de ciclo de mudanças de infra.
- Incidentes por drift ou apply mal revisado.
- Cobertura de módulos (percentual de infra padronizada vs artesanal).

---

## Frameworks e Ferramentas do Mercado

- Lint/scan: `tflint`, `checkov`, `tfsec`.
- State/backends: S3+DynamoDB, GCS, Azure Storage.
- Terragrunt: pode ajudar organização, mas adiciona camada (use com critério).

---

## Recursos Avançados e Leituras Recomendadas

- HashiCorp docs (state, workspaces, modules).
- Boas práticas de platform engineering (guardrails, blast radius).

---

## FAQ Especialista

**Por que drift é tão perigoso?**  
Porque o Terraform passa a operar em cima de suposições erradas e pode destruir/recriar recursos inesperadamente.

**Workspaces resolvem tudo?**  
Não. Em muitos times, separar diretórios/stacks por ambiente simplifica governança e auditoria.

---

## Referências e Práticas do Mercado

- HashiCorp Terraform docs
- Scanners e práticas de review de IaC

---

[Anterior](kubernetes.md) | [Índice](../../SUMMARY.md) | [Próximo](ansible.md)
