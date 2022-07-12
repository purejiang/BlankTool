# -*- coding:utf-8 -*-

from utils.file_helper import FileHelper
from utils.other_util import currentTimeMillis

class Loguer(object):
    """

    @author: purejiang
    @created: 2022/5/25

    日志工具

    """
    def __init__(self, log_file, start_line="="*10, end_line="-"*10):
        super().__init__()
        parent_dir = FileHelper.parentDir(log_file)
        if not FileHelper.fileExist(parent_dir):
            FileHelper.createDir(parent_dir)
        self.__log_file = log_file
        self.__log_content = ""
        self.__step_time_dict = {}
        self.__start_line = start_line
        self.__end_line = end_line

    def log(self, msg):
        msg = "\n{0}\n".format(msg)
        self.__log_content = self.__log_content + msg
        print(msg)

    def log_tag(self, tag, msg):
        msg = "{0}: {1}\n".format(tag, msg)
        self.__log_content = self.__log_content + msg
        print(msg)

    def log_start(self, key, msg):
        self.__step_time_dict[key] = currentTimeMillis()
        start_msg = "\n{0} {1} {0}\n".format(self.__start_line, msg) + "\n"
        self.__log_content = self.__log_content + start_msg
        print(start_msg)

    def log_end(self, key, msg="end"):
        if key not in self.__step_time_dict:
            print("log key ({0}) is not found".format(key))
        content = "{0}, {1}s".format(
            msg, currentTimeMillis() - self.__step_time_dict[key])
        end_msg = "\n{0} {1} {0}\n".format(self.__end_line, content) + "\n"
        self.__log_content = self.__log_content + end_msg
        print(end_msg)
    
    def save(self):
        with open(self.__log_file, "w+", encoding="utf-8") as file:
            file.write(self.__log_content)