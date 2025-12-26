
# Task Core Trainer

Projeto de estudo focado em **backend architecture em Python**, com o objetivo de treinar:

- Clean Architecture
- Domain-Driven Design (DDD)
- Separação clara de responsabilidades
- Regras de negócio explícitas e testáveis

O foco do projeto é o **core de domínio**, não frameworks nem infraestrutura.

## O que o projeto faz

Cria e avalia tarefas e produz **flags de monitorização** com base em regras de negócio independentes.

As flags representam **interpretações do estado da tarefa**, não decisões humanas.

Uma tarefa pode gerar:
- Zero ou mais flags
- Uma flag principal, determinada por severidade

Exemplos de flags:
- `NORMAL` — nenhuma condição relevante
- `ATTENTION` — requer atenção humana
- `CRITICAL` — risco iminente
- `OVERDUE` — prazo ultrapassado

As regras:
- São independentes
- Não alteram o estado da tarefa
- Podem coexistir

## Arquitetura

app/
├── domain/            # Regras de negócio e entidades
├── application/       # Casos de uso (orquestração)
├── infrastructure/    # Implementações técnicas
└── interfaces/        # Pontos de entrada (CLI / API)

Princípios seguidos:
- O domínio não depende de nenhuma outra camada
- Infraestrutura é substituível (ex: PostgreSQL no futuro)
- Interfaces apenas orquestram chamadas


## Estado atual

Implementado:

- Entidade `Task` como Aggregate Root
- Sistema de flags baseado em regras de domínio
- Avaliação de múltiplas regras em simultâneo
- Repositório em memória
- Interface CLI pedagógica
- Testes unitários focados no domínio e casos de uso


## Executar o projeto (CLI)

A interface atual é **experimental e pedagógica**, usada para demonstrar o fluxo da aplicação.

Exemplo:

```bash
uv run python -m app.interfaces.cli.main
```

O CLI:
- Cria tarefas em memória
- Avalia flags com base em regras
- Mostra o resultado com logs explicativos

## Executar testes

```bash
uv run pytest
```

Os testes focam-se em:
- Comportamento do domínio
- Avaliação correta das flags
- Prioridade entre múltiplas regras

## Objetivo do projeto

Este projeto existe para aprender e explicar backend sério.
- Tudo é explícito
- Tudo é testável
- A arquitetura é pensada para escalabilidade

## Próximos passos
- Persistência com PostgreSQL
- API HTTP (FastAPI)
- Documentação técnica do domínio e fluxos