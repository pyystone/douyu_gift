from douyu.api import *
import json
import os

room_data_list_file_path = "data_list.txt"


def start():
    print("更新关注信息")
    update_room_list()

    if os.path.exists(room_data_list_file_path) and os.path.getsize(room_data_list_file_path) > 0:
        with open(room_data_list_file_path, 'r') as f:
            data = f.read()
            room_id_list = json.loads(data)
    else:
        print("{0} 文件不存在，请联系开发人员".format(room_data_list_file_path))
        return

    cookie_jar = get_cookie_from_chrome("www.douyu.com")
    dy_did = cookie_jar['acf_did']
    sid = cookie_jar['acf_uid']

    print("查询礼物信息")
    gift_count = query_gift(196)
    print("粉丝荧光棒剩余:{0}\n".format(gift_count))
    i = 0
    while i < gift_count:
        for rid in room_id_list:
            if i < gift_count:
                result = send_gift(dy_did, sid, room_id_list[rid]["did"], rid)
                if result:
                    print("{0: <10}: 粉丝荧光棒赠送成功".format(room_id_list[rid]["name"]))
                else:
                    print("{0: <10}: 粉丝荧光棒赠送失败".format(room_id_list[rid]["name"]))
                i = i + 1
            else:
                break

    print("\n礼物赠送结束\n当前关注信息\n")
    update_room_list()
    print("\n")
