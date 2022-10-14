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
from utils.other_util import currentTimeMillis, write_print

class ResToRcc(object):
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

        file_text =""
        for file in os.listdir(dir):
            if file.endswith(".ico"):
                continue
            file_text += self.fileText(os.path.join(dir, file))
        return self.qresource_text_temp.format(tag, file_text)
    
    def fileText(self, file):
        return self.file_text_temp.format(FileHelper.filename(file, False), file)
    
    def createQrc(self, qresource_list, qrc_file):
        qresources = ""
        for qresource in qresource_list:
            qresources+=qresource
        qrc_text = self.qrc_text_temp.format(qresources)
        return FileHelper.writeContent(qrc_file, qrc_text)

    def createRcc(self, rcc_exe, qrc_file, rcc_file):
        cmd_result = CMD.qrc2Rcc(rcc_exe, qrc_file, rcc_file)
        write_print(None, cmd_result[1])
        return cmd_result[0]
    
    def start(self, rcc_exe, res_dir, tags, qrc_file, rcc_file):
        qResource_list = []
        for dir in  os.listdir(res_dir):
            if dir in tags:
                tag = dir 
                qResource_list.append(self.qResourceText(os.path.join(res_dir, dir), tag))
            else:
                write_print(None, "tag not in tags")
        if self.createQrc(qResource_list, qrc_file):
            return self.createRcc(rcc_exe, qrc_file, rcc_file)
        else:
            write_print(None, "creata qrc file failed")
            return False


if __name__=="__main__":
    exclude_files =[".git", "cache", "project2exe.py", "README_ZH.md", "README.md", "requirements.txt"]
    # 第一步，当前版本为发布版本时，完全复制项目到工作目录
    debug_project  = os.path.abspath(os.path.dirname(__file__))
    release_project = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "blank_tool_release"))
    release_zip = os.path.join(release_project, "release.zip")
    if FileHelper.fileExist(release_project):
        FileHelper.delFile(release_project)
    FileHelper.createDir(release_project)
    for file in FileHelper.getChild(debug_project, FileHelper.TYPE_BOTH):
        file_name = FileHelper.filename(file)
        if file_name not in exclude_files:
            new_file = os.path.join(os.path.abspath(release_project), file_name)
            FileHelper.copyFile(file, new_file)
    os.chdir(release_project)
    # 第二步，替换并修改文件中所使用的静态资源的相对路径为二进制资源包中的路径，例：.res/qss/xxxx.qss 为 :qss/xxxx
    check_dirs = ["ui", "res/qss"]
    for check_dir in check_dirs:
        for file in FileHelper.getChild(os.path.join(release_project, check_dir), FileHelper.TYPE_FILE):
            print(file)
            content = FileHelper.fileContent(file)
            str_list = re.findall("\./res/.*[\.\w?]", content)
            for str in str_list:
                print(str_list)
                new_str = str.replace("./res/", ":").split(".")[0]
                content = content.replace(str, new_str)
            FileHelper.writeContent(file, content.replace(str, new_str))

    # 第三步，生成 res.rcc 文件
    rcc_exe = r"D:\ProgramData\Miniconda3\envs\py_blank_tool\Lib\site-packages\PySide2\rcc.exe"
    res_dir = os.path.join(release_project, "res")
    tags = ["img", "qss", "ui"]
    resource_path = os.path.join(release_project, "resource")
    FileHelper.createDir(resource_path)
    qrc_file= os.path.join(resource_path, "res_{0}.qrc".format(currentTimeMillis()))
    rcc_file= os.path.join(resource_path, "res_{0}.rcc".format(currentTimeMillis()))
    if not ResToRcc().start(rcc_exe, res_dir, tags, qrc_file, rcc_file):
        print("res2rcc failed")
        exit()
    # else:
        # FileHelper.delFile(qrc_file)
    pyinstaller_exe = r"D:\ProgramData\Miniconda3\envs\py_blank_tool\Scripts\pyinstaller.exe"

    # 第四步，命令行使用 pyinstaller 打包 main.py 文件
    main_py =  os.path.join(release_project, "main.py")
    kvs = {"os.chdir(sys.path[0])":""}
    FileHelper.replace(main_py, kvs)
    cmd_result = CMD.pyinstallerExe(pyinstaller_exe, main_py)
    if not cmd_result[0]:
        print(cmd_result[1])
        exit()

    # 第五步，复制运行时环境 re 和 res.rcc 到 .exe 的同级路径下
    copy_dirs = ["re", resource_path]
    main_dir = os.path.join(release_project, "dist/main")
    for copy_dir in copy_dirs:
        new_dir = os.path.join(main_dir, FileHelper.filename(copy_dir))
        FileHelper.copyFile(copy_dir, new_dir)
    
    # 第六步，打包成 zip 等压缩文件，解压即可运行
    # main.py 优化处理
    FileHelper.tozip(main_dir, release_zip)
    
