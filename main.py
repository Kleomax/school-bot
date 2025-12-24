import sys
import asyncio
import logging
import fontstyle
# from redis import Redis
# from aiogram.fsm.storage.redis import RedisStorage
# from aiogram.types import TelegramObject, Message

from aiogram import Dispatcher
from config import bot

from handlers import *

from middleware import BlockUsers, AntiFloodMiddleware

async def main():
    dp = Dispatcher(maintenance_mode=False)

    # process = multiprocessing.Process(target=worker)
    # process.start()

    # redis = Redis(host=localhost, port=6379/0, decode_responses=True)
    # storage = RedisStorage.from_url(redis://localhost:6379/0)
    # dp.message.middleware(ThrottlingMiddleware(storage)

    dp.include_routers(
        Maintenance_router,
        ChangeDataBtns_router,
        ChangeDataFunctions_router,
        Schedule_router,
        Ideas_router,
        ExamInfo_router,
        UserQuestions_router,
        HomeworkHelper_router,
        AdminQuestions_router,
        # StudyingTheme_router,
        # EducationTheme_router,
        # DnevnikTheme_router,
        # DirectorTheme_router,
        AllThemes_router,
        InBotMailing_router,
        ChannelMailing_router,
        Statistics_router,
        ActivityUsers_router,
        BlockUsers_router,
        AnyMessage_router
    )
    
    # dp.message.middleware.register(AntiFloodMiddleware(30))
    dp.message.middleware.register(BlockUsers())
                                   
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        print(fontstyle.apply("[+] Бот запущен", "bold/Italic/green"))
        print(fontstyle.apply("[INFO] Для остановки бота нажмите сочетание клавиш: Ctrl + C", "italic/yellow"))

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())

    except KeyboardInterrupt:
        print(fontstyle.apply("[-] Бот выключен", "bold/Italic/red"))