# multi_level_user.py

# Модули по умолчанию
from typing import Union, Tuple

# Сторонние модули
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix = "menu"):
    level: int
    menu_name: str
    category: Union[int, None] = None
    page: int = 1
    product_id: Union[int, None] = None


# Метод генерации кнопок юзера по умолчанию
def gen_main_keyboard(level: int, size: tuple = (2,)):
    keyboard = InlineKeyboardBuilder()
    buttons = {
        "Товары 🍕": "catalog",
        "Корзина 🛒": "cart",
        "О нас ℹ️": "about",
        "Оплата 💰": "payment",
        "Доставка ⛵": "shipping"
    }

    for text, menu_name in buttons.items():
        if menu_name == "catalog":
            keyboard.add(
                InlineKeyboardButton(
                    text = text,
                    callback_data = MenuCallBack(
                        level = level + 1, menu_name = menu_name
                    ).pack()
                )
            )

        elif menu_name == "cart":
            keyboard.add(
                InlineKeyboardButton(
                    text = text,
                    callback_data = MenuCallBack(
                        level = 3, menu_name = menu_name
                    ).pack()
                )
            )

        else:
            keyboard.add(
                InlineKeyboardButton(
                    text = text,
                    callback_data = MenuCallBack(
                        level = level, menu_name = menu_name
                    ).pack()
                )
            )

    return keyboard.adjust(*size).as_markup()


# Метод генерации кнопок юзера для catalog
def gen_catalog_keyboard(
        level: int,
        categories: list,
        size: tuple = (2,)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text = "Назад",
            callback_data = MenuCallBack(
                level = level - 1, menu_name = "main"
            ).pack()
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text = "Корзина 🛒",
            callback_data = MenuCallBack(
                level = 3, menu_name = "cart"
            ).pack()
        )
    )

    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text = category.name,
                callback_data = MenuCallBack(
                    level = level + 1,
                    menu_name = category.name,
                    category = category.category_id
                ).pack()
            )
        )

    return keyboard.adjust(*size).as_markup()


# Метод генерации кнопок для каждого продукта
def gen_products_keyboard(
        level: int,
        category: int,
        page: int,
        pages_buttons: dict,
        product_id: int,
        size: Tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text = "Назад",
            callback_data = MenuCallBack(
                level = level - 1, menu_name = "main"
            ).pack()
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text = "Корзина 🛒",
            callback_data = MenuCallBack(
                level = 3, menu_name = "cart"
            ).pack()
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text = "Купить 💵",
            callback_data = MenuCallBack(
                level = level,
                menu_name = "add_to_cart",
                product_id = product_id
            ).pack()
        )
    )

    keyboard.adjust(*size)

    row = []

    for text, menu_name in pages_buttons.items():
        if menu_name == "next":  # Следующий товар
            row.append(
                InlineKeyboardButton(
                    text = text,
                    callback_data = MenuCallBack(
                        level = level,
                        menu_name = menu_name,
                        category = category,
                        page = page + 1
                    ).pack()
                )
            )

        elif menu_name == "previous":  # Предыдущий товар
            row.append(
                InlineKeyboardButton(
                    text = text,
                    callback_data = MenuCallBack(
                        level = level,
                        menu_name = menu_name,
                        category = category,
                        page = page - 1
                    ).pack()
                )
            )

    return keyboard.row(*row).as_markup()


# Метод генерации кнопок для корзины
def gen_cart_keyboard(
        level: int,
        page: Union[int, None],
        pages_buttons: Union[dict, None],
        product_id: Union[int, None],
        size: Tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()

    if page:
        keyboard.add(
            InlineKeyboardButton(
                text = "Удалить⛔️",
                callback_data = MenuCallBack(
                    level = level,
                    menu_name = "delete",
                    product_id = product_id,
                    page = page
                ).pack()
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                text = "-1",
                callback_data = MenuCallBack(
                    level = level,
                    menu_name = "decrement",
                    product_id = product_id,
                    page = page
                ).pack()
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                text = "+1",
                callback_data = MenuCallBack(
                    level = level,
                    menu_name = "increment",
                    product_id = product_id,
                    page = page
                ).pack()
            )
        )

        keyboard.adjust(*size)

        row = []

        for text, menu_name in pages_buttons.items():
            if menu_name == "next":
                row.append(
                    InlineKeyboardButton(
                        text = text,
                        callback_data = MenuCallBack(
                            level = level,
                            menu_name = menu_name,
                            page = page + 1
                        ).pack()
                    )
                )

            elif menu_name == "previous":
                row.append(
                    InlineKeyboardButton(
                        text = text,
                        callback_data = MenuCallBack(
                            level = level,
                            menu_name = menu_name,
                            page = page - 1
                        ).pack()
                    )
                )

        keyboard.row(*row)

        row2 = [
            InlineKeyboardButton(
                text = "На главную 🏠",
                callback_data = MenuCallBack(
                    level = 0, menu_name = "main"
                ).pack()
            )
        ]

        return keyboard.row(*row2).as_markup()
    
    else:
        keyboard.add(
            InlineKeyboardButton(
                text = "На главную 🏠",
                callback_data = MenuCallBack(
                    level = 0, menu_name = "main"
                ).pack()
            )
        )

        return keyboard.adjust(*size).as_markup()
