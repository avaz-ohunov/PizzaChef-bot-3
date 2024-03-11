# reset.py

# Метод, который сбрасывает любое состояние
async def reset_state(message, state, keyboard = None) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.clear()
        await message.answer(
            "Действия отменены",
            reply_markup = keyboard
        )
