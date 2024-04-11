# -*- coding: utf-8 -*-

import locale
import platform
import subprocess
import traceback
from typing import Union


class BaseCMD(object):
    """

    @author: purejiang
    @created: 2021/8/25

    命令行工具集

    """

    @classmethod
    def run(cls, win_cmd, linux_cmd, mac_cmd)->Union[bool, str, str]:
        """
        执行 CMD 命令

        :param win_cmd: windows 系统的命令行
        :param linux_cmd: linux 系统的命令行
        :param mac_cmd: mac 上的命令行

        """
        try:
            if platform.system() == "Windows":
                cmd = win_cmd
            elif platform.system() == "Linux":
                cmd = linux_cmd
            elif platform.system() == 'Darwin':
                cmd = mac_cmd
            else:
                return False, "Cmd not support this System.", cmd
            process = subprocess.check_output(cmd, shell=True)
            try:
                # 不指定utf-8，在windows上会有gbk转utf-8的问题
                cmd_result = process.decode(encoding=locale.getpreferredencoding())
            except UnicodeDecodeError:
                cmd_result = process.decode("gbk")
            return True, cmd_result, cmd
        except Exception as e:
            e_msg = traceback.format_exc()
            return False, "exce:\n{0}".format(e_msg), cmd


if __name__ == "__main__":
    # cmd = r"F:\Local\Programs\Python\Python37\DLLs\Scripts\virtualenv.exe"
    # sys.executable = ("F:\Local\Programs\Python\Python37\python.exe")
    # print(sys.executable)
    # cmdBySystem(cmd, cmd, "error")
    pass
