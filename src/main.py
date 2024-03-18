import asyncio
import os
from aiogram import Bot, Dispatcher
from configparser import ConfigParser

from modules.handlers import questions, different_types

async def main():
    #Ключ из конфига
    config = ConfigParser()
    config.read(os.path.abspath("txt/config.ini"))
    apiKey:str = config['MAIN']['BOT_TOKEN']
    
    #Объект бота
    bot:Bot = Bot(token=apiKey)
    dp:Dispatcher = Dispatcher()

    #Роутеры
    dp.include_routers(questions.router, different_types.router)

    #Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
