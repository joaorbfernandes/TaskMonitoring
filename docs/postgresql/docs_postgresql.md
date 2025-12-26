# Ambiente de Desenvolvimento — PostgreSQL (DEV)

## Objetivo

Disponibilizar um ambiente PostgreSQL estável para desenvolvimento local.

Este ambiente é:
- isolado de TEST e PROD
- reprodutível a qualquer momento
- descartável

DEV existe para trabalho humano; não é fonte de verdade histórica.

## Stack usada

- PostgreSQL 16 (Docker)
- psycopg v3
- Python (CLI apenas para validação do core)

## Configuração do ambiente DEV

- Container: `task-db-dev`
- Database: `task_core_dev`
- User: `task_user`
- Porta (host): `5433`
- Porta (container): `5432`
- Dados persistidos em volume Docker

## Entry point oficial

O ambiente DEV **não deve ser criado manualmente**.

Usa sempre o script:

```bash
scripts/dev_setup.sh
```

Este script:
- sobe o container PostgreSQL via Docker Compose
- espera até o serviço estar pronto
- cria o schema `task_core`
- cria as tabelas base
- aplica seed de desenvolvimento

## String de ligação
```text
postgresql://task_user:task_pass@localhost:5433/task_core_dev
```

Usada por:
- CLI
- Repositório PostgreSQL
- Aplicação

## O que DEV pode ter
- seed de dados
- dados temporários
- resets completos

DEV serve para:
- desenvolver
- explorar
- testar manualmente

## O que DEV não usa
- db/schema.sql como mecanismo de execução
- db/ci/bootstrap.sql
- migrations como fonte inicial de DEV
- search_path implícito

## Reset do ambiente DEV

Para destruir completamente o ambiente:

```bash
docker compose -f docker/docker-compose.dev.yml down -v
```

Depois disso, o ambiente pode ser recriado com:

```bash
scripts/dev_setup.sh
```

## Regras importantes
- Nunca usar a porta 5432 no host
- DEV é descartável
- A fonte de verdade da base de dados vive nas migrations
- Infra não depende de contexto implícito


## Estado atual do projeto

- Domínio modelado
- Infra PostgreSQL funcional
- Separação clara DEV / TEST / CI
- Scripts reprodutíveis
- Testes de infraestrutura a passar

## O que isto resolve

- Elimina caminhos antigos
- Não contradiz CI
- Reflete exatamente o que testaste
- É compreensível daqui a 6 meses
- Não cria decisões implícitas