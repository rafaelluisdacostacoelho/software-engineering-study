[Anterior](FailFast.md) | [Índice](../../SUMMARY.md) | [Próximo](../archtecture/hexagonal-architecture.md)

# YAGNI — You Aren’t Gonna Need It (Evite Construir o que Não É Necessário) (Princípio)

## Visão Geral e Contexto de Mercado

YAGNI recomenda não construir funcionalidades, abstrações ou generalizações antes de precisar delas. Em ambientes de produto, requisitos mudam — “preparar para o futuro” frequentemente vira dívida técnica.

No mercado, YAGNI protege:

- foco (entregar valor real primeiro)
- previsibilidade (menos caminhos e combinações)
- velocidade (menos manutenção de features não usadas)

YAGNI não é “não planejar”: é planejar com opções reversíveis e entregar incrementalmente.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	YAGNI vem do XP. O aprendizado central: otimizações e abstrações prematuras custam caro porque ampliam surface area sem feedback real.

- **Padrões e Protocolos Usados no Mercado**
	- **MVP e incrementos:** entregar fatias verticais.
	- **Refatoração contínua:** manter design limpo sem antecipar tudo.
	- **Feature flags:** lançar sem expor para todos.
	- **Evolutionary architecture:** decisões reversíveis sempre que possível.

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	“Preparar para N variações” cria matriz de teste enorme. Sem necessidade real, isso rouba tempo de qualidade onde importa.

- **Performance e Manutenção**  
	Código “não usado” ainda precisa ser mantido, atualizado e operado.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: frameworks internos que ninguém usa.
	- Coverage: testes para caminhos que não existem no produto.
	- Flakiness: complexidade aumenta taxa de testes instáveis.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Regras de PR: abstração só com caso de uso real e teste que justifique.
	- Remover dead code e features abandonadas.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: testar o que existe hoje.
	- Integração: só quando a integração existe.
	- E2E: somente fluxos reais.

- **Métrica de Qualidade**  
	- Percentual de código não exercitado em produção
	- Dead code e feature flags permanentes
	- Churn em módulos “framework” sem valor

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: não criar uma “engine genérica” antes de ter variações.

### Python

```python
def discount(total_cents: int) -> int:
		# Hoje existe uma regra. Quando houver outra, extraímos strategy.
		return total_cents - 100
```

### C#

```csharp
public static int Discount(int totalCents)
{
		return totalCents - 100;
}
```

### Go

```go
package pricing

func Discount(totalCents int) int {
		return totalCents - 100
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Evite abstrações “porque um dia vai precisar”.
- Prefira decisões reversíveis: wrappers simples, feature flags, composição.
- Quando a variação aparecer 2–3 vezes (com sinais claros), aí sim abstraia.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** reduzir complexidade reduz superfície de incidentes.
- **Pipelines CI/CD:** manter pipeline rápido e estável evitando matriz inútil.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** menos caminhos = melhor observabilidade.
- **Testes e Infra-as-Code:** ambientes mais simples e reprodutíveis.

---

## Métricas, Monitoramento e Melhoria Contínua

- Uso real de features (telemetria)
- Dead code e flags antigas
- Tempo para remover feature abandonada

---

## Frameworks e Ferramentas do Mercado

- Feature flag platforms
- Ferramentas de coverage e dead code

---

## Recursos Avançados e Leituras Recomendadas

- Extreme Programming Explained
- Refactoring (Fowler)

---

## FAQ Especialista

**YAGNI impede arquitetura?**  
Não. Ele incentiva arquitetura evolutiva e decisões reversíveis, com refatoração e automação.

**Quando antecipar faz sentido?**  
Quando o custo de mudança futura é altíssimo e previsível (ex.: compliance, segurança, contratos públicos). Mesmo assim, seja explícito e teste.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](FailFast.md) | [Índice](../../SUMMARY.md) | [Próximo](../archtecture/hexagonal-architecture.md)
