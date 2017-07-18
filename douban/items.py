# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()
    movie_name = scrapy.Field()
    score = scrapy.Field()
    star_score = scrapy.Field()
    ratting_people = scrapy.Field()
    five_stars = scrapy.Field()
    four_stars = scrapy.Field()
    three_stars = scrapy.Field()
    two_stars = scrapy.Field()
    one_star = scrapy.Field()
    shortComment_num = scrapy.Field()
    short_comments = scrapy.Field()
    movieComment_num = scrapy.Field()
    movie_comments = scrapy.Field()
    most_popular_comment = scrapy.Field()
    pass    


class commentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #first page and the second page should be grabbed
    domain = scrapy.Field()
    mobile_url = scrapy.Field()
    url = scrapy.Field()
    movie_name = scrapy.Field()
    comment_title = scrapy.Field()
    comment_content_words = scrapy.Field()
    comment_writer = scrapy.Field()
    comment_recommendation = scrapy.Field()
    comment_star = scrapy.Field()
    comment_useful = scrapy.Field()
    comment_useless = scrapy.Field()

class writerItem(scrapy.Item):
    domain = scrapy.Field()
    comment_url = scrapy.Field()
    url = scrapy.Field()
    movie_name = scrapy.Field()
    writer_name = scrapy.Field()
    writer_join_time = scrapy.Field()
    writer_focus_num = scrapy.Field()
    writer_be_focused_num = scrapy.Field()
    writer_comment_num = scrapy.Field()
    writer_movies_num = scrapy.Field()

class completeCommentItem(scrapy.Item):
    movie_name = scrapy.Field()
    writer_name = scrapy.Field()
    writer_join_time = scrapy.Field()
    writer_focus_num = scrapy.Field()
    writer_be_focused_num = scrapy.Field()
    writer_comment_num = scrapy.Field()
    writer_movies_num = scrapy.Field()
    comment_title = scrapy.Field()
    comment_content_words = scrapy.Field()
    comment_recommendation = scrapy.Field()
    comment_star = scrapy.Field()
    comment_useful = scrapy.Field()
    comment_useless = scrapy.Field()
    