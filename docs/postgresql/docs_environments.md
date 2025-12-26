# Ambientes do Projeto — Task Core

Este projeto utiliza **ambientes isolados por responsabilidade**.

Cada ambiente tem:
- um objetivo claro
- regras próprias
- scripts oficiais de gestão

Não existem ambientes “híbridos”.

---

## DEV — Desenvolvimento Local

### Objetivo
Ambiente para desenvolvimento diário.

Características:
- destrutivo
- reprodutível
- com seed
- isolado de TEST e CI

Usado por:
- developers
- exploração manual
- validação rápida

### Configuração
- Docker Compose project: `dev`
- PostgreSQL 16
- Porta: `5433`
- Volume persistente: `dev_task_pg_dev`

### Script oficial

```bash
scripts/dev_setup.sh
```

Este script:
- sobe o PostgreSQL (DEV)
- espera pelo serviço
- cria schema e tabelas
- aplica seed de desenvolvimento

Reset completo:

```bash
docker compose -p dev -f docker/docker-compose.dev.yml down -v --remove-orphans
```

## TEST — Ambiente de Testes Estável

### Objetivo

Ambiente estável para testes humanos.

Características:
- não destrutivo
- sem seed
- dados persistem
- idempotente

Usado por:
- testers
- developers
- validação funcional

### Configuração
- Docker Compose project: test
- PostgreSQL 16
- Porta: 5434
- Volume persistente: test_task_pg_test

### Script oficial

```bash
scripts/test_setup.sh
```

Este script:
- sobe o PostgreSQL (TEST)
- aplica bootstrap idempotente
- aplica migrations
- não apaga dados

O script pode ser executado múltiplas vezes sem efeitos colaterais.

Reset completo:

```bash
docker compose -p test -f docker/docker-compose.test.yml down -v --remove-orphans
```