#coding=utf-8
import urllib
import time
import scrapy
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from ..items import MovieItem, writerItem, commentItem, completeCommentItem
from scrapy.http import Request, FormRequest
MOVIE_LIST = [
    "幸运是我",
    "路边野餐",
    "追凶者也",
    "踏血寻梅",
    "一个叫欧维的男人决定去死",
    "完美陌生人",
    "萨利机长",
    "大空头",
    "初恋这首情歌",
    "卧虎藏龙 青冥宝剑",
    "致青春 原来你也在这里",
    "惊天破",
    "我的新野蛮女友",
    "封神传奇",
    "功夫熊猫3",
    "一切都好",
    "消失的爱人",
    "真相禁区",
    "极限挑战",
    "星球大战之原力觉醒",
    "过年好",
    "西游记之孙悟空之三大白骨精",
    "美人鱼",
    "澳门风云3",
    "叶问3",
    "地心营救",
    "疯狂动物城",
    "爱情麻辣烫之情定终身",
    "荒野猎人",
    "大轰炸",
    "不速之客",
    "睡在我上铺的兄弟",
    "火锅英雄",
    "大唐玄奘",
    "梦想合伙人",
    "美国队长3",
    "百鸟朝凤",
    "夜孔雀",
    "爱丽丝梦游仙境2：镜中奇遇记",
    "X战警：天启",
    "魔兽",
    "独立日2：卷土重来",
    "惊天魔盗团2",
    "赏金猎人",
    "寒战2",
    "大鱼海棠",
    "致青春 原来你还在这里",
    "盗墓笔记",
    "夏有乔木 雅望天堂",
    "使徒行者",
    "鲨滩",
    "七月与安生",
    "大话西游3",
    "爵迹",
    "从你的全世界路过",
    "湄公河行动",
    "王牌逗王牌",
    "圆梦巨人",
    "驴得水",
    "奇异博士",
    "比利·林恩的中场战事",
    "我不是潘金莲",
    "神奇动物在哪里",
    "你的名字",
    "血战钢锯岭",
    "罗曼蒂克消亡史",
    "长城"
  ]


class douban_spider(scrapy.Spider):
    urlTpl = "https://movie.douban.com/subject_search?search_text="
    urlEnd = "https://www.baidu.com/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate,sdch,br",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Host":"movie.douban.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0(Windows NT 6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/56.0.2924.87Safari/537.36"
    }
    movie_urls = []

    commentURLs = []

    name = 'dbspider'
    domain = 'douban.com'

    def start_requests(self):
        return [Request("https://www.douban.com/accounts/login?source=movie",
                        callback=self.Login, meta={"cookiejar": 1})]

    def Login(self,response):
        url = "https://www.douban.com/accounts/login?source=movie"
        if response.css('#capcha_image::attr(src)'):
            captcha =  response.css('#captcha_image::attr(src)').extract()[0]
            print ('Saving picture')
            captchapicfile = "D:/spider_douban/douban/captcha.png"
            urllib.urlretrieve(captcha,filename = captchapicfile)
            print ('input the valid code')
            captcha_value = raw_input()
            data = {
                'form_email':"317851337@qq.com",
                'form_password':"sunshuguang9051",
                'captcha-solution':captcha_value
            }
        else:
            data = {
                'form_email': "317851337@qq.com",
                'form_password': "sunshuguang9051",
            }
        print ('------------------------------loading-----------------------------------')
        return [FormRequest.from_response(response,
                                              meta={"cookiejar":response.meta["cookiejar"]},
                                              formdata = data,
                                              callback=self.url_parse,
                                              )]


    def url_parse(self,response):
        for movie_name in MOVIE_LIST:
            print '---------------------------search movie------------------------'
            movie_url = self.urlTpl + movie_name
            yield Request(movie_url, meta={"cookiejar":response.meta["cookiejar"],'movie_name':movie_name},headers={'Referer': response.url}, callback=self.page_parse)
        pass

    def page_parse(self,response):
        movie_url = response.css('.pl2 a::attr(href)').extract()[0]
        print '---------------------------get url----------------------'+movie_url+'---------------'
        yield Request(movie_url, headers={'Referer': response.url},
                meta={"cookiejar":response.meta["cookiejar"],'movie_name':response.meta['movie_name']}, callback=self.movie_parse)
        pass

    def movie_parse(self,response):
        curURL = response.url
        movie = MovieItem()
        movie['movie_name'] = response.meta['movie_name']
        star_rate = response.css('span.rating_per::text').extract()
        movie['five_stars'] = star_rate[0].strip()
        movie['four_stars'] = star_rate[1].strip()
        movie['three_stars'] = star_rate[2].strip()
        movie['two_stars'] = star_rate[3].strip()
        movie['one_star'] = star_rate[4].strip()
        movie['score'] = response.css('.ll.rating_num::text').extract()[0]
        movie['star_score'] = int(filter(str.isdigit,response.css('.rating_right div::attr(class)').extract()[0].encode('utf-8')))/10.0
        shortNum = response.css('#comments-section .mod-hd h2 span a::text').extract()[0].strip()
        movie['shortComment_num'] = filter(str.isdigit, shortNum.encode('utf-8'))
        commentNum = response.css('section header .pl a::text').extract()[0].strip()
        movie['movieComment_num'] = filter(str.isdigit, commentNum.encode('utf-8'))
        movie['ratting_people'] = response.css('.rating_people span::text').extract()[0]
        movieCommentUrl = curURL + 'reviews'
        shotCommentUrl = curURL + 'comments?status=P'
        # return movie
        yield Request(self.urlEnd, headers = {'Referer':response.url},meta={"cookiejar":response.meta["cookiejar"],'movie':movie,'movie_name':response.meta['movie_name']},callback=self.movie_retrive)
        yield Request(movieCommentUrl, headers = {'Referer':response.url},meta={"cookiejar":response.meta["cookiejar"],'movie_name':response.meta['movie_name']}, callback=self.movie_comments_parse)
        # yield Request(shotCommentUrl, headers = {'Referer':response.request.url}, callback=self.shotCommentParse)
        # print movie['film_name']
        # for k,v in movie.items():
        #     print " dict[%s]=" % k,v
        # print movie['film_name']
        # print movie['five_stars']
        # print movie['four_stars']
        # print movie['three_stars']
        # print movie['two_stars']


    def movie_comments_parse(self,response):
        next_page_url = response.url + '?start=20'
        page_comment_urls = response.css('.review-list .title-link::attr(href)').extract()
        for comment in page_comment_urls:
            yield Request(comment.strip(), headers = {'Referer':response.url},meta={"cookiejar":response.meta["cookiejar"],'movie_name':response.meta['movie_name']},callback=self.movie_comment_parse)
        if (response.css('.paginator .next a')):
            yield Request(next_page_url, headers={'Referer': response.url},meta={"cookiejar":response.meta["cookiejar"],'movie_name':response.meta['movie_name']}, callback=self.movie_comments_next_parse)
        pass

    def movie_comments_next_parse(self,response):
        page_comment_urls = response.css('.review-list .title-link::attr(href)').extract()
        for comment in page_comment_urls:
            yield Request(comment.strip(), headers={'Referer': response.url},meta={"cookiejar":response.meta["cookiejar"],'movie_name':response.meta['movie_name']}, callback=self.movie_comment_parse)
        pass

    def movie_comment_parse(self,response):
        comment = commentItem()
        print '---------------------movieCommentParse: '+response.url+'----------------------'
        comment['movie_name'] = response.meta['movie_name']
        comment['comment_title'] = response.css('h1 span::text').extract()[0].strip()
        comment['comment_content_words'] = len((response.css('.review-content::text').extract()[0]).strip())
        comment['comment_writer'] = response.css('.main-hd a span::text').extract()[0].strip()
        comment['comment_recommendation'] = response.css('span.rec a::text').extract()[0].strip()
        comment['comment_star'] = response.css('.main-hd span::text').extract()[1].strip()
        comment['comment_useful'] = response.css('.btn.useful_count::text').extract()[0].strip()
        comment['comment_useless'] = response.css('.btn.useless_count::text').extract()[0].strip()
        comment_writer_url = response.css('.main-hd a::attr(href)').extract()[0].strip()
        yield Request(comment_writer_url, headers={'Referer': response.url},meta={"cookiejar":response.meta["cookiejar"],'Comment':comment,'movie_name':response.meta['movie_name']}, callback=self.comment_writer_parse)
        pass

    def comment_writer_parse(self,response):
        completeItem = completeCommentItem()
        completeItem['movie_name'] = response.meta['movie_name']
        completeItem['writer_name'] = response.css('h1::text').extract()[0].strip()
        completeItem['writer_join_time'] = response.css('.user-info .pl::text').extract()[1].strip()[0:10]
        completeItem['writer_focus_num'] = response.css('#friend .pl a::text').extract()[0][2:]
        completeItem['writer_be_focused_num'] = filter(str.isdigit,response.css('.rev-link a::text').extract()[0].encode('utf-8'))
        completeItem['writer_comment_num'] = response.css('#review a::text').extract()[0][2:]
        completeItem['writer_movies_num'] = filter(str.isdigit,response.css('#review a::text').extract()[0].encode('utf-8'))
        completeItem['comment_title'] = response.meta['Comment']['comment_title']
        completeItem['comment_content_words'] = response.meta['Comment']['comment_content_words']
        completeItem['comment_recommendation'] = response.meta['Comment']['comment_recommendation']
        completeItem['comment_star'] = response.meta['Comment']['comment_star']
        completeItem['comment_useful'] = response.meta['Comment']['comment_useful']
        completeItem['comment_useless'] = response.meta['Comment']['comment_useless']
        return completeItem
        pass

    def movie_retrive(self,response):
        print '------movie-retrive-------'
        return response.meta['movie']

