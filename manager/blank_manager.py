# -*- coding:utf-8 -*-


import traceback
from common.constant import *
from utils.file_helper import FileHelper
from utils.other_util import currentTime, write_print


class BlankManager(object):
    
    """

    @author: purejiang
    @created: 2022/7/20

    工具相关的功能管理

    """

    @classmethod
    def cleanCache(cls, progress_callback, loguer = None):
        """
        清理缓存

        :param progress_callback: 执行进度
        :param loguer: 日志工具

        """
        write_print(loguer, "开始清理缓存，时间："+ currentTime())
        try:
            file_list = FileHelper.getChild(CACHE_PATH, FileHelper.TYPE_BOTH)
            file_count = len(file_list)
            progress_factor = file_count/100
            for index in range(file_count):
                file = file_list[index]
                FileHelper.delFile(file)
                write_print(loguer, "index*progress_factor:"+index*progress_factor)
                progress_callback(index*progress_factor, "删除："+file)
            cls.check_cache_dir(loguer)
            return True
        except Exception as e:
            write_print(loguer, "清理失败："+traceback.format_exc())
            return False

    @classmethod
    def init(cls, loguer = None):
        """
        初始化
        
        1. 程序自检
        2. 设置临时环境变量

        """
        # 程序自检
        cls.__checkApplcation(loguer)
        # 设置临时的环境变量
        tmp_path= "{0};{1};{2}".format(JAVA_PATH, AAPT2_PATH, ADB_PATH)
        write_print(loguer, "初始化临时环境变量:{0}".format(tmp_path))
        os.environ['PATH']+=tmp_path
        
        # CMD.setPath(tmp_path)

    @classmethod
    def __checkApplcation(cls, loguer):
        cls.check_cache_dir(loguer)

    @classmethod
    def check_cache_dir(cls, loguer):
        write_print(loguer, "检测缓存目录是否完整")
        for cache_dir in [CACHE_PATH, *BASE_CACHE_LIST, *APK_CACHE_LIST]:
            # 如果缓存目录被误删则重新创建缓存目录
            if not FileHelper.fileExist(cache_dir):
                FileHelper.createDir(cache_dir)