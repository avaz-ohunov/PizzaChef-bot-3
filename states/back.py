# back.py

# Метод, который возвращает назад любое состояние
async def back_state(class_name, message, state):
    current_state = await state.get_state()
    previous = None

    for step in class_name.__all_states__:
        # Если нет предыдущего состояния
        if class_name.__all_states__[0].state == current_state:
            await message.answer(
                "Предыдущего шага нет. "
                "Нажмите «Отмена»"
            )
            return

        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                "Ок, Вы вернулись к прошлому шагу.\n"
                f"{class_name.texts[previous.state]}"
            )
            return
        
        previous = step
