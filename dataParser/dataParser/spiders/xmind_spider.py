#coding=utf-8
import scrapy
from scrapy import Request
from ..items import DataparserItem
KEY_LIST_DEFAULT = [
    '思维导图',
    'xmind',
    'xmind cloud',
    'lighten',
    '流程图',
    '头脑风暴'
]

class xmind_spider(scrapy.Spider):
    urlTpl = "https://aso100.com/search?country=cn&search="
    urlEnd = "https://www.baidu.com/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":" , deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control":"max-age=0",
        "Host":"aso100.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }

    name = 'xmspider'
    domain = 'aso100.com'

    def start_requests(self):
        return [Request("https://aso100.com/",
                        callback=self.url_parse)]

    def url_parse(self, response):
        print "---------------------------Get Url------------------------"
        for keyword in KEY_LIST_DEFAULT:
            url = self.urlTpl + keyword
            yield Request(url, meta={'dont_redirect':True,'handle_httpstatus_list':[302],'keyword':keyword},headers={'Referer': response.url}, callback=self.data_parse)

    def data_parse(self, response):
        # parse_item = DataparserItem()
        # parse_item['keyword'] = response.meta['keyword']
        # parse_item['searchIndex'] = response.css('.search-index-list td a::text').extract()[0].strip()
        # parse_item['resultCount'] = response.css('.search-index-list td a::text').extract()[1].strip()
        # key_list = response.css('.keyword-histroy .media-body .media-heading a::text').extract()
        # parse_item['cRank'] = self.get_rank(key_list)[0]
        # parse_item['lRank'] = self.get_rank(key_list)[1]
        tempItem = {}
        tempItem['keyword'] = response.meta['keyword']
        tempItem['searchIndex'] = response.css('.search-index-list td a::text').extract()[0].strip()
        tempItem['resultCount'] = response.css('.search-index-list td a::text').extract()[1].strip()
        for i in range(5):
          child_url = 'https://aso100.com/search/searchMore?page=' + \
          str(i) + \
          '&search=' + \
          response.meta['keyword'] + \
          '&country=cn'
          print "******************"+child_url+"***************************************"
          yield Request(child_url, meta={'dont_redirect':True,'handle_httpstatus_list':[302],'tempItem':tempItem},headers={'Referer': response.url}, callback=self.data_gen)     
    
    def data_gen(self, response):
        key_list = response.css('.keyword-histroy .media-body .media-heading a::text').extract()
        (c_rank, l_rank) = self.get_rank(key_list)
        if c_rank == -1 and l_rank == -1:
            print '*********************c_rank=-1,l_rank=-1****************************'
            return
        parse_item = DataparserItem()
        parse_item['keyword'] = response.meta['tempItem']['keyword']
        parse_item['searchIndex'] = response.meta['tempItem']['searchIndex']
        parse_item['resultCount'] =  response.meta['tempItem']['resultCount']
        if c_rank != -1:
            parse_item['cRank'] = '#c' + c_rank
        else:
            parse_item['cRank'] = 'none'
        if l_rank != -1:
            parse_item['lRank'] = '#l' + l_rank
        else:
            parse_item['lRank'] = 'none'
        return parse_item

    def get_rank (self, ranklist):
        ''' get the rank of key word '''
        c_rank = -1
        l_rank = -1
        dest_str1 = "Lighten-思维导图，美且好用的头脑风暴脑图工具 by XMind"
        dest_str2 = "XMind Cloud" 
        for item in ranklist:
            if item.find(dest_str2) != -1:
                c_rank = str(filter(str.isdigit, item.encode('utf-8').strip()[0:3]))
            elif item.find(dest_str1) != -1:
                l_rank = str(filter(str.isdigit, item.encode('utf-8').strip()[0:3]))
        return (c_rank, l_rank)