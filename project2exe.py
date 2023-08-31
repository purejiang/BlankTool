# -*- coding:utf-8 -*-

"""
打包项目为可以发布的 .exe  程序

@author: purejiang
@created: 2022/9/14

"""
import os
import re
from cmd_util.app_cmd import AppCMD

from utils.file_helper import FileHelper
from utils.jloger import JLogger
from utils.other_util import currentTimeMillis, currentTimeNumber


class ResHelper():
    __QRC_HODLER_TEXT = "<!DOCTYPE RCC>\n<RCC version=\"1.0\">\n{0}\n</RCC>"
    __QRESOURCE_HOLDER_TEXT = "\t<qresource prefix=\"{0}\">\n{1}\n\t</qresource>\n"
    __FILE_HOLDER_TEXT = "\t\t<file alias=\"{0}\">{1}</file>\n"

    def __init__(self, rcc_exe) -> None:
        super().__init__()
        self.__rcc_exe = rcc_exe
        self.__logger = JLogger()

    def _qResourceText(self, resource_dir, prefix_tag)->str:
        """
        生成外层的 prefix tag 文本，例如：<qresource prefix="img"> </qresource>
        """
        qresource_content = ""
        for file in os.listdir(resource_dir):
            # .ico 文件不加入资源映射
            if file.endswith(".ico"):
                continue
            qresource_content += self._fileText(os.path.join(resource_dir, file))
        qresource_text = self.__QRESOURCE_HOLDER_TEXT.format(prefix_tag, qresource_content)
        self.__logger.info("生成外层的 prefix tag 文本:"+ prefix_tag)
        return qresource_text

    def _fileText(self, file_path):
        """
        生成内层的文件映射文本，例如：<file alias="app_icon_small">f:\app_icon_small.png</file>
        """
        alias_name = FileHelper.filename(file_path, False)
        file_text = self.__FILE_HOLDER_TEXT.format(alias_name, file_path)   
        self.__logger.info("生成内层的文件映射文本:"+alias_name)
        return file_text

    def _createQrc(self, qresource_list, qrc_file):
        """
        生成 .qrc 文件
        """
        qresources = ""
        for qresource in qresource_list:
            qresources += qresource
        qrc_text = self.__QRC_HODLER_TEXT.format(qresources)
        result = FileHelper.writeContent(qrc_file, qrc_text)
        self.__logger.info("生成 .qrc 文件:{0} is {1}".format(qrc_file, str(result)))
        return result

    def _createRcc(self, rcc_exe, qrc_file, rcc_file):
        """
        将 .qrc 文件的映射转换为二进制的 .rcc 文件（.qrc 中所有映射的资源文件都会打包进 .rcc 文件）
        """
        cmd_result = AppCMD.qrc2Rcc(rcc_exe, qrc_file, rcc_file)
        self.__logger.info("转换为二进制的 .rcc 文件:{0} is {1}".format(rcc_file, str(cmd_result[0])))
        return cmd_result[0]

    def res2rcc(self, res_dirs, qrc_file, rcc_file):
        qresource_list = []
        for res_dir in res_dirs:
            tag = FileHelper.filename(res_dir, False)
            qresource_list.append(self._qResourceText(res_dir, tag))

        if self._createQrc(qresource_list, qrc_file):
            return self._createRcc(self.__rcc_exe, qrc_file, rcc_file)
        else:
            print("creata qrc file failed")
            return False

class ExeHelper(object):

    def __init__(self, project_path, pyinstaller_exe, rcc_exe) -> None:
        super().__init__()
        self.__pyinstaller_exe = pyinstaller_exe
        self.__project_path = project_path
        self.__res_helper =ResHelper(rcc_exe)
        self.__logger = JLogger()

    def run(self):
        ####### step 1 ：当前版本为发布版本时，复制项目到工作目录 #######
        debug_project, release_project, release_zip = self._initDir()

        ####### step 2：替换并修改文件中所使用的静态资源的相对路径为二进制资源包中的路径，例：.res/qss/xxxx.qss 为 :qss/xxxx #######
        check_paths = ["widget", "res/qss"]
        check_dirs = [os.path.join(release_project, check_name) for check_name in check_paths]
        self._replaceStaticResPath(check_dirs)

        ####### step 3：生成 res.rcc 文件 #######
        res_dir = os.path.join(release_project, "res")
        resource_path = os.path.join(release_project, "resource")
        FileHelper.createDir(resource_path)
        qrc_file = os.path.join(
            resource_path, "res_{0}.qrc".format(currentTimeMillis()))
        rcc_file = os.path.join(
            resource_path, "res_{0}.rcc".format(currentTimeMillis()))
        tags = ["img", "qss", "ui"]
        res_dirs = [os.path.join(res_dir, tag) for tag in tags]
        if not self.__res_helper.res2rcc(res_dirs, qrc_file, rcc_file):
            return
        ####### step 4：写入程序信息文件 #######

        ####### step 5：命令行使用 pyinstaller 打包，使用配置文件 main.spec #######
        self._createExe(release_project, release_zip)

    def _createExe(self, project_path, release_zip=None):
        """
        生成 .exe
        """
        os.chdir(project_path)
        # 命令行使用 pyinstaller 打包，使用配置文件 main.spec
        main_spec = os.path.join(project_path, "main.spec")
        cmd_result = AppCMD.pyinstallerExe(self.__pyinstaller_exe, main_spec)
        self.__logger.info("生成 .exe is {0}".format(cmd_result[0]))
        if cmd_result[0]:
            if release_zip!=None:
                # 打包成 zip 等压缩文件，解压即可运行
                main_dir = os.path.join(project_path, "dist/main")
                result = FileHelper.tozip(main_dir, release_zip)
                self.__logger.info("生成 免安装包：{0} is {1}".format(release_zip, result))
            return True
        else:
            return False

    def _initDir(self):
        # 不复制的文件/文件夹
        exclude_files = [".git", "cache", "project2exe.py",
                        "README_ZH.md", "README.md", "requirements.txt"]
        # 开发版本路径
        debug_project = self.__project_path
        # 发行版本路径
        release_project = os.path.abspath(os.path.join(os.path.dirname(self.__project_path), "blank_tool_release_v5_{}".format(currentTimeNumber())))
        # 最终生成的程序免安装包
        release_zip = os.path.join(
            release_project, "blank_tool_release_v5_{}.zip".format(currentTimeNumber()))

        if FileHelper.fileExist(release_project):
            FileHelper.delFile(release_project)
        FileHelper.createDir(release_project)
        for file in FileHelper.getChild(debug_project):
            file_name = FileHelper.filename(file)
            if file_name not in exclude_files:
                new_file = os.path.join(
                    os.path.abspath(release_project), file_name)
                FileHelper.copyFile(file, new_file)
        self.__logger.info("初始化项目：{0}".format(release_project))
        return debug_project, release_project, release_zip

    def _replaceStaticResPath(self, res_dirs):
        """
        替换并修改文件中所使用的静态资源的相对路径为二进制资源包中的路径，例：.res/qss/xxxx.qss 为 :qss/xxxx
        """
        for check_dir in res_dirs:
            for file in FileHelper.getAllChild(check_dir, FileHelper.TYPE_FILE):
                if FileHelper.getSuffix(file)==".py" or FileHelper.getSuffix(file)==".qss":
                    content = FileHelper.fileContent(file)
                    res_list = re.findall("[\"(]\./res/.*?[\")]", content)
                    for res in res_list:
                        old_str = res.replace(")","").replace("(","").replace("\"","")
                        new_str = old_str.replace("./res/", ":").split(".")[0]
                        content = content.replace(old_str, new_str)
                    FileHelper.writeContent(file, content.replace(res, new_str))
        self.__logger.info("替换并修改静态资源路径")


if __name__ == "__main__":
    # 用到的工具
    rcc_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Lib\site-packages\PySide6\rcc.exe"
    pyinstaller_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Scripts\pyinstaller.exe"
    project_path  = r"F:\python_project\blank_tool_v5"
    ExeHelper(project_path=project_path, rcc_exe=rcc_exe, pyinstaller_exe=pyinstaller_exe).run()