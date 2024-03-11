# menu_processing.py

# Модули по умолчанию
from typing import Union

# Сторонние модули
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
import orm
from utils.pagination import Paginator
from keyboards.multi_level_user import (
    gen_main_keyboard,
    gen_catalog_keyboard,
    gen_products_keyboard,
    gen_cart_keyboard,
)


# Главное меню
async def main_menu(session: AsyncSession, level: int, menu_name: str):
    banner = await orm.banner.get(session, menu_name)
    image = InputMediaPhoto(
            media = banner.image,
            caption = banner.description
        )

    keyboard = gen_main_keyboard(level = level)

    return image, keyboard


# Категории товаров
async def catalog(session: AsyncSession, level: int, menu_name: str):
    banner = await orm.banner.get(session, menu_name)
    image = InputMediaPhoto(
            media = banner.image,
            caption = banner.description
        )

    categories = await orm.categories.get(session)
    keyboard = gen_catalog_keyboard(level = level, categories = categories)

    return image, keyboard


# Метод генерации дополнительных кнопок в пагинации
def pages(paginator: Paginator):
    button = dict()

    # Если есть предыдущая страница, то добавляем кнопку
    if paginator.has_previous():
        button["◀ Пред."] = "previous"

    # Если есть следующая страница, то добавляем кнопку
    if paginator.has_next():
        button["След. ▶"] = "next"

    return button


# Отображение товаров с помощью пагинации
async def products(session: AsyncSession, level: int, category: int, page: int):
    products = await orm.product.get_all(session, category)
    paginator = Paginator(products, page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media = product.image,
        caption = f"<strong>{product.name}</strong>"
            f"\n{product.description}"
            f"\nСтоимость: {round(product.price, 2)}"
            f"\n<strong>{paginator.page} из {paginator.pages}</strong>"
    )

    pages_buttons = pages(paginator)

    keyboard = gen_products_keyboard(
        level = level,
        category = category,
        page = page,
        pages_buttons = pages_buttons,
        product_id = product.product_id
    )

    return image, keyboard


# Корзина юзера
async def cart(session: AsyncSession, level: int, menu_name: str, page: int, user_id: int, product_id: int):
    if menu_name == "delete":
        await orm.cart.delete_all(session, user_id, product_id)
        if page > 1: page -= 1
    
    elif menu_name == "decrement":
        is_cart = await orm.cart.reduce_product(session, user_id, product_id)
        if page > 1 and not is_cart: page -= 1

    elif menu_name == "increment":
        await orm.cart.add(session, user_id, product_id)

    carts = await orm.cart.get_all(session, user_id)

    if not carts:  # Если в корзине ничего нет
        banner = await orm.banner.get(session, "cart")
        image = InputMediaPhoto(
            media = banner.image,
            caption = f"<strong>{banner.description}</strong>"
        )

        keyboard = gen_cart_keyboard(
            level = level,
            page = None,
            pages_buttons = None,
            product_id = None
        )

    else:
        paginator = Paginator(carts, page)

        cart = paginator.get_page()[0]

        # Общая сумма одинаковых товаров в корзине
        cart_price = round(cart.quantity * cart.product.price, 2)

        # Общая сумма всех товаров в корзине
        cart_total_price = round(
            sum(
                cart.quantity * cart.product.price
                for cart in carts
            ),
            2
        )

        image = InputMediaPhoto(
            media = cart.product.image,
            caption = f"<strong>{cart.product.name}</strong>"
                    f"\n₽{round(cart.product.price, 2)} х {cart.quantity} = ₽{cart_price}"
                    f"\nТовар {paginator.page} из {paginator.pages} в корзине."
                    f"\nОбщая стоимость товаров в корзине: ₽{cart_total_price}"
        )

        pages_buttons = pages(paginator)

        keyboard = gen_cart_keyboard(
            level = level,
            page = page,
            pages_buttons = pages_buttons,
            product_id = cart.product.product_id
        )

    return image, keyboard


# Универсальный метод для хендлера
async def get_menu_content(
        session: AsyncSession,
        level: int,
        menu_name: str,
        category: Union[int, None] = None,
        page: Union[int, None] = None,
        product_id: Union[int, None] = None,
        user_id: Union[int, None] = None
):
    if level == 0:
        return await main_menu(session, level, menu_name)
    
    elif level == 1:
        return await catalog(session, level, menu_name)
    
    elif level == 2:
        return await products(session, level, category, page)
    
    elif level == 3:
        return await cart(session, level, menu_name, page, user_id, product_id)
