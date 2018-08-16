from net.app_http import *
from tools.chrome_cookie import get_cookie_from_chrome
import json


def get_douyu_http_data(url, referer= ""):
    http_data = HttpData(url)
    http_data.cookies = get_cookie_from_chrome("www.douyu.com")
    http_data.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'origin': 'https://www.douyu.com',
        'referer': referer,
        'x-requested-with': 'XMLHttpRequest'
    }
    return http_data


# dy:               dy_did
# prop_id: 268      礼物id 粉丝荧光棒
# num: 1            数量
# sid: xxx          acf_uid
# did: xx           主播的uid
# did               获取地址：https://www.douyu.com/ztCache/WebM/room/196 ,\"owner_uid\":5748,\
# rid: xx           房间id
def send_gift(dy,sid,did,rid):
    data = get_douyu_http_data("https://www.douyu.com/member/prop/send", "https://www.douyu.com/%d".format(rid))
    data.data = {
        'dy': dy,
        'prop_id': 268,
        'num': 1,
        'sid': sid,
        'did': did,
        'rid': rid,
    }
    result = http_post(data)
    print(result)


def query_did(num):
    url = "https://www.douyu.com/ztCache/WebM/room/{0}".format(num)
    result = http_get_json(HttpData(url))
    did = result['$ROOM']
    result = json.loads(did)
    did = result['owner_uid']
    return did


# Url: https://www.douyu.com/member/prop/query
# Method: POST
# Form Data:
# rid: 196
def query_gift(rid):
    url = "https://www.douyu.com/member/prop/query"
    data = get_douyu_http_data(url, "https://www.douyu.com/%d".format(rid))
    data.data = {'rid': rid}
    result = http_post(data)
    print(result)
    data = json.loads(result.msg)
    data = data['data']['list']
    for item in data:
        if item['prop_id'] == 268:
            return item['count']
    return 0