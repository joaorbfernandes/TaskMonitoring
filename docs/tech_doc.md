Princípios aplicados:
- O domínio não depende de nenhuma outra camada
- Infraestrutura é substituível (ex: PostgreSQL no futuro)
- Interfaces apenas chamam casos de uso
- Nada “fala diretamente” com a base de dados ou frameworks

## Entidade principal: Task

### O que é uma Task

`Task` é o **Aggregate Root** do domínio.

Responsabilidades:
- Manter estado consistente
- Garantir invariantes
- Expor comportamento controlado

A entidade **não sabe**:
- Como é persistida
- Como é avaliada
- Que regras existem

### Atributos relevantes

- `due_date`  
  Base para regras temporais

- `status`  
  Estado operacional da tarefa  
  (`TODO`, `BLOCKED`, `DONE`)

- `active`  
  Pre-condição global para avaliação

### Invariantes importantes

- Uma task inativa **não é avaliada**
- Datas inválidas são bloqueadas na criação
- Alterações de estado são explícitas e controladas

## Flags (Value Objects)

### O que são flags

Flags são **Value Objects** que representam o resultado da avaliação automática de uma task.

Características:
- Não são persistidas
- Podem ser recalculadas a qualquer momento
- Não pertencem à entidade `Task`
- Não alteram estado

### Flags existentes

| Flag | Significado |
|-----|------------|
| NORMAL | Nenhuma condição relevante |
| ATTENTION | Requer atenção humana |
| CRITICAL | Risco iminente |
| OVERDUE | Prazo ultrapassado |

### Severidade

Cada flag possui uma severidade implícita.

A severidade é usada para:
- Resolver conflitos
- Determinar a **flag principal**

## Regras de domínio (Rules)

### O que são regras

Regras são **avaliações independentes** aplicadas a uma task.

Cada regra:
- Avalia apenas uma condição
- Não altera a task
- Não conhece outras regras
- Retorna uma flag ou `None`

Interface comum: `BaseTaskFlagRule`

Task → Rule → Flag | None

### Regras implementadas

#### OverdueRule
- Condição: `due_date < hoje`
- Flag: `OVERDUE`

#### NearDueDateRule
- Condição: `due_date dentro de N dias`
- Flag: `CRITICAL`

#### BlockedRule
- Condição: `status == BLOCKED`
- Flag: `ATTENTION`

### Coexistência de regras

Regras **podem coexistir**.

Exemplo:
- Task bloqueada
- Task perto do prazo

Resultado:
- Flags: `[CRITICAL, ATTENTION]`
- Flag principal: `CRITICAL`

## Avaliação de flags

### TaskFlagEvaluator

Responsável por:
- Aplicar todas as regras
- Agregar flags
- Determinar a flag principal

### Fluxo simplificado:

  Task
    ↓
Pre-condition (active?)
    ↓
Apply rules
    ↓
Collect flags
    ↓
Determine primary flag
    ↓
Return TaskFlagEvaluation

### Pre-condition global

Se `task.active == False`:
- Nenhuma regra é aplicada
- O resultado é sempre `NORMAL`

Esta regra:
- Não pertence a nenhuma rule
- É uma regra transversal do domínio

## Resultado da avaliação

### TaskFlagEvaluation

Objeto que representa o resultado final da avaliação.

Contém:
- `flags` → lista de todas as flags ativas
- `primary_flag` → flag com maior severidade

Este objeto:
- Não contém lógica
- Apenas transporta informação

## Casos de uso (Application Layer)

### EvaluateTaskFlagUseCase

Responsável por orquestrar:
1. Obtenção da task via repositório
2. Avaliação de regras no domínio
3. Devolução do resultado

O caso de uso:
- Não conhece regras específicas
- Não conhece infraestrutura
- Apenas coordena o fluxo

## Repositório

### TaskRepository (interface)

Define:
- Como obter uma task
- Sem saber onde ou como está armazenada

### InMemoryTaskRepository

Implementação atual:
- Usada em testes
- Usada pelo CLI
- Simula persistência em memória

Nota importante:
> Cada execução do CLI cria um novo repositório em memória.

Por isso:
- Tasks não persistem entre comandos
- Este comportamento é esperado no estado atual

### PostgreSQLTaskRepository

Implementação de repositório baseada em PostgreSQL.

Responsabilidades:
- traduzir entidades de domínio para SQL
- garantir persistência consistente
- não expor detalhes da base de dados ao domínio

Esta implementação:
- é totalmente substituível
- não altera o domínio
- é validada por testes de infraestrutura

## Interface CLI (estado atual)

O CLI existe para:
- Demonstrar o fluxo do sistema
- Executar cenários pedagógicos
- Tornar visíveis as decisões do domínio via logs

Não é uma CLI de produção.

Fluxo típico:
1. Inicializa repositório
2. Cria tasks em memória
3. Avalia flags
4. Apresenta resultados

## Fronteiras da arquitetura

O domínio:
- não conhece base de dados
- não conhece frameworks
- não conhece interfaces externas

A aplicação:
- coordena fluxos
- chama o domínio
- depende de abstrações

A infraestrutura:
- implementa detalhes técnicos
- pode ser substituída
- nunca contém lógica de negócio

As interfaces (CLI, futura API):
- apenas chamam casos de uso
- não executam regras
- não acedem diretamente à base de dados

## Estado atual do projeto

O projeto encontra-se num estado sólido:

- Domínio isolado
- Regras explícitas
- Testes unitários consistentes
- Arquitetura preparada para evolução

Nada no domínio terá de ser alterado para:
- Introduzir PostgreSQL
- Expor API com FastAPI
- Adicionar novos interfaces

## Estado atual e próximos passos

O domínio encontra-se estável e isolado.

Atualmente o projeto já inclui:
- persistência real via PostgreSQL (repositório)
- testes de infraestrutura com base de dados real
- scripts de bootstrap para DEV e TEST

Próximos passos:
- exposição via API HTTP (FastAPI)
- consolidação do mapper Python ↔ SQL
- documentação do fluxo completo request → domínio → persistência

## Objetivo do projeto

Este projeto existe para **aprender backend**.

Nada acontece por magia.  
Tudo é explícito.  
Tudo é testável.