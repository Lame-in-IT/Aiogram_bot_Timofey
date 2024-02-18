import logging

from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.types import CallbackQuery
from core.utils.dbconnect import Request
from core.keyboards.inline import get_inline_catal, get_inline_subcate, creat_button_sale
from core.handlers.basic import get_list_categ, get_list_subcategory, get_list_products
from core.handlers.pay import order

async def select_category(call: CallbackQuery, request: Request):
    try:
        page = int(call.data.split('Kategori_')[1])
        categ = await get_list_categ(request)
        await call.message.edit_reply_markup(reply_markup=get_inline_catal(categ[0], categ[1], page))
    except Exception as error:
        logging.exception(error)


async def select_subcategory(call: CallbackQuery, request: Request):
    try:
        page = call.data
        subcate = await get_list_subcategory(request, page)
        image_category = FSInputFile(r'subcategory.png')
        await call.message.answer_photo(image_category, reply_markup=get_inline_subcate(subcate[0], subcate[1], subcate[2], 0))
    except Exception as error:
        logging.exception(error)

async def select_subcategory_next(call: CallbackQuery, request: Request):
    try:
        page_subc = call.data.split('|')
        subcate = await get_list_subcategory(request, page_subc[1])
        await call.message.edit_reply_markup(reply_markup=get_inline_subcate(subcate[0], subcate[1], subcate[2], int(page_subc[-1])))
    except Exception as error:
        logging.exception(error)

async def select_products(call: CallbackQuery, request: Request):
    try:
        product = await get_list_products(request, call.data)
        for index_products, item_products in enumerate(product[0]):
            image_products = FSInputFile(r'i.webp')
            await call.message.answer_photo(image_products, caption=f'{item_products} \n'
                                            f'{product[1][index_products]}', reply_markup=creat_button_sale(product[2][index_products], 1))
    except Exception as error:
        logging.exception(error)

async def select_products_change_number(call: CallbackQuery):
    try:
        namber_prod= call.data.split('|')
        if namber_prod[1] == "+":
            namber = int(namber_prod[2]) + 1
        if namber_prod[1] == "-":
            namber = int(namber_prod[2]) - 1
        await call.message.edit_reply_markup(reply_markup=creat_button_sale(namber_prod[-1], namber))
    except Exception as error:
        logging.exception(error)

async def add_to_purchases(call: CallbackQuery, request: Request):
    try:
        product = call.data.split('|')
        add_product = await request.add_prod_in_basket(call.from_user.id, product[0], product[1])
        await call.answer(f"{add_product}", show_alert=True)
    except Exception as error:
        logging.exception(error)

async def delete_prod(call: CallbackQuery, request: Request):
    try:
        data_del = call.data.split('|')
        req_del = await request.delet_prod(int(data_del[1]), data_del[2], data_del[3])
        await call.answer(f"{req_del}", show_alert=True)
    except Exception as error:
        logging.exception(error)

async def pay_and_delivery(call: CallbackQuery, bot: Bot):
    try:
        data_pay = call.data.split('|')
        await order(call.from_user.id, bot, int(data_pay[1]))
    except Exception as error:
        logging.exception(error)