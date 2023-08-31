# -*- coding:utf-8 -*-
import hashlib
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile

APKTOOL_PATH = os.path.join(sys.path[0], r"re\apktool_2.7.0.jar")
AAPT_PATH = os.path.join(sys.path[0], r"C:\Users\Administrator\AppData\Local\Android\Sdk\build-tools\30.0.3\aapt2.exe")
ANDROID_JAR_PATH = os.path.join(sys.path[0], r"C:\Users\Administrator\AppData\Local\Android\Sdk\platforms\android-30\android.jar")
BUDNLE_TOOL_PATH = os.path.join(sys.path[0], r"re\bundletool-all-1.7.0.jar")
SMALI_PATH = os.path.join(sys.path[0], r"re\smali-2.5.2.jar")
SIGNER_PATH = os.path.join(sys.path[0], r"re\jre\bin\jarsigner.exe")
JAVA_PATH = os.path.join(sys.path[0], r"D:\ProgramFiles\Java\jdk-11\bin\java.exe")
DEFAULT_MANIFEST_PATH = os.path.join(sys.path[0], r"AndroidManifest.xml")
CACHE_PATH = os.path.join(sys.path[0], "cache")


class Apk2Aab(object):
    """

    @author: purejiang
    @created: 2022/7/19

    apk 转 aab

    """

    def __init__(self, apk_path, output_path, apktool_path, aapt2_path, android_jar_path, bundle_tool_path, smali_tool_path, ver_config, signer_config) -> None:
        """
        :param apk_path: 需要转换的 .apk
        :param output_path: 生成的 .aab
        :param apktool_path: apktool.jar 路径
        :param aapt2_path: aapt2.exe 路径
        :param android_jar_path: android.jar 路径
        :param bundle_tool_path: bundletool.jar 路径
        :param smali_tool_path: smali.jar 路径
        :param ver_config: 版本配置

        """
        self.__apk_path = apk_path
        self.__apktool = apktool_path
        self.__aapt2 = aapt2_path
        self.__android_jar = android_jar_path
        self.__bundle_tool = bundle_tool_path
        self.__smali_tool = smali_tool_path
        self.__output_path = output_path
        self.__ver_config = ver_config
        self.__signer_config = signer_config
        self.__work_space = os.path.join(CACHE_PATH, str(
            hashlib.md5(open(apk_path, 'rb').read()).hexdigest()))
        self.__depackage_path = os.path.join(self.__work_space, "depackage")

        self.__other = os.path.join(self.__work_space, "other")
        self.__aab_project_path = os.path.join(
            self.__work_space, "aab_project")
        self.__base_path = os.path.join(self.__aab_project_path, "base")
        self.__assets_res_path = os.path.join(
            self.__aab_project_path, "AssetsPackGameRes")
        self.__base_zip_file = os.path.join(
            self.__aab_project_path, "base.zip")
        self.__assets_zip_file = os.path.join(
            self.__aab_project_path, "AssetsPackGameRes.zip")

    def start(self):
        # 反编
        if not self.depackage():
            print("depackage failed")
            return
        # 编译资源
        if not self.compileZip():
            print("compileZip failed")
            return
        # 链接资源
        if not self.linkRes():
            print("linkRes failed")
            return
        # 整理 base 模块
        if not self.arrangeBaseApk():
            print("arrangeBaseApk failed")
            return
        # 整理 assets 模块
        if not self.arrangeAssets():
            print("arrangeAssets failed")
            return
        # aab 构建
        if not self.bundleBuild():
            print("bundleBuild failed")
            return
        # aab 签名
        if not self.signerAab():
            print("signerAab failed")
            return

    def depackage(self):
        if Path(self.__work_space).exists():
            shutil.rmtree(self.__work_space)
        result = depackage(self.__apktool, self.__apk_path,
                           self.__depackage_path)
        self.parsePackage(self.__depackage_path)
        print(result[1])
        return result[0]

    def parsePackage(self, depackage_path):
        with open(os.path.join(depackage_path, "AndroidManifest.xml"), "r", encoding="utf-8") as file:
            content = file.read()
        # 非贪婪模式，取第一个
        self.__package_name = re.findall("package=\"(.*?)\"", content)[0]

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
        result = linkRes(self.__aapt2, self.__zip_path, self.__base_apk, self.__android_jar, manifest,
                         self.__ver_config["min_ver"], self.__ver_config["tar_ver"], self.__ver_config["ver_code"], self.__ver_config["ver_name"], self.__ver_config["compile_ver_name"])
        print(result[1])
        return result[0]

    def arrangeBaseApk(self):
        try:
            move_dict = {}
            with zipfile.ZipFile(self.__base_apk, 'a') as zf:
                zf.extractall(self.__base_path)
            manifest_dir = os.path.join(self.__base_path, "manifest")
            os.makedirs(manifest_dir)
            # 移动 manifest
            old_manifest = os.path.join(
                self.__base_path, "AndroidManifest.xml")
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
            # 移动 其他文件夹到 unknown
            old_unknown = os.path.join(self.__depackage_path, "unknown")
            kotlin = os.path.join(self.__depackage_path, "kotlin")
            meta_inf = os.path.join(self.__depackage_path, "original/META-INF")
            new_kotlin = os.path.join(old_unknown, "kotlin")
            new_meta_inf = os.path.join(old_unknown, "META-INF")
            shutil.copytree(kotlin, new_kotlin)
            shutil.copytree(meta_inf, new_meta_inf)

            # 移动 unknown
            root = os.path.join(self.__base_path, "root")
            move_dict[old_unknown] = root

            for old, new in move_dict.items():
                if os.path.exists(old):
                    print(old+" -> "+new)
                    if os.path.isfile(old):
                        shutil.move(old, new)
                    else:
                        shutil.copytree(old, new)
            # smali 转 dex
            result = self.smali2dex(self.__base_path)
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
                    dex_file = os.path.join(
                        new_dex, file_name.split("smali_")[1]+".dex")
                else:
                    dex_file = os.path.join(new_dex, "classes.dex")
                result = result and smali2dex(
                    self.__smali_tool, dex_file, os.path.join(self.__depackage_path, file))
        return result

    def bundleBuild(self):
        zip_txt = ""
        dir_path = self.__base_path
        with zipfile.ZipFile(self.__base_zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                fpath = dirpath.replace(dir_path, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), fpath+filename)
        zip_txt += self.__base_zip_file
        dir2_path = self.__assets_res_path
        if Path(dir2_path).exists():
            with zipfile.ZipFile(self.__assets_zip_file, 'w', zipfile.ZIP_DEFLATED) as zf2:
                for dirpath, dirnames, filenames in os.walk(dir2_path):
                    fpath = dirpath.replace(dir2_path, '')
                    fpath = fpath and fpath + os.sep or ''
                    for filename in filenames:
                        if filename != "resources.pb":
                            zf2.write(os.path.join(
                                dirpath, filename), fpath+filename)
            zip_txt += (","+self.__assets_zip_file)
        print("zip_txt:"+zip_txt)
        return buildBundle(self.__bundle_tool, zip_txt, self.__output_path)

    def signerAab(self):
        result = signerBundle(SIGNER_PATH, self.__output_path, self.__signer_config["key_store"], self.__signer_config[
                              "store_password"], self.__signer_config["key_password"], self.__signer_config["alias"])
        print(result[1])
        return result[0]

    def arrangeAssets(self):
        self.__assets_apk = os.path.join(self.__other, "game_res.apk")
        base_assets = os.path.join(self.__base_path, "assets")
        # base 的 assets 大于150 mb() 则分割资源
        size = os.path.getsize(self.__apk_path) / 1024.0 ** 2

        if size > 150+1024:
            print("apk 过大，无法分割 assets")
            return False
        elif size > 150:
            os.makedirs(self.__assets_res_path)
            new_assets = os.path.join(self.__assets_res_path, "assets")
            os.makedirs(new_assets)
            manifest_dir = os.path.join(self.__assets_res_path, "manifest")
            os.makedirs(manifest_dir)
            manifest = os.path.join(
                self.__assets_res_path, "AndroidManifest.xml")
            new_manifest = os.path.join(manifest_dir, "AndroidManifest.xml")
            shutil.copyfile(DEFAULT_MANIFEST_PATH, manifest)
            # 将manifest里面的${package_name}替换成包名
            with open(manifest, "r", encoding="utf-8") as file:
                content = file.read()
            with open(manifest, "w", encoding="utf-8") as file:
                file.write(content.replace(
                    r"${applicationId}", self.__package_name))
            for file in os.listdir(base_assets):
                old_file = os.path.join(base_assets, file)
                new_file = os.path.join(new_assets, file)
                # 如果是文件夹就移到 切割的assets
                if not os.path.isfile(old_file):
                    shutil.move(old_file, new_file)
                else:
                    if ".bundle" in os.path.basename(file):
                        shutil.move(old_file, new_file)
            result = linkResByDir(
                self.__aapt2, self.__assets_apk, self.__android_jar, manifest)
            print(result[1])
            if result[0]:
                with zipfile.ZipFile(self.__assets_apk, 'a') as zf:
                    zf.extractall(self.__assets_res_path)
                shutil.move(manifest, new_manifest)
            return result[0]
        else:
            return True


def depackage(apktool, apk_path, output_path):
    """
    java -jar [ apktool 文件] [-s (可选)] d [--only -main-classes (可选)] [需要反编的 apk 文件] -o [反编后输出的目录]

    """
    cmd = "{0} -jar {1} d {2} -o {3} --only-main-classes".format(
        JAVA_PATH, apktool, apk_path, output_path)
    return cmdBySystem(cmd, cmd)


def compileZip(aapt2, res_path, output_zip_path):
    """
    [ aapt2 文件] compile --dir [ res 路径] -o [生成资源的 zip ]
    """
    cmd = "{0} compile --dir {1} -o {2}".format(
        aapt2, res_path, output_zip_path)
    return cmdBySystem(cmd, cmd)


def linkRes(aapt2, zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name, compile_ver_name):
    """
    [ aapt2 文件] link --proto-format [资源的 zip ] -o [输出的 base.apk] -I [ android.jar 文件] --manifest [ manifest 文件] --min-sdk-version [最小版本] --target-sdk-version [目标版本] --version-code [版本号] --version-name [版本名] --compile-sdk-version-name [版本名]
    """
    cmd = "{0} link --proto-format {1} -o {2} -I {3} --manifest {4} --min-sdk-version {5} --target-sdk-version {6} --version-code {7} --version-name {8} --compile-sdk-version-name {9}".format(
        aapt2, zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name, compile_ver_name)
    linux_cmd = ""
    return cmdBySystem(cmd, cmd)


def linkResByDir(aapt2, base_apk_path, android_jar, manifest_file):
    """
    [ aapt2 文件] link --proto-format [资源的 dir ] -o [输出的 base.apk] -I [ android.jar 文件] --auto-add-overlay
    """
    cmd = "{0} link --proto-format -o {1} -I {2} --manifest {3} --auto-add-overlay".format(
        aapt2, base_apk_path, android_jar, manifest_file)
    return cmdBySystem(cmd, cmd)


def smali2dex(smali_jar, dex_path, smali_path):
    """
    java -jar [ smali.jar ] assemble -o [ dex 文件] [ smali 文件夹]
    """
    cmd = "{0} -jar {1} assemble -o {2} {3}".format(
        JAVA_PATH, smali_jar, dex_path, smali_path)
    return cmdBySystem(cmd, cmd)


def buildBundle(bundle_tool, base_zips, output_aab):
    """
    java -jar [ bundletool.jar ] build-bundle --modules [ base.zip 文件] --output=[输出的 aab ]
    """
    cmd = "{0} -jar {1} build-bundle --modules {2} --output={3}".format(
        JAVA_PATH, bundle_tool, base_zips, output_aab)
    return cmdBySystem(cmd, cmd)


def signerBundle(signer_tool, aab, keystore, store_password, key_password, alias):
    """
    jarsigner -digestalg SHA1 -sigalg SHA1withRSA -keystore [keystore 文件] -storepass [store password] -keypass [key password] [aab 文件] [store alias]
    """
    cmd = "{0} -digestalg SHA1 -sigalg SHA1withRSA -keystore {1} -storepass {2} -keypass {3} {4} {5}".format(
        signer_tool, keystore, store_password, key_password, aab, alias)
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
        return True, cmd+"\n"+"cmd_result:\n"+process.decode(encoding='gbk')
    except Exception as Arugment:
        return False, cmd+"\nexce:\n"+traceback.format_exc()


if __name__ == "__main__":
    """
    《阿尔米亚》 需要自适应ICON
    """
    apk_path = r"C:\Users\Administrator\Desktop\com.almia.zgen_7e4bea85e4.apk"
    app_version_code = 19
    app_version_name = "19.0"
    ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    singer_config = {"key_store": r"E:\work\keystore\aemydzg.jks", "store_password": "aemydzg_lnovs",
                  "key_password": "aemydzg_lnovs", "alias": "com.leniu_ovs.aemydzg", }
    """
    《PA》需要去掉以下权限
    • CAMERA 
    • ACCESS_FINE_LOCATION 
    • READ_PHONE_STATE 
    • READ_EXTERNAL_STORAGE 
    • WRITE_EXTERNAL_STORAGE
    需要自适应ICON，
    
    需要处理黑屏问题（母包已处理）
    """
    # apk_path = r"C:\Users\Administrator\Desktop\com.paaz.chronicle_65a6467394.apk"
    # app_version_code = 19
    # app_version_name = "19.0"
    # ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    # singer_config = {"key_store": r"E:\work\keystore\paen.jks", "store_password": "com.paan.chronicle",
    #                  "key_password": "com.paan.chronicle", "alias": "com.paan.chronicle", }
    """
    PA-欧美-包
    需要去掉以下权限
    • CAMERA 
    • ACCESS_FINE_LOCATION 
    • READ_PHONE_STATE 
    • READ_EXTERNAL_STORAGE 
    • WRITE_EXTERNAL_STORAGE
    需要自适应ICON，
    
    需要处理黑屏问题（母包已处理）
    """
    apk_path = r"C:\Users\Administrator\Desktop\com.euan.darkness_49b7cfd382.apk"
    app_version_code = 8
    app_version_name = "8.0"
    ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    singer_config = {"key_store": r"E:\work\keystore\leniu_oversea.keystore", "store_password": "leniu_oversea",
                     "key_password": "leniu_oversea", "alias": "com.ln.oversea", }
    """
    PA-繁體-包

    需要处理黑屏问题（检查母包是否已处理）
    """
    # apk_path = r"C:\Users\Administrator\Desktop\com.an.thechosen_9091d66f7c.apk"
    # app_version_code = 1
    # app_version_name = "1.0"
    # ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    # singer_config = {"key_store": r"E:\work\keystore\leniu_oversea.keystore", "store_password": "leniu_oversea",
    #                  "key_password": "leniu_oversea", "alias": "com.ln.oversea", }
    """
    九灵越南-二发包
    """
    # apk_path = r"C:\Users\Administrator\Desktop\vn.vplay.giangho.t011a_c72584e7c0.apk"
    # app_version_code = 18
    # app_version_name = "8.10"
    # ver_config = {"min_ver": 21, "tar_ver": 31, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "31"}
    # singer_config = {"key_store": r"C:/Users/Administrator/Desktop/vtvsdk.keystore", "store_password": "a@!23456*",
    #                  "key_password": "a@!23456*", "alias": "vlive", }

    """
    H5项目-谷歌包-繁体B
    
    """
    # apk_path = r"C:\Users\Administrator\Desktop\com.an.shanhai_21d1435007.apk"
    # app_version_code = 2
    # app_version_name = "2.0"
    # ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    # singer_config = {"key_store": r"E:\work\keystore\paai.keystore", "store_password": "ai123456",
    #                  "key_password": "ai123456", "alias": "com.paai.ln", }
    ##################################
    """
    H5项目-谷歌包-繁体A
    
    """
    # apk_path = r"C:\Users\Administrator\Desktop\com.jwdxz.gb_3fb4ec883b.apk"
    # app_version_code = 7
    # app_version_name = "7.0"
    # ver_config = {"min_ver": 21, "tar_ver": 33, "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name": "33"}
    # singer_config = {"key_store": r"E:\work\keystore\paai.keystore", "store_password": "ai123456",
    #                  "key_password": "ai123456", "alias": "com.paai.ln", }
    ##################################
    # apk_path = r"C:\Users\Administrator\Desktop\com.jygn.jqyau_51bd28d5f2.apk"
    # out_dir = os.path.abspath(os.path.dirname(apk_path))
    # app_version_code = 5
    # app_version_name = "1.4"
    # ver_config = {"min_ver": 21, "tar_ver": 31,
    #               "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name":"31"}
    # singer_config = {"key_store": r"E:\work\keystore\leniu_oversea_blade_origin_oriental.keystore", "store_password": "123456",
    #               "key_password": "123456", "alias": "com.leniu.blade_origin_oriental_fantasy", }
    ##################################
    # apk_path = r"C:\Users\Administrator\Desktop\jlsy_russia_google.apk"
    # out_dir = os.path.abspath(os.path.dirname(apk_path))
    # app_version_code = 9
    # app_version_name = "9.0"
    # ver_config = {"min_ver": 21, "tar_ver": 31,
    #               "ver_code": app_version_code, "ver_name": app_version_name, "compile_ver_name":"31"}
    # singer_config = {"key_store": r"E:\work\keystore\leniu_oversea.keystore", "store_password": "leniu_oversea",
    #               "key_password": "leniu_oversea", "alias": "com.ln.oversea", }
    out_dir = os.path.abspath(os.path.dirname(apk_path))
    output_path = os.path.join(out_dir, os.path.splitext(
        os.path.basename(apk_path))[0]+"_{0}.aab".format(app_version_name))
    Apk2Aab(apk_path, output_path, APKTOOL_PATH, AAPT_PATH,
            ANDROID_JAR_PATH, BUDNLE_TOOL_PATH, SMALI_PATH, ver_config, singer_config).start()
    # shutil.copytree(r"F:\python_project\apk2aab\cache\ca0c46edb58ec98e1cb0379ca5060770\depackage\unknown", r"F:\python_project\apk2aab\cache\ca0c46edb58ec98e1cb0379ca5060770\aab_project\base\root")
