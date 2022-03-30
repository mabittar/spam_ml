#Machine Learning Model using FastAPI

## Configuracoes iniciais
requisitos básicos:

`
pip install alembic asyncio asyncpg fastapi psycopg2 psycopg2[binary] python-jose tenacity pydantic[emailvalidator]
`
## Configuracao de Ambiente


## Banco de dados e conexões


## Async Alembic
executar a partir da linha de comando a pasta raiz do projeto:

`
alembic init -t async app/dabase/migrations
`

verificar no arquivo alembic.ini se está apontando para a pasta de configuracoes:

`
script_location = app/database/migrations
`
e comentar a variável:

`#sqlalchemy.url = driver://user:pass@localhost/dbname`

editar o arquivo envp.py:

```python 
...
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from app.database.base_class import Base
from app.database.session import SQLALCHEMY_DATABASE_URI

config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
...
```
executar na linha de comando:

```bash
$ alembic revision --autogenerate -m "create first migrations"

$ alembic upgrade head

```
