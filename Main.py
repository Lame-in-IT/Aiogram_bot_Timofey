import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F
from logg import log_info
from core.handlers.basic import run_start, get_category, get_basket
from core.settings import settings
from core.middlewares.dbmiddleware import Dbasession
from core.handlers.callback import select_category, select_subcategory, select_subcategory_next
from core.handlers.callback import select_products, select_products_change_number, add_to_purchases
from core.handlers.callback import delete_prod, pay_and_delivery
from core.handlers.pay import pre_checkout_querys, payment_done, check_shopping

async def say_start_bot(bot: Bot):
    try:
        await bot.send_message(settings.bots.admin_id, text="Бот запущен!")
    except Exception as error:
        logging.exception(error)

async def say_stop_bot(bot: Bot):
    try:
        await bot.send_message(settings.bots.admin_id, text="Бот остановлен!")
    except Exception as error:
        logging.exception(error)

async def create_pool():
    return await asyncpg.create_pool(user=settings.bots.dbuser,
                                                 password=settings.bots.dbpassword,
                                                 database=settings.bots.dbdatabase,
                                                 host=settings.bots.dbhost,
                                                 port=settings.bots.dbport)

async def start():
    try:
        """Запуск бота"""
        try:
            log_info()
            bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
            pool_connect = await create_pool()
            dp = Dispatcher()
            dp.startup.register(say_start_bot)
            dp.shutdown.register(say_stop_bot)
            dp.update.middleware.register(Dbasession(pool_connect))
            dp.message.register(get_category, F.text == "Каталог")
            dp.message.register(get_basket, F.text == "Корзина")
            dp.pre_checkout_query.register(pre_checkout_querys)
            dp.message.register(payment_done, F.successful_payment)
            dp.shipping_query.register(check_shopping)
            dp.callback_query.register(select_category, F.data.startswith('Kategori_'))
            dp.callback_query.register(select_subcategory, F.data.startswith('Kate_'))
            dp.callback_query.register(select_subcategory_next, F.data.startswith('subcateg|'))
            dp.callback_query.register(select_products, F.data.startswith('Subcate_'))
            dp.callback_query.register(select_products_change_number, F.data.startswith('change|'))
            dp.callback_query.register(add_to_purchases, F.data.startswith('products_'))
            dp.callback_query.register(delete_prod, F.data.startswith('Delete|'))
            dp.callback_query.register(pay_and_delivery, F.data.startswith('Pay|'))
            
            dp.message.register(run_start, Command(commands=['start', 'run']))
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
    except Exception as error:
        logging.exception(error)

if __name__ == "__main__":
    asyncio.run(start())