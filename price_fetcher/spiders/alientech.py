import math
import scrapy
import json
from lxml import etree

from price_fetcher.items import ProductItem


class AlienTechSpider(scrapy.Spider):
    name = 'AlienTech'
    allowed_domains = ['alientech.pt']
    url_format = 'https://www.alientech.pt/toogas/product/ajax/action/index/uniqueSearchId/{}/page/{}?q=%25&price=20%2C999999999&order=price-high-to-low'
    added_urls = set()
    start_urls = [
        'https://www.alientech.pt/toogas/product/ajax/action/index/uniqueSearchId/1/page/1?q=%25&price=20%2C999999999&order=price-high-to-low',
    ]

    def parse(self, response):
        response = json.loads(response.body_as_unicode())
        products = etree.HTML(response['products'])
        for sel in products.xpath('//div[contains(@class, "item")]/form/div[@class="box-product"]'):
            item = ProductItem()
            temp = sel.xpath('div/div[@class="prod-name"]')[0]
            item['name'] = temp.xpath('a/text()')[0].strip()
            item['url'] = temp.xpath('a/@href')[0]
            item['part_number'] = temp.xpath('small/text()')[0].strip()

            prices = sel.xpath('div/div/div[@class="block-price"]')[0]
            sale_price = prices.xpath('span[contains(@class, "prod-old-price")]/text()')[0].strip().split(' ')[0]
            sale_price = sale_price.replace(',', '')
            norm_price = prices.xpath('span[contains(@class, "prod-price")]/text()')[0].strip().split(' ')[0]
            norm_price = norm_price.replace(',', '')
            if float(sale_price) != float(norm_price):
                item['sale_price'] = sale_price
                item['on_sale'] = True
                item['price'] = norm_price
            else:
                item['sale_price'] = 0
                item['on_sale'] = False
                item['price'] = norm_price
            yield item

        
        for numb in range(1, int(response['max_pages']) + 1):
            url = self.url_format.format(response['uniqueSearchId'], numb)
            if numb not in self.added_urls:
                self.added_urls.add(numb)
                print(url)
                yield scrapy.Request(url)
