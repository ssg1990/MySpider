#coding=utf-8
import urllib2
import scrapy
from scrapy import Request
from ..items import IpItem

class ip_spider(scrapy.Spider):
    urlInit = "http://www.xicidaili.com/nn/"
    urlTpl = "http://www.xicidaili.com"
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

    name = 'ipspider'
    domain = 'xicidaili.com/'

    def start_requests(self):
        return [Request(self.urlInit,
                        callback=self.data_parse)]

    def data_parse(self, response):
        self.ip_get(response)
        if len(response.css('.next_page'))!=0:
          yield Request(self.urlTpl+response.css('.next_page::attr(href)').extract()[0], meta={'dont_redirect':True,'handle_httpstatus_list':[302]},headers={'Referer': response.url}, callback=self.data_parse)     
    
    def ip_get(self,response):
        ipItem = IpItem()
        ip_item = response.css('tr.odd')
        # [0] ip  [1] port [10] ttl
        for ip_addr in ip_item:
            curItem = ip_addr.css('td::text').extract()
            if self.test_valid(curItem[0], curItem[1]):
                ipItem['ip'] = curItem[0]
                ipItem['port'] = curItem[1]
                ipItem['ttl'] = curItem[10]
        return ipItem
    
    def test_valid(self, ip, port):
        print '------------------------test valid---------------------'
        proxy={'http':ip+':'+port}
        print proxy

        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

        test_url = 'http://www.baidu.com'
        req = urllib2.Request(test_url)
        try:
          resp = urllib2.urlopen(req, timeout=10)
          if resp.code == 200:
            print '-------------------sucess------------------------'
            return True
          else:
            return False
        except:
          print '--------------------not work-----------------------'
          return False