# -*- coding: utf-8 -*-
import sys
import codecs
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
reload(sys)
sys.setdefaultencoding('utf8')
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class JsonWriterPipeline(object):
    ''' write item to the files'''
    @classmethod
    def from_crawler(cls, crawler):
        ''' start the spider automatically '''
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self):
        ''' open spider '''
        self.file = codecs.open('items.json', 'w', encoding='utf-8')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self):
        ''' close  spider '''
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        ''' process item '''
        self.exporter.export_item(item)
        return item
