#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoztools.net"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    # def parse(self, response):
    #     filename = response.url.split("/")[-2]
    #     with open(filename,'wb') as f :
    #         f.write(response.body)
    def parse(self, response):
        for sel in response.xpath('//div[@class="title-and-desc"]'):
            item = DmozItem()
            item['title'] = sel.xpath('//div/a[@target="_blank"]/div/text()').extract()
            item['link'] = sel.xpath('//div/a[@target="_blank"]/@href').extract()
            item['desc'] = sel.xpath('//div[@class="site-descr "]/text()').extract()
        yield item

