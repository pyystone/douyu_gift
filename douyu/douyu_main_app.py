from douyu.api import *
import json
import os

room_data_list_file_path = "data_list.txt"


# 用于临时送指定礼物的代码
# 原本设计用于web没提供批量送礼物而写的脚本
# 可惜服务端有做检查，结果无论填多少最后送出的数量只有1个，所以这块代码暂时弃用
def temp_start():
    with open(room_data_list_file_path, 'r') as f:
        data = f.read()
        room_id_list = json.loads(data)

    cookie_jar = get_cookie_from_chrome("www.douyu.com")
    dy_did = cookie_jar['acf_did']
    sid = cookie_jar['acf_uid']

    send_temp_gift(dy_did, sid, room_id_list["196"]["did"], 196, 4, 47)


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
