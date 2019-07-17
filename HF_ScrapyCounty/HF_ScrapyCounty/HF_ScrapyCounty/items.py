# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sheriff_no = scrapy.Field()
    case_no = scrapy.Field()
    sale_date = scrapy.Field()
    schd_data = scrapy.Field()
    address = scrapy.Field()
    upset = scrapy.Field()

    plf = scrapy.Field()
    dfd = scrapy.Field()
    att = scrapy.Field()
    att_ph = scrapy.Field()
