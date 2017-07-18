import urllib
import scrapy
from scrapy.http import Request,FormRequest
from scrapy.crawler import CrawlerRunner
from twisted.internet.task import reactor
from douban_spider import douban_spider
class DoubanLoginSpider(scrapy.Spider):
    name = 'DoubanLogin'
    allowed_domains = ['douban.com']

    UserAgent = {
        "User-Agent:": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2050.400 QQBrowser/9.5.10169.400"}

    def start_requests(self):
        return [Request("https://www.douban.com/accounts/login?source=movie", headers = {"User-Agent":self.UserAgent} ,callback=self.login, meta={"cookiejar": 1})]

    def login(self,response):
        captcha =  response.css('#captcha_image::attr(src)').extract()[0]
        # url = "https://www.douban.com/accounts/login?source=movie"
        print ('Saving picture')
        captchapicfile = "D:/spider_douban/douban/captcha.png"
        urllib.urlretrieve(captcha,filename = captchapicfile)
        print ('input the valid code')
        captcha_value = input()

        data = {
            'form_email':"317851337@qq.com",
            'form_password':"sunshuguang9051",
            'captcha-solution':captcha_value
        }
        print ('loading')
        return [FormRequest.from_response(response,
                                              meta={"cookiejar":response.meta["cookiejar"]},
                                              headers = self.UserAgent,
                                              formdata = data,
                                              callback=self.crawlerdata,
                                              )]
    def crawlerdata(self):
        runner = CrawlerRunner()
        runner.crawl(douban_spider)
        reactor.run()
        # print(content2[0])