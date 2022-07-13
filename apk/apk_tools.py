# -*- coding:utf-8 -*-

import os
from common.constant import ADB_PATH, APK_TOOL_PATH
from utils.other_util import cmdBySystem, write_print

class ApkTools(object):


    @classmethod
    def install_apk(cls, apk_path, loguer = None):
        """
        安装 apk
        :param apk_path: apk 路径
        adb install [apk 路径]
        """
        write_print(loguer, "install {0} ...".format(apk_path))
        # apk_name = os.path.basename(re.sub(r"( |)\(.\)", "", apk_path)) # 过滤掉(XX)字符
        win_linux_cmd = "{0} install {1}".format(
            ADB_PATH, apk_path)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: install apk failed", loguer)

    @classmethod
    def depackage(cls, apk_path, output_dir, is_pass_dex=False, is_only_res=False, loguer = None):
        """
        反编 apk
        :param apktool_ver: apktool 版本
        :param apk_path: apk 路径
        :param output_dir: 反编后目录
        :param is_pass_dex: 是否忽略错误的 dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有
        java -jar [ apktool 文件] [-s (可选)] d [--only -main-classes (可选)] [需要反编的 apk 文件] -o [反编后输出的目录]
        """
        write_print(loguer, "depackage {0} ...".format(apk_path))
        if os.path.exists(output_dir):
            write_print(loguer, "dir is exist: {0}".format(output_dir))
            return False
        # apk_name = os.path.basename(re.sub(r"( |)\(.\)", "", apk_path)) # 过滤掉(XX)字符
        pass_dex = ""
        if is_pass_dex:
            pass_dex = " --only -main-classes"
        s = ""
        if is_only_res:
            s = " -s"
        win_linux_cmd = "java -jar {0}{1} d{2} {3} -o {4}".format(
            APK_TOOL_PATH, s, pass_dex, apk_path, output_dir)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: depackage failed", loguer)

    @classmethod
    def repackage(cls, dir_path, output_apk_path, is_support_aapt2=False, loguer=None):
        """
        重编译目录

        :param apktool_ver: apktool 版本
        :param dir_path: 需要重编的目录
        :param output_apk_path: 重编后输出的 apk 路径
        :param is_support_aapt2: 重编译过程中是否支持 aapt2, 默认不支持

        java -jar [ apktool 文件] b [--use-aapt2 (可选)] [需要重编的目录] -f -o [重编后的 apk 路径]
        """
        write_print(loguer, "repackage {0} ...".format(dir_path))

        if os.path.exists(output_apk_path):
            write_print(loguer, "apk is exist: {0}".format(output_apk_path))
            return False
        # apk_name = os.path.basename(re.sub(r"( |)\(.\)", "", apk_path)) # 过滤掉(XX)字符
        aapt2 = ""
        if is_support_aapt2:
            aapt2 = " --use-aapt2"
        win_linux_cmd = "java -jar {0} b{1} {2} -f -o {3}".format(
            APK_TOOL_PATH, aapt2, dir_path, output_apk_path)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: repackage failed", loguer)
