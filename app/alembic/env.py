import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context

from app.database.base import Base
from app.database.db import engine
from app.database.models import User

sys.path.append(str(Path(__file__).parent.parent.parent))
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
