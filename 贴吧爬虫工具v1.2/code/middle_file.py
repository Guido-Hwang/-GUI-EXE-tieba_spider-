config = {
    'bar_name': '',  # 吧名
    'post_num': 5,  # 默认爬取2000个帖子
    'user_num': 5,  # 默认爬取2000个用户
    'comment_num': 2000,  # 默认爬取2000条评论
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
    # 3 暂停标志位，暂停
    'count_flag': False,  # 统计人数功能
    'spider_name': '',  # 正在进行的任务
    'bar_type': 'old_school',
    # 不同的贴吧有不同的格式，需要做不同的处理
    # old_school 有加载total_comment文件的贴吧
    # new_school 没有
    'comment_crawl_flag': 0,  # 评论内容爬取标志位
    'good_crawl_flag': False,  # 精品帖子爬取标志位
}