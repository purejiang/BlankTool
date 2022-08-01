# -*-coding:utf-8 -*-

import traceback
from common.cmd import CMD
from common.constant import BUNDLE_TOOL_PATH
from utils.file_helper import FileHelper
from utils.other_util import currentTime, write_print

class BundleManager(object):
    """
    @author: purejiang
    @created: 2022/7/13

    .aab 相关的功能管理

    """
    @classmethod
    def aab2apks(cls, bundle_tool_path, aab_path, apks_path, keystore_config, loguer=None):
        """
        .aab 转 .apks
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        write_print(loguer, "aab2apks...")
        cmd_result = CMD.aab2Apks(bundle_tool_path, aab_path, apks_path, keystore_config)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def install_apks(cls, bundle_tool_path, apks_path, loguer=None):
        """
        安装 .apks
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        write_print(loguer, "install apks...")
        cmd_result = CMD.installApks(bundle_tool_path, apks_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def install_aab(cls, aab_path, apks_path, keystore_config, loguer, progress_callback):
        loguer.log_start(0, "开始安装 aab，时间："+ currentTime())
        try:
            loguer.log_start(1, "开始 清理输出目录")
            if FileHelper.fileExist(apks_path):
                FileHelper.delFile(apks_path)
            loguer.log_end(1, "清理输出目录完成")

            progress_callback(30, "aab 转 apks ...")
            loguer.log_start(2, "开始 aab2apks")
            if cls.aab2apks(BUNDLE_TOOL_PATH, aab_path, apks_path, keystore_config, loguer):
                loguer.log_end(2, "aab2apks 完成")
            else:
                loguer.log_end(2, "aab2apks 失败")
                return False
            progress_callback(70, "安装 apks ...")
            loguer.log_start(3, "安装 apks")
            if cls.install_apks(BUNDLE_TOOL_PATH, apks_path, loguer):
                loguer.log_end(3, "安装 apks 完成")
            else:
                loguer.log_end(3, "安装 apks 失败")
                return False
            return True
        except Exception as e:
            loguer.log(traceback.format_exc())
            return False
        finally:
            loguer.log_end(0, "安装结束")
            loguer.save()

    @classmethod
    def apk2aab(cls, bundle_tool_path, apks_path, loguer=None):
        """
        apk 转adb
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        write_print(loguer, "install apks...")
        cmd_result = CMD.installApks(bundle_tool_path, apks_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]