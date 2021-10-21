# 微信推送消息工具类
# Author: https://github.com/xiaoliu66

# 获取微信api 进入凭证url
import requests
import json

access_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?access_token='
send_message_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?'


def get_access_token(corpid, corpsecret):
    """
    获取微信api进入凭证
    :param corpid: 企业id 方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid
    :param corpsecret: 应用的凭证密钥 ，获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret
    :return: dict
    """
    resp = requests.get(access_token_url + 'corpid=' + corpid + '&corpsecret=' + corpsecret)
    return resp.json()['access_token']


def send_text_message(access_token, agentid, content):
    """
    发送文字消息
    :param access_token: 微信api进入凭证
    :param content: 文字消息内容
    :param agentid: 企业微信应用id
    :return:
    """

    # 组装参数 详细参考：https://work.weixin.qq.com/api/doc/90000/90135/90236#%E6%96%87%E6%9C%AC%E6%B6%88%E6%81%AF
    data = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content
        }
    }
    print(send_message_url + "access_token=" + access_token)
    post = requests.post(send_message_url + access_token, json.dumps(data))
    print(post.json())


def send_textcard_message(access_token, agentid, title, description, url):
    """
    发送文字卡片消息
    :param access_token: 登录凭证
    :param agentid: 应用id
    :param title:  标题，不超过128个字节，超过会自动截断（支持id转译）
    :param description: 描述，不超过512个字节，超过会自动截断（支持id转译）
    :param url: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
    :return: 返回json请求结果
    """
    data = {
        "touser": "@all",
        "msgtype": "textcard",
        "agentid": agentid,
        "textcard": {
            "title": title,
            "description": description,
            "url": url
        }
    }
    # print(data)
    response = requests.post(send_message_url + access_token, json.dumps(data))
    return response.json()


def send_markdown_message(access_token, agentid, content):
    """
    发送markdown格式的文字消息（微信不支持查看，企业微信可以）
    :param access_token: 微信api进入凭证
    :param agentid: 应用id
    :param content: markdown文字 需要用三引号 包起来
    :return:
    """
    data = {
        "touser": "@all",
        "msgtype": "markdown",
        "agentid": agentid,
        "markdown": {
            "content": content
        }
    }

    response = requests.post(send_message_url + access_token, json.dumps(data))
    return response.json()

