# texts_for_db.py

from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ["Еда", "Напитки"]

description_for_info_pages = {
    "main": "Добро пожаловать в PizzaChef!",
    "about": "Пиццерия PizzaChef.\nРежим работы - круглосуточно.",
    
    "payment": as_marked_section(
        Bold("Варианты оплаты:"),
        "Банковская карта",
        "Наличные",
        "Криптовалюта",
        marker="✅ ",
    ).as_html(),
    
    "shipping": as_list(
        as_marked_section(
            Bold("Способы доставки:"),
            "Автомобиль",
            "Велосипед",
            "Пешком",
            marker="✅ "
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Самокат",
            "Дроны",
            marker="❌ "
        ),
        sep="\n----------------------\n",
    ).as_html(),
    
    "catalog": "Категории:",
    "cart": "В корзине ничего нет!"
}
