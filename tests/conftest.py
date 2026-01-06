from pathlib import Path

import pytest
from alembic.config import Config
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy import text


@pytest.fixture
def alembic_config():
    base_dir = Path(__file__).resolve().parent.parent
    alembic_ini = base_dir / "alembic.ini"

    config = Config(str(alembic_ini))
    config.set_main_option("script_location", str(base_dir / "alembic"))

    return config


_postgres_db = create_postgres_fixture()


@pytest.fixture
def alembic_engine(_postgres_db):
    """
    Este fixture agora depende do _postgres_db (o DB temporário)
    e garante que o esquema 'gpt_teacher' seja criado nele.
    """
    engine = _postgres_db  # _postgres_db já é o engine da SQLAlchemy

    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS gpt_teacher;"))
        connection.commit()

    return engine
