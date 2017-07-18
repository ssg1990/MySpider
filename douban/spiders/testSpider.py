import scrapy

class TestSpider(scrapy.Spider):
    name = 'test'
    def start_requests(self):
        requests = []
        for item in self.start_urls:
            requests.append(scrapy.Request(url = item, headers={'Referer':'https://www.baidu.com'},callback = self.parse))
        return requests

    def parse(self,response,crawler):
        print 'now'
        print crawler.settings.getlist('USER_AGENTS')
