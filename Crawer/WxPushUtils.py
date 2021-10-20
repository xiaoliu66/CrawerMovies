# 微信推送消息工具类

# 获取微信api 进入凭证url
import requests

access_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
send_message_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?'


def getAccessToken(corpid, corpsecret):
    """
    获取微信api进入凭证
    :param corpid: 企业id 方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid
    :param corpsecret: 应用的凭证密钥 ，获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret
    :return: dict
    """
    resp = requests.get(access_token_url + 'corpid=' + corpid + '&corpsecret=' + corpsecret)
    return resp.json()


def sendTextMessage(access_token, agentid, content):
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
    requests.post(send_message_url + "access_token=" + access_token)
