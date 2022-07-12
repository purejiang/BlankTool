# -*-coding:utf-8 -*-

import os
from utils.file_helper import FileHelper
from utils.loguer import Loguer
from utils.other_util import cmdBySystem, currentTime, currentTimeMillis, write_print

class BundleToolBuilder(object):
    """
    @author: purejiang
    @created: 2022/6/13

    bundletool 构建工具，用来处理 .aab 包
    """

    def __init__(self, bundletool_path, apks_path, log_path, keystore_config):
        super().__init__()
        """
        :param bundletool_path: bundletool 的路径
        :param apks_path: 输出的 apks 路径
        :param log_path: 日志输出的路径
        :param keystore_config: 签名配置字典
        """
        self._bundle_tool_path = bundletool_path
        self._keystore_config = keystore_config
        self._apks_path = apks_path
        self._loguer = Loguer(os.path.join(log_path, "bundletool_{0}.log".format(currentTimeMillis())))

    def aab2apks(self, aab_path):
        """
        .aab 转 .apks
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        return aab2apks(self._bundle_tool_path, aab_path, self._apks_path, self._keystore_config, loguer=self._loguer)

    def installApks(self, apks_path):
        return installApks(self._bundle_tool_path, apks_path, loguer=self._loguer)

    def install_aab(self, aab_path):
        self._loguer.log_start(0, "开始安装 aab，时间："+ currentTime())
        try:
            self._stepStart(aab_path)
        except Exception as e:
            self._loguer.log(str(e))
        finally:
            self._loguer.log_end(0, "安装结束")
            self._loguer.save()
    
    def _stepStart(self, aab_path):
        """
        安装 .aab

        :param aab_path: aab 文件路径
        """
        self._loguer.log_start(1, "开始 清理输出目录")
        if FileHelper.fileExist(self._apks_path):
            FileHelper.delFile(self._apks_path)
        self._loguer.log_end(1, "清理输出目录完成")

        self._loguer.log_start(2, "开始 aab2apks")
        if self.aab2apks(aab_path, self._apks_path):
            self._loguer.log_end(2, "aab2apks 完成")
        else:
            self._loguer.log_end(2, "aab2apks 失败")
            return

        self._loguer.log_start(3, "安装 apks")
        if self.installApks(self._apks_path):
            self._loguer.log_end(3, "安装 apks 完成")
        else:
            self._loguer.log_end(3, "安装 apks 失败")
            return



def aab2apks(bundletool_path, aab_path, output_apks_path, keystore_config=None, loguer=None):
    """
    .aab 转 .apks

    :param aab_path: aab 文件路径
    :param bundletool_path: bundletool 文件路径
    :param keystore_config: keystore 配置

    java -jar [ bundletool 文件] build-apks --bundle [ aab 文件] --output [ apks 文件]
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

def installApks(bundletool_path, apks_path, loguer=None):
    """
    安装 .apks
    :param bundletool_path: bundletool 文件路径
    :param apks_path: apks 文件路径
    java -jar [ bundletool 文件] install-apks --apks [ apks 文件]
    """
    write_print(loguer, "install apks...")
    win_linux_cmd = "java -jar {0} install-apks --apks {1}".format(
        bundletool_path, apks_path)
    return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: install apks failed", loguer)



