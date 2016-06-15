import math
import scrapy

from price_fetcher.items import ProductItem


class AlienTechSpider(scrapy.Spider):
    name = 'AlienTech'
    allowed_domains = ['alientech.pt']
    start_urls = [
        'http://www.alientech.pt/advanced_search_result.php?keywords=%25&pfrom=20&sort=3d&&page=1',
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@class="productBoxContents"]/tr[position()>1]'):
            item = ProductItem()
            item['name'] = sel.xpath('td/a/text()').extract_first()
            item['part_number'] = sel.xpath('td/small/text()').extract_first()[1:-1]
            temp_price = sel.xpath('td/span/s/text()').extract_first()
            sale_price = sel.xpath('td/span/text()').extract_first().strip().replace('.', '').replace(',', '.')[:-1]
            if temp_price is not None:
                item['price'] = temp_price.replace('.', '').replace(',', '.')[:-1]
                item['sale_price'] = sale_price
            else:
                item['price'] = sale_price
            yield item

        pages = response.xpath('//a[@class="pageResults"]/@href')
        for href in pages[:math.ceil(len(pages)/2)]:
            url = response.urljoin(href.extract()).split('&osCsid')[0]
            yield scrapy.Request(url)
