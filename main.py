from douyu.douyu_main_app import start
from tools.my_log import MyLog
import sys
from tools.utls import *


def init_app():
    MyLog.set_status(0)


if __name__ == "__main__":
    init_app()
    start_type = -1
    print('************************')
    print('*   0: 退出' + my_align(u'0: 退出', 18) + '*')
    print('*   1: 每日续牌' + my_align(u'0: 每日续牌', 17) + '*')
    print('*   2: 均分续牌' + my_align(u'0: 均分续牌', 17) + '*')
    print('*                      *')
    print('*                      *')
    print('*   version: 1.3       *')
    print('************************')
    start_type = int(input("请输入："))
    # while start_type != 0:
    try:
        start(start_type)
    except:
        print("Unexpected error:", sys.exc_info())

    input("Press <enter> to END")
