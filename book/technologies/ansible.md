[Anterior](terraform.md) | [Índice](../../SUMMARY.md) | [Próximo](csharp.md)

# Ansible — Automação, Configuração e Operação Idempotente (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Ansible é uma ferramenta de automação para **configuração**, **deploy** e **operações** baseada em playbooks declarativos (YAML) e execução via SSH/WinRM. No mercado, ele aparece muito em:

- Provisionamento e configuração de VMs (quando não é Kubernetes).
- Rotinas de operação (patching, hardening, setup de serviços).
- Padronização de servidores (evitar “snowflakes”).

O ponto sênior: o valor vem da **idempotência** e de playbooks legíveis/versões revisáveis, não de “scripts gigantes”.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Inventory**: grupos/hosts e variáveis por ambiente.
- **Roles**: modularização e reuso.
- **Idempotência**: rodar N vezes e chegar no mesmo estado final.
- **Handlers**: ações disparadas quando houve mudança (ex.: restart serviço).

Padrões:

- Roles pequenas e composáveis.
- Separação de vars por ambiente e uso de `ansible-vault` (ou integração com secret manager).

---

## Principais Desafios no Uso Profissional

- **Drift e snowflakes**: sem padronização, cada host vira único.
- **Segredos**: vazamento em vars/logs.
- **Escala**: execuções longas e paralelismo mal configurado.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Modelar por papéis (roles) e invariantes**
	- “O que é um servidor web?” vs “rodar este script”.
	- Evite tarefas que dependam de estado implícito.

- **Testabilidade**
	- Molecule para testar roles.
	- Linters (`ansible-lint`) e CI.

---

## Exemplos Avançados (playbook mínimo)

```yaml
- name: Configure web
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

---

## Boas Práticas Sêniores e Armadilhas

- Evite `shell`/`command` quando existir módulo idempotente.
- Use `check mode` para previsibilidade (quando possível).
- Mantenha inventário e vars sob controle (separação por env).
- Cuidado com `become` global: aplique privilégio mínimo.

---

## Integração na Arquitetura Real

- Em ambientes com Kubernetes, Ansible continua útil para “infra ao redor”: nodes/VMs, hardening, bootstrap.
- Integração com pipelines: rodar playbooks com aprovação e logs auditáveis.

---

## Métricas, Monitoramento e Melhoria Contínua

- Tempo de execução e taxa de falhas por playbook.
- Frequência de mudanças manuais (indicador de drift).
- Cobertura de roles (quanto está automatizado vs manual).

---

## Frameworks e Ferramentas do Mercado

- `ansible-lint`, Molecule.
- `ansible-vault` (ou secret manager externo).
- AWX/Ansible Tower para execução e auditoria.

---

## Recursos Avançados e Leituras Recomendadas

- Documentação oficial do Ansible (roles, inventories, idempotência).
- Práticas de hardening e execução com auditoria (AWX/Tower).

---

## FAQ Especialista

**Quando usar Ansible vs Terraform?**  
Terraform para provisionar recursos (infra). Ansible para configurar/operar o OS e serviços dentro de hosts (configuração).

**Idempotência é automática?**  
Não. Depende de usar módulos corretos e modelar o estado desejado.

---

## Referências e Práticas do Mercado

- Ansible docs, ansible-lint, Molecule

---

[Anterior](terraform.md) | [Índice](../../SUMMARY.md) | [Próximo](csharp.md)
