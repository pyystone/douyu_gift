from net.app_http import *
from tools.chrome_cookie import get_cookie_from_chrome
from bs4 import BeautifulSoup
import json
import os

room_data_list_file_path = "data_list.txt"


def get_douyu_http_data(url, referer= ""):
    http_data = HttpData(url)
    http_data.cookies = get_cookie_from_chrome("www.douyu.com")
    http_data.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
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
def send_gift(dy, sid, did, rid):
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
    return result.code == 0


def send_temp_gift(dy, sid, did, rid, gift_id, num):
    data = get_douyu_http_data("https://www.douyu.com/member/prop/send", "https://www.douyu.com/%d".format(rid))
    data.data = {
        'dy': dy,
        'prop_id': gift_id,
        'num': num,
        'sid': sid,
        'did': did,
        'rid': rid,
    }
    result = http_post(data)
    return result.code == 0


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
    data = json.loads(result.msg)
    data = data['data']['list']
    for item in data:
        if item['prop_id'] == 268:
            return item['count']
    return 0


def update_room_list():
    did_list_file_change = False
    room_id_list = {}
    if os.path.exists(room_data_list_file_path) and os.path.getsize(room_data_list_file_path) > 0:
        with open(room_data_list_file_path, 'r') as f:
            data = f.read()
            room_id_list = json.loads(data)

    # 获得粉丝牌列表
    badge_list_msg = http_get(get_douyu_http_data('https://www.douyu.com/member/cp/getFansBadgeList')).msg
    # 格式转化为dom
    soup = BeautifulSoup(badge_list_msg, "lxml")
    # 格式化输出查看数据
    # print(soup.prettify())

    print("{0: <8}|{1: >10}|{2: >7}|{3: >10}|{4: >7} | {5}".
          format("Id", "Rank", "Lv", "Intimacy", "TodayIntimacy", "Name"))
    for item in soup.find_all(has_room_attr):
        room_id = item.attrs['data-fans-room']
        room_lv = item.attrs['data-fans-level']
        room_rank = item.attrs['data-fans-rank']
        room_intimacy = item.attrs['data-fans-intimacy']
        room_name = item.contents[3].text.replace("\n", "")
        today_intimacy = item.contents[7].text.replace("\n", "")
        print("{0: <8}|{1: >10}|{2: >7}|{3: >10}|{4: >7} | {5}".
              format(room_id, room_rank, room_lv, room_intimacy, today_intimacy, room_name))
        if room_id_list.get(room_id, -1) == -1:
            did_list_file_change = True
            room_data = {"did": query_did(room_id), "name": room_name}
            room_id_list[room_id] = room_data

    if did_list_file_change:
        with open(room_data_list_file_path, 'w') as f:
            f.write(json.dumps(room_id_list))


def has_room_attr(tag):
    return tag.has_attr('data-fans-room')
