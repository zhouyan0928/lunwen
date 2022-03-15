#-*- coding: utf-8 -*-
# @Time    : 12:44
# @Author  : zhouyan
# @File    :run.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl('cnblog_spider')
process.start()