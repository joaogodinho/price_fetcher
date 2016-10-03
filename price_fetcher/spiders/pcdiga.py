import math
import re
import scrapy

from price_fetcher.items import ProductItem


class PCDigaSpider(scrapy.Spider):
    name = 'PCDiga'
    allowed_domains = ['pcdiga.com']
    start_urls = [
        'https://www.pcdiga.com/catalogsearch/advanced/result/?dir=desc&mode=list&order=price&price%5Bfrom%5D=20&limit=25'
    ]

    def parse(self, response):
        for sel in response.xpath('//ul[@id="products-list"]/li'):
            item = ProductItem()
            item['name'] = sel.xpath('.//h2[@class="product-name"]/a/text()').extract_first().strip()
            item['url'] = sel.xpath('.//h2[@class="product-name"]/a/@href').extract_first()
            item['part_number'] = sel.xpath('.//div[@class="product-sku"]/text()').extract_first().strip()

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
                item['sale_price'] = 0
                item['on_sale'] = False
            yield item

        pages = response.xpath('//div[contains(@class, "toolbar-bottom")]/div/div[@class="pages"]/ol/li/a/@href')
        for href in pages:
             url = response.urljoin(href.extract())
             yield scrapy.Request(url)

