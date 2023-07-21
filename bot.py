from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.input_file import InputFile
from aiogram.types.message import ContentType
import datetime

from config import TOKEN, ADMINS_ID

#Модель бота и клас диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

class applicateion_bot(StatesGroup):
    text = State()

@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    if message:
        await bot.send_message(message.from_user.id, """Привет!
            
<b>Оставь свою заявку!:</b>""")
        await applicateion_bot.text.set()
    else: await bot.send_message("Что-то пошло не так")
    await message.delete()

@dp.message_handler(state=applicateion_bot.text)
async def start_command(message : types.Message):
    if ADMINS_ID:
        for admin in ADMINS_ID:
            await bot.send_message(admin, f"""Заявка от пользователя @{message.from_user.username}

{message.text}

<i>Дата: {datetime.datetime.now()}</i>""")


@dp.message_handler(commands=["admin"])
async def start_command(message : types.Message):
    for id in ADMINS_ID:
        if str(message.chat.id) == id:
            await bot.send_message(message.from_user.id, "Привет админ!")
            await message.delete()
            break

#Функция которая запускается со стартом бота
async def on_startup(_):
    print('bot online')
#Пулинг бота
executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота

#Вывод уведомления про отключение бота
print("Bot offline")