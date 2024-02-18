import logging

from aiogram import Bot
from aiogram.types import Message, FSInputFile
from core.keyboards.reply import reply_keyboard
from core.utils.dbconnect import Request
from core.keyboards.inline import get_inline_catal, del_product_in_basket, botton_pay


async def run_start(message: Message, bot: Message, request: Request):
    try:
        await request.add_user(message.from_user.id, message.from_user.first_name)
        await message.answer(f"<b>{message.from_user.first_name}, вас приветствуют в данном боте.</b>",
                               reply_markup=reply_keyboard)
    except Exception as error:
        logging.exception(error)

async def get_list_categ(request):
    try:
        list_catalog = await request.read_category()
        list_id_catal = []
        list_name_catal = []
        for cate in list_catalog:
            list_id_catal.append(cate["id_category"])
            list_name_catal.append(cate["name_category"])
        return list_id_catal, list_name_catal
    except Exception as error:
        logging.exception(error)

async def get_list_subcategory(request, categ):
    try:
        list_subcategory = await request.read_subcategory(categ)
        list_id_subcategory = []
        list_name_subcategory = []
        list_ig_category = []
        for subcate in list_subcategory:
            list_id_subcategory.append(subcate["id_subcategory"])
            list_name_subcategory.append(subcate["name_subcategory"])
            list_ig_category.append(subcate["ig_category"])
        return list_id_subcategory, list_name_subcategory, list_ig_category
    except Exception as error:
        logging.exception(error)

async def get_list_products(request, categ):
    try:
        list_products = await request.read_products(categ)
        list_id_products = []
        list_name_products = []
        list_description_products = []
        for subcate in list_products:
            list_id_products.append(subcate["id_products"])
            list_name_products.append(subcate["name_products"])
            list_description_products.append(subcate["description_products"])
        return list_name_products, list_description_products, list_id_products
    except Exception as error:
        logging.exception(error)

async def get_category(message: Message, bot: Bot, request: Request):
    try:
        image_category = FSInputFile(r'Catal.webp')
        categ = await get_list_categ(request)
        await bot.send_photo(message.chat.id, image_category, reply_markup=get_inline_catal(categ[0], categ[1], 0))
    except Exception as error:
        logging.exception(error)

async def get_basket(message: Message, bot: Bot, request: Request):
    try:
        list_basket = await request.read_basket(message.chat.id)
        for item_basket in list_basket:
            image_products = FSInputFile(r'i.webp')
            await message.answer_photo(image_products, caption=f'Название товара: {item_basket["name_product"]}\n'
                                       f'Описание товара: {item_basket["description_products"]}\n'
                                       f'Количество в заказе: {item_basket["quantity_product"]} шт.', reply_markup=del_product_in_basket(message.chat.id, item_basket["id_product"], item_basket["name_product"]))
        await message.answer("Оплатить все заказы и доставку.", reply_markup=botton_pay(message.chat.id))
    except Exception as error:
        logging.exception(error)