from aiogram.filters.callback_data import CallbackData

class Catalog_info(CallbackData, prefix='page'):
    categ: str
    subcateg: str