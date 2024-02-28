# -*- coding: utf-8 -*-
from typing import Union

from .base_cmd import BaseCMD

class AdbCMD(BaseCMD):

    ########################### ADB命令 ###############################################
    @classmethod
    def adbKillServer(cls):
        """
        adb关闭

        adb kill-server
        """
        win_cmd ="adb kill-server"
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def adbStartServer(cls):
        """
        adb连接
        adb start-server
        """
        win_cmd ="adb start-server"
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def adbDevices(cls):
        """
        adb连接的设备
        adb devices
        """
        win_cmd ="adb devices -l"
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def adbInstallApk(cls, apk_file, device_name=None)->Union[bool, str]:        
        """
        安装 .apk

        :param apk_file: 需要安装的 .apk 文件

        adb install xxx.apk
        """
        s = ""
        if device_name!=None:
            s = "-s {0} ".format(device_name)
        all_cmd = "adb {0}install \"{1}\"".format(s,apk_file)
        return cls.run(all_cmd, all_cmd, all_cmd)
    
    @classmethod
    def getAppsByAdb(cls, info_file, is_install, is_path, is_sys, device_name=None):
        """
        adb 获取手机上的包名列表

        :param info_file: 存储信息的文件

        adb shell pm list packages [-i 可选，附加安装来源（会有报错）] [-f 可选，附加安装路径] [-s / -3 可选，输出系统包/输出第三方包]
        """
        s = ""
        if device_name!=None:
            s = "-s {0} ".format(device_name)
        val_cmd = ""
        if is_install:
            val_cmd+=" -i"
        if is_path:
            val_cmd+=" -f"
        if is_sys:
            val_cmd+=" -s"
        win_cmd = "adb {0}shell pm list packages{1} >> \"{2}\"".format(s, val_cmd, info_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def getAppInfo(cls, info_file, device_name=None):
        """
        adb 获取手机上的包体信息

        :param info_file: 存储信息的文件

        adb shell dumpsys package [packages 可选，包体信息] 
        """
        s = ""
        if device_name!=None:
            s = "-s {0} ".format(device_name)
        win_cmd = "adb {0}shell dumpsys package packages >> \"{1}\"".format(s, info_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def getInphonePath(cls, package_name, info_file, device_name=None):
        """
        获取 apk 在手机上的安装目录


        :param pakcage_name: 包名
        :param info_file: 存储信息的文件路径

        adb shell pm path [包名]
        """
        s = ""
        if device_name!=None:
            s = "-s {0} ".format(device_name)
        win_cmd = "adb {0}shell pm path {1} >> \"{2}\"".format(s, package_name, info_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def pullApkByAdb(cls, in_phone_file, target_dir, device_name=None):
        """
        通过 adb 命令将手机路径下的 apk 导出到指定路径

        :param in_phone_path: .apk 在手机内的路径
        :param target_dir: 导出的目录

        """
        s = ""
        if device_name!=None:
            s = "-s {0} ".format(device_name)
        all_cmd = "adb {0}pull \"{1}\" \"{2}\"".format(s, in_phone_file, target_dir)
        return cls.run(all_cmd, all_cmd, all_cmd)