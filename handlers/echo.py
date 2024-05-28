from aiogram import Router, types

echo_router = Router()


@echo_router.message()
async def echo_message(message: types.Message):
    words = message.text.split()
    reversed_words = words[::-1]
    reversed_message = ' '.join(reversed_words)
    await message.answer(reversed_message)

