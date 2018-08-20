from bs4 import BeautifulSoup

from douyu.api import *
import json
import os

room_data_list_file_path = "data_list.txt"


def start():
    update_room_list()

    if os.path.exists(room_data_list_file_path) and os.path.getsize(room_data_list_file_path) > 0:
        with open(room_data_list_file_path, 'r') as f:
            data = f.read()
            room_id_list = json.loads(data)
    else:
        print("{0} 文件路径不存在，请联系开发人员".format(room_data_list_file_path))
        return

    cookie_jar = get_cookie_from_chrome("www.douyu.com")
    dy_did = cookie_jar['acf_did']
    sid = cookie_jar['acf_uid']

    gift_count = query_gift(196)
    MyLog.logcat("粉丝荧光棒剩余:{0}".format(gift_count))
    i = 0
    while i < gift_count:
        for rid in room_id_list:
            if i < gift_count:
                send_gift(dy_did, sid, room_id_list[rid]["did"], rid)
                MyLog.logcat("{0: <20}: 粉丝荧光棒赠送成功".format(room_id_list[rid]["name"]))
                i = i + 1
            else:
                break


