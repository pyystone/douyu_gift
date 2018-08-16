from bs4 import BeautifulSoup

from douyu.api import *
import json
import os

did_list_file_path = "did_list.txt"


def start():
    did_list_file_change = False
    cookie_jar = get_cookie_from_chrome("www.douyu.com")
    dy_did = cookie_jar['acf_did']
    sid = cookie_jar['acf_uid']

    did_list = {}
    if os.path.exists(did_list_file_path) and os.path.getsize(did_list_file_path) > 0:
        with open(did_list_file_path, 'r') as f:
            data = f.read()
            did_list = json.loads(data)

    # 获得粉丝牌列表
    badge_list_msg = http_get(get_douyu_http_data('https://www.douyu.com/member/cp/getFansBadgeList')).msg
    # 格式转化为dom
    soup = BeautifulSoup(badge_list_msg, "lxml")
    # 格式化输出查看数据
    # print(soup.prettify())

    for item in soup.find_all(has_room_attr):
        room_id = item.attrs['data-fans-room']
        if did_list.get(room_id, -1) == -1:
            did_list_file_change = True
            did_list[room_id] = query_did(room_id)

    if did_list_file_change:
        with open('did_list.txt', 'w') as f:
            f.write(json.dumps(did_list))

    gift_count = query_gift(196)
    MyLog.logcat("粉丝荧光棒剩余:{0}".format(gift_count))
    i = 0
    while i < gift_count:
        for rid in did_list:
            if i < gift_count:
                send_gift(dy_did, sid, did_list[rid], rid)
                MyLog.logcat("房间号{0}: 粉丝荧光棒赠送成功".format(rid))
                i = i + 1
            else:
                break


def has_room_attr(tag):
    return tag.has_attr('data-fans-room')
