import asyncio
import datetime
import logging
import time

import app
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher, Bot

import handlers

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(level=logging.ERROR, filename="bot_log.log", format=_log_format)

dp = Dispatcher()
dp.include_router(handlers.router)
bot = Bot(token=config.bot_token)
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

async def start_scheduler():
    scheduler.start()

    scheduler.add_job(
        app.get_news,
        trigger='interval',
        hours=1)
    scheduler.add_job(
        handlers.check_new_posts,
        trigger='interval',
        hours=1,
        minutes=15,
        args=[handlers.bot]
    )
async def main():
    await start_scheduler()
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.exception(datetime.datetime.now(), e)
            time.sleep(3)
            print(e)
