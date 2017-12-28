#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy

class lianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ["cd.lianjia.com"]
    start_urls = ['https://cd.lianjia.com/ershoufang/']

    def parse(self, response):
        print(response.body)
