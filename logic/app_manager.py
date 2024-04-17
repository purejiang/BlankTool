# -*- coding:utf-8 -*-


import json
import os
import sys
import time
import traceback
from cmd_util.app_cmd import AppCMD
from common.config import AppConfig, UserConfig
from utils.file_helper import FileHelper
from utils.jlogger import JLogger
from PySide6.QtCore import QResource

from utils.other_util import currentTimeNumber


class AppManager():
    DEBUG_MODE = "DEBUG"
    REALEASE_MODE = "RELEASE"
    cache_files = []
    """

    @author: purejiang
    @created: 2022/7/20

    工具相关的功能管理

    """

    @classmethod
    def __initRe(cls, logger) -> bool:
        """
        初始化工具的执行环境

        设置临时环境变量

        """
        # 1. 设置临时的环境变量
        user_path_config = UserConfig.getPath()
        tmp_path = "{0};{1};{2};".format(
            user_path_config.java_path, user_path_config.aapt2_path, user_path_config.adb_path)
        logger.info("设置临时的环境变量: {0}".format(tmp_path))
        os.environ['PATH'] = tmp_path+os.environ['PATH']
        logger.info("最终环境变量: {0}".format(os.environ['PATH']))
        # AppCMD.setPath(tmp_path)
        # os.chdir(sys.path[0])
        time.sleep(1)
        return True

    @classmethod
    def __loadRcc(cls, logger) -> bool:
        """
        加载 .rcc 资源

        """
        logger.info("加载 .rcc 资源")
        time.sleep(1)
        try:
            user_path_config = UserConfig.getPath()
            for file in FileHelper.getChild(user_path_config.res, FileHelper.TYPE_FILE):
                if FileHelper.getSuffix(file) == ".rcc":
                    QResource.registerResource(file)
            return True
        except Exception as e:
            # 开发版会报错，可忽略
            logger.warning("load .rcc file error")
            return False

    @classmethod
    def __checkToolDir(cls, logger) -> bool:
        """
        检测工具目录
        """
        logger.info("检测工具目录完整性")
        app_dir = []
        user_path_config = UserConfig.getPath()
        cache_dir_list = UserConfig.getAllCache()
        app_dir.extend(cache_dir_list)
        app_dir.append(user_path_config.log_data)
        app_dir.append(user_path_config.res)
        app_dir.append(user_path_config.assets_res_manifest_file)

        for tool_dir in app_dir:
            # 如果缓存目录被误删则重新创建缓存目录
            logger.info("检测目录: {}".format(tool_dir))
            if not FileHelper.fileExist(tool_dir):
                logger.info("不存在目录：{}，重建:".format(tool_dir))
                FileHelper.createDir(tool_dir)
        time.sleep(1)
        return True

    @classmethod
    def __checkRe(cls, logger):
        """
        检测运行环境
        """
        logger.info("检测运行环境")
        re_list = UserConfig.getAllRe()
        for re_dir in re_list:
            # 如果运行环境被误删则报错
            if not FileHelper.fileExist(re_dir):
                logger.info("缺少必要的运行环境: {}".format(re_dir))
                return False
        return True

    @classmethod
    def checkUpdate(cls, logger):
        """
        检测更新
        """
        logger.info("检测更新")
        time.sleep(3)
        return True

    @classmethod
    def getFunctions(cls, progress_callback):
        """
        获取功能列表（暂为本地）
        """
        # progress_callback("获取功能列表")
        # apk_function = Function("Apk 分析", "./res/img/app_icon_small", ["Apk 解析", "Apk 解析结果"])
        # return []

    @classmethod
    def initApplication(cls, progress_callback) -> bool:
        """
        初始化程序
        """
        logger = JLogger(log_name="init_pplication_{0}.log".format(
            currentTimeNumber()), save_file=True)
        init_result = cls.__initRe(logger)
        progress_callback(20, "初始化环境变量", "", init_result)
        if not init_result:
            return False
        check_re_result = cls.__checkRe(logger)

        progress_callback(40, "检查运行环境", "", check_re_result)
        if not check_re_result:
            return False
        load_result = cls.__loadRcc(logger)

        progress_callback(60, "加载 .rcc", "", load_result)
        app_info = AppConfig.getAppInfo()
        if not load_result and app_info.mode == cls.REALEASE_MODE:
            return False

        check_dir_result = cls.__checkToolDir(logger)
        progress_callback(80, "检查工具目录", "", check_dir_result)
        if not check_dir_result:
            return False
        update_result = cls.checkUpdate(logger)
        progress_callback(90, "检查更新", "", update_result)
        if not update_result:
            return False
        return True

    @classmethod
    def getChache(cls, progress_callback) -> str:
        """
        获取缓存大小

        :param progress_callback: 执行进度

        """
        logger = JLogger(log_name="get_cache_{0}.log".format(
            currentTimeNumber()), save_file=True)
        logger.info("开始分析缓存文件...")
        total_size = 0
        progress = 0
        cache_dir_list = UserConfig.getAllCache()
        cache_len = len(cache_dir_list)
        try:
            for folder_path in cache_dir_list:
                progress += 1
                progress_callback(progress*100/cache_len,
                                  "分析：{0}".format(folder_path), "", True)
                for file in FileHelper.getAllChild(folder_path, FileHelper.TYPE_FILE):
                    cls.cache_files.append(file)
                    total_size += FileHelper.fileSize(file)
            logger.info("分析缓存文件完成")
            if total_size <= 1024.0:
                return "{:.2f} B".format(total_size)
            elif total_size <= 1024.0**2:
                return "{:.2f} KB".format(total_size/1024.0)
            elif total_size <= 1024.0**3:
                return "{:.2f} MB".format(total_size/(1024.0 ** 2))
            else:
                return "{:.2f} GB".format(total_size/(1024.0 ** 3))
        except Exception as e:
            logger.warning("分析缓存文件失败："+traceback.format_exc())
            return None

    @classmethod
    def cleanCache(cls, progress_callback) -> bool:
        """
        清理缓存

        :param progress_callback: 执行进度

        """
        logger = JLogger(log_name="clean_cache_{0}.log".format(
            currentTimeNumber()), save_file=True)
        logger.info("开始清理缓存...")
        dir_list = []
        cache_dir_list = UserConfig.getAllCache()
        try:
            for folder_path in cache_dir_list:
                for dir in FileHelper.getChild(folder_path, FileHelper.TYPE_DIR):
                    dir_list.append(dir)
            del_file_counts = 0
            all_file_counts = len(cls.cache_files)

            for file in cls.cache_files:
                del_file_counts += 1
                try:
                    file_str = "...{0}".format(file.split(os.path.sep)[-1])
                    del_result = FileHelper.delFile(file)
                    progress_callback(
                        del_file_counts*100/all_file_counts, "{0}".format(file_str), "", del_result)
                except Exception as e:
                    logger.warning("清理文件失败："+traceback.format_exc())
            logger.info("预清理文件数：{0}".format(del_file_counts))
            for dir in dir_list:
                FileHelper.delFile(dir)
                logger.info("清理文件夹：" + dir)
            return True
        except Exception as e:
            logger.warning("清理缓存失败："+traceback.format_exc())
            return False

    @classmethod
    def applySetting(cls, config, progress_callback) -> bool:
        """
        修改配置

        :param config: 配置
        :param progress_callback: 执行进度

        """
        pass
        # logger = JLogger(log_name="set_setting_{0}.log".format(currentTimeNumber()), save_file=True)
        # logger.info("开始修改配置")
        # UserConfig
        # origin_json = Config.APP_CONFIG_JSON
        # for key in config:
        #     origin_json["setting"][key] = config[key]
        #     logger.info("{0} -> {1}".format(key, config[key]))
        # return FileHelper.writeContent(Config.APP_CONFIG_PATH, json.dumps(origin_json))
