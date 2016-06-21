import math
import scrapy
import re

from price_fetcher.items import ProductItem


class ChiptecSpider(scrapy.Spider):
    name = 'Chiptec'
    allowed_domains = ['chiptec.net']
    start_urls = [
        'http://www.chiptec.net/catalogsearch/advanced/result/?dir=desc&limit=25&mode=list&order=price&price%5Bfrom%5D=20'
    ]
    pn_regex = re.compile(r'(.+)\s+by\s+')

    def parse(self, response):
        for sel in response.xpath('//li[contains(@class, "item")]'):
            item = ProductItem()
            item['name'] = sel.xpath('.//h2[@class="product-name"]/a/text()').extract_first().strip()
            item['url'] = sel.xpath('.//h2[@class="product-name"]/a/@href').extract_first()

            img_alt = sel.xpath('.//a[@class="product-image"]/img/@alt').extract_first().strip()
            pn_search = self.pn_regex.search(img_alt[len(item['name']):].strip())
            if pn_search is not None:
                item['part_number'] = pn_search.group(1)
            else:
                item['part_number'] = None

            temp_price = sel.xpath('.//span[@class="regular-price"]/span[@class="price"]/text()').extract_first()
            if temp_price is None:
                temp_price = sel.xpath('.//div[@class="price-box"]/span[@class="price"]/text()').extract_first()
            if temp_price is None:
                temp_price = sel.xpath('.//p[@class="price-from"]/span[@class="price"]/text()').extract_first()
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

        pages = response.xpath('//div[contains(@class, "toolbar-bottom")]/div/div[@class="pager"]/div[@class="pages"]/ol/li/a/@href')
        for href in pages:
             url = response.urljoin(href.extract())
             yield scrapy.Request(url)
