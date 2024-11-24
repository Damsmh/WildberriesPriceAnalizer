from os import path
from curl_cffi import requests
import json


class Parser:
    def __init__(self):
        self.headers = {'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',}
        self.product_cards = []
        self.directory = path.dirname(__file__)
    def get_category(self):
        pass
        
    def format_items(self, response):
        
        products = []
        
        products_raw = response.get('data', {}).get('products', None)
        
        if products_raw != None and len(products_raw) > 0:
            for product in products_raw:
                print(product.get('name', None))
                products.append({
                    'brand': product.get('brand', None),
                    'name': product.get('name', None),
                    'id': product.get('id', None),
                    'reviewRating': product.get('reviewRating', None),
                    'feedbacks': product.get('feedbacks', None),
                    'price': int(product.get('sizes', None)[0].get('price', None).get('product'))/100,
                })
                
        with open('wb_catalogue.json', 'w', encoding='UTF-8') as file:
            json.dump(products, file, indent=2, ensure_ascii=False)
        return products
    
    def get_search_products(self, query: str):
        url = f"https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=-1255987&query={'%20'.join(query.split())}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"

        response = requests.get(url, impersonate="chrome")

        return response.json()
    def run(self):
        response = self.get_search_products(input('Введите запрос: '))
        products = self.format_items(response)
        
        print(products)

if __name__ == '__main__':
    pars = Parser()
    pars.run()