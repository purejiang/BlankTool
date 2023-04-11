# -*- coding:utf-8 -*-


import os
import sys
import traceback
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.b_loger import Loger
from utils.other_util import currentTime
from PySide6.QtCore import QResource

from vo.function import Function


class BlankManager():
    DEBUG_MODE= "DEBUG"
    REALEASE_MODE="RELEASE"
    loger = Loger()
    """

    @author: purejiang
    @created: 2022/7/20

    工具相关的功能管理

    """

    @classmethod
    def cleanCache(cls, progress_callback)->bool:
        """
        清理缓存

        :param progress_callback: 执行进度
        :param loguer: 日志工具

        """
        cls.loger.info("开始清理缓存，时间：" + currentTime())
        try:
            for dir in Constant.Path.ALL_CACHE_PATH_LIST:
                file_list = FileHelper.getAllChild(dir, FileHelper.TYPE_DIR)
                if file_list is None:
                    progress_callback("很干净，没有数据需要清理")
                    return True
                else:
                    for file in file_list:
                        progress_callback("删除："+file)
                        FileHelper.delFile(file)
            return True
        except Exception as e:
            cls.loger.warning("清理失败："+traceback.format_exc())
            return False
        finally:
            cls.check_cache_dir()

    @classmethod
    def __initRe(cls)->bool:
        """
        初始化工具的执行环境

        设置临时环境变量

        """
        # 1. 设置临时的环境变量
        tmp_path = "{0};{1};{2};".format(
            Constant.Re.JAVA_PATH, Constant.Re.AAPT2_PATH, Constant.Re.ADB_PATH)
        cls.loger.info("设置临时的环境变量: {0}".format(tmp_path))
        os.environ['PATH'] = tmp_path+os.environ['PATH']
        cls.loger.info("最终环境变量: {0}".format(os.environ['PATH']))
        # CMD.setPath(tmp_path)
        os.chdir(sys.path[0]) 
        return True

    @classmethod   
    def __loadRcc(cls)->bool:
        """
        加载 .rcc 资源

        """
        cls.loger.info("加载 .rcc 资源")
        try:
            for file in FileHelper.getChild(os.path.join(Constant.AppPath.APP_PATH, Constant.AppPath.RESOURCE_PATH), FileHelper.TYPE_FILE):
                if FileHelper.getSuffix(file) == ".rcc":
                    QResource.registerResource(file)
            return True
        except Exception as e:
            # 开发版会报错，可忽略
            cls.loger.warning("load .rcc file error")
            return False


    @classmethod
    def initApplication(cls, callback_progress)->bool:
        """
        初始化程序
        """
        callback_progress(20, "初始化环境变量", "")
        if not cls.__initRe():
            return False

        callback_progress(40, "检查运行环境", "")
        if not cls.__checkRe():
            return False

        callback_progress(60, "加载 .rcc", "")
        if not cls.__loadRcc() and Constant.AppInfo.MODE==cls.DEBUG_MODE:
            return False

        callback_progress(80, "检查工具目录", "")
        if not cls.checkToolDir():
            pass

        callback_progress(90, "检查更新", "")
        if not cls.checkUpdate():
            pass
        return True

    @classmethod
    def checkToolDir(cls)->bool:
        """
        检测工具目录
        """
        cls.loger.info("检测工具目录完整性")
        for tool_dir in [Constant.Path.CACHE_PATH, *Constant.Path.ALL_CACHE_PATH_LIST, Constant.Path.DATA_PATH, *Constant.Path.ALL_OTHER_PATH_LIST]:
            # 如果缓存目录被误删则重新创建缓存目录
            if not FileHelper.fileExist(tool_dir):
                cls.loger.info("重建: {}".format(tool_dir))
                FileHelper.createDir(tool_dir)
    
    @classmethod
    def __checkRe(cls):
        """
        检测运行环境
        """
        cls.loger.info("检测运行环境")
        for re_dir in Constant.Re.ALL_RE_PATH_LIST:
            # 如果运行环境被误删则报错
            if not FileHelper.fileExist(re_dir):
                cls.loger.info("缺少必要的运行环境: {}".format(re_dir))
                return False
        return True

    @classmethod
    def checkUpdate(cls):
        """
        检测更新
        """
        pass

    @classmethod
    def getFunctions(cls, progress_callback):
        """
        获取功能列表（暂为本地）
        """
        progress_callback("获取功能列表")
        apk_function = Function("Apk 分析", "./res/img/app_icon_small", ["Apk 解析", "Apk 解析结果"])
        return []
