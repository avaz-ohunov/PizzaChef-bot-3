# cart.py

# Сторонние модули
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

# Мои модули
from database.models import Cart


###################  Корзина  ###################

# Добавление товара в корзину
async def add(
        session: AsyncSession,
        telegram_id: int,
        product_id: int
):
    query = select(Cart).where(
        Cart.telegram_id == telegram_id,
        Cart.product_id == product_id
    ).options(joinedload(Cart.product))
    
    cart = await session.execute(query)
    cart = cart.scalar()
    
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(
            Cart(
                telegram_id = telegram_id,
                product_id = product_id,
                quantity = 1
            )
        )
        
        await session.commit()


# Удаление всех одинаковых товаров из корзины
async def delete_all(
        session: AsyncSession,
        telegram_id: int,
        product_id: int
):
    query = delete(Cart).where(
        Cart.telegram_id == telegram_id,
        Cart.product_id == product_id
    )

    await session.execute(query)
    await session.commit()


# Удаление товара из корзины
async def reduce_product(
        session: AsyncSession,
        telegram_id: int,
        product_id: int
):
    query = select(Cart).where(
        Cart.telegram_id == telegram_id,
        Cart.product_id == product_id
    )
    
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await delete_all(session, telegram_id, product_id)
        await session.commit()
        return False
    

# Выбираем все товары из корзины юзера
async def get_all(session: AsyncSession, telegram_id: int):
    query = select(Cart).filter(
        Cart.telegram_id == telegram_id
    ).options(joinedload(Cart.product))
    
    result = await session.execute(query)
    return result.scalars().all()
