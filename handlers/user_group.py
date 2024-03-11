# user_group.py

# Модули по умолчанию
from string import punctuation

# Сторонние модули
from aiogram import types, Router

# Мои модули
from filters.chat_types import ChatTypeFilter


router = Router()

# Роутер будет работать в групповых чатах с ботом
router.message.filter(ChatTypeFilter(["group", "supergroup"]))
router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


# Типа это нецензурные слова
obscene_words = {"дурак", "дебил", "тупой", "лох"}


# Очищаем текст от разных маскировок
def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


# Фильтруем базар в чате группы
@router.edited_message()
@router.message()
async def cleaner(message: types.Message):
    if obscene_words.intersection(
        clean_text(message.text.lower()).split()
    ):
        await message.answer(
            f"{message.from_user.first_name}, фильтруем базар!"
        )

        await message.delete()
