from aiogram import Bot
from core.utils.dbconnect import Request
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup, ShippingOption, ShippingQuery
from aiogram.types import InputFile

from core.filters.file_pay import creat_pay_file



keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплата заказа и доставки',
            pay=True
        )
    ]
])

RU_SHIPPING = ShippingOption(
    id='ru',
    title='Доставка по России',
    prices=[
        LabeledPrice(
            label='Доставка СДЭК',
            amount=5000
        )
    ]
)

BY_SHIPPING = ShippingOption(
    id='by',
    title='Доставка по Беларуси',
    prices=[
        LabeledPrice(
            label='Доставка Белпочтой',
            amount=8000
        )
    ]
)

async def check_shopping(shipping_query: ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ["RU", "BY"]
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False, error_message="В вашу страну доставка не производится")
    
    if shipping_query.shipping_address.country_code == "RU":
        shipping_options.append(RU_SHIPPING)

    if shipping_query.shipping_address.country_code == "BY":
        shipping_options.append(BY_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)
    

async def order(id_chat, bot: Bot, id_user: int):
    await bot.send_invoice(
        chat_id=id_chat,
        title="Покупка в боте Timofey",
        description="Описание товаров покупки",
        payload=f"{id_user}",
        provider_token="381764678:TEST:78237",\
        currency="rub",
        prices=[
            LabeledPrice(
                label="Покупка в магазине Timofey",
                amount=19900
            )
        ],
        start_parameter='notlink',
        provider_data=None,
        photo_url='https://i.postimg.cc/zX74Yz8s/14a13b71-28f1-4f9e-b76b-128ad6668ae6.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=keyboard,
        request_timeout=15
    )

async def pre_checkout_querys(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def payment_done(message: Message, request: Request, bot: Bot):
    data_pay = await request.read_basket(message.successful_payment.invoice_payload)
    list_name_product = []
    list_quantity_product = []
    for item_pay in data_pay:
        list_name_product.append(item_pay["name_product"])
        list_quantity_product.append(item_pay["quantity_product"])
    creat_pay_file(list_name_product, list_quantity_product, message.successful_payment)
    await request.pay_del_prod(message.successful_payment.invoice_payload)
    await message.answer(f"Оплата на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency}." \
           f'\r\n мы приняли вашу заявку и готовим товар для отправки.')