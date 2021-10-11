from redisbloom.client import Client

# r = redis.StrictRedis(host='172.27.183.10', port=6379, db=0)
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
from Crawer import DataBaseUtil

rb = Client(host='localhost', port=6379)

# 将数据库中的数据加载到redis中

rb.bfAdd('urls', 'baidu')
rb.bfAdd('urls', 'baidu')
rb.bfAdd('urls', 'google')
if rb.bfExists('urls', 'baidu') == 1:
    print("该值已经存在")
# print()  # out: 1
# print(rb.bfExists('urls', 'tencent'))  # out: 0
#
# rb.bfMAdd('urls', 'a', 'b')
# print(rb.bfMExists('urls', 'google', 'baidu', 'tencent'))  # out: [1, 1, 0]

# rb.delete('urls')
#
# sql = """select url from t_web_crawler"""
# all = DataBaseUtil.UsingMysql().__enter__().fetch_all(sql)
# for i in all:
#     url = i['url']
#     rb.bfAdd('urls', url)

