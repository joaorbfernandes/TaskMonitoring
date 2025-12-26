# Ambiente de Desenvolvimento — PostgreSQL

	•	Ter um ambiente DEV estável
	•	Separado de TEST e PROD
	•	Reprodutível a qualquer momento


# Stack usada

	•	PostgreSQL 16 (Docker)
	•	psycopg v3
	•	Python (CLI apenas para demonstração do core)


# Container de base de dados (DEV)

Nome
	•	Container: task-db-dev
	•	Database: task_core_dev
	•	User: task_user
	•	Password: task_pass

Porta
	•	Host: 5433
	•	Container: 5432

```bash
docker run --name task-db-dev \
  -e POSTGRES_USER=task_user \
  -e POSTGRES_PASSWORD=task_pass \
  -e POSTGRES_DB=task_core_dev \
  -p 5433:5432 \
  -d postgres:16
```

# Aplicar schema SQL

```bash
docker exec -i task-db-dev \
  psql -U task_user -d task_core_dev < db/schema.sql
```
## Verification

```bash
docker exec -it task-db-dev \
  psql -U task_user -d task_core_dev
```

```sql
\dt
```

# DEV

```text
postgresql://task_user:task_pass@localhost:5433/task_core_dev
```

Esta string é usada por:
	•	CLI
	•	Repositório PostgreSQL
	•	Testes de infraestrutura (mais tarde)

# Limpar ambiente DEV

## Apagar dados (Manter Container)
```sql
TRUNCATE TABLE tasks;
```

## Reset total
```bash
docker stop task-db-dev
docker rm task-db-dev
```

Depois subir novamente e reaplicar schema.

# Notas importantes

Nunca usar porta 5432 em DEV
	•	Evita conflitos com PostgreSQL local
CLI não é produto
	•	Serve apenas para validar domínio + infra
Schema é manual
	•	Migrações só entram quando houver API real

# Estado atual do projeto

✔️ Domínio modelado
✔️ Infraestrutura PostgreSQL funcional
✔️ Separação clara DEV / futuro TEST
⏭️ Próximo passo: testes de infraestrutura