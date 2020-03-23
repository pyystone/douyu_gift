from douyu.api import *
import json
import os
import time

room_data_list_file_path = "data_list.txt"
default_gift_id = 268


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

    send_dy_gift(dy_did, sid, room_id_list["196"]["did"], 196, 4, 47)


# startType 1 续每日牌子 2均分所有礼物
def start(start_type: 1):
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
    MyLog.logcat(cookie_jar)
    dy_did = cookie_jar['acf_did']
    sid = cookie_jar['acf_uid']

    print("查询礼物信息")
    gift_count = query_gift(196)
    print("粉丝荧光棒剩余:{0}\n".format(gift_count))

    gift_num = int(gift_count / len(room_id_list))
    gift_last = gift_count % len(room_id_list)
    send_count = 0
    temp_rid = ""
    max_intimacy = 0.0

    if start_type == 2 and gift_num != 0:
        for rid in room_id_list:
            # time.sleep(200)
            intimacy = float(room_id_list[rid]["intimacy"].replace(',',''))
            if intimacy > max_intimacy:
                temp_rid = rid
                max_intimacy = intimacy
            send_gift(dy_did, sid, room_id_list[rid]["did"], rid, default_gift_id, gift_num, room_id_list[rid]["name"])

        if gift_last != 0:
            send_gift(dy_did, sid, room_id_list[temp_rid]["did"], temp_rid, default_gift_id, gift_last
                      , room_id_list[temp_rid]["name"])
    if start_type == 1 and gift_count > 0:
        for rid in room_id_list:
            # time.sleep(200)
            if send_count < gift_count:
                send_gift(dy_did, sid, room_id_list[rid]["did"], rid, default_gift_id, 1, room_id_list[rid]["name"])
                send_count = send_count + 1
            else:
                break

    print("\n礼物赠送结束\n当前关注信息\n")
    update_room_list()
    print("\n")


def send_gift(dy_did, sid, room_did, rid, gift_id, gift_num, room_name):
    result = send_dy_gift(dy_did, sid, room_did, rid, gift_id, gift_num)
    if result:
        print("{0: <10}: 粉丝荧光棒 × {1:2}赠送成功".format(room_name, gift_num))
    else:
        print("{0: <10}: 粉丝荧光棒 × {1:2}赠送失败".format(room_name, gift_num))
