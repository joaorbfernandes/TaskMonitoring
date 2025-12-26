# Documentação — Testes de Infraestrutura (PostgreSQL)

## Objetivo

Os testes de infraestrutura existem para:

- testar a infraestrutura real
- validar integração com PostgreSQL
- garantir que a persistência funciona como esperado
- evitar execução acidental em ambientes errados

Estes testes não substituem testes de domínio nem de aplicação.

---

## Ambiente usado

Os testes de infraestrutura usam **exclusivamente o ambiente TEST**.

- PostgreSQL em Docker
- Database: `task_core_test`
- Porta: `5434`
- Ambiente descartável
- Nunca apontar para DEV nem PROD

O ambiente TEST deve ser criado antes da execução dos testes.

---

## Setup do ambiente TEST

O ambiente TEST é criado através do script:

```bash
scripts/test_setup.sh
```

Este script:
- sobe o container PostgreSQL de TEST
- espera até o serviço estar pronto
- aplica o bootstrap inicial
- aplica todas as migrations
- não aplica seed

⸻

## Separação de testes

Testes normais (default)
- Domain
- Application
- Não usam base de dados real
- São seguros
- Correm sempre

```bash
uv run pytest
```

## Testes de infraestrutura
- Usam PostgreSQL real (Docker)
- Criam e leem dados reais
- Podem apagar dados
- Não são idempotentes
- Nunca correm por defeito

Estão marcados com:

```python
@pytest.mark.infrastructure
```

## Proteção extra (obrigatória)

Os testes de infraestrutura só correm se esta variável existir:

```bash
RUN_INFRA_TESTS=1
```

Sem esta variável:
- os testes são automaticamente ignorados
- não há risco de execução acidental

## Executar testes de infraestrutura

```bash
RUN_INFRA_TESTS=1 uv run pytest -m infrastructure -v
```

Antes de correr este comando:
- o ambiente TEST deve estar ativo
- criado via scripts/test_setup.sh

⸻

## Regra de ouro

- Testes de infraestrutura nunca devem correr sem isolamento
- Isolamento significa:
	- base de dados própria
	- porta própria
	- dados descartáveis
	- bootstrap automático
- Nunca apontar para DEV
- Nunca apontar para PROD