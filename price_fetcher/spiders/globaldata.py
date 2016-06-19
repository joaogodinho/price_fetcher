import math
import scrapy
import re

from price_fetcher.items import ProductItem


class ChiptecSpider(scrapy.Spider):
    name = 'Globaldata'
    allowed_domains = ['globaldata.pt']
    start_urls = [
        'http://www.globaldata.pt/catalogsearch/advanced/result/?dir=desc&limit=100&order=price&price%5Bfrom%5D=20',
    ]

    def parse(self, response):
        for sel in response.xpath('//ol[@id="products-list"]/li'):
            item = ProductItem()
            item['name'] = sel.xpath('.//h2[@class="product-name"]/a/text()').extract_first().strip()
            item['url'] = sel.xpath('.//h2[@class="product-name"]/a/@href').extract_first()
            item['part_number'] = sel.xpath('.//p[@class="sku"]/text()').extract_first()

            temp_price = sel.xpath('.//span[@class="regular-price"]/span[@class="price"]/text()').extract_first()
            if temp_price is None:
                temp_price = sel.xpath('.//div[@class="price-box"]/span[@class="price"]/text()').extract_first()
            if temp_price is None:
                temp_price = sel.xpath('.//p[@class="minimal-price"]/span[@class="price"]/text()').extract_first()
            if temp_price is None:
                item['price'] = sel.xpath('.//p[@class="old-price"]/span[@class="price"]/text()').extract_first().strip()\
                    .replace('\xa0', '').replace('€', '').replace(',', '.')
                item['sale_price'] = sel.xpath('.//p[@class="special-price"]/span[@class="price"]/text()').extract_first()\
                    .strip().replace('\xa0', '').replace('€', '').replace(',', '.')
                item['on_sale'] = True
            else:
                item['price'] = temp_price.replace('\xa0', '').replace('€', '').replace(',', '.')
                item['on_sale'] = False
            yield item

        pages = response.xpath('//div[contains(@class, "toolbar-bottom")]/div/div[@class="pager"]/div[@class="pages"]/ol/li/a/@href')
        for href in pages:
             url = response.urljoin(href.extract())
             yield scrapy.Request(url)
