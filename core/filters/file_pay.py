import logging
import openpyxl

def creat_pay_file(list_name_product, list_quantity_product, data_pay):
    try:
        book = openpyxl.load_workbook('Сводная по продажам.xlsx')
        sheet = book['Сводная по продажам']
        for index, item in enumerate(list_name_product):
            sheet.append([
                item,
                list_quantity_product[index],
                data_pay.order_info.name,
                data_pay.order_info.phone_number,
                data_pay.order_info.email,
                data_pay.order_info.shipping_address.city,
                data_pay.order_info.shipping_address.street_line1,
                data_pay.order_info.shipping_address.post_code,
            ])
        book.save("Сводная по продажам.xlsx")
        book.close()
    except Exception as error:
        logging.exception(error)