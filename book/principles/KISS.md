[Anterior](DRY.md) | [Índice](../../SUMMARY.md) | [Próximo](SOLID.md)

# KISS — Keep It Simple, Stupid (Simplicidade como Estratégia) (Princípio)

## Visão Geral e Contexto de Mercado

KISS é um princípio que prioriza soluções simples e compreensíveis. Em sistemas profissionais, simplicidade não é “poucos arquivos”: é reduzir complexidade acidental, diminuir surface area e tornar mudanças previsíveis.

No mercado, KISS reduz:

- tempo de onboarding
- bugs por interações inesperadas
- custo de operar e depurar em produção

KISS não significa “não abstrair” — significa abstrair apenas quando a abstração realmente reduz complexidade.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Histórico e Evolução do Tema**  
	A indústria aprendeu que software vive mais tempo do que o esperado. O custo dominante é manutenção. KISS é um “hedge” contra a evolução inevitável.

- **Padrões e Protocolos Usados no Mercado**
	- **YAGNI + KISS:** não construir mecanismos complexos antes de precisar.
	- **Separation of Concerns:** simples por módulo, não por “tudo num lugar”.
	- **Design for testability:** simples é testável e determinístico.
	- **Observabilidade:** simples de operar (logs/metrics claros).

---

## Principais Desafios no Uso Profissional

- **Escalabilidade dos Testes/Padrões**  
	O “simples” muda com escala. Uma solução “simples” em 1 serviço pode virar caos em 50 serviços sem padronização.

- **Performance e Manutenção**  
	Soluções “espertas” tendem a ter efeitos colaterais difíceis de manter. KISS favorece caminhos explícitos, mesmo que mais verbosos.

- **Gerenciamento Técnico (Debt, Coverage, Flakiness)**  
	- Debt: abstrações criadas cedo demais.
	- Coverage: complexidade dificulta testes.
	- Flakiness: infra “mágica” e mocks complicados.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Integração com CI/CD**
	- Automatize checks que promovem simplicidade: lint, complexidade, dead code.
	- Enforce padrões de arquitetura para evitar “cada time inventa um jeito”.

- **Práticas de mercado: Pirâmide de Testes, Testes em múltiplos ambientes, mocks de infraestrutura**
	- Unit: simples de escrever e manter.
	- Integração: poucas, bem definidas.
	- E2E: mínima e confiável.

- **Métrica de Qualidade**  
	- Complexidade ciclomática e churn
	- Tempo para adicionar feature simples
	- MTTR (simplicidade operacional)

---

## Exemplos Avançados (Python, C# e Go)

Exemplo: priorizar validação explícita em vez de comportamento implícito.

### Python

```python
def parse_page_size(raw: str) -> int:
		try:
				value = int(raw)
		except ValueError:
				raise ValueError("page_size must be an integer")
		if value <= 0 or value > 200:
				raise ValueError("page_size must be between 1 and 200")
		return value
```

### C#

```csharp
public static int ParsePageSize(string raw)
{
		if (!int.TryParse(raw, out var value))
				throw new ArgumentException("page_size must be an integer");
		if (value is < 1 or > 200)
				throw new ArgumentException("page_size must be between 1 and 200");
		return value;
}
```

### Go

```go
package paging

import "fmt"

func ParsePageSize(raw string) (int, error) {
		var value int
		if _, err := fmt.Sscanf(raw, "%d", &value); err != nil {
				return 0, fmt.Errorf("page_size must be an integer")
		}
		if value < 1 || value > 200 {
				return 0, fmt.Errorf("page_size must be between 1 and 200")
		}
		return value, nil
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Prefira soluções explícitas e fáceis de debugar.
- Evite “frameworks internos” antes da hora.
- “Simples” != “rápido de codar”; simples é o que continua claro em 6 meses.

---

## Integração na Arquitetura Real

- **Orquestração com Docker/Kubernetes:** simplicidade operacional (readiness, logs, config clara).
- **Pipelines CI/CD:** checks automáticos para complexidade e regressões.
- **Integração com ferramentas de QA, análise estática, monitoramento pós-deploy:** qualidade contínua para evitar complexidade acidental.
- **Testes e Infra-as-Code:** ambientes reprodutíveis simplificam debug.

---

## Métricas, Monitoramento e Melhoria Contínua

- Complexidade por módulo e tendências
- Tempo de pipeline e tempo de PR
- Incidentes por “comportamento inesperado”

---

## Frameworks e Ferramentas do Mercado

- Linters e analyzers (complexidade, dead code)
- OpenTelemetry (simplicidade na observabilidade)

---

## Recursos Avançados e Leituras Recomendadas

- A Philosophy of Software Design (Ousterhout)
- Clean Code (com ressalvas e contexto)

---

## FAQ Especialista

**KISS conflita com abstrações e padrões?**  
Não. Use padrões quando eles reduzem complexidade total. Se aumentam indireção sem ganho, não são KISS.

**Como decidir o que é “simples”?**  
Pelo custo de entender, testar, operar e mudar. Faça a escolha que minimiza o custo total, não só a implementação.

---

## Referências e Práticas do Mercado

- ThoughtWorks Tech Radar (práticas e tendências em engenharia)
- Martin Fowler (refactoring, arquitetura evolutiva, patterns)
- Google SRE Book / SRE Workbook (operações e confiabilidade)

---


[Anterior](DRY.md) | [Índice](../../SUMMARY.md) | [Próximo](SOLID.md)
