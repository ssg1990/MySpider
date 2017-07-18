# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataparserItem(scrapy.Item):
    '''parse item'''
    # define the fields for your item here like:
    # name = scrapy.Field()
    keyword = scrapy.Field()
    searchIndex = scrapy.Field()
    resultCount = scrapy.Field()
    cRank = scrapy.Field()
    lRank = scrapy.Field()
    ranking = scrapy.Field()

class IpItem(scrapy.Item):
    ''' available ip and port item'''
    ip = scrapy.Field()
    port = scrapy.Field()
    ttl = scrapy.Field()
    