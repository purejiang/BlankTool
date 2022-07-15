# -*- coding:utf-8 -*-

import os
from utils.file_helper import FileHelper
from utils.other_util import cmdBySystem, write_print

class ApkTools(object):


    @classmethod
    def install_apk(cls, adb_path, apk_path, loguer = None):
        """
        安装 apk
        :param apk_path: apk 路径
        adb install [apk 路径]
        """
        write_print(loguer, "install {0} ...".format(apk_path))
        # apk_name = os.path.basename(re.sub(r"( |)\(.\)", "", apk_path)) # 过滤掉(XX)字符
        win_linux_cmd = "{0} install {1}".format(
            adb_path, apk_path)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: install apk failed", loguer)

    @classmethod
    def depackage(cls, apktool_path, apk_path, output_dir, is_pass_dex=False, is_only_res=False, loguer = None):
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
            write_print(loguer, "output_dir is exist: {0}".format(output_dir))
            return True
        # apk_name = os.path.basename(re.sub(r"( |)\(.\)", "", apk_path)) # 过滤掉(XX)字符
        pass_dex = ""
        if is_pass_dex:
            pass_dex = " --only -main-classes"
        s = ""
        if is_only_res:
            s = " -s"
        win_linux_cmd = "java -jar {0}{1} d{2} {3} -o {4}".format(
            apktool_path, s, pass_dex, apk_path, output_dir)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: depackage failed", loguer)

    @classmethod
    def repackage(cls, apktool_path, dir_path, output_apk_path, is_support_aapt2=False, loguer=None):
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
            apktool_path, aapt2, dir_path, output_apk_path)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: repackage failed", loguer)
    
    @classmethod
    def aapt_apk_info(cls, aapt_path, apk_path, info_file_path, loguer=None):
        """
        获取本地的 apk 信息

        :param aapt_path: aapt 路径
        :param apk_path: apk 路径
        :param info_file_path: 输出信息的文件
        :param loguer: 日志工具

        """
        write_print(loguer, "aapt get {0} 's info ...".format(apk_path))
        if not FileHelper.fileExist(info_file_path):
            FileHelper.createDir(FileHelper.parentDir(info_file_path))
        win_linux_cmd = "{0} dump badging {1} >> {2}".format(aapt_path, apk_path, info_file_path)
        result = cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: aapt get info failed", loguer)
        return result

    @classmethod
    def pull_apks(cls, adb_path, info_file_path, loguer=None):
        """
        获取手机上的 apk 列表

        :param adb_path: adb 路径
        :param info_file_path: 输出信息的文件
        :param loguer: 日志工具

        """
        write_print(loguer, "pull packages ...")
        if not FileHelper.fileExist(info_file_path):
            FileHelper.createDir(FileHelper.parentDir(info_file_path))
        win_linux_cmd = "{0} shell pm list packages >> {1}".format(adb_path, info_file_path)
        result = cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: pull failed", loguer)
        return result

    @classmethod
    def get_inphone_path(cls, adb_path, info_file_path, package_name, loguer=None):
        """
        获取 apk 在手机上的安装目录

        :param adb_path: adb 路径
        :param info_file_path: 输出信息的文件
        :param package_name: 包名
        :param loguer: 日志工具

        """
        write_print(loguer, "get path ...")
        if not FileHelper.fileExist(info_file_path):
            FileHelper.createDir(FileHelper.parentDir(info_file_path))
        win_linux_cmd = "{0} shell pm path {1} >> {2}".format(adb_path, package_name, info_file_path)
        result = cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: get path failed", loguer)
        return result

    @classmethod
    def get_apk(cls, adb_path, in_phone_path, target_path, loguer=None):
        """
        通过 adb 命令将指定路径下的 apk 拉到 pc

        :param adb_path: adb 路径
        :param package_name: 包名
        :param loguer: 日志工具
        """
        write_print(loguer, "get path ...")

        win_linux_cmd = "{0} pull {1} {2}".format(adb_path, in_phone_path, target_path)
        return cmdBySystem(win_linux_cmd, win_linux_cmd, "Error: get apk failed", loguer)