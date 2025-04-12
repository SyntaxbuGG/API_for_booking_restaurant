import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context

# Важно: импортируйте вашу базовую модель и все модели!
# Измените на ваш реальный путь
from app.database import Base  

from dotenv import load_dotenv

load_dotenv()

# Конфигурация логгера Alembic
config = context.config
fileConfig(config.config_file_name)

# Целевые метаданные (из ваших моделей SQLAlchemy)
target_metadata = Base.metadata


def get_url():
    # Приоритеты получения URL:
    # 1. Переменная окружения SYNC_DATABASE_URL
    # 2. Настройки из alembic.ini

    return os.getenv("SYNC_DATABASE_URL") or config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме (без подключения к БД)."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Сравнивать типы столбцов
        compare_server_default=True,  # Сравнивать дефолтные значения
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в онлайн-режиме (с реальным подключением)."""
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,  # Не использовать пул соединений для миграций
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,  # Учитывать схемы БД
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
