# chat_types.py

# Сторонние модули
from aiogram.filters import Filter
from aiogram import types, Bot


# Класс по которому можно отфильтровать тип чата
class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


# Проверка админа
class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        # Узнаём актуальных админов группового чата
        admins_list = await bot.get_chat_administrators(-4139166257)
    
        # Генерируем список из id админов чата
        bot.admins_list = [
            member.user.id
            for member in admins_list
            if member.status == "creator" or member.status == "administrator"
        ]

        return message.from_user.id in bot.admins_list
