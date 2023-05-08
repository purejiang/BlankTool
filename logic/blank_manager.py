# -*- coding:utf-8 -*-


import os
import shutil
import traceback
from common.constant import APP_PATH, Constant
from utils.file_helper import FileHelper
from utils.j_loger import JLoger
from utils.other_util import currentTime
from PySide6.QtCore import QResource



class BlankManager():
    DEBUG_MODE= "DEBUG"
    REALEASE_MODE="RELEASE"
    loger = JLoger()
    """

    @author: purejiang
    @created: 2022/7/20

    工具相关的功能管理

    """


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
        # os.chdir(sys.path[0]) 
        return True

    @classmethod   
    def __loadRcc(cls)->bool:
        """
        加载 .rcc 资源

        """
        cls.loger.info("加载 .rcc 资源")
        try:
            for file in FileHelper.getChild(os.path.join(APP_PATH, Constant.Path.RESOURCE_PATH), FileHelper.TYPE_FILE):
                if FileHelper.getSuffix(file) == ".rcc":
                    QResource.registerResource(file)
            return True
        except Exception as e:
            # 开发版会报错，可忽略
            cls.loger.warning("load .rcc file error")
            return False

    @classmethod
    def __checkToolDir(cls)->bool:
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
        if not cls.__loadRcc() and Constant.AppInfo.MODE==cls.REALEASE_MODE:
            return False

        callback_progress(80, "检查工具目录", "")
        if not cls.__checkToolDir():
            pass

        callback_progress(90, "检查更新", "")
        if not cls.checkUpdate():
            pass
        return True
    

    @classmethod
    def getChache(cls, progress_callback)->str:
        """
        获取缓存大小

        :param progress_callback: 执行进度

        """
        cls.loger.info("开始分析缓存文件：" + currentTime())
        total_size = 0
        progress = 0 
        cache_len = len(Constant.Path.ALL_CACHE_PATH_LIST)
        try:
            for folder_path in Constant.Path.ALL_CACHE_PATH_LIST:
                progress+=1
                progress_callback(progress*100/cache_len, "分析：{0}".format(folder_path), "")
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for file_name in filenames:
                        file_path = os.path.join(dirpath, file_name)
                        try:
                            total_size += FileHelper.fileSize(file_path)
                        except Exception as e:
                            cls.loger.warning("获取文件大小失败："+traceback.format_exc())   
            if total_size <= 1024.0:
                return "{:.2f} B".format(total_size)
            elif total_size <= 1024.0**2:
                return "{:.2f} KB".format(total_size/1024.0)
            elif total_size <= 1024.0**3:
                return "{:.2f} MB".format(total_size/(1024.0 ** 2))
            else:
                return "{:.2f} GB".format(total_size/(1024.0 ** 3))
        except Exception as e:
            cls.loger.warning("分析缓存文件失败："+traceback.format_exc())
            return None

    @classmethod
    def cleanCache(cls, progress_callback)->bool:
        """
        清理缓存

        :param progress_callback: 执行进度

        """
        cls.loger.info("开始清理缓存，时间：" + currentTime())
        cache_len = len(Constant.Path.ALL_CACHE_PATH_LIST)
        progress = 0 
        try:
            for folder_path in Constant.Path.ALL_CACHE_PATH_LIST:
                progress+=1
                progress_callback(progress*100/cache_len, "清理：{0}".format(folder_path), "")
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for dir in dirnames:
                        try:
                            cls.loger.info("开始清理文件夹：" + os.path.join(dirpath, dir))
                            FileHelper.delFile(os.path.join(dirpath, dir))
                        except Exception as e:
                            cls.loger.warning("清理清理文件夹失败："+traceback.format_exc())
                            return False
                    for file in filenames:
                        try:
                            cls.loger.info("开始清理文件：" + file)
                            FileHelper.delFile(os.path.join(dirpath, file))
                        except Exception as e:
                            cls.loger.warning("清理文件失败："+traceback.format_exc())     
            return True
        except Exception as e:
            cls.loger.warning("清理缓存失败："+traceback.format_exc())
            return False
    


    @classmethod
    def checkUpdate(cls):
        """
        检测更新
        """
        cls.loger.info("检测更新")

    # @classmethod
    # def getFunctions(cls, progress_callback):
    #     """
    #     获取功能列表（暂为本地）
    #     """
    #     progress_callback("获取功能列表")
    #     apk_function = Function("Apk 分析", "./res/img/app_icon_small", ["Apk 解析", "Apk 解析结果"])
    #     return []
