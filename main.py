import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# настройка логгера
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token='5907878677:AAGb4dzNQXFvOBU-_gqPQmykTBqM2psEk_g')
dp = Dispatcher(bot, storage=MemoryStorage())

# создание класса состояний
class GuessNumber(StatesGroup):
    waiting_for_number = State()

# обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я загадал число от 1 до 5. Попробуй угадать его! Чтобы остановить игру введи /stop")

    # переход в состояние waiting_for_number
    await GuessNumber.waiting_for_number.set()
# обработчик команды /stop
@dp.message_handler(commands=['stop'], state='*')
async def stop(message: types.Message, state: FSMContext):
    # завершение состояния и сброс контекста
    await state.finish()
    await message.reply("До новых встреч!")
# обработчик текстовых сообщений
@dp.message_handler(state=GuessNumber.waiting_for_number)
async def process_number(message: types.Message, state: FSMContext):
    # проверка введенного числа
    try:
        number = int(message.text)
    except ValueError:
        await message.reply("Это не число. Попробуй еще раз.")
        return

    # проверка, угадал ли пользователь число
    if number == random.randint(1, 5):
        await message.reply("Поздравляю, ты угадал число!")
        await message.reply("Я загадал новое число от 1 до 5. Попробуй угадать его! Чтобы остановить игру введи /stop")

    else:
        await message.reply("К сожалению, ты не угадал число. Попробуй еще раз.")

    # переход в состояние waiting_for_number
    await GuessNumber.waiting_for_number.set()



# обработчик неправильных сообщений
@dp.message_handler(lambda message: message.text not in ['/start', '/stop'], state='*')
async def process_wrong_message(message: types.Message):
    await message.reply("Я не понимаю, что ты говоришь. Попробуй /start, чтобы начать игру.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)