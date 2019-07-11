from douyu.douyu_main_app import start
from douyu.douyu_main_app import temp_start
from tools.my_log import MyLog
import os


def init_app():
    MyLog.set_status(0)


if __name__ == "__main__":
    init_app()
    start()
    # temp_start()
    input("Press <enter> to END")
