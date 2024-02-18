import logging
import asyncpg

class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_user(self, user_id, user_name):
        query = f"INSERT INTO users (user_id, user_name) VALUES ({user_id}, '{user_name}')"\
             f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)
    
    async def read_category(self):
        return await self.connector.fetch("SELECT * FROM category")
    
    async def read_subcategory(self, categ: str):
        return await self.connector.fetch(f"SELECT * FROM subcategory WHERE ig_category = '{categ}'")
    
    async def read_products(self, prod: str):
        return await self.connector.fetch(f"SELECT * FROM products WHERE id_subcategory = '{prod}'")
    
    async def read_basket(self, id_user: int):
        return await self.connector.fetch(f"SELECT * FROM basket WHERE id_user_basket = {id_user}")
    
    async def pay_del_prod(self, id_user: int):
        return await self.connector.fetch(f"DELETE FROM basket WHERE id_user_basket = {id_user}")
    
    async def delet_prod(self, id_user: int, id_prod: str, name_prod:str):
        try:
            await self.connector.fetch(f"DELETE FROM basket WHERE id_user_basket = {id_user} AND id_product = '{id_prod}'")
            return f"Товар {name_prod} удален из корзины."
        except Exception as error:
            logging.exception(error)
            return f"Товара {name_prod} нет в корзины."
    
    async def add_prod_in_basket(self, user_id: int, id_product: str, quantity: int):
        try:
            product =  await self.connector.fetch(f"SELECT * FROM products WHERE id_products = '{id_product}'")
            name = product[0]['name_products']
            description = product[0]['description_products']
            await self.connector.execute(f"INSERT INTO basket (id_user_basket, id_product, name_product, quantity_product, description_products)"
                                        f"VALUES ({user_id}, '{id_product}', '{product[0]['name_products']}', {quantity} , '{product[0]['description_products']}')")
            return "Товар добавлен в корзину"
        except Exception as error:
            logging.exception(error)
            return "Произошла ошибка добавления товара в корзину"