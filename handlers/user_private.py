# user_private.py

# Сторонние модули
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
import orm
from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from keyboards.multi_level_user import MenuCallBack


router = Router()

# Роутер будет работать только в приватных чатах с ботом
router.message.filter(ChatTypeFilter(["private"]))


# Обработка команды /start
@router.message(CommandStart())
async def start(message: types.Message, session: AsyncSession):
    main_image, main_keyboard = await get_menu_content(
                                    session,
                                    level = 0,
                                    menu_name = "main"
                                )
    
    await message.answer_photo(
        main_image.media,
        caption = main_image.caption,
        reply_markup = main_keyboard
    )

    user = message.from_user
    await orm.user.add(
        session,
        user.id,
        first_name = user.first_name,
        last_name = user.last_name,
    )


# Обработка фабрики коллбэков(многоуровневого инлайн меню)
@router.callback_query(MenuCallBack.filter())
async def user_menu(
        callback: types.CallbackQuery,
        callback_data: MenuCallBack,
        session: AsyncSession
):
    if callback_data.menu_name == "add_to_cart":
        user = callback.from_user        
        await orm.cart.add(session, user.id, callback_data.product_id)
        await callback.answer(
            "Товар добавлен в корзину",
            show_alert = True
        )

        return

    image, keyboard = await get_menu_content(
        session,
        level = callback_data.level,
        menu_name = callback_data.menu_name,
        category = callback_data.category,
        page = callback_data.page,
        product_id = callback_data.product_id,
        user_id = callback.from_user.id
    )

    await callback.message.edit_media(
        media = image, reply_markup = keyboard
    )
