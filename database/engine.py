# engine.py

# Модули по умолчанию
import os

# Сторонние модули
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# Мои модули
import orm
from database.models import Base
from common.texts_for_db import categories, description_for_info_pages


# Подключение SQLite
engine = create_async_engine(os.getenv("DB_SQLITE"))

# Подключение PostgreSQL
# engine = create_async_engine(os.getenv("DB_PGSQL"))

session_maker = async_sessionmaker(
    bind = engine, class_ = AsyncSession, expire_on_commit = False
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await orm.categories.create(session, categories)
        await orm.banner.add_description(session, description_for_info_pages)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
