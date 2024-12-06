from asyncio import sleep as asleep

from aiogram import Bot, Dispatcher, types, F, Router, flags
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from bd import get_all_products

router = Router()
bot = Bot(config.bot_token)

@router.message(Command('start'))
async def start(message: Message):
    await message.answer(text="Бот для сбора и автопостинга ProductHunt")


async def check_new_posts():
    products = await get_all_products()
    for product in products:
        if product.posted == 0:
            # inline кнопка для ссылки
            kb_app = InlineKeyboardBuilder()
            kb_app.add(types.InlineKeyboardButton(
                text='Подробнее',
                url=product.link
            ))
            try:
                await bot.send_photo(chat_id=config.channel_id,
                                 photo=product.img,
                                 caption=product.review,
                                 reply_markup=kb_app.as_markup(),
                                 parse_mode='Markdown')
                await asleep(4)
            except Exception as e:
                print(e)
                continue
            await asleep(4)