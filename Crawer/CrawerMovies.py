import time
import uuid

import requests
from bs4 import BeautifulSoup
from redisbloom.client import Client
from Crawer import DataBaseUtil

print("======开始清除redis上次残存的数据======")
rb = Client(host='localhost', port=6379)
rb.delete('urls')  # 每次重新加载时，先删除上次key的信息
print("======清除成功！======")

print("======开始将数据加载到redis======")
# 先将数据库中的数据加载到redis中
sql = """select url from t_web_crawler"""
all = DataBaseUtil.UsingMysql().__enter__().fetch_all(sql)
for i in all:
    items = i['url']
    rb.bfAdd('urls', items)
print("======数据加载到redis中成功！======")

url = 'https://www.dytt8.net/index.htm'
context = requests.get(url)
# 解决乱码 原网站用的是gb2312，用了之后个别字体仍然是乱码。换成了GBK 兼容GB 2312 编码,为GB 2312 的升级版本。
context.encoding = 'gbk'
html = context.text
# 获取所有的a标签
target = BeautifulSoup(html, 'lxml').find('div', class_='co_content2').find_all('a')

base_url = 'https://www.dytt8.net'
beginTime = time.time()
print("爬虫任务开始--->" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
num = 0

# 实例化
# wb = Workbook()
# 激活 worksheet
# ws = wb.active

# ws['A1'] = "日期"
# ws['B1'] = "电影名称"
# ws['C1'] = "网址"
# ws['D1'] = "磁力链接"

db = DataBaseUtil.UsingMysql().__enter__()
for a in target:
    tempLink = a.get('href')
    # 过滤
    if tempLink.find("20160320") >= 0:
        continue
    # 截取链接中的日期
    n = tempLink.find("2")
    date = tempLink[n:n + 8]

    href = base_url + tempLink  # 每个详细页面的url

    # 如果该url存在，则跳出本次循环
    if rb.bfExists('urls', href) == 1:
        print(href + " 已经存在。")
        continue

    context1 = requests.get(href)
    context1.encoding = 'gbk'
    detail_html = context1.text
    # 获取电影标题
    detail_title = BeautifulSoup(detail_html, 'lxml').find('div', class_='title_all').find('h1')

    # 获取电影的种子链接
    target = BeautifulSoup(detail_html, 'lxml').find('div', id='Zoom').find('a')
    magnet = target['href']
    # 电影简介内容(简介中有 '  会导致sql语句有问题，把’ 替换成空)
    context = BeautifulSoup(detail_html, 'lxml').find('div', id='Zoom').get_text().replace("'", "")

    uid = str(uuid.uuid4()).replace('-', '')
    name = detail_title.text
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    is_delete = 'N'

    sql = "INSERT INTO t_web_crawler(id, date, name, url, magnet, create_time, modify_time, is_delete, context)\
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (uid, date, name, href, magnet, create_time, modify_time, is_delete, context)
    print("sql：", sql)

    db.insert_one(sql)
    # ws.cell(row=num + 2, column=1).value = date
    # ws.cell(row=num + 2, column=2).value = detail_title.text
    # ws.cell(row=num + 2, column=3).value = href
    # ws.cell(row=num + 2, column=4).value = magnet

    print(href + " ---> " + detail_title.text)

    num = num + 1

endTime = time.time()
useTime = (endTime - beginTime)
print(useTime)
print('本次爬虫条数为：' + str(num))
print("爬虫任务结束--->" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 关闭数据库链接
db.__exit__()
# 将结果保存到excel中
# wb.save('movies.xlsx')
