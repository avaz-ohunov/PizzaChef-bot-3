# product.py

# Сторонние модули
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
from database.models import Product


###################  Таблица Product  ###################

# Добавление продукта в таблицу Product
async def add(session: AsyncSession, data: dict):
    product = Product(
        name = data["name"],
        description = data["description"],
        price = float(data["price"]),
        image = data["image"],
        category_id = int(data["category"])
    )

    session.add(product)
    await session.commit()


# Выборка всех данных из таблицы Product
async def get_all(session: AsyncSession, category_id: int):
    query = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all()


# Выборка определённого продукта по его id из таблицы Product
async def get(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.product_id == product_id)
    result = await session.execute(query)
    return result.scalar()


# Обновление данных определённого продукта по его id из таблицы Product
async def update(session: AsyncSession, product_id: int, data):
    query = update(Product).where(Product.product_id == product_id).values(
        name = data["name"],
        description = data["description"],
        price = float(data["price"]),
        image = data["image"],
        category_id = int(data["category"])
    )
    
    await session.execute(query)
    await session.commit()


# Удаление определённого продукта по его id из таблицы Product
async def delete(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.product_id == product_id)
    await session.execute(query)
    await session.commit()
