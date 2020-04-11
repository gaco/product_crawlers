# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ProductCrawlersItem(scrapy.Item):
    name = Field()
    price = Field()
    origin_domain = Field()
    origin_url = Field()
    extract_date = Field()