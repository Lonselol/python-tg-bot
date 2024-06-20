from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from configparser import ConfigParser
import os

from modules.handlers import questions, bju

#Ключ из конфига
config = ConfigParser()
config.read(os.path.abspath("txt/config.ini"))
API_TOKEN:str = config['MAIN']['BOT_TOKEN']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/bju_product", description="Рассчитать БЖУ продукта"),
        BotCommand(command="/bju_meal", description="Рассчитать БЖУ приёма пищи"),
    ]
    await bot.set_my_commands(commands)

questions.register_handlers_start(router)
bju.register_handlers_bju(router)

dp.include_router(router)

async def main():
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())