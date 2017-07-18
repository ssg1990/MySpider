# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import codecs
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.exceptions import DropItem 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spiders.douban_spider import MOVIE_LIST
from items import MovieItem,commentItem,writerItem
class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def __init__ (self):
        self.key_dict = dict()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if item['keyword'] in self.key_dict.keys():
          if item['cRank'] != 'none':
            self.key_dict[item['keyword']] = item['cRank']
          if item['lRank'] != 'none':
            self.key_dict[item['keyword']] = item['lRank']
          raise DropItem('Duplicate item:%s' % item)
        else:
          self.key_dict[item['keyword']] = item['keyword']
        self.exporter.export_item(item)
        return item