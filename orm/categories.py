# categories.py

# Сторонние модули
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
from database.models import Category


###################  Категории  ###################

# Выборка всех категорий товаров
async def get(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()


# Создание категории товаров
async def create(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    
    session.add_all([Category(name = name) for name in categories])

    await session.commit()
