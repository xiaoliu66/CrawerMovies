import time
import uuid

import requests
from bs4 import BeautifulSoup
from redisbloom.client import Client
import WxPushUtils
import DataBaseUtil

print("======开始清除redis上次残存的数据======")
rb = Client(host='localhost', port=6379)
rb.delete('urls')  # 每次重新加载时，先删除上次key的信息
print("======清除成功！======")

print("======开始将数据加载到redis======")
# 先将数据库中的数据加载到redis中
# 默认的error_rate(误判率)是0.01，initial_size（表示预计放入的元素数量）是100。
rb.bfCreate('urls', 0.01, 1000)
sql = """select url from t_web_crawler"""
all = DataBaseUtil.UsingMysql().__enter__().fetch_all(sql)
for i in all:
    items = i['url']
    rb.bfAdd('urls', items)
print("======数据加载到redis中成功！======")

url = 'https://www.dytt8.net/index.htm'
# 伪装成浏览器去发送请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
context = requests.get(url=url, headers=headers)
# 解决乱码 原网站用的是gb2312，用了之后个别字体仍然是乱码。换成了GBK 兼容GB 2312 编码,为GB 2312 的升级版本。
context.encoding = 'gbk'
html = context.text
# 获取所有的a标签
target = BeautifulSoup(html, 'lxml').find('div', class_='co_content2').find_all('a')

base_url = 'https://www.dytt8.net'
beginTime = time.time()
print("爬虫任务开始--->" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
num = 0

list = []  # 爬取到的电影信息集合

db = DataBaseUtil.UsingMysql().__enter__()
for a in target:
    tempLink = a.get('href')
    # 过滤广告
    if tempLink.find("20160320") >= 0:
        continue
    # 截取链接中的日期
    n = tempLink.find("2")
    date = tempLink[n:n + 8]

    href = base_url + tempLink  # 每个详细页面的url

    # 如果该url存在，则跳出本次循环
    if rb.bfExists('urls', href) == 1:
        # print(href + " 已经存在。")
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

    # 获取电影海报图片地址
    image_url = BeautifulSoup(detail_html, 'lxml').find('div', id='Zoom').find('img').get('src')
    # 获取电影简介
    begin = context.index("◎简　　介")
    end = context.rindex("。")
    movie_synopsis = context[begin + 5:end + 1]

    uid = str(uuid.uuid4()).replace('-', '')
    name = detail_title.text
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    is_delete = 'N'

    info = {'title': name, 'description': movie_synopsis, 'url': href, 'image_url': image_url}  # 每次获取到的电影信息

    list.append(info)

    sql = "INSERT INTO t_web_crawler(id, date, name, url, magnet, create_time, modify_time, is_delete, context, image_url, movie_synopsis)\
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s')" % \
          (uid, date, name, href, magnet, create_time, modify_time, is_delete, context, image_url, movie_synopsis)
    print("sql：", sql)

    db.insert_one(sql)

    print(href + " ---> " + name)

    num = num + 1

endTime = time.time()
useTime = (endTime - beginTime)
print(useTime)
print('本次爬虫条数为：' + str(num))
print("爬虫任务结束--->" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 关闭数据库链接
db.__exit__()

print('====' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 开始推送微信消息 ====')
if num > 0:
    desp = '本次爬取到 ' + str(num) + '个电影资源。\n分别是：'
    # datas = {"title": "有新电影资源可供下载", "desp": desp}
    # print("微信推送信息：" + str(datas))
    # res = requests.get(url, datas)
    access_token = WxPushUtils.get_access_token('自己的企业id', '自己的应用秘钥')
    WxPushUtils.send_text_message(access_token, 1000002, desp)

    for i in list:
        WxPushUtils.send_news_messsage(access_token, 1000002, i['title'], i['description'], i['url'], i['image_url'])

print('====' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' 推送微信消息结束 ====')
