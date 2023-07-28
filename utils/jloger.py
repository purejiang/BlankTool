# -*- coding:utf-8 -*-

import logging
import os
from common.constant import APP_PATH, Constant
from utils.other_util import currentTimeNumber


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class JLogger():
    """

    @author: purejiang
    @created: 2023/2/21

    日志工具

    """

    def __init__(self, set_level="INFO",
                 name=Constant.AppInfo.APP_NAME,
                 log_name="{}.log".format(currentTimeNumber()),
                 log_path=os.path.join(APP_PATH, "log"),
                 use_console=True,
                 save_file=False):
        """
        :param set_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name，默认为运行程序的name
        :param log_name: 日志文件的名字，默认为当前时间（年月日时.log）
        :param log_path: 日志文件夹的路径，默认为loger.py同级目录中的log文件夹
        :param use_console: 是否在控制台打印，默认为True
        :param save_file: 是否保存日志文件，默认为False
        """
        if not set_level:
            set_level = self._exec_type()  # 设置set_level为None，自动获取当前运行模式
        self.__loger = logging.getLogger(name)
        self.setLevel(
            getattr(logging, set_level.upper()) if hasattr(logging, set_level.upper()) else logging.INFO)  # 设置日志级别
        if not os.path.exists(log_path) and save_file:  # 创建日志目录
            os.makedirs(log_path)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        handler_list = list()
        if save_file:
            handler_list.append(logging.FileHandler(
                os.path.join(log_path, log_name), encoding="utf-8"))
        if use_console:
            handler_list.append(logging.StreamHandler())
        for handler in handler_list:
            handler.setFormatter(formatter)
            self.addHandler(handler)

    def __getattr__(self, item):
        return getattr(self.loger, item)

    @property
    def loger(self):
        return self.__loger

    @loger.setter
    def loger(self, func):
        self.__loger = func

    def _exec_type(self):
        return "DEBUG" if os.environ.get("IPYTHONENABLE") else "INFO"

    # loger.critical("这是一个 critical 级别的问题！")
    # loger.error("这是一个 error 级别的问题！")
    # loger.warning("这是一个 warning 级别的问题！")
    # loger.info("这是一个 info 级别的问题！")
    # loger.debug("这是一个 debug 级别的问题！")
