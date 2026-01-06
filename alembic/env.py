import os
import sys
from logging.config import fileConfig
from typing import get_args, get_origin

import alembic_postgresql_enum  # noqa
import dotenv
from alembic import context
from gpt_teacher_db.gpt_teacher.core.base_model_json_conversor import PydanticJSONType
from sqlalchemy import (
    engine_from_config,
    pool,
    schema as sa_schema,
)
from sqlalchemy_utils import create_database, database_exists

sys.path = ["", ".."] + sys.path[1:]


from gpt_teacher_db.gpt_teacher import (
    SQLModelGPTTeacher,
    metadata as gpt_teacher_metadata,
)


def create_database_with_schema_if_not_exists(engine, schema_name):
    conn = engine.connect()
    if not database_exists(engine.url):
        create_database(engine.url)
    if not conn.dialect.has_schema(conn, schema_name):
        conn.execute(sa_schema.CreateSchema(schema_name))
        conn.commit()
    conn.close()


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name, disable_existing_loggers=False)


## IMPORTANT -> READ TO UNDERSTAND
# Import all personalized SQLModel Classes and metadatas
# This is the schema personalized classes (see core)

# from gpt_teacher_db.another_schema import SQLModelSchema


# from gpt_teacher_db.another_schema import metadata as another_schema_metadata

schemas_metadata = {
    "gpt_teacher": {
        "model": SQLModelGPTTeacher,
        "metadata": SQLModelGPTTeacher.metadata,
        "schemas": [
            gpt_teacher_metadata.DEFAULT_SCHEMA_NAME,
        ],
        "all_tables": gpt_teacher_metadata.all_tables,
    },
    # 'another_schema': {
    #     'model': SQLModelSchema,
    #     'metadata': SQLModelSchema.metadata,
    #     'schema': another_schema_metadata.SCHEMA_NAME,
    #     'all_tables': another_schema_metadata.all_tables,
    # },
}


def get_metadata(schema: str):
    schema = schema.lower()
    if schema not in schemas_metadata:
        raise KeyError(f"Project '{schema}' not supported or not found in Alembic.")
    return schemas_metadata[schema]


SCHEMA = os.getenv("SCHEMA", "gpt_teacher")
schema_metadata = get_metadata(SCHEMA)

ENV_FILE = os.getenv("ENV_FILE", ".env")
loaded_env_vars = dotenv.load_dotenv(ENV_FILE, override=True)

print(f"Alembic | Loaded env vars from '{ENV_FILE}'? {loaded_env_vars}")
print(f"Alembic | POSTGRES_SERVER={os.getenv('POSTGRES_SERVER', '')}")
print(f"Alembic | POSTGRES_PORT={os.getenv('POSTGRES_PORT', '')}")
print(f"Alembic | POSTGRES_PASSWORD={os.getenv('POSTGRES_PASSWORD', '')}")


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def include_name(name, type_, parent_names):
    """Function used to filter out tables that are not managed by Alembic migrations for now"""
    if type_ == "schema":
        # Alembic will only "watch" tables from the default schema or the one defined in settings
        return name in schema_metadata["schemas"]
    elif type_ == "table":
        # Alembic will only "watch" the tables which names are included here
        return name in schema_metadata["all_tables"]
    else:
        return True


def render_item(type_, obj, autogen_context):
    """
    Função para renderizar tipos customizados nas migrações

    https://alembic.sqlalchemy.org/en/latest/autogenerate.html#affecting-the-rendering-of-types-themselves
    """
    if isinstance(obj, PydanticJSONType):
        autogen_context.imports.add(
            "from gpt_teacher_db.gpt_teacher.core.base_model_json_conversor import PydanticJSONType"
        )

        pydantic_type_name = obj.pydantic_type.__name__
        if hasattr(obj.pydantic_type, "__origin__"):
            if get_origin(obj.pydantic_type) is list:
                item_type = get_args(obj.pydantic_type)[0]
                autogen_context.imports.add(
                    f"from gpt_teacher_db.gpt_teacher import {item_type.__name__}"
                )
                return f"PydanticJSONType(list[{item_type.__name__}])"
        else:
            autogen_context.imports.add(
                f"from gpt_teacher_db.gpt_teacher import {pydantic_type_name}"
            )
            return f"PydanticJSONType({pydantic_type_name})"

    return False


def _assert_schemas_exists(engine, schemas_list: list[str]):
    for schema_name in schemas_list:
        create_database_with_schema_if_not_exists(engine, schema_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=schema_metadata["metadata"],
        include_name=include_name,
        include_schemas=True,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        configuration = context.config.get_section(context.config.config_ini_section)
        configuration["sqlalchemy.url"] = get_url()
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        _assert_schemas_exists(connectable, schema_metadata["schemas"])

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=schema_metadata["metadata"],
            include_name=include_name,
            include_schemas=True,
            compare_type=True,
            compare_server_default=True,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
