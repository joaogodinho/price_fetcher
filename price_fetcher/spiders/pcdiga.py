import math
import re
import scrapy

from price_fetcher.items import ProductItem


class PCDigaSpider(scrapy.Spider):
    name = 'PCDiga'
    allowed_domains = ['pcdiga.com']
    start_urls = [
        'https://www.pcdiga.com/nm_pesquisa.php?pesquisa=%&pagina=1&ordem=4&categoria=&marca=',
    ]
    pn_regex = re.compile(r'\(([^)]+)\)$')

    def parse(self, response):
        continue_scraping = True
        for sel in response.xpath('//table[@height="170px"]'):
            item = ProductItem()
            item['url'] = sel.xpath('.//a/@href').extract_first().split('?')[0]
            item['name'] = sel.xpath('.//a[@class="prod"]/text()').extract_first().strip()

            pn_search = self.pn_regex.search(item['name'])
            if pn_search is not None:
                item['part_number'] = pn_search.group(1)
            else:
                item['part_number'] = None

            item['price'] = sel.xpath('.//td[@class="preco"]/text()').extract()[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
            if float(item['price']) < 20.0:
                continue_scraping = False

            on_sale = sel.xpath('.//parent::td/div/div/img/@src').extract_first()
            if on_sale is not None:
                item['on_sale'] = True
            else:
                item['on_sale'] = False

            if continue_scraping:
                yield item

        if continue_scraping:
            pages = response.xpath('//a[@class="cinza"]/@href')
            for href in pages[:math.ceil(len(pages)/2)]:
                yield scrapy.Request(href.extract())
