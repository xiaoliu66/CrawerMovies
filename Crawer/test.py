import time

import pyperclip
import requests
from bs4 import BeautifulSoup
import os
import lxml
import pyautogui
# 测试用迅雷自动下载电影

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

url = 'https://www.dytt8.net/html/gndy/jddy/20210530/61474.html'
context = requests.get(url, headers=headers)
# 解决乱码
context.encoding = 'gbk'
html = context.text

# 获取所有的a标签
target = BeautifulSoup(html, 'lxml').find('div', id='Zoom').find('a')
magnet = target['href']

print(target['href'])

time.sleep(2)
# 模拟组合热键 win + d 关闭所有窗口回到桌面
pyautogui.hotkey('win', 'd')

# 1秒钟鼠标移动坐标为143,28位置  绝对移动
pyautogui.moveTo(x=143, y=28, duration=1, tween=pyautogui.linear)
# 打开迅雷
pyautogui.doubleClick()
# 新建下载任务
# pyautogui.moveTo(x=479, y=110, duration=1, tween=pyautogui.linear)
# pyautogui.click()
# 等待软件启动完成
time.sleep(3)
# 复制获取到的磁力链接
pyperclip.copy(magnet)
# pyperclip.paste()
# 点击确定
# pyautogui.moveTo(x=1203, y=580, duration=1, tween=pyautogui.linear)
# pyautogui.click()
# 点击‘立即下载’
pyautogui.moveTo(x=926, y=773, duration=1, tween=pyautogui.linear)
pyautogui.click()
