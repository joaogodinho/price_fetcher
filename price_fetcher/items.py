# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    part_number = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    on_sale = scrapy.Field()
    url = scrapy.Field()
