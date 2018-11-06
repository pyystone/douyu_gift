# _*_ coding:UTF-8 _*_
from http import cookiejar
import requests
import json
from tools.my_log import MyLog


class HttpState:
    code = 0
    msg = ''
    cookie = cookiejar.CookieJar()

    def set_code(self, code):
        self.code = code

    def set_msg(self, msg):
        self.msg = msg

    def set_cookie(self, cookie):
        self.cookie = cookie


class HttpData:
    def __init__(self, url):
        self.url = url

    url = ''
    method = 'GET'
    headers = {}
    timeout = 5
    cookies = cookiejar.CookieJar()
    data = {}

    # proxies = {
    # "http": "http://user:pass@10.10.1.10:3128/",
    # }
    proxies = {}


def test_http():
    url = "http://httpbin.org/post"
    result = http_post(HttpData(url))
    print(result)


def http_open(http_data: HttpData):
    if http_data.method == 'GET':
        http_get(http_data)
    else:
        http_post(http_data)


def http_post(http_data):

    state = HttpState()
    try:
        r = requests.post(http_data.url, cookies=http_data.cookies, headers=http_data.headers, data=http_data.data, proxies=http_data.proxies, timeout=10)
        MyLog.logcat(r.text)
        state.set_code(0)
        state.set_msg(r.text)
    except requests.HTTPError as e:
        MyLog.logcat('Http Code: {0}'.format(e.response))
        state.set_code(e.errno)
    except requests.URLRequired as e:
        MyLog.logcat('URLError reason: {0}'.format(e.response))
        state.set_code(-1)
        state.set_msg(e.response)
    except requests.RequestException as e:
        state.set_code(-1)
        state.set_msg(e.response)
    return state


def http_get_json(http_data):
    html = http_get(http_data)
    return json.loads(html.msg)


def http_get(http_data):
    # MyLog.logcat("Http Get:{0}".format(http_data.url))

    state = HttpState()

    try:
        r = requests.get(http_data.url, cookies=http_data.cookies, headers=http_data.headers, proxies=http_data.proxies, timeout=10)
        # MyLog.logcat(r.text)
        state.set_code(0)
        state.set_msg(r.text)
    except requests.HTTPError as e:
        MyLog.logcat('Http Code: {0}'.format(e.response))
        state.set_code(e.errno)
    except requests.URLRequired as e:
        MyLog.logcat('URLError reason: {0}'.format(e.response))
        state.set_code(-1)
        state.set_msg(e.response)
    except requests.RequestException as e:
        state.set_code(-1)
        state.set_msg(e.response)
    return state
