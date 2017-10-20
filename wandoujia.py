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
    for i in range(1,2):
        urlsnames.append(name)
        urls.append(url+'/'+str(i))

# ============= 三、抓取子分类页面下各APP对应的URL ============
# 根据每一页的url抓出对应app的链接
app_urls = []

for url in urls:
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')

    # 返回每个页面中app对应的链接
    # 为防止报错，做异常处理
    try:
        app_lists = soup.findAll('ul', {'id':'j-tag-list'})[0]
        app_urls.extend([i.findAll('a')[0]['href'] for i in app_lists.findAll('h2', {'class':'app-title-h2'})])
    except:
        pass

# ============= 四、抓取各类APP的详细信息 ================
# 构建空的列表，用于数据的存储
appname = []
appcategory = []
install = []
love = []
comments = []
size = []
update = []
version = []
platform = []
company = []

for url in app_urls:
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        #通过标记抓取APP的信息
        appname.append(soup.find('p',{'class':'app-name'}).text.strip())
        appcategory.append('-'.join(soup.find('dl', {'class':'infos-list'}).findAll('dd')[1].text.strip().split('\n')))
        install.append(soup.find('span',{'class':'item install'}).find('i').text)
        love.append(soup.find('span',{'class':'item love'}).find('i').text)
        comments.append(soup.find('div',{'class':'comment-area'}).find('i').text)
        size.append(soup.find('dl',{'class':'infos-list'}).findAll('dd')[0].text.strip())
        update.append(soup.find('dl',{'class':'infos-list'}).findAll('dd')[3].text.strip())
        version.append(soup.find('dl',{'class':'infos-list'}).findAll('dd')[4].text.strip())
        platform.append(soup.find('dl',{'class':'infos-list'}).findAll('dd')[5].text.strip().split('\n')[0])
        company.append(soup.find('dl',{'class':'infos-list'}).findAll('dd')[6].text.strip())
    except:
        pass

# ================ 五、数据存储 ====================
# 将数据的列表写入到字典，并进行数据的转换
apps = pd.DataFrame({
    'appname':appname,
    'appcategory':appcategory,
    'install':install,
    'love':love,
    'comments':comments,
    'size':size,
    'update':update,
    'version':version,
    'platform':platform,
    'company':company
})
# 数据导出
apps.to_excel('app.xlsx', index=False)

