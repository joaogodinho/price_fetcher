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
    pn_regex = re.compile(r'\((.+)\)')

    def parse(self, response):
        for sel in response.xpath('//table[@height="170px"]'):
            item = ProductItem()
            item['name'] = sel.xpath('.//a[@class="prod"]/text()').extract_first()

            pn_search = self.pn_regex.search(item['name'])
            if pn_search is not None:
                item['part_number'] = pn_search.group(1)
            else:
                item['part_number'] = None

            item['price'] = sel.xpath('.//td[@class="preco"]/text()').extract()[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
            yield item

        # pages = response.xpath('//a[@class="pageResults"]/@href')
        # for href in pages[:math.ceil(len(pages)/2)]:
        #     url = response.urljoin(href.extract()).split('&osCsid')[0]
        #     yield scrapy.Request(url)
