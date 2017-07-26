# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from fake_useragent import UserAgent
from AmazonSpider.tools.crawl_xici_ip import GetIP


class RandomUserAgentMiddleware(object):
    # 随即更换user_agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            ''' Gets random UA based on the type setting (random, firefox…) '''
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        get_ip = GetIP().get_random_ip()
        request.meta['proxy'] = get_ip

