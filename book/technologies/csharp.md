[Anterior](ansible.md) | [Índice](../../SUMMARY.md) | [Próximo](golang.md)

# C# / .NET — Engenharia de Produto com Performance, DX e Operação (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

C# (no ecossistema .NET) é uma stack madura para serviços backend, APIs, workers e aplicações corporativas. No mercado moderno, .NET é comum em:

- Serviços de alta produtividade com boa observabilidade e tooling.
- Sistemas que exigem performance consistente com GC robusto.
- Ambientes que valorizam contratos, tipagem e refatoração segura.

O ponto sênior: o valor vem de **arquitetura testável**, bons limites entre camadas e disciplina operacional (logging/tracing/config), não só de “frameworks”.

---

## Fundamentos, Evolução e Padrões de Mercado

- **DI e composição**: container como mecanismo, não como arquitetura.
- **Async/await**: essencial para IO; cuidado com deadlocks e context.
- **Hosting model**: minimal APIs, ASP.NET Core, background services.
- **Observabilidade**: OpenTelemetry, structured logging.

Padrões comuns:

- Clean/Hexagonal (ports/adapters), especialmente para testabilidade.
- MediatR/cqrs em casos específicos (com critério).

---

## Principais Desafios no Uso Profissional

- **Complexidade acidental**
	- Excesso de abstrações e layers “por padrão”.
	- Handlers/mediators sem necessidade real.

- **Performance**
	- Alocações excessivas, hot paths, uso inadequado de LINQ em loops críticos.
	- Configuração de GC e limites em containers.

- **Operação**
	- Logs sem correlação (sem trace/span ids).
	- Config duplicada por ambiente.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Contratos e validação**
	- Valide inputs na borda e garanta invariantes no core.
	- Use DTOs/commands e evite vazar entidade de domínio.

- **Observabilidade por padrão**
	- Logs estruturados (com contexto: request id, user id, trace id).
	- Métricas e traces com OpenTelemetry.

- **Entrega em containers**
	- Imagens base `mcr.microsoft.com/dotnet/aspnet` (runtime) e `sdk` (build).
	- Pronto para Kubernetes: health endpoints e shutdown gracioso.

---

## Exemplos Avançados (minimal API com health)

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new { status = "ok" }));
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");

app.Run();
```

---

## Boas Práticas Sêniores e Armadilhas

- Prefira DI por construtor e mantenha dependências explícitas.
- Evite `static` global e service locator.
- Use `CancellationToken` em IO e background jobs.
- Testes: unit no core, integração nos adapters.

---

## Integração na Arquitetura Real

- CI: build + testes + análise estática + scan de imagem.
- Deploy: versionamento de releases e rollback.
- Integração com filas/DB: trate idempotência e retries.

---

## Métricas, Monitoramento e Melhoria Contínua

- p95/p99 de latência por endpoint.
- Alocações/GC pauses (especialmente em carga).
- Taxa de erro e tempo de recuperação (MTTR).

---

## Frameworks e Ferramentas do Mercado

- ASP.NET Core, HealthChecks.
- OpenTelemetry, Serilog.
- xUnit/NUnit, FluentAssertions.
- `dotnet format`, analyzers.

---

## Recursos Avançados e Leituras Recomendadas

- Documentação ASP.NET Core (hosting, DI, config).
- Práticas de performance (allocations, GC, async).

---

## FAQ Especialista

**Minimal API é sempre melhor?**  
Não. É ótima para serviços pequenos/médios; para domínios complexos, organização por módulos e padrões claros importam mais.

**DI container define arquitetura?**  
Não. Arquitetura é sobre dependências e limites; o container só monta o grafo.

---

## Referências e Práticas do Mercado

- Microsoft docs (.NET, ASP.NET Core)
- OpenTelemetry para .NET

---

[Anterior](ansible.md) | [Índice](../../SUMMARY.md) | [Próximo](golang.md)
