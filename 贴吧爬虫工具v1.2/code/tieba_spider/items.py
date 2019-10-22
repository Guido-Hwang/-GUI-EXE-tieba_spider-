# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NumItem(scrapy.Item):
    thread_id = scrapy.Field()  # 帖子的ID
    id = scrapy.Field()  # 用户ID
    row = scrapy.Field()  # 用户ID
    has_crawl_page = scrapy.Field()  # 已经爬过的页面数量
    total_page = scrapy.Field()  # 总共有多少页


class PostItem(scrapy.Item):  # 贴吧信息
    id = scrapy.Field()
    url = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    user_num = scrapy.Field()
    bar_name = scrapy.Field()
    reply_num = scrapy.Field()
    thread_id = scrapy.Field()  # 帖子的ID
    post_create_time = scrapy.Field()
    # is_good = scrapy.Field()  # 精品贴标志


class PostContentItem(scrapy.Item):  # 贴吧信息
    comment_content = scrapy.Field()


class UserItem(scrapy.Item):  # 贴吧用户信息
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    post_num = scrapy.Field()
    client = scrapy.Field()
    sex = scrapy.Field()
    year = scrapy.Field()
    focus_num = scrapy.Field()
    fan_num = scrapy.Field()
    client = scrapy.Field()


class UserBarItem(scrapy.Item):  # 用户关注贴吧的信息
    url = scrapy.Field()
    name = scrapy.Field()
    bar_num = scrapy.Field()
    bar_name = scrapy.Field()
    bar_grade = scrapy.Field()
