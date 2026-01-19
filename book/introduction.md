[Índice](../SUMMARY.md) | [Próximo](principles/dry.md)

# Introdução

## Visão Geral e Contexto de Mercado

Este repositório é um “book” de engenharia de software: princípios, arquitetura, padrões, escalabilidade, cloud, concorrência, testes e operação. Ele foi pensado para uso prático no dia a dia (code reviews, design discussions, incidentes e system design), com uma ordem de leitura e navegação consistentes.

Na prática do mercado, times de engenharia precisam equilibrar:

- velocidade de entrega vs. qualidade e previsibilidade
- mudança constante de requisitos vs. estabilidade de sistemas
- escala organizacional (múltiplos squads) vs. consistência técnica

O objetivo aqui é consolidar conceitos essenciais com profundidade suficiente para decisões reais, incluindo trade-offs, integração com CI/CD e exemplos em Python/C#/Go.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	A engenharia de software evoluiu de “entregar features” para operar produtos digitais 24/7 com confiabilidade, segurança e governança. O que era “boa prática” isolada virou disciplina operacional: observabilidade, pipelines automatizados, arquitetura orientada a mudanças e qualidade contínua.

- **Padrões e Protocolos Usados no Mercado**
	- Git + code review, trunk-based ou GitFlow (dependendo do contexto)
	- CI/CD com gates automatizados (testes, linters, SAST)
	- Observabilidade (metrics/logs/traces) e SLOs
	- Design patterns e princípios para reduzir custo de mudança

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O principal desafio é aplicar princípios de forma consistente em uma base de código grande e distribuída: sem governança e automação, a dívida técnica cresce mais rápido do que a capacidade de refatorar.

- **Performance e Manutenção**  
	Sistemas reais acumulam integrações, exceções e casos de borda. A manutenção se torna o custo dominante. A documentação precisa refletir esse cenário e não apenas “exemplos didáticos”.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	Falta de testes determinísticos e observabilidade torna mudanças arriscadas. Debt sem visibilidade vira incidentes recorrentes.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Use o book para guiar padrões de PR: testabilidade, acoplamento, tratamento de erro.
	- Crie checklists de revisão por tema (ex.: observabilidade, idempotência, caches).

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: validar regras e invariantes
	- Integração: dependências externas (DB, filas, HTTP)
	- E2E: fluxos críticos

- **Métrica de Qualidade**  
	- Lead time e change failure rate
	- MTTR, incident count, SLO compliance
	- Flaky rate e tempo de pipeline

---

## Exemplos Avançados (Python, C# e Go)

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
		topic: str
		tradeoff: str
		decision: str


def record_decision(topic: str, tradeoff: str, decision: str) -> Decision:
		return Decision(topic=topic, tradeoff=tradeoff, decision=decision)
```

### C#

```csharp
public sealed record Decision(string Topic, string Tradeoff, string Decision);

public static Decision Record(string topic, string tradeoff, string decision)
		=> new(topic, tradeoff, decision);
```

### Go

```go
package docs

type Decision struct {
		Topic    string
		Tradeoff string
		Decision string
}

func Record(topic, tradeoff, decision string) Decision {
		return Decision{Topic: topic, Tradeoff: tradeoff, Decision: decision}
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Leia o sumário como “trilha” de estudo, mas use como referência em problemas reais.
- Evite dogmas: princípios precisam de contexto (time, produto, risco, escala).
- Trate incidentes como feedback: cada capítulo deve ajudar a evitar a repetição de falhas.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** os temas de cloud, observabilidade e resiliência refletem execução real em produção.
- **Pipelines CI/CD:** os capítulos priorizam decisões testáveis e automatizáveis.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** use os capítulos como base para gates e padrões.
- **Testes e Infra-as-Code:** recomendações focam em repetibilidade e ambientes efêmeros.

---

## Métricas, Monitoramento e Melhoria Contínua

- Métricas de entrega (DORA)
- Qualidade (complexidade, bugs, cobertura útil)
- Operação (SLO, MTTR, alert fatigue)

---

## Frameworks e Ferramentas do Mercado

- GitHub Actions/Azure DevOps/Jenkins
- SonarQube/SonarCloud
- OpenTelemetry + Prometheus/Grafana

---

## Recursos Avançados e Leituras Recomendadas

- Accelerate (Forsgren/Humble/Kim)
- Site Reliability Engineering (Google)
- Continuous Delivery (Humble/Farley)

---

## FAQ Especialista

**Por onde começar?**  
Siga a ordem do [Sumário](../SUMMARY.md) e foque nos princípios + testes antes de padrões avançados.

**Como usar isso no trabalho?**  
Use como checklist em PR e referência em design docs e incident reviews.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Índice](../SUMMARY.md) | [Próximo](principles/dry.md)
