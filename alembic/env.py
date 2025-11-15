import asyncio
import os
from logging.config import fileConfig
from typing import Any, Dict

from alembic import context
from sqlalchemy import pool, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config
from sqlalchemy.engine import Connection, Engine

from app.db.database import Base
from app.models import user
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata: MetaData = Base.metadata


def get_url() -> str:
    """Return the database URL from environment variables."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL not set in .env")
    return url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url: str = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations given a live connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using async engine."""
    config_section: Dict[str, Any] = config.get_section(
        config.config_ini_section) or {}

    connectable: AsyncEngine = async_engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    async with connectable.connect() as connection:  # type: ignore
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Main entry
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
