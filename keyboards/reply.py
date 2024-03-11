# reply.py

# Модули по умолчанию
from typing import List, Tuple

# Сторонние модули
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Метод генерации кнопок
def gen_keyboard(
        buttons: List[str],  # Массив с текстами кнопок
        placeholder: str = None,  # Текст, который будет показан в плейсхолдере юзера
        request_contact: int = None,  # Индекс кнопки, которая принимает контакт
        request_location: int = None, # Индекс кнопки, которая принимает местоположение
        size: Tuple[int] = (1,)  # Как должны быть расположены кнопки(по умолчанию 1 в ряд)
    ) -> ReplyKeyboardMarkup:
    
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons, start = 0):
        if (request_contact and request_contact) == index:
            keyboard.add(KeyboardButton(text = text, request_contact = True))

        elif (request_location and request_location) == index:
            keyboard.add(KeyboardButton(text = text, request_location = True))

        else:
            keyboard.add(KeyboardButton(text = text))

    return keyboard.adjust(*size).as_markup(
        resize_keyboard = True,
        input_field_placeholder = placeholder
    )


# Удаление клавиатуры
remove = ReplyKeyboardRemove()
