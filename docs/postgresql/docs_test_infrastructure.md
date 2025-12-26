# Documentação — Testes de Infraestrutura (PostgreSQL)

Objetivo
	•	Testar a infraestrutura real
	•	Validar integração com PostgreSQL
	•	Garantir que persistência funciona como esperado
	•	Nunca correr estes testes por acidente

## Separação de testes

Testes normais (default)
	•	Domain
	•	Application
	•	Não usam DB real
	•	Seguros
	•	Correm sempre

```bash
uv run pytest
```

## Testes de infraestrutura

	•	Usam PostgreSQL real (Docker)
	•	Criam e leem dados reais
	•	Podem apagar dados
	•	Nunca correm por defeito

Estão marcados com:

```python
@pytest.mark.infrastructure
```

### Proteção extra (obrigatória)

Os testes de infraestrutura só correm se esta variável existir:

```bash
	RUN_INFRA_TESTS=1
```

Sem isto, os testes são automaticamente ignorados.

## Correr testes

```bash
RUN_INFRA_TESTS=1 uv run pytest -m infrastructure -v
```