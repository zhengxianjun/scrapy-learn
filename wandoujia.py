#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ================= 一、抓取每个子分类的URL ==============
# 导入第三方包
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import pandas as pd


# 设置请求头
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

# 豌豆荚应用首页 > 安卓软件分类 > 网上购物 > 商城下载的链接
url = 'http://www.wandoujia.com/category/5017_591'

# 发送请求
res = requests.get(url, headers = headers).text

# print(res)
# 解析html
soup = BeautifulSoup(res, 'html.parser')

# 商城类APP的5个分类链接及名称
urls_all = soup.findAll('ul', {'class':'switch-tab cate-tab'})[0].findAll('li')[1:]
category_urls = [i.findAll('a')[0]['href'] for i in urls_all]
category_names = [i.text.strip() for i in urls_all]
# print(category_names)

# ============= 二、生成所有子分类及页码的URL ==============
# 各类别的前10页
urlsnames = []
urls =[]

for url,name in zip(category_urls,category_names):
    for i in range(1,11):
        urlsnames.append(name)
        urls.append(url+'/'+str(i))

