# -*- coding:utf-8 -*-

"""
打包项目为可以发布的 .exe  程序

@author: purejiang
@created: 2022/9/14

"""
import os
import re
from common.cmd import CMD

from utils.file_helper import FileHelper
from utils.other_util import currentTimeMillis, currentTimeNumber


class ResToRcc():
    qrc_text_temp = """
<!DOCTYPE RCC>
<RCC version="1.0">
{0}
</RCC>
"""
    qresource_text_temp = "\t<qresource prefix=\"{0}\">\n{1}\n\t</qresource>\n"
    file_text_temp = "\t\t<file alias=\"{0}\">{1}</file>\n"

    def __init__(self) -> None:
        super().__init__()

    def qResourceText(self, dir, tag):
        """
        生成外层的 tag 文本，例如：<qresource prefix="img"> </qresource>
        """
        file_text = ""
        for file in os.listdir(dir):
            # .ico 文件不加入资源映射
            if file.endswith(".ico"):
                continue
            file_text += self.fileText(os.path.join(dir, file))
        return self.qresource_text_temp.format(tag, file_text)

    def fileText(self, file):
        """
        生成内层的文件映射文本，例如：<file alias="app_icon_small">f:\app_icon_small.png</file>
        """
        return self.file_text_temp.format(FileHelper.filename(file, False), file)

    def createQrc(self, qresource_list, qrc_file):
        """
        生成 .qrc 文件
        """
        qresources = ""
        for qresource in qresource_list:
            qresources += qresource
        qrc_text = self.qrc_text_temp.format(qresources)
        return FileHelper.writeContent(qrc_file, qrc_text)

    def createRcc(self, rcc_exe, qrc_file, rcc_file):
        """
        将 .qrc 文件的映射转换为二进制的 .rcc 文件（.qrc 中所有映射的资源文件都会打包进 .rcc 文件）
        """
        cmd_result = CMD.qrc2Rcc(rcc_exe, qrc_file, rcc_file)
        print(cmd_result[1])
        return cmd_result[0]

    def start(self, rcc_exe, res_dir, tags, qrc_file, rcc_file):
        qResource_list = []
        for tag in os.listdir(res_dir):
            if tag in tags:
                qResource_list.append(self.qResourceText(
                    os.path.join(res_dir, tag), tag))
            else:
                print("tag not in tags")
        if self.createQrc(qResource_list, qrc_file):
            return self.createRcc(rcc_exe, qrc_file, rcc_file)
        else:
            print("creata qrc file failed")
            return False


if __name__ == "__main__":
    # 用到的工具
    rcc_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Lib\site-packages\PySide6\rcc.exe"
    pyinstaller_exe = r"D:\ProgramData\Miniconda3\envs\pyside6_re\Scripts\pyinstaller.exe"

    ####### step 1 ：当前版本为发布版本时，复制项目到工作目录 #######
    # 不复制的文件/文件夹
    exclude_files = [".git", "cache", "project2exe.py",
                     "README_ZH.md", "README.md", "requirements.txt"]
    # 开发版本路径
    debug_project = os.path.abspath(os.path.dirname(__file__))
    # 发行版本路径
    release_project = os.path.abspath(os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "blank_tool_release_{}".format(currentTimeNumber())))
    # 最终生成的程序免安装包
    release_zip = os.path.join(
        release_project, "release_{}.zip".format(currentTimeNumber()))

    if FileHelper.fileExist(release_project):
        FileHelper.delFile(release_project)
    FileHelper.createDir(release_project)
    for file in FileHelper.getChild(debug_project):
        file_name = FileHelper.filename(file)
        if file_name not in exclude_files:
            new_file = os.path.join(
                os.path.abspath(release_project), file_name)
            FileHelper.copyFile(file, new_file)
            
    ####### step 2：替换并修改文件中所使用的静态资源的相对路径为二进制资源包中的路径，例：.res/qss/xxxx.qss 为 :qss/xxxx #######
    # 命令行进入到发行版根目录
    os.chdir(release_project)
    check_dirs = ["widget", "res/qss"]
    for check_dir in check_dirs:
        for file in FileHelper.getAllChild(os.path.join(release_project, check_dir), FileHelper.TYPE_FILE):
            if FileHelper.getSuffix(file)==".py" or FileHelper.getSuffix(file)==".qss":
                content = FileHelper.fileContent(file)
                res_list = re.findall("[\"(]\./res/.*?[\")]", content)
                for res in res_list:
                    old_str = res.replace(")","").replace("(","").replace("\"","")
                    new_str = old_str.replace("./res/", ":").split(".")[0]
                    content = content.replace(old_str, new_str)
                FileHelper.writeContent(file, content.replace(res, new_str))

    ####### step 3：生成 res.rcc 文件 #######
    res_dir = os.path.join(release_project, "res")
    tags = ["img", "qss", "ui"]
    resource_path = os.path.join(release_project, "resource")
    FileHelper.createDir(resource_path)
    qrc_file = os.path.join(
        resource_path, "res_{0}.qrc".format(currentTimeMillis()))
    rcc_file = os.path.join(
        resource_path, "res_{0}.rcc".format(currentTimeMillis()))
    if not ResToRcc().start(rcc_exe, res_dir, tags, qrc_file, rcc_file):
        print("res2rcc failed")
        exit()
    # else:
        # FileHelper.delFile(qrc_file)
    # main.py 优化处理,删掉某些代码块
    kvs = {"os.chdir(sys.path[0])": ""}
    main_py = os.path.join(release_project, "main.py")
    FileHelper.replace(main_py, kvs)

    ####### step 4：命令行使用 pyinstaller 打包，使用配置文件 main.spec #######
    main_spec = os.path.join(release_project, "main.spec")
    cmd_result = CMD.pyinstallerExe(pyinstaller_exe, main_spec)
    if not cmd_result[0]:
        print(cmd_result[1])
        exit()

    ####### step 5：打包成 zip 等压缩文件，解压即可运行 #######
    main_dir = os.path.join(release_project, "dist/main")
    FileHelper.tozip(main_dir, release_zip)
