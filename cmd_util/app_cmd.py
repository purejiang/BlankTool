# -*- coding: utf-8 -*-
from typing import Union

from .base_cmd import BaseCMD

class AppCMD(BaseCMD):

    ########################### 设置环境 ###############################################
    @classmethod
    def setPath(cls, path):
        """
        设置临时系统环境变量

        :param path: 系统环境变量的路径

        windows: set path=[系统环境变量的路径]
        linux: export PATH=[系统环境变量的路径]

        例如： 
        set path=F:\python_project\blank_tool\re\jre\bin
        export PATH=/usr/local/blank_tool/re/jre/bin
        """
        win_cmd = "set path=".format(path)
        linux_cmd = "export PATH=".format(path)
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
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
    
    ########################### 打包命令 ###############################################
    @classmethod
    def qrc2Rcc(cls, rcc_exe, qrc_file, rcc_file):
        """
        qrc 转 rcc

        :param rcc_exe: rcc.exe 路径
        :param qrc_file:  .qyc 文件
        :param rcc_file:  输出的 .rcc （包含了资源的二进制文件）

        [ rcc.exe ] -binary [.qrc 文件] -o [输出的 .rcc 文件]
        """
        win_cmd ="\"{0}\" -binary \"{1}\" -o \"{2}\"".format(rcc_exe, qrc_file, rcc_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def pyinstallerExe(cls, pyinstaller, spec_file):
        """
        打包 python 项目

        :param spec_file: 配置文件

        [ pyinsatller.exe ] [ spec 配置文件]
        """
        win_cmd ="\"{0}\" \"{1}\"".format(pyinstaller, spec_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)