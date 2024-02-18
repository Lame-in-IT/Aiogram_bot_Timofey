from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_inline_paginations.paginator import Paginator

def get_inline_catal(list_id_catal, list_name_catal, page_kate: int):
    kb = [
        [
            InlineKeyboardButton(
                text=f"{str(item)}", callback_data=f"{list_id_catal[index]}"
            )
        ]
        for index, item in enumerate(list_name_catal)    
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    paginator = Paginator(data=kb, callback_startswith="Kategori_", size=5)
    return paginator(current_page=page_kate)

def get_inline_subcate(list_id_subcate, list_name_subcate, list_ig_category, page_kate):
    kb = [
        [
            InlineKeyboardButton(
                text=f"{str(item)}", callback_data=f"{list_id_subcate[index]}"
            )
        ]
        for index, item in enumerate(list_name_subcate)    
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=kb)
    paginator = Paginator(data=kb, callback_startswith=f"subcateg|{list_ig_category[0]}|", size=5)
    return paginator(current_page=page_kate)

def creat_button_sale(product, number):
    keyboard_sale = InlineKeyboardBuilder()
    keyboard_sale.button(text=f'Добавить в корзину {number} шт.', callback_data=f'{product}|{number}')
    keyboard_sale.button(text='+ 1 шт.', callback_data=f'change|+|{number}|{product}')
    keyboard_sale.button(text='- 1 шт.', callback_data=f'change|-|{number}|{product}')

    keyboard_sale.adjust(1, 2)
    return keyboard_sale.as_markup()

def del_product_in_basket(id_user: int, id_prod: str, name_prod: str):
    keyboard_del = InlineKeyboardBuilder()
    keyboard_del.button(text=f'Удалить {name_prod}', callback_data=f'Delete|{id_user}|{id_prod}|{name_prod}')

    return keyboard_del.as_markup()

def botton_pay(id_user):
    keyboard_pay = InlineKeyboardBuilder()
    keyboard_pay.button(text='Оплата и доставка', callback_data=f"Pay|{id_user}")
    
    return keyboard_pay.as_markup()