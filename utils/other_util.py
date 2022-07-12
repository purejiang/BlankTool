# -*- coding:utf-8 -*-

import time
import os
import platform
import subprocess
import sys
from utils.file_helper import FileHelper
"""

@author: purejiang
@created: 2022/3/25

其他方法

"""
def currentTime():
    """
    当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

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

def cleanCache():
    FileHelper.delFile("./cache")

def cmdBySystem(win_cmd, linux_cmd, error_msg, loguer=None):
    """
    执行 CMD 命令

    :param win_cmd: windows 系统的命令行
    :param linux_cmd: linux 系统的命令行
    :param error_msg: 执行命令行错误的提示信息
    """
    result = False
    try:
        if platform.system() == "Windows":
            cmd = win_cmd
        elif platform.system() == "Linux":
            cmd = linux_cmd
        else:
            write_print(loguer, "cmd not support this system")
            return result
        write_print(loguer, cmd)
        process = subprocess.check_output(cmd, shell=True)
        write_print(loguer, "cmd: "+process.decode(encoding='gbk'))
        # b = os.popen(cmd)
        # write_print(loguer, "cmd: "+b.read())
        result = True
    except Exception as Arugment:
        write_print(loguer, "{0}:\n{1}".format(error_msg, str(Arugment)))
        result = False
    finally:
        return result

