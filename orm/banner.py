# banner.py

# Сторонние модули
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
from database.models import Banner


###################  Баннеры (Информационные страницы) ###################

# Добавление описания к баннеру
async def add_description(session: AsyncSession, data: dict):
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    
    session.add_all(
        [
            Banner(name = name, description = description)
            for name, description in data.items()
        ]
    )

    await session.commit()


# Изменение фотки баннера
async def change_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image = image)
    await session.execute(query)
    await session.commit()


# Получение определённого баннера
async def get(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


# Выборка всех баннеров
async def get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()
