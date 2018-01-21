# -*- coding: utf-8 -*-
import scrapy
import re


#class StocksSpider(scrapy.Spider):
#    name = 'stocks'
#    start_urls = ['http://quote.eastmoney.com/stocklist.html']
#    
#
#    def parse(self, response):
#        for href in response.css('a::attr(href)').extract():
#            try:
#                stock = re.findall(r"[s][hz]\d{6}",href)[0]
#                url = "https://gupiao.baidu.com/stock/"+stock+".html"
#                yield scrapy.Request(url,callback=self.parse_stock)
#            except:
#                continue
#    
#    def parse_stock(self, response):
#        infoDict = {}
#        stockInfo = response.css('.stock-bets')
#        name = stockInfo.css('.bets-name').extract()[0]
#        keyList = stockInfo.css('dt').extract()
#        valueList = stockInfo.css('dd').extract()
#        for i in range(len(keyList)):
#            key = re.findall(r'>.*</dt>',keyList[i])[0][1:-5]
#            try:
#                val = re.findall(r'\d+\.?.*</dd>',valueList[i])[0][0:-5]
#            except:
#                val = '--'
#            infoDict[key] = val
#        infoDict.update(
#                {'股票名称': re.findall('\s.*\(', name)[0].split()[0] + \
#                re.findall(r'\>.*\<',name)[0][1:-1]})
#                
#        yield infoDict
            
class StocksSpider(scrapy.Spider):
    name = "stocks"
    start_urls = ['http://quote.eastmoney.com/stocklist.html']
 
    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}", href)[0]
                url = 'http://gupiao.baidu.com/stock/' + stock + '.html'
                cookies = {                        
                        'BAIDUID':'E6411BDBE70B8C49CBD38E4F7E188437',
                        'FG':'1', 
                        'BIDUPSID':'E6411BDBE70B8C49CBD38E4F7E188437', 
                        'PSTM':'1457659595', 
                        'BDUSS':'1lIUzIwMEJ6NEozT1QzRDE3U3ZpaEpOZWFmTjAzdmtMVFpLMHd2bWtIM0hsSzlaTUFBQUFBJCQAAAAAAAAAAAEAAADwMBwNvvPHv9ChzeO2uQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMcHiFnHB4hZY', 
                        'H_PS_PSSID':'1421_21092_20718', 
                        'BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598', 
                        'Hm_lvt_35d1e71f4c913c126b8703586f1d2307':'1516455601', 
                        'PSINO':'2', 
                        'BDRCVFR[feWj1Vr5u3D]':'I67x6TjHwwYf0', 
                        'Hm_lpvt_35d1e71f4c913c126b8703586f1d2307':'1516539423'
                        }
                yield scrapy.Request(url,cookies=cookies, callback=self.parse_stock)
            except:
                continue
 
    def parse_stock(self, response):
        infoDict = {}
        stockInfo = response.css('.stock-bets')
        name = stockInfo.css('.bets-name').extract()[0]
        keyList = stockInfo.css('dt').extract()
        valueList = stockInfo.css('dd').extract()
        for i in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[i])[0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>', valueList[i])[0][0:-5]
            except:
                val = '--'
            infoDict[key]=val
 
        infoDict.update(
            {'股票名称': re.findall('\s.*\(',name)[0].split()[0] + \
             re.findall('\>.*\<', name)[0][1:-1]})
        yield infoDict        
        
        
