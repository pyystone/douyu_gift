from douyu.douyu_main_app import start
from tools.my_log import MyLog
import sys
import traceback
from tools.utls import *


def init_app():
    MyLog.set_status(0)


app_version = 1.4
if __name__ == "__main__":
    init_app()
    start_type = -1
    print('************************')
    print('*   0: 退出' + my_align(u'0: 退出', 18) + '*')
    print('*   1: 每日续牌' + my_align(u'0: 每日续牌', 17) + '*')
    print('*   2: 均分续牌' + my_align(u'0: 均分续牌', 17) + '*')
    print('*                      *')
    print('*                      *')
    print('*   version: {0}       *'.format(app_version))
    print('************************')
    start_type = int(input("请输入："))
    # while start_type != 0:
    try:
        start(start_type)
    except Exception as e:
        print("Unexpected error:", sys.exc_info())
        print("str(e):\t\t", str(e))
        traceback.print_exc()

    input("Press <enter> to END")
