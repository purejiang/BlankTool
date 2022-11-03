# -*- coding:utf-8 -*-

import time
"""

@author: purejiang
@created: 2022/3/25

其他方法

"""
def currentTime():
    """
    当前时间，字符串形式，例如："2022-03-25 12:15:12"
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def currentTimeNumber():
    """
    当前时间，数字形式，例如："20220325121512"
    """
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

def currentTimeMillis():
    """
    当前时间戳
    """
    return int(time.time())

def write_print(loguer, msg):
    if loguer:
        loguer.log(msg)
    else:
        print(msg)
