from douyu.douyu_main_app import start
from tools.my_log import MyLog


def init_app():
    MyLog.set_status(1)

if __name__ == "__main__":
    init_app()
    start()
