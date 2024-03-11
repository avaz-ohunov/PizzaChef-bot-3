# admin_private.py

# Сторонние модули
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

# Мои модули
import orm
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import gen_keyboard
from keyboards.inline import gen_inline_keyboard
from states.admin_states import AddProduct, AddBanner
from states.reset import reset_state
from states.back import back_state


router = Router()
router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


# Кнопки админа по умолчанию
admin_kb = gen_keyboard(
    buttons = [
        "Добавить товар", "Ассортимент",
        "Добавить/Изменить баннер"
    ],
    placeholder = "Выберите действие",
    size = (2, 1)
)


# Кнопки "Отмена" и "Назад"
cancel_and_back = gen_keyboard(
    buttons = ["Отмена", "Назад"],
    size = (2,)
)


# Обработка команды /admin
@router.message(Command("admin"))
async def admin(message: types.Message):
    await message.answer(
        "Выберите действие",
        reply_markup = admin_kb
    )


# Отмена состояний админа
@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_add(message: types.Message, state: FSMContext) -> None:
    await reset_state(message, state, keyboard = admin_kb)


# Возвращение к предыдущему состоянию AddProduct
@router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_add(message: types.Message, state: FSMContext) -> None:
    await back_state(AddProduct, message, state)


# Запуск состояния изменения товара
@router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm.product.get(session, int(product_id))

    AddProduct.product_for_change = product_for_change
    await callback.answer("Введите название товара")
    await callback.message.answer(
        "Введите название товара",
        reply_markup = gen_keyboard(
            [
                "Пропустить",
                "Отмена", "Назад",
            ],
            size = (1, 2)
        )
    )
    
    await state.set_state(AddProduct.name)


# Запуск состояния Добавления товара
@router.message(StateFilter(None), F.text == "Добавить товар")
async def add_pizza(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара",
        reply_markup = cancel_and_back
    )

    await state.set_state(AddProduct.name)


# Название товара
@router.message(AddProduct.name, or_f(F.text, F.text.lower() == "пропустить"))
async def add_name(message: types.Message, state: FSMContext):
    if message.text.lower() == "пропустить":
        # Оставляем то же самое название
        await state.update_data(name = AddProduct.product_for_change.name)
    else:
        await state.update_data(name = message.text)
    
    await message.answer("Введите описание для товара")
    await state.set_state(AddProduct.description)


# Описание товара
@router.message(AddProduct.description, or_f(F.text, F.text.lower() == "пропустить"))
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text.lower() == "пропустить":
        # Оставляем то же самое описание
        await state.update_data(description = AddProduct.product_for_change.description)
    else:
        await state.update_data(description = message.text)
    
    categories = await orm.categories.get(session)
    buttons = {
        category.name: str(category.category_id)
        for category in categories
    }
    
    await message.answer(
        "Выберите категорию товара",
        reply_markup = gen_inline_keyboard(buttons, size = (2,))
    )
    
    await state.set_state(AddProduct.category)


# Ловим callback выбора категории
@router.callback_query(AddProduct.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext , session: AsyncSession):
    if int(callback.data) in [category.category_id for category in await orm.categories.get(session)]:
        await callback.answer()
        await state.update_data(category = callback.data)
        await callback.message.answer("Теперь введите цену товара.")
        await state.set_state(AddProduct.price)
    else:
        await callback.answer()
        await callback.message.answer("Выберите катеорию из кнопок.")


# Если админ не нажимает на inline кнопку
@router.message(AddProduct.category)
async def not_category(message: types.Message, state: FSMContext):
    await message.answer("Нажмите на одну из кнопок👆") 


# Цена пиццы
@router.message(
    AddProduct.price,
    or_f(
        F.text.replace(".", "").isnumeric(),  # Проверка на число
        F.text.lower() == "пропустить"
    )
)
async def add_price(message: types.Message, state: FSMContext):
    if message.text.lower() == "пропустить":
        # Оставляем ту же самую стоимость
        await state.update_data(price = AddProduct.product_for_change.price)
    else:
        await state.update_data(price = float(message.text))
    
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


# Если введена цена не в числовом виде
@router.message(
    AddProduct.price,
    ~F.text.replace(".", "").isnumeric(),  # Если не число
)
async def bad_price(message: types.Message):
    await message.answer("Введите корректное значение цены")


# Изображение пиццы
@router.message(AddProduct.image, or_f(F.photo, F.text.lower() == "пропустить"))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text.lower() == "пропустить":
        # Оставляем то же самое изображение
        await state.update_data(image = AddProduct.product_for_change.image)
    else:
        await state.update_data(image = message.photo[-1].file_id)

    data = await state.get_data()

    if AddProduct.product_for_change:
        await orm.product.update(
            session,
            AddProduct.product_for_change.product_id,
            data
        )
        await message.answer(
            "Данные изменены",
            reply_markup = admin_kb
        )
    
    else:
        await orm.product.add(session, data)
        await message.answer(
            "Товар добавлен в меню",
            reply_markup = admin_kb
        )

    await state.clear()


# Если пришла не фотка
@router.message(AddProduct.image, ~F.photo)
async def not_image(message: types.Message):
    await message.answer("Отправьте изображение в формате PNG/JPG/JPEG")


# Запуск состояния AddBanner
@router.message(StateFilter(None), F.text == "Добавить/Изменить баннер")
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [
        page.name
        for page in await orm.banner.get_info_pages(session)
    ]

    await message.answer(
        "Отправьте фото баннера"
        "\nВ описании укажите для какой страницы:"
        f"\n{', '.join(pages_names)}"
    )

    await state.set_state(AddBanner.image)


# Добавление/Изменение фотки в таблице
@router.message(AddBanner.image, F.photo)
async def load_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [
        page.name
        for page in await orm.banner.get_info_pages(session)
    ]

    if for_page not in pages_names:
        await message.answer(
            "Введите правильное название!"
            f"\nили {', или '.join(pages_names)}"
        )
        return
    
    await orm.banner.change_image(session, for_page, image_id)
    await message.answer("Баннер добавлен/изменён")
    await state.clear()


# Обработка кнопки "Ассортимент"
# Выбор категории
@router.message(F.text == "Ассортимент")
async def click_assortment(message: types.Message, session: AsyncSession):
    categories = await orm.categories.get(session)
    buttons = {
        category.name: f"category_{category.category_id}" for category in categories
    }

    await message.answer(
        "Выберите категорию",
        reply_markup = gen_inline_keyboard(buttons, size = (2,))
    )


# Отображение всех продуктов определённой категории товаров
@router.callback_query(F.data.startswith("category_"))
async def get_assortment(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer()
    
    category_id = callback.data.split("_")[-1]
    
    for product in await orm.product.get_all(session, category_id):
        await callback.message.answer_photo(
            product.image,
            caption = f"<strong>{product.name}</strong>"
                      f"\n{product.description}"
                      f"\nСтоимость: ₽{round(product.price, 2)}",
            
            reply_markup = gen_inline_keyboard(
                {
                    "Удалить": f"delete_{product.product_id}",
                    "Изменить": f"change_{product.product_id}"
                },
                size = (2,)
            )
        )


# Удаление продукта из базы данных
@router.callback_query(StateFilter(None), F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm.product.delete(session, int(product_id))

    await callback.message.delete()
    await callback.message.answer("Товар удалён")
    await callback.answer("Товар удалён")
