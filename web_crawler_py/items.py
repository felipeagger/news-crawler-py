# -*- coding: utf-8 -*-
import scrapy


class NoticiasItem(scrapy.Item):
    uuid = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
