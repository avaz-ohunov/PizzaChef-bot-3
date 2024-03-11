# admin_states.py

# Сторонние модули
from aiogram.fsm.state import State, StatesGroup


# FSM добавления пиццы
class AddProduct(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        "AddProduct:name": "Введите название заново",
        "AddProduct:description": "Введите описание заново",
        "AddProduct:category": "Выберите категорию заново",
        "AddProduct:price": "Введите стоимость заново",
        "AddProduct:image": "",
    }


# FSM для загрузки/изменения баннера
class AddBanner(StatesGroup):
    image = State()
