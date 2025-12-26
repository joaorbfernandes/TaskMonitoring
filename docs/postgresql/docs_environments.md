## Ambiente de Desenvolvimento — PostgreSQL (DEV)

## Objetivo
Base de dados PostgreSQL para desenvolvimento local.

Este ambiente é:
- usado por humanos
- recriável do zero
- não é fonte de verdade histórica

---

## Stack
- PostgreSQL 16 (Docker)
- Database: `task_core_dev`
- Porta: `5433`
- Dados persistentes em volume Docker

---

## Entry point oficial

O ambiente de DEV **não deve ser criado manualmente**.

Usa sempre o script:

```bash
scripts/dev_setup.sh
```

Este script:
- sobe o container PostgreSQL
- espera até o serviço estar pronto
- cria o schema task_core
- cria as tabelas base
- aplica seed de desenvolvimento

```text
DATABASE_URL=postgresql://task_user:task_pass@localhost:5433/task_core_dev
```

Usada pelo CLI e pela aplicação.

## O que DEV pode ter

- seed de dados
- dados temporários
- resets completos

## DEV existe para:

- desenvolver
- explorar
- testar manualmente

⸻

## O que DEV não usa

- db/schema.sql
- db/ci/bootstrap.sql
- migrations como fonte inicial
- search_path implícito

⸻

## Parar e limpar ambiente

Para destruir completamente o ambiente DEV:

```bash
docker compose -f docker/docker-compose.dev.yml down -v
```

Depois disso, o ambiente pode ser recriado novamente com:

```bash
scripts/dev_setup.sh
```

## Regra importante

DEV é descartável.
A fonte de verdade da base de dados vive nas migrations.