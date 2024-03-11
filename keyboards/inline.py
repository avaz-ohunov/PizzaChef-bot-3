# inline.py

# Модули по умолчанию
from typing import Dict, Tuple

# Сторонние модули
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Метод генерации inline кнопок
def gen_inline_keyboard(
        buttons: Dict[str, str],  # Словарь, в котором ключ – text inline кнопки, а значение – callback_data
        size: Tuple[int] = (1,)  # Как должны быть расположены кнопки(по умолчанию 1 в ряд)
    ) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()

    for text, call_data in buttons.items():
        keyboard.add(
            InlineKeyboardButton(
                text = text, callback_data = call_data
            )
        )

    return keyboard.adjust(*size).as_markup()


# Метод генерации inline кнопок со ссылками
def gen_inline_links_keyboard(
        buttons: Dict[str, str],  # Словарь, в котором ключ – text inline кнопки, а значение – url
        size: Tuple[int] = (1,)  # Как должны быть расположены кнопки(по умолчанию 1 в ряд)
    ) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()

    for text, url in buttons.items():
        keyboard.add(
            InlineKeyboardButton(
                text = text, url = url
            )
        )

    return keyboard.adjust(*size).as_markup()


# Метод генерации смешанной инлайн клавиатуры, в котором и url, и callback_data 
def gen_inline_mix_keyboard(
        buttons: Dict[str, str],  # Словарь, в котором есть и callback, и url inline кнопки
        size: Tuple[int] = (1,)  # Как должны быть расположены кнопки(по умолчанию 1 в ряд) 
    ) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if "://" in value:  # Если ссылка
            keyboard.add(
                InlineKeyboardButton(
                    text = text, url = value
                )
            )

        else:
            keyboard.add(
                InlineKeyboardButton(
                    text = text, callback_data = value
                )
            )

    return keyboard.adjust(*size).as_markup()
