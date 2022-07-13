# -*-coding:utf-8 -*-

import os
from common.constant import CACHE_PATH
from utils.file_helper import FileHelper
from utils.loguer import Loguer
from utils.other_util import cmdBySystem, currentTime, currentTimeMillis, write_print

class BundleTools(object):
    """
    @author: purejiang
    @created: 2022/6/13

    bundletool 构建工具，用来处理 .aab 包
    """
    @classmethod
    def aab2apks(cls, bundle_tool_path, aab_path, apks_path, keystore_config, loguer=None):
        """
        .aab 转 .apks
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        return aab2apks_cmd(bundle_tool_path, aab_path, apks_path, keystore_config, loguer)

    @classmethod
    def install_apks(cls, bundle_tool_path, apks_path, loguer=None):
        return install_apks_cmd(bundle_tool_path, apks_path, loguer)

    @classmethod
    def install_aab(cls, bundle_tool_path, aab_path, apks_path, keystore_config, install_callback, loguer=None):
        if loguer is None:
            loguer = Loguer(os.path.join(CACHE_PATH, "bundletool_{0}.log".format(currentTimeMillis())))  
        loguer.log_start(0, "开始安装 aab，时间："+ currentTime())
        try:
            loguer.log_start(1, "开始 清理输出目录")
            if FileHelper.fileExist(apks_path):
                FileHelper.delFile(apks_path)
            loguer.log_end(1, "清理输出目录完成")

            install_callback(30, "aab 转 apks ...")
            loguer.log_start(2, "开始 aab2apks")
            if cls.aab2apks(bundle_tool_path, aab_path, apks_path, keystore_config, loguer):
                loguer.log_end(2, "aab2apks 完成")
            else:
                loguer.log_end(2, "aab2apks 失败")
                install_callback(100, "aab 转 apks 失败")
                return
            install_callback(70, "安装 apks ...")
            loguer.log_start(3, "安装 apks")
            if cls.install_apks(bundle_tool_path, apks_path, loguer):
                loguer.log_end(3, "安装 apks 完成")
                install_callback(100, "安装 apks 完成")
            else:
                loguer.log_end(3, "安装 apks 失败")
                install_callback(100, "安装 apks 失败")
        except Exception as e:
            raise e
        finally:
            loguer.log_end(0, "安装结束")
            loguer.save()


def aab2apks_cmd(bundletool_path, aab_path, output_apks_path, keystore_config=None, loguer=None):
    """
    .aab 转 .apks

    :param aab_path: aab 文件路径
    :param bundletool_path: bundletool 文件路径
    :param keystore_config: keystore 配置

    java -jar [ bundletool 文件] build-apks --bundle [ aab 文件] --output [ apks 文件] --adb [adb 文件]
        --ks=[签名文件]
        --ks-pass=pass:[签名密码]
        --ks-key-alias=[别名]
        --key-pass=pass:[别名密码]
    """
    write_print(loguer, "aab2apks...")
    keystore_str = ""
    if keystore_config:
        keystore_str = " --ks={0} --ks-pass=pass:{1} --ks-key-alias={2} --key-pass=pass:{3}".format(
            keystore_config["store_file"], keystore_config["store_password"], keystore_config["key_alias"], keystore_config["key_password"])
    win_linux_cmd = "java -jar {0} build-apks --bundle {1} --output {2}{3}".format(
        bundletool_path, aab_path, output_apks_path, keystore_str)
    return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: aab2apks failed", loguer)

def install_apks_cmd(bundletool_path, apks_path, loguer=None):
    """
    安装 .apks
    :param bundletool_path: bundletool 文件路径
    :param apks_path: apks 文件路径
    java -jar [ bundletool 文件] install-apks --apks [ apks 文件] --adb [adb 文件]
    """
    write_print(loguer, "install apks...")
    win_linux_cmd = "java -jar {0} install-apks --apks {1}".format(
        bundletool_path, apks_path)
    return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: install apks failed", loguer)



