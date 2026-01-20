[Anterior](golang.md) | [Índice](../../SUMMARY.md) | [Próximo](github-actions.md)

# Linux — Operação, Performance e Debug em Produção (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Linux é o sistema operacional dominante em servidores e cloud. Para engenharia sênior, Linux é menos “comandos” e mais **modelo mental operacional**: processos, memória, filesystem, rede, permissões e observabilidade.

No mercado, dominar Linux acelera:

- Debug de incidentes (latência, erros intermitentes, saturação).
- Entendimento de containers/Kubernetes (namespaces, cgroups, networking).
- Otimização e troubleshooting de aplicações.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Processos e signals**: lifecycle, SIGTERM/SIGKILL, zombie/orphan.
- **Memória**: RSS/VSZ, page cache, swap, OOM killer.
- **Filesystem**: permissões, ownership, mounts, inode, journaling.
- **Rede**: sockets, DNS, routing, MTU, conexões e TIME_WAIT.

---

## Principais Desafios no Uso Profissional

- **"Funciona no dev"**: diferenças de kernel, libc, limites de ulimit e cgroups.
- **Debug sob pressão**: encontrar sinal útil em meio a ruído.
- **Permissões**: problemas de file permissions, capabilities e SELinux/AppArmor.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Torne o sistema observável**
	- Logs estruturados + métricas e traces.
	- Dashboards baseados em sintomas (latência, erros, saturação).

- **Debug por hipóteses**
	- Comece pelo “o que mudou?” e pelo caminho do request.
	- Separe: CPU vs IO vs rede vs lock contention.

---

## Exemplos Avançados (comandos essenciais)

- Processos: `ps aux`, `top`, `htop`, `pidstat`, `kill -TERM`.
- Arquivos: `ls -la`, `df -h`, `du -sh`, `lsof`.
- Rede: `ss -tupn`, `dig`, `curl -v`, `tcpdump`.
- Sistema: `dmesg`, `journalctl`, `free -m`, `vmstat`.

---

## Boas Práticas Sêniores e Armadilhas

- Prefira shutdown gracioso (SIGTERM) e respeite timeouts.
- Cuidado com “reiniciar resolve”: trate causa raiz.
- Entenda limites: file descriptors, threads, sockets.

---

## Integração na Arquitetura Real

- Em containers: observe cgroups/limits e diferenças de filesystem.
- Em Kubernetes: debug inclui `kubectl exec/logs/describe` + sinais do node.

---

## Métricas, Monitoramento e Melhoria Contínua

- CPU (user/system/iowait), memória (RSS, page faults), IO (latência de disco), rede (RTT, retransmits).
- Taxa de OOMKilled e throttling por cgroups.

---

## Frameworks e Ferramentas do Mercado

- Observabilidade: eBPF tools (quando disponível), perf, strace.
- Gestão: systemd, journald.

---

## Recursos Avançados e Leituras Recomendadas

- Brendan Gregg (performance), guias de Linux observability.
- Documentação sobre cgroups/namespaces.

---

## FAQ Especialista

**Por que OOM acontece com memória “livre”?**  
Porque page cache conta como “usável” e porque limites de cgroup podem ser menores que a memória do host.

---

## Referências e Práticas do Mercado

- Linux performance tooling e guias de troubleshooting

---

[Anterior](golang.md) | [Índice](../../SUMMARY.md) | [Próximo](github-actions.md)
