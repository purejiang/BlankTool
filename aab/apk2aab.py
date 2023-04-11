# -*- coding:utf-8 -*-
import os
import platform
import shutil
import subprocess
import time
import zipfile

apktool_path = r".\re\apktool_2.6.1.jar"
aapt2= r".\re\aapt2.exe"
android_jar = r".\re\android.jar"
bundle_tool = r".\re\bundletool-all-1.7.0.jar"
smali_tool = r".\re\smali-2.5.2.jar"  

class Apk2Aab():
    """

    @author: purejiang
    @created: 2022/7/19

    apk 转 aab

    """
    def __init__(self, apk_path, output_path, apktool_path, aapt2_path, android_jar_path, bundle_tool_path, smali_tool_path, ver_args) -> None:
        """
        :param apk_path: 需要转换的 .apk
        :param output_path: 生成的 .aab
        :param apktool_path: apktool.jar 路径
        :param aapt2_path: aapt2.exe 路径
        :param android_jar_path: android.jar 路径
        :param bundle_tool_path: bundletool.jar 路径
        :param smali_tool_path: smali.jar 路径
        :param ver_args: 版本信息字典 {"min_ver":"", "tar_ver":"", "ver_code":"", "ver_name":""}
        """
        self.__apk_path = apk_path
        self.__apktool = apktool_path
        self.__aapt2 = aapt2_path
        self.__android_jar = android_jar_path
        self.__bundle_tool= bundle_tool_path
        self.__smali_tool= smali_tool_path
        self.__output_path = output_path
        self.__ver_args = ver_args
        self.__work_space = os.path.join("./cache", str(time.time()))
        self.__depackage_path = os.path.join(self.__work_space, "depackage")
        self.__other = os.path.join(self.__work_space, "other")
        self.__aab_project_path = os.path.join(self.__work_space, "aab_project")
        self.__base_path = os.path.join(self.__aab_project_path, "base")
    
    def start(self):
        if not self.depackage():
            return
        if not self.compileZip():
            return
        if not self.linkRes():
            return
        if not self.arrangeBaseApk():
            return
        if not self.bundleBuild():
            return

    def depackage(self):
        result = depackage(self.__apktool, self.__apk_path, self.__depackage_path)
        print(result[1])
        return result[0]

    def compileZip(self):
        res_path = os.path.join(self.__depackage_path, "res")
        os.makedirs(self.__aab_project_path)
        os.makedirs(self.__other)
        self.__zip_path = os.path.join(self.__other, "compile.zip")
        result = compileZip(self.__aapt2, res_path, self.__zip_path)
        print(result[1])
        return result[0]

    def linkRes(self):
        self.__base_apk = os.path.join(self.__other, "base.apk")
        manifest = os.path.join(self.__depackage_path, "AndroidManifest.xml")
        result= linkRes(self.__aapt2, self.__zip_path, self.__base_apk, self.__android_jar, manifest, self.__ver_args["min_ver"], self.__ver_args["tar_ver"], self.__ver_args["ver_code"], self.__ver_args["ver_name"])
        print(result[1])
        return result[0]
    
    def arrangeBaseApk(self):
        try:
            move_dict={}
            with zipfile.ZipFile(self.__base_apk, 'a') as zf:
                zf.extractall( self.__base_path)
            manifest_dir = os.path.join(self.__base_path, "manifest")
            os.makedirs(manifest_dir)
            # 移动 manifest
            old_manifest = os.path.join(self.__base_path, "AndroidManifest.xml")
            new_manifest = os.path.join(manifest_dir, "AndroidManifest.xml")
            move_dict[old_manifest] = new_manifest
            # 移动 assets
            old_assets = os.path.join(self.__depackage_path, "assets")
            new_assets = os.path.join(self.__base_path, "assets")
            move_dict[old_assets] = new_assets
            # 移动 lib
            old_lib = os.path.join(self.__depackage_path, "lib")
            new_lib = os.path.join(self.__base_path, "lib")
            move_dict[old_lib] = new_lib
            # 移动 unknown
            root = os.path.join( self.__base_path, "root")
            os.makedirs(root)
            old_unknown= os.path.join(self.__depackage_path, "unknown")
            new_unknown = os.path.join(root, "unknown")
            move_dict[old_unknown] = new_unknown

            for old,new in move_dict.items():
                if os.path.exists(old):
                    print(old+"->"+new)
                    shutil.move(old, new)
            # smali 转 dex
            result = self.smali2dex( self.__base_path)
            print(result[1])
            return result[0]
        except Exception as e:
            print(str(e))
            return False
    
    def smali2dex(self, base_path):
        result = True
        new_dex = os.path.join(base_path, "dex")
        os.makedirs(new_dex)
        for file in os.listdir(self.__depackage_path):
            file_name = os.path.basename(file)
            if not os.path.isfile(file) and "smali" in file_name:
                if "smali_" in file_name:
                    dex_file = os.path.join(new_dex, file_name.split("smali_")[1]+".dex")
                else:
                    dex_file = os.path.join(new_dex, "classes.dex")
                result = result and smali2dex(self.__smali_tool, dex_file, os.path.join(self.__depackage_path, file))
        return result

    def bundleBuild(self):
        zip_file = os.path.join(self.__aab_project_path, "base.zip")
        dir_path = self.__base_path
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                fpath = dirpath.replace(dir_path, '')
                fpath = fpath and fpath + os.path.sep or ''
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), fpath+filename)
        return buildBundle(self.__bundle_tool, zip_file, self.__output_path)

    def end(self, msg):
        print(msg)
        return

def depackage(apktool, apk_path, output_path):
    """
    java -jar [ apktool 文件] [-s (可选)] d [--only -main-classes (可选)] [需要反编的 apk 文件] -o [反编后输出的目录]

    """
    cmd = "java -jar {0} d {1} -o {2}".format(apktool, apk_path, output_path)
    return cmdBySystem(cmd, cmd)

def compileZip(aapt2, res_path, output_zip_path):
    """
    [ aapt2 文件] compile --dir [ res 路径] -o [生成资源的 zip ]
    """
    cmd = "{0} compile --dir {1} -o {2}".format(aapt2, res_path, output_zip_path)
    return cmdBySystem(cmd, cmd)

def linkRes(aapt2, zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name):
    """
    [ aapt2 文件] link --proto-format [资源的 zip ] -o [输出的 base.apk] -I [ android.jar 文件] --manifest [ manifest 文件] --min-sdk-version [最小版本] --target-sdk-version [目标版本] --version-code [版本号] --compile-sdk-version-name [版本名]
    """
    cmd = "{0} link --proto-format {1} -o {2} -I {3} --manifest {4} --min-sdk-version {5} --target-sdk-version {6} --version-code {7} --compile-sdk-version-name {8}".format(aapt2, zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name)
    return cmdBySystem(cmd, cmd)

def smali2dex(smali_jar, dex_path, smali_path):
    """
    java -jar [ smali.jar ] assemble -o [ dex 文件] [ smali 文件夹]
    """
    cmd = "java -jar {0} assemble -o {1} {2}".format(smali_jar, dex_path, smali_path)
    return cmdBySystem(cmd, cmd)

def buildBundle(bundle_tool, base_zip, output_aab):
    """
    java -jar [ bundletool.jar ] build-bundle --modules [ base.zip 文件] --output=[输出的 aab ]
    """
    cmd = "java -jar {0} build-bundle --modules {1} --output={2}".format(bundle_tool, base_zip, output_aab)
    return cmdBySystem(cmd, cmd)

def cmdBySystem(win_cmd, linux_cmd):
    """
    执行 CMD 命令

    :param win_cmd: windows 系统的命令行
    :param linux_cmd: linux 系统的命令行
    """
    try:
        if platform.system() == "Windows":
            cmd = win_cmd
        elif platform.system() == "Linux":
            cmd = linux_cmd
        else:
            return False, cmd+"\n"+"cmd not support this system"
        process = subprocess.check_output(cmd, shell=True)
        return True, cmd+"\n"+"result: "+process.decode(encoding='gbk')
    except Exception as Arugment:
        return False, cmd+"\n"+str(Arugment)


if __name__=="__main__":
    apk_path =r"F:\360MoveData\Users\Administrator.PC-20180314KCTP\Desktop\com.jlsy.mhlld_eb6e1752f3.apk"
    output_path =r"F:\360MoveData\Users\Administrator.PC-20180314KCTP\Desktop\com.jlsy.mhlld_eb6e1752f3.aab"
   
    Apk2Aab(apk_path, output_path, apktool_path, aapt2, android_jar, bundle_tool, smali_tool).start()


