# -*- coding:utf-8 -*-

"""
打包项目为可以发布的 .exe  程序

@author: purejiang
@created: 2022/9/14

"""
import json
import os
import re
from cmd_util.app_cmd import AppCMD

from utils.file_helper import FileHelper
from utils.jlogger import JLogger
from utils.other_util import currentTimeMillis, currentTimeNumber


class ResHelper():
    __QRC_HODLER_TEXT = "<!DOCTYPE RCC>\n<RCC version=\"1.0\">\n{0}\n</RCC>"
    __QRESOURCE_HOLDER_TEXT = "\t<qresource prefix=\"{0}\">\n{1}\n\t</qresource>\n"
    __FILE_HOLDER_TEXT = "\t\t<file alias=\"{0}\">{1}</file>\n"

    def __init__(self, rcc_exe) -> None:
        super().__init__()
        self.__rcc_exe = rcc_exe
        self.__logger = JLogger()

    def __getResMappingText(self, resource_dir, prefix_tag)->str:
        """
        生成资源映射的内容

        :param resource_dir: 资源文件目录
        :param prefix_tag: 外层的 tag
        """
        qresource_content = ""
        for file in os.listdir(resource_dir):
            # .ico 文件不用资源映射
            if file.endswith(".ico"):
                continue
            qresource_content += self.__getFileMappingText(os.path.join(resource_dir, file))
        # 生成外层的 prefix tag 文本，例如：<qresource prefix="img"> </qresource>
        qresource_text = self.__QRESOURCE_HOLDER_TEXT.format(prefix_tag, qresource_content)
        self.__logger.info("生成外层的 prefix tag 文本:"+ prefix_tag)
        return qresource_text

    def __getFileMappingText(self, file_path):
        """
        生成内层的文件映射文本，例如：<file alias="app_icon_small">f:\app_icon_small.png</file>

        :param file_path: 资源文件的路径
        """
        alias_name = FileHelper.filename(file_path, False)
        file_text = self.__FILE_HOLDER_TEXT.format(alias_name, file_path)   
        self.__logger.info("生成内层的文件映射文本:"+alias_name)
        return file_text

    def __createQrc(self, qresource_list, qrc_file):
        """
        生成 .qrc 文件

        :param qresource_list: 资源文件列表
        :param qrc_file: 生成的.qrc文件
        """
        qresources = ""
        for qresource in qresource_list:
            qresources += qresource
        qrc_text = self.__QRC_HODLER_TEXT.format(qresources)
        result = FileHelper.writeContent(qrc_file, qrc_text)
        self.__logger.info("生成 .qrc 文件:{0} is {1}".format(qrc_file, str(result)))
        return result

    def __createRcc(self, rcc_exe, qrc_file, rcc_file):
        """
        将 .qrc 文件的映射转换为二进制的 .rcc 文件（.qrc 中所有映射的资源文件都会打包进 .rcc 文件）

        :param rcc_exe: rcc.exe 工具路径
        :param qrc_file: 生成的.qrc文件
        :param rcc_file: 生成的.rcc文件
        """
        cmd_result = AppCMD.qrc2Rcc(rcc_exe, qrc_file, rcc_file)
        self.__logger.info("转换为二进制的 .rcc 文件:{0} is {1}".format(rcc_file, str(cmd_result)))
        return cmd_result[0]

    def run(self, res_dirs, output_dir):
        """
        根据资源列表生成 .rcc 文件（.qrc 中所有映射的资源文件都会打包进 .rcc 文件）

        :param rcc_exe: rcc.exe 工具路径
        :param output_dir: 生成资源文件的目录
        """
        qrc_file = os.path.join(output_dir, "res_{0}.qrc".format(currentTimeMillis()))
        rcc_file = os.path.join(output_dir, "res_{0}.rcc".format(currentTimeMillis()))
        qresource_list = []
        
        for res_dir in res_dirs:
            tag = FileHelper.filename(res_dir, False)
            qresource_list.append(self.__getResMappingText(res_dir, tag))

        if self.__createQrc(qresource_list, qrc_file):
            return self.__createRcc(self.__rcc_exe, qrc_file, rcc_file)
        else:
            return False

class ExeHelper(object):
    """

    """
    __EXCLUDE_FILES = [".git", "cache", "test", "data", "project2exe.py", "project2exe_v2.py", "plan.md", "app_version_list.json", "README_ZH.md", "README.md","README.md", "requirements.txt"]
    __RES_TAGS = ["img", "qss", "ui"]

    def __init__(self, origin_project, pyinstaller_exe, rcc_exe, app_config, default_setting, output_install_exe=None) -> None:
        """
        :param origin_project: 源项目（开发版）
        :param pyinstaller_exe: 版本号
        :param rcc_exe: 是否输出日志
        :param app_config: app 配置
        :param output_install_exe: 安装程序输出路径，没有配置的话则默认为源项目同级目录下
        """
        super().__init__()
        self.__pyinstaller_exe = pyinstaller_exe
        self.__rcc_exe = rcc_exe
        self.__origin_project = origin_project
        self.__output_install_exe = output_install_exe
        self.__app_config = app_config
        self.__default_setting = default_setting
        self.__logger = JLogger()

    def run(self):
        ####### step 1：复制项目到工作目录，作为发行版本 #######
        if self.__output_install_exe is None:
            # 发行版本路径
            origin_parent_dir = os.path.dirname(self.__origin_project)
        else:
            origin_parent_dir = os.path.dirname(self.__output_install_exe)

        release_project = os.path.abspath(os.path.join(origin_parent_dir, "blank_tool_release_project_{}".format(currentTimeNumber())))

        release_dist = os.path.abspath(os.path.join(origin_parent_dir, "blank_tool_release_{}.zip".format(currentTimeNumber())))

        installer_exe = os.path.abspath(os.path.join(origin_parent_dir, "blank_tool_release_{}.exe".format(currentTimeNumber())))

        self.__copyProject(self.__origin_project, release_project)

        ####### step 2：替换并修改文件中的路径 #######

        self.__replaceStaticResPath(release_project)

        ####### step 3：生成 res.rcc 文件 #######

        res_dir = os.path.join(release_project, "res")
        resource_path = os.path.join(release_project, "resource")
        FileHelper.createDir(resource_path)
        res_dirs = [os.path.join(res_dir, tag) for tag in self.__RES_TAGS]
        if not ResHelper(self.__rcc_exe).run(res_dirs, resource_path):
            return
        
        ####### step 4：写入程序信息文件 #######
        app_config_file = os.path.join(release_project, "config/app_config.json")
        default_config_file = os.path.join(release_project, "config/default_config.json")
        self._writeAppConfig(self.__app_config, self.__default_setting, app_config_file, default_config_file)

        ####### step 5：清理测试数据 #######
        # self._cleanTestData(release_project)

        ####### step 6：命令行使用 pyinstaller 打包，使用配置文件 main.spec #######
        self._createRelease(release_project, release_dist)

    
    def _cleanTestData(self, release_project):
        """
        删除测试的数据
        """
        user_config_data_file = os.path.join(release_project, "data/user_config.json")
        signer_data_file = os.path.join(release_project, "data/signer.json")
        test_files = [user_config_data_file, signer_data_file]
        for file in test_files:
            if FileHelper.fileExist(file):
                FileHelper.delFile(file)

    def _createRelease(self, project_path, release_dist):
        """
        生成 .exe

        :param project_path: 项目目录
        :param release_dist: 应用压缩包
        """
        os.chdir(project_path)
        # 命令行使用 pyinstaller 打包，使用配置文件 main.spec
        main_spec = os.path.join(project_path, "main.spec")
        cmd_result = AppCMD.pyinstallerExe(self.__pyinstaller_exe, main_spec)
        self.__logger.info("生成 .exe is {0}".format(cmd_result[0]))
        if cmd_result[0]:
            if release_dist!=None:
                # 打包成 zip 等压缩文件，解压即可运行
                main_dir = os.path.join(project_path, "dist/main")
                result = FileHelper.tozip(main_dir, release_dist)
                self.__logger.info("生成exe：{0} is {1}".format(release_dist, result))
            return True
        else:
            return False

    def __copyProject(self, origin_project, release_project):
        """
        移动发行项目到正式项目目录

        :param origin_project: 发行版版项目目录
        :param release_project: 正式版项目目录

        """
        if FileHelper.fileExist(release_project):
            FileHelper.delFile(release_project)

        FileHelper.createDir(release_project)
        for file in FileHelper.getChild(origin_project):
            file_name = FileHelper.filename(file)
            if file_name not in self.__EXCLUDE_FILES:
                new_file = os.path.join(os.path.abspath(release_project), file_name)
                FileHelper.copyFile(file, new_file)
        self.__logger.info("copy项目：{0}".format(release_project))

    def __replaceStaticResPath(self, release_project):
        """
        替换并修改文件中所使用的静态资源的相对路径为二进制资源包中的路径，例：.res/qss/xxxx.qss 改为 :qss/xxxx

        :param release_project: 正式版项目目录
        """
        check_paths = ["widget", "res/qss"]
        for check_dir in [os.path.join(release_project, check_name) for check_name in check_paths]:
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
    
    def _writeAppConfig(self, new_app_config, default_setting, app_config_file, default_config_file):
        """
        写入app信息到文件

        :param version_name: 版本名
        :param version_code: 版本号
        :param is_out_log: 是否输出日志
        :param mode: 模式，DEBUG和RELEASE
        :param web_url: 官网地址
        """
        app_config = json.loads(FileHelper.fileContent(app_config_file))
        app_config["app_info"]["app_name"] = new_app_config["app_name"]
        app_config["app_info"]["version_code"] = new_app_config["version_code"]
        app_config["app_info"]["version_name"] = new_app_config["version_name"]
        app_config["app_info"]["web_url"] = new_app_config["web_url"]
        app_config["app_info"]["build_time"] = currentTimeNumber()
        app_config["app_info"]["mode"] = new_app_config["mode"]
        
        app_config_result = FileHelper.writeContent(app_config_file, json.dumps(app_config))

        default_config = json.loads(FileHelper.fileContent(default_config_file))
        default_config["setting"]["app"]["is_out_log"] = default_setting["is_out_log"]
        default_config["setting"]["app"]["theme"] = default_setting["theme"]
        default_config["setting"]["adb"]["choose_first"] = default_setting["choose_first"]
        default_config_result = FileHelper.writeContent(default_config_file, json.dumps(default_config))
        return app_config_result and default_config_result

if __name__ == "__main__":
    # 用到的工具
    rcc_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Lib\site-packages\PySide6\rcc.exe"
    pyinstaller_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Scripts\pyinstaller.exe"
    project_path  = r"F:\python_project\blank_tool_v5"
    # app 配置信息
    app_config = {}
    app_config["app_name"] = "BlankTool 5"
    app_config["version_code"] = "06020240313"
    app_config["version_name"] = "0.6.0"
    app_config["web_url"] = "https://purejiang.github.io/"
    app_config["mode"] = "DEBUG"

    default_setting={}
    default_setting["is_out_log"] = True
    default_setting["theme"] = "dark"
    default_setting["choose_first"] = True
    
    ExeHelper(project_path, pyinstaller_exe, rcc_exe, app_config, default_setting).run()