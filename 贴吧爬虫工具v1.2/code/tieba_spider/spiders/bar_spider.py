import scrapy
import urllib
import json
from tieba_spider.items import PostItem, PostContentItem
import tieba_spider
import os
import re


class BarSpider(scrapy.Spider):  # 贴吧爬虫
    name = 'bar_spider'
    print('bar_spider的当前路径是：' + os.getcwd())

    def __init__(self, config=None, *args, **kwargsf):
        if not config:
            pass
        try:
            if config:
                tieba_spider.config = config[0]  # 将字符串 转化为字典
                tieba_spider.config['bar_name'] = urllib.parse.unquote(tieba_spider.config['bar_name'])
                tieba_spider.config['post_num'] = int(tieba_spider.config['post_num'])
                tieba_spider.config['spider_name'] = self.name
        except TypeError:
            pass
        if not tieba_spider.config['bar_name']:
            tieba_spider.config['bar_name'] = input('请输入吧名:')
        self.start_urls = ['https://tieba.baidu.com/f?kw=%s' % tieba_spider.config['bar_name']]  # 三国杀吧 PC贴吧

    def start_requests(self):
        # 携带cookie登录
        cookies = 'BAIDUID=45FB8DA09A914E629390863C57F0DC4B:FG=1; BIDUPSID=45FB8DA09A914E629390863C57F0DC4B; PSTM=1559219844; TIEBAUID=c9d81907c343f58656236b9c; TIEBA_USERTYPE=771c50dd5a2a1babb2474f72; bdshare_firstime=1559460699558; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; IS_NEW_USER=c1fb106822622ad8692c2bf4; CLIENTWIDTH=400; CLIENTHEIGHT=922; H_WISE_SIDS=134003_126125_127760_100807_131676_131656_114744_125695_133678_120195_133967_132866_131602_133017_132911_133044_131246_132440_130762_132378_131517_118892_118867_118852_118831_118804_132841_132604_107315_133158_132782_130127_133352_133302_129653_127027_132538_133837_133473_131906_128891_133847_132552_133287_133387_131423_133215_133414_133916_110085_132354_133893_127969_123289_131755_131298_127416_131549_133728_128808_100459; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1561985898,1562900188,1562930631,1562931008; Hm_lvt_7d6994d7e4201dd18472dd1ef27e6217=1562814883,1562917177,1562919244,1562980079; SET_PB_IMAGE_WIDTH=391; BDUSS=lTN2RJMnliRXpYMkVZTWF0emRCQ3d4cjdybThEN1IzdGpxTEI5c1B2cFd5MUJkSVFBQUFBJCQAAAAAAAAAAAEAAAA3T50bMTY2OTEzODMwMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFY-KV1WPildMn; STOKEN=b9b4098b3f68faa05a0a493f5df1739e3fcec7d8d588524739c0f497534c9302; SEENKW=%E4%B8%89%E5%9B%BD%E6%9D%80%23%E6%9E%AA%E7%A5%9E%E7%BA%AA%23%E6%B1%82%E7%94%9F%E4%B9%8B%E8%B7%AF%23%E6%8A%80%E6%9C%AF%E5%AE%85%23%C8%FD%B9%FA%C9%B1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1563070081,1563073804,1563076073,1563153425; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1563154339'
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split(";")}  # cookies 切割
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        for sel in response.xpath('//li[contains(@class, "j_thread_list")]'):  # 获取帖子信息
            data = json.loads(sel.xpath('@data-field').extract_first())
            post_item = PostItem()
            post_item['reply_num'] = data['reply_num']
            # post_item['is_good'] = data['is_good']
            post_item['title'] = sel.xpath('.//div[contains(@class, "threadlist_title")]/a/text()').extract_first()
            post_item['url'] = 'http://tieba.baidu.com/p/%d' % data['id']
            if tieba_spider.config['comment_crawl_flag']:
                # 不爬顶置帖子
                # if not tieba_spider.config['good_crawl_flag'] and data['is_good'] or data['is_top']:
                #     continue
                yield scrapy.Request(  # 进入帖子,爬取评论
                    post_item['url'],
                    callback=self.parse_comment_content,
                )
            else:
                yield scrapy.Request(  # 进入帖子
                    post_item['url'],
                    callback=self.parse_detail,
                    meta={"post_item": post_item},
                )
        # 自动翻页
        next_url = response.xpath("//a[@class='next pagination-item ']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                dont_filter=True  # 防止过滤，不然进入不了执行函数
            )

    # 进入帖子抓取帖子的信息
    def parse_detail(self, response):
        post_item = response.meta["post_item"]

        # 进入帖子抓取帖子的开贴时间信息
        if response.xpath("//*[@id='j_p_postlist']/div[1]/div[2]/div[4]/div[1]/div/span[4]"):
            post_item["post_create_time"] = response.xpath(  # 不是空列表
                "//*[@id='j_p_postlist']/div[1]/div[2]/div[4]/div[1]/div/span[4]/text()").extract_first()  # 帖子的创建时间
        elif response.xpath("//*[@id='j_p_postlist']/div[1]/div[2]/div[4]/div[1]/div/span[3]/text()").extract_first():
            post_item["post_create_time"] = response.xpath(
                "//*[@id='j_p_postlist']/div[1]/div[2]/div[4]/div[1]/div/span[3]/text()").extract_first()  # 帖子的创建时间
        else:
            try:
                data = json.loads(response.xpath("//*[@id='j_p_postlist']/div[1]/@data-field").extract_first())
                post_item["post_create_time"] = data['content']['date']
            except KeyError:
                print('缺少元素')

        yield post_item

    # 进入帖子抓取评论内容
    def parse_comment_content(self, response):
        for floor in response.xpath("//*[@id='j_p_postlist']/div"):
            post_content_item = PostContentItem()
            post_content_item['comment_content'] = []
            content = floor.xpath(
                ".//*[@class='d_post_content j_d_post_content  clearfix']").extract_first()  # new school
            # print(content)
            # print(re.findall(r'style="display:;"> (.*?)</div>', content))
            # 判断字体是否有加强
            if re.findall("<strong>", content):
                # print(re.findall(r'<strong> (.*?)</strong>', content))
                post_content_item['comment_content'] = re.findall(r'<strong>(.*?)</strong>', content)
            else:
                # print(re.findall(r'style="display:;"> (.*?)</div>', content))
                # \S 除了空格以外的所有字符
                post_content_item['comment_content'] = re.findall(r'style="display:;">(.*?)<.*?>', content)

            # 去除空格
            post_content_item['comment_content'] = post_content_item['comment_content'][0].replace(' ', '')
            # print(post_content_item['comment_content'])
            if post_content_item['comment_content']:
                yield post_content_item
            else:
                pass

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    # os.chdir('../.././dist/main')
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl('bar_spider')
    process.start()
