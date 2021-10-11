import time
import uuid

import requests
from bs4 import BeautifulSoup

from Crawer import DataBaseUtil

sql = """select url from t_web_crawler where context is null"""
db = DataBaseUtil.UsingMysql().__enter__()
all = db.fetch_all(sql)
for i in all:
    item = i['url']

    context1 = requests.get(item)
    context1.encoding = 'gbk'
    detail_html = context1.text
    # 获取电影标题
    detail_title = BeautifulSoup(detail_html, 'lxml').find('div', class_='title_all').find('h1')

    # 获取电影的种子链接
    target = BeautifulSoup(detail_html, 'lxml').find('div', id='Zoom').find('a')
    magnet = target['href']
    # 电影简介内容(简介中有 '  会导致sql语句有问题，把’ 替换成空)
    context = BeautifulSoup(detail_html, 'lxml').find('div', id='Zoom').get_text().replace("'", "")

    sql = "update t_web_crawler set context = '%s' where url = '%s'" % (context, item)
    print("sql: " + sql)
    db.insert_one(sql)

    print(item + "更新完成！")
# 关闭数据库链接
db.__exit__()
