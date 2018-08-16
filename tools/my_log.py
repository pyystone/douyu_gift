#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 日志打印标准程序


class MyLog:
    isDebug = 0

    @staticmethod
    def set_status(status):
        MyLog.isDebug = status

    @staticmethod
    def logcat(str):
        if MyLog.isDebug:
            print(str)
