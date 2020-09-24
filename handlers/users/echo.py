from aiogram import types
from loader import dp


@dp.message_handler(state='*')
async def bot_echo(message: types.Message):
    await message.answer('Неизвестная команда. Воспользуйтесь командами из меню или нажмите /help')
