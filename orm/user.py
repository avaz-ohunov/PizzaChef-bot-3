# user.py

# Сторонние модули
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
from database.models import User


###################  Добавляем юзера в таблицу User  ###################

async def add(
        session: AsyncSession,
        telegram_id: int,
        first_name: str,
        last_name: str = None,
        phone: str = None
):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(
                telegram_id = telegram_id,
                first_name = first_name,
                last_name = last_name,
                phone = phone
            )
        )
        
        await session.commit()
