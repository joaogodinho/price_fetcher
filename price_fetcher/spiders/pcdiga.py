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
    pn_regex = re.compile(r'\(([^)]+)\)$|\(([^)]+)\)\s*\+\s+oferta', re.IGNORECASE)

    def parse(self, response):
        continue_scraping = True
        for sel in response.xpath('//table[@height="170px"]'):
            item = ProductItem()
            url = sel.xpath('.//a/@href').extract_first().split('?')[0]
            temp = url.split('/')
            temp[-1] = '-'
            item['url'] = '/'.join(temp)
            item['name'] = sel.xpath('.//a[@class="prod"]/text()').extract_first().strip()

            pn_search = self.pn_regex.search(item['name'])
            if pn_search is not None:
                item['part_number'] = next(pn for pn in pn_search.groups() if pn is not None)
            else:
                item['part_number'] = None

            price = sel.xpath('.//td[@class="preco"]/text()').extract()[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
            if float(price) < 20.0:
                continue_scraping = False

            on_sale = sel.xpath('.//parent::td/div/div/img/@src').extract_first()
            if on_sale is not None:
                item['on_sale'] = True
                item['sale_price'] = price
                item['price'] = 0
            else:
                item['on_sale'] = False
                item['price'] = price
                item['sale_price'] = 0

            if continue_scraping:
                yield item

        if continue_scraping:
            pages = response.xpath('//a[@class="cinza"]/@href')
            for href in pages[:math.ceil(len(pages)/2)]:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url)
