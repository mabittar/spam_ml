# Machine Learning Model using FastAPI

## Configurações iniciais
requisitos básicos:

`
pip install alembic asyncio asyncpg fastapi psycopg2 psycopg2[binary] python-jose tenacity pydantic[emailvalidator] python-multipart  
`
## Configuração de Ambiente


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
e a variável:

`#sqlalchemy.url = `

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
from app.models.user import User # noqa
target_metadata = [Base.metadata]
...
```
executar na linha de comando para criar as tabelas no banco de dados:

```bash
$ alembic revision --autogenerate -m "create first migrations"

$ alembic upgrade head

```

## Autenticação do usuário

Para autenticar um usuário primeiramente é necessário criar um usuário utilizando o endpoint `user/register`. 
Após criá-lo utilize o endpoint `/login/` fornecendo o username e a senha preenchidas no cadastro do registro.

Você irá receber um token com validade de uma hora. Esse token será sua autenticação para utilizar os serviços de verificação de Spam.