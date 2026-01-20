[Anterior](csharp.md) | [Índice](../../SUMMARY.md)

# Golang — Serviços Simples, Confiáveis e “Production Friendly” (nível Sênior / Especialista)

## Visão Geral e Contexto de Mercado

Go é uma linguagem muito usada para serviços backend, CLIs e componentes de infraestrutura por combinar:

- Performance consistente e execução simples (binário único).
- Concurrency pragmática (goroutines/channels) com bom tooling.
- Ecossistema forte em cloud-native (Kubernetes, Terraform providers, etc.).

O ponto sênior: Go favorece simplicidade, mas sistemas reais exigem disciplina com contratos, observabilidade e testes.

---

## Fundamentos, Evolução e Padrões de Mercado

- **Interfaces pequenas**: facilitam testabilidade e DIP.
- **Context**: cancelamento, timeouts e propagação de metadados.
- **Tooling**: `go test`, `go fmt`, `golangci-lint`.

Padrões comuns:

- Clean/Hexagonal em Go via pacotes e interfaces (sem overengineering).
- `internal/` para encapsular pacotes.

---

## Principais Desafios no Uso Profissional

- **Gerenciamento de dependências**
	- Módulos e versões; evite “forks invisíveis”.

- **Observabilidade**
	- Logs sem correlação e sem contexto.
	- Tracing mal instrumentado.

- **Confiabilidade**
	- Timeouts ausentes levam a goroutines presas e saturação.

---

## Estratégias Avançadas e Decisões Arquiteturais

- **Context-first**
	- Toda chamada externa deve ter timeout/cancelamento.
	- Propague `context.Context` até a borda.

- **Erros com contexto**
	- Wrap de erros e categorização (retryable vs fatal).
	- Evite perder a causa raiz.

- **Testabilidade sem mocks excessivos**
	- Prefira fakes simples e interfaces pequenas.
	- Separar core (regras) de adapters (HTTP/DB).

---

## Exemplos Avançados (HTTP server com shutdown gracioso)

```go
package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health/live", func(w http.ResponseWriter, r *http.Request) { w.WriteHeader(200) })
	mux.HandleFunc("/health/ready", func(w http.ResponseWriter, r *http.Request) { w.WriteHeader(200) })

	srv := &http.Server{Addr: ":8080", Handler: mux}

	go func() { _ = srv.ListenAndServe() }()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = srv.Shutdown(ctx)
}
```

---

## Boas Práticas Sêniores e Armadilhas

- Defina timeouts padrão em clients HTTP/DB.
- Evite goroutine leak (sempre tenha cancelamento ou bounded work queues).
- Use `-race` em CI para concorrência.
- Mantenha pacotes pequenos; evite dependências pesadas.

---

## Integração na Arquitetura Real

- Containerização simples (binário único) e imagens pequenas.
- Pronto para Kubernetes: endpoints de health + shutdown gracioso.
- Integração com filas e bancos: idempotência e retries com backoff.

---

## Métricas, Monitoramento e Melhoria Contínua

- Latência p95/p99 e saturação (goroutines, CPU).
- Taxa de erro categorizada (timeout, upstream, validação).
- Tempo de build e qualidade via lint/race.

---

## Frameworks e Ferramentas do Mercado

- Router: net/http, chi, gin (use com critério).
- Observabilidade: OpenTelemetry Go.
- Lint: golangci-lint.

---

## Recursos Avançados e Leituras Recomendadas

- Go blog (context, concurrency).
- Effective Go + Go Code Review Comments.

---

## FAQ Especialista

**Channels em todo lugar?**  
Não. Use canais quando houver necessidade de coordenação/streaming; para muita lógica, funções + context + filas explícitas costumam ser mais legíveis.

**Go serve para sistemas grandes?**  
Sim, mas exige padrões de pacote, testes e observabilidade. Simplicidade não acontece sozinha.

---

## Referências e Práticas do Mercado

- Effective Go, Go blog
- OpenTelemetry para Go

---

[Anterior](csharp.md) | [Índice](../../SUMMARY.md)
