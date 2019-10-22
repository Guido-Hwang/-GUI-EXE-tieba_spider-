import urllib.robotparser

import scrapy.core.downloader.handlers.ftp
import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.chunked
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory
# myself file
import urllib
import os
import openpyxl
import ast
import re
import json
import tkinter as tk
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import threading
import time
import middle_file

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

config = {
    'bar_name': '',  # 吧名
    'post_num': 5,  # 默认爬取2000个帖子
    'user_num': 5,  # 默认爬取2000个用户
    'comment_num': 1000000,  # 默认爬取2000条评论
    'section': 0,
    # 0 爬取帖子，用户，用户关注的贴吧
    # 1 只爬取帖子,用户
    # 2 只爬取帖子
    # 3 只爬取用户关注贴吧
    # 4 只爬取用户
    'spider_status': 0,  # 爬虫状态标志位
    # 0 空闲状态，等待命令
    # 1 开启状态
    # 2 结束标志位，准备停止爬取
    'comment_crawl_flag': 0,  # 评论内容爬取标志位
    'good_crawl_flag': False,  # 精品帖子爬取标志位

}
spider_list = []  # 用于放置将执行的爬虫名字


class Gui():

    def __init__(self):
        # 启动按钮
        self.resume_hit = True
        self.start_hit = True
        self.stop_hit = True
        self.exit_hit = True

    def show(self):
        self.window = tk.Tk()
        self.window.title('百度贴吧爬虫程序v1.2')
        self.window.geometry('380x600')  # 这里的乘是小x
        # 第3步，在图形界面上设定标签
        bar_label = tk.Label(self.window, text='请输入吧名', font=('Arial', 11), width=40, height=2)
        bar_label.pack()  # Label内容content区域放置位置，自动调节尺寸
        self.bar_name = tk.Entry(self.window, font=('Arial', 13), width=20,
                                 textvariable=tk.StringVar(value='三国杀'))  # 设置默认的吧名
        self.bar_name.pack()

        self.post_num_label = tk.Label(self.window, text='请输入要爬取的帖子的数量', font=('Arial', 12), width=40,
                                       height=1)
        self.post_num_label.pack()  # Label内容content区域放置位置，自动调节尺寸
        self.post_num = tk.Entry(self.window, font=('Arial', 13), width=20, textvariable=tk.StringVar(value='10'))
        self.post_num.pack()

        self.user_num_label = tk.Label(self.window, text='请输入要爬取的用户的数量', font=('Arial', 12), width=40,
                                       height=2)
        self.user_num_label.pack()  # Label内容content区域放置位置，自动调节尺寸
        self.user_num = tk.Entry(self.window, font=('Arial', 13), width=20, textvariable=tk.StringVar(value='10'))
        self.user_num.pack()

        ################################ 显示帖子统计人数选项
        def count_selection():
            count.config(text='你选择了第' + self.count_flag.get() + '项')

        self.count_flag = tk.StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        self.count_flag.set('0')
        count = tk.Label(self.window, width=40, text='统计功能：请选择一个选项，默认关闭统计功能')
        count.pack()
        tk.Radiobutton(self.window, text='关闭统计帖子参与讨论的人数', variable=self.count_flag, value=0,
                       command=count_selection).pack()
        tk.Radiobutton(self.window, text='开启统计帖子参与讨论的人数', variable=self.count_flag, value=1,
                       command=count_selection).pack()

        ################################ 评论内容爬取选项
        def comment_func_selection():
            count.config(text='你选择了第' + self.count_flag.get() + '项')

        self.comment_crawl_flag = tk.StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        self.comment_crawl_flag.set('0')
        comment = tk.Label(self.window, width=40, text='爬取评论功能：请选择一个选项，默认关闭功能')
        comment.pack()
        tk.Radiobutton(self.window, text='关闭爬取评论内容功能', variable=self.comment_crawl_flag, value=0,
                       command=comment_func_selection()).pack()
        tk.Radiobutton(self.window, text='开启爬取评论内容功能', variable=self.comment_crawl_flag, value=1,
                       command=comment_func_selection()).pack()

        ######################## 显示启动选项
        def print_selection():
            l.config(text='你选择了第' + self.operation.get() + '项')

        self.operation = tk.StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        self.operation.set('0')
        l = tk.Label(self.window, width=40, text='参数设置：请选择一个选项，默认为爬取全部')
        l.pack()
        # 第5步，创建三个radiobutton选项，其中variable=var, value='A'的意思就是，当我们鼠标选中了其中一个选项，把value的值A放到变量var中，然后赋值给variable
        tk.Radiobutton(self.window, text='只爬取用户关注的贴吧,(已经有用户数据才可以使用！！！)', variable=self.operation, value=3,
                       command=print_selection).pack()
        tk.Radiobutton(self.window, text='爬取帖子，用户，用户关注的贴吧', variable=self.operation, value=0,
                       command=print_selection).pack()
        tk.Radiobutton(self.window, text='只爬取帖子,用户', variable=self.operation, value=1, command=print_selection).pack()
        tk.Radiobutton(self.window, text='只爬取帖子', variable=self.operation, value=2, command=print_selection).pack()

        tk.Button(self.window, text='开始爬取', font=('Arial', 11), width=15, height=1,
                  command=self.start_func).pack()
        tk.Button(self.window, text='结束程序', font=('Arial', 11), width=15, height=1,
                  command=self.exit_func).pack()
        tk.Button(self.window, text='结束当前任务', font=('Arial', 11), width=15, height=1,
                  command=self.stop_func).pack()
        tk.Button(self.window, text='暂停爬取/恢复爬取', font=('Arial', 11), width=15, height=1,
                  command=self.resume_func).pack()

        self.window.mainloop()

    def resume_func(self):
        if self.resume_hit:
            self.resume_hit = False
            middle_file.config['spider_status'] = 3  # 停止爬虫标志位
        else:
            middle_file.config['spider_status'] = 1  # 停止爬虫标志位
            self.resume_hit = True

    def stop_func(self):
        if self.stop_hit:
            self.stop_hit = False
            middle_file.config['spider_status'] = 2  # 停止爬虫标志位
        else:
            self.stop_hit = True

    def exit_func(self):
        if self.exit_hit:
            self.exit_hit = False
            reactor.callFromThread(reactor.stop)
        else:
            self.exit_hit = True

    def start_func(self):
        if self.start_hit:
            self.start_hit = False
            config['bar_name'] = self.bar_name.get()
            config['post_num'] = int(self.post_num.get())
            config['user_num'] = int(self.user_num.get())
            config['section'] = int(self.operation.get())
            config['count_flag'] = int(self.count_flag.get())
            config['comment_crawl_flag'] = int(self.comment_crawl_flag.get())

            if not config['section'] == 3:
                spider_list.append('bar_spider')
                if not config['section'] == 2:
                    spider_list.append('user_spider')
                    if not config['section'] == 1:
                        spider_list.append('user_bar_spider')
            else:
                spider_list.append('user_bar_spider')

            config['spider_status'] = 1  # 启动爬虫
            # 0 爬取帖子，用户，用户关注的贴吧
            # 1 只爬取帖子,用户
            # 2 只爬取帖子
            # 3 只爬取用户关注的贴吧
            # 启动
            # gui.window.quit()
            if config['count_flag']:
                self.user_num.delete(0, 10)
                self.user_num.insert(0, '全部爬取')
        else:
            self.start_hit = True


# 开启多线程，GUI界面
gui = Gui()
t_gui = threading.Thread(target=gui.show, name='gui_thread')
t_gui.start()
while not config['spider_status']:
    print(time.strftime("wait for GUI command %Y-%m-%d %H:%M:%S", time.localtime()))
    time.sleep(1)

print(spider_list)
start_time = time.time()  # 转化格式
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    for spider in spider_list:
        yield runner.crawl('%s' % spider, [config])
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
print('完成任务,请关闭窗口')
end_time = time.time()  # 转化格式

# 这是计算此时运行耗费多长时间，特意转化为 时:分:秒
Total_time = end_time - start_time
m, s = divmod(Total_time, 60)
h, m = divmod(m, 60)
print("共耗时===>%d时:%02d分:%02d秒" % (h, m, s))
gui.window.destroy()
