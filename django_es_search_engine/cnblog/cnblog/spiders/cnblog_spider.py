#-*- coding: utf-8 -*-
# @Time    : 15:51
# @Author  : zhouyan
# @File    :cnblog.py

import scrapy as scrapy
from ..items import cnblogItem


class XpathRule(object):
    '''
    xpath规则
    '''
    post_author = ".//div[@class='post_item_foot']/a/text()"   # 发布作者
    author_link = ".//div[@class='post_item_foot']/a/@href"   # 作者博客主页链接
    post_date = ".//div[@class='post_item_foot']/text()"     # 发布时间
    digg_num = ".//span[@class='diggnum']/text()"      # 推荐数
    title = ".//h3/a/text()"         # 标题
    title_link = ".//h3/a/@href"    # 标题链接
    item_summary = ".//p[@class='post_item_summary']/text()"  # 摘要
    comment_num = ".//span[@class='article_comment']/a/text()"    # 评论数
    view_num = ".//span[@class='article_view']/a/text()"      # 阅读数

    nexturl = ".//a[text()='Next >']/@href"



class cnbolgSpider(scrapy.Spider):
    name = "cnblog_spider"

    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0.1,
        'RETRY_TIMES': 3,  # 重试机制
        'ITEM_PIPELINES': {
            # "scrapyLearn.pipelines.cnblogMysqlPipeline": 100,
            'cnblog.pipelines.cnblogPipeline': 100
        }
    }
    start_url = "https://www.cnblogs.com/legacy"

    def start_requests(self):

        yield scrapy.Request(self.start_url,callback=self.parse)

    def parse(self, response):
        divLst = response.xpath('//div[@id="post_list"]/div')
        for div in divLst:
            item = cnblogItem()
            item["post_author"] = div.xpath(XpathRule.post_author).extract_first()
            item["author_link"] = div.xpath(XpathRule.author_link).extract_first()
            item["post_date"] = div.xpath(XpathRule.post_date).extract()[1].strip().replace('发布于','')
            item["comment_num"] = "".join(div.xpath(XpathRule.comment_num).extract_first()).strip()
            item["view_num"] = div.xpath(XpathRule.view_num).extract_first()
            item["title"] = div.xpath(XpathRule.title).extract_first()
            item["title_link"] = div.xpath(XpathRule.title_link).extract_first()
            summary_lst = div.xpath(XpathRule.item_summary).extract()
            if len(summary_lst) > 1:
                item["item_summary"] = summary_lst[1].strip()
            else:
                item["item_summary"] = summary_lst[0].strip()
            item["digg_num"] = div.xpath(XpathRule.digg_num).extract_first()

            # print(item)
            yield item

            nexturl = response.xpath(XpathRule.nexturl).extract_first()

            if nexturl is not None:
                nexturl = 'https://www.cnblogs.com' + nexturl
                yield scrapy.Request(nexturl, callback=self.parse)

