# -*- coding: utf-8 -*-

import os
import platform
import subprocess
import traceback


class CMD(object):
    """

    @author: purejiang
    @created: 2021/8/25

    命令行工具集

    """
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
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)

    ########################### apk 相关 ###############################################
    @classmethod
    def depackage(cls, apktool_path, apk_path, output_dir, is_pass_dex=False, is_only_res=False):
        """
        反编 .apk

        :param apktool_path: apktool 路径
        :param apk_path: .apk 路径
        :param output_dir: 反编后目录
        :param is_pass_dex: 是否忽略错误的 .dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有

        java -jar [ apktool 文件] [-s (可选)] d [--only -main-classes (可选)] [需要反编的 .apk 文件] -o [反编后输出的目录]
        """
        if os.path.exists(output_dir):
            return True, "dir is exist: {0}".format(output_dir)
        pass_dex = ""
        if is_pass_dex:
            pass_dex = " --only -main-classes"
        s = ""
        if is_only_res:
            s = " -s"
        all_cmd = "java -jar {0}{1} d{2} {3} -o {4}".format(
            apktool_path, s, pass_dex, apk_path, output_dir)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def repackage(cls, apktool_path, dir_path, output_apk_path, is_support_aapt2=False):
        """
        重编译目录

        :param apktool_path: apktool 路径
        :param dir_path: 需要重编的目录
        :param output_apk_path: 重编后输出的 .apk 路径
        :param is_support_aapt2: 重编译过程中是否支持 aapt2, 默认不支持

        java -jar [ apktool 文件] b [--use-aapt2 (可选)] [需要重编的目录] -f -o [重编后的 .apk 路径]
        """
        if os.path.exists(output_apk_path):
            return False, "apk is exist: {0}".format(output_apk_path)
        aapt2 = ""
        if is_support_aapt2:
            aapt2 = " --use-aapt2"
        all_cmd = "java -jar {0} b{1} {2} -f -o {3}".format(
            apktool_path, aapt2, dir_path, output_apk_path)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def apk2jarByenjarify(cls, enjarify_path, apk_path, output_jar_path):
        """
        反编 apk 为 jar（使用 enjarify）

        :param enjarify_path: enjarify 工具的路径
        :param apk_path: .apk 文件路径
        :param output_jar_path: 输出的 .jar 路径

        python [ enjarify 的 debug.py 文件] -o [ .jar 输出路径] [源 .apk 文件]
        """
        if os.path.exists(output_jar_path):
            return False, "jar is exist: {0}".format(output_jar_path)
        all_cmd = "python {0}/debug.py -o {1} {2}".format(
            enjarify_path, output_jar_path, apk_path)
        
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def dex2jarByd2j(cls, dex2jar_path, dexs_list, output_jar_path):
        """
        反编 .dex 为 .jar（使用 dex2jar）

        :param dex2jar_path: dex2jar 工具的路径
        :param dexs_list: 单个或多个 .dex 的文件列表
        :param jar_path: 输出的 .jar 路径

        win: d2j-dex2jar.bat [ .dex 文件] -o [ .jar 输出路径]
        linux: d2j-dex2jar [ .dex 文件] -o [ .jar 输出路径]
        """
        result = False
        msg = ""
        if os.path.exists(output_jar_path):
            return False, "jar is exist: {0}".format(output_jar_path)
        for dex_path in dexs_list:
            win_cmd = "{0}/d2j-dex2jar.bat {1} -o {2}".format(
                dex2jar_path, dex_path, output_jar_path)
            linux_cmd = "{0}/d2j-dex2jar {1} -o {2} ".format(
                dex2jar_path, dex_path, output_jar_path)
            mac_cmd = ""
            cmd_result = cmdBySystem(win_cmd, linux_cmd, mac_cmd)
            result = result & cmd_result[0]
            msg += (cmd_result[1])
        return result, msg

    @classmethod
    def apk2jarByd2j(cls, dex2jar_path, apk_path, output_jar_path):
        """
        反编 .apk 为 .jar（使用 dex2jar）

        :param apk_path: .apk 路径
        :param output_jar_path:输出的 .jar 路径

        win: d2j-dex2jar.bat [源 .apk 文件] -o [ .jar 输出路径]
        linux: d2j-dex2jar [源 .apk 文件] -o [ .jar 输出路径]
        """
        if os.path.exists(output_jar_path):
            return False, "jar is exist: {0}".format(output_jar_path)
        win_cmd = "{0}/d2j-dex2jar.bat {1} -o {2}".format(
            dex2jar_path, apk_path, output_jar_path)
        linux_cmd = "{0}/d2j-dex2jar {1} -o {2} ".format(
            dex2jar_path, apk_path, output_jar_path)
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def gradleAssemble(cls, gradle_bin_path):
        """
        Gradle 打包

        :param gradle_bin_path: gradle 路径下的 bin 目录

        win: gradle.bat assembleRelease
        linux: gradle assembleRelease

        """
        win_cmd = "{0}/gradle.bat assembleRelease".format(gradle_bin_path)
        linux_cmd = "{0}/gradle assembleRelease".format(gradle_bin_path)
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def signApk(cls,jarsigner_path, kwargs):
        """
        jarsigner 签名

        :param kwargs: 签名配置

        """
        win_cmd = "{0} -keystore {1} -storepass {2} -keypass {3} -digestalg SHA1 -sigalg MD5withRSA -signedjar {4} {5} {6}".format(
            jarsigner_path, kwargs['ks_path'], kwargs['ksw'], kwargs['kw'], kwargs['final_apk'], kwargs['new_apk'], kwargs['kalias'])
        linux_cmd = ""
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def installApk(cls, apk_path):
        """
        安装 .apk

        :param apk_path: 需要安装的 .apk 文件路径

        adb install xxx.apk
        """
        all_cmd = "adb install {0}".format(apk_path)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def apkInfoByAapt(cls, apk_path, info_file_path):
        """
        aapt 获取 apk 信息

        :param apk_path: 需要获取信息的 .apk 文件路径
        :param info_file_path: 存储信息的文件路径

        aapt dump badging xxx.apk
        """
        if os.path.exists(info_file_path):
            return True, "info file is exist: {0}".format(info_file_path)
        win_cmd = "aapt2 dump badging {0} >> {1}".format(apk_path, info_file_path)
        linux_cmd = ""
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def apkInPhone(cls, info_file_path, is_install, is_path, is_sys):
        """
        adb 获取手机上的包名列表

        :param info_file_path: 存储信息的文件路径

        adb shell pm list packages [-i 可选，附加安装来源（会有报错）] [-f 可选，附加安装路径] [-s / -3 可选，输出系统包/输出第三方包]
        """
        if os.path.exists(info_file_path):
            return True, "info file is exist: {0}".format(info_file_path)
        win_cmd = "adb shell pm list packages >> {0}".format(info_file_path)
        linux_cmd = ""
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def apkInfoInPhone(cls, info_file_path):
        """
        adb 获取手机上的信息

        :param info_file_path: 存储信息的文件路径

        adb shell dumpsys package [packages 可选，包体信息] 
        """
        if os.path.exists(info_file_path):
            return True, "info file is exist: {0}".format(info_file_path)
        win_cmd = "adb shell dumpsys package packages >> {0}".format(info_file_path)
        linux_cmd = ""
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def apkInPhone(cls, package_name, info_file_path):
        """
        获取 apk 在手机上的安装目录


        :param pakcage_name: 包名
        :param info_file_path: 存储信息的文件路径

        adb shell pm path [包名]
        """
        if os.path.exists(info_file_path):
            return True, "info file is exist: {0}".format(info_file_path)
        win_cmd = "adb shell pm path {0} >> {1}".format(package_name, info_file_path)
        linux_cmd = ""
        mac_cmd = ""
        return cmdBySystem(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def pullApk(cls, in_phone_path, target_path):
        """
        通过 adb 命令将手机路径下的 apk 导出到指定路径

        :param in_phone_path: .apk 在手机内的路径
        :param target_path: 导出的目录

        """
        all_cmd = "adb pull {0} {1}".format(in_phone_path, target_path)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)
        
    ########################### aab 相关 ###############################################
    @classmethod
    def gradleBundle(cls):
        """
        Gradle 打包

        win: gradle.bat bundle
        linux: gradle bundle
        
        """
        all_cmd = "gradle bundleRelease"
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def aab2Apks(cls, bundletool_path, aab_path, output_apks_path, keystore_config=None):
        """
        .aab 转 .apks

        :param aab_path: aab 文件路径
        :param bundletool_path: bundletool 文件路径
        :param keystore_config: keystore 配置

        java -jar [ bundletool 文件] build-apks --bundle [ .aab 文件] --output [ .apks 文件]
            --ks=[签名文件]
            --ks-pass=pass:[签名密码]
            --ks-key-alias=[别名]
            --key-pass=pass:[别名密码]
        """

        keystore_str = ""
        if keystore_config:
            keystore_str = " --ks={0} --ks-pass=pass:{1} --ks-key-alias={2} --key-pass=pass:{3}".format(
                keystore_config["store_file"], keystore_config["store_password"], keystore_config["key_alias"], keystore_config["key_password"])
        all_cmd = "java -jar {0} build-apks --bundle {1} --output {2}{3}".format(
            bundletool_path, aab_path, output_apks_path, keystore_str)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def installApks(cls, bundletool_path, apks_path):
        """
        安装 .apks

        :param bundletool_path: bundletool 文件路径
        :param apks_path: apks 文件路径

        java -jar [ bundletool 文件] install-apks --apks [ .apks 文件]  --adb= [ .adb 文件]
        """
        all_cmd = "java -jar {0} install-apks --apks {1}".format(
            bundletool_path, apks_path)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def compileZip(cls, res_path, output_zip_path):
        """
        将资源编译为 zip

        :param aapt2_path: aapt2 文件路径
        :param res_path: 资源文件夹
        :param output_zip_path: 生成资源的 zip

        [ aapt2 文件] compile --dir [ res 路径] -o [生成资源的 .zip ]
        """
        all_cmd = "aapt2 compile --dir {0} -o {1}".format(
             res_path, output_zip_path)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def linkRes(cls, zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name):
        """
        链接资源(AAPT2 会将各种编译后的资源链接到一个 APK 中)

        :param zip_path: 资源的 .zip
        :param base_apk_path: 输出的 base.apk 路径
        :param android_jar: android.jar 文件
        :param manifest_file: manifest 文件
        :param min_ver: 最小版本
        :param target_ver: 目标版本
        :param ver_code: 版本号
        :param ver_name: 版本名

        [ aapt2 文件] link --proto-format [资源的 zip ] -o [输出的 base.apk] -I [ android.jar 文件] --manifest [ manifest 文件] --min-sdk-version [最小版本] --target-sdk-version [目标版本] --version-code [版本号] --compile-sdk-version-name [版本名]
        """
        all_cmd = "aapt2 link --proto-format {0} -o {1} -I {2} --manifest {3} --min-sdk-version {4} --target-sdk-version {5} --version-code {6} --compile-sdk-version-name {7}".format(
             zip_path, base_apk_path, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name)

        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def smali2dex(cls, smali_jar_path, dex_path, smali_dir):
        """
        smali 文件夹转 .dex 文件

        :param smali_jar_path: smali.jar 路径
        :param dex_path: 输出的 .dex 文件
        :param smali_dir: smali 文件夹

        java -jar [ smali.jar ] assemble -o [ .dex 文件] [ smali 文件夹]
        """
        all_cmd = "java -jar {0} assemble -o {1} {2}".format(
            smali_jar_path, dex_path, smali_dir)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)

    @classmethod
    def buildBundle(cls, bundle_tool_path, base_zip, output_aab):
        """
        构建 appbundle 

        :param bundle_tool_path: bundletool.jar 路径
        :param base_zip:  base.zip 文件
        :param output_aab:  输出的 .aab 

        java -jar [ bundletool.jar ] build-bundle --modules [ base.zip 文件] --output=[输出的 .aab ]
        """
        all_cmd = "java -jar {0} build-bundle --modules {1} --output={2}".format(
            bundle_tool_path, base_zip, output_aab)
        return cmdBySystem(all_cmd, all_cmd, all_cmd)


def cmdBySystem(win_cmd, linux_cmd, mac_cmd):
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
            return False, cmd+"\n"+"cmd not support this system"
        process = subprocess.check_output(cmd, shell=True)
        return True, cmd+"\n"+"cmd_result:\n"+process.decode(encoding='gbk')
    except Exception as e:
        return False, cmd+"\nexce:\n"+traceback.format_exc()


if __name__ == "__main__":
    # cmd = r"F:\Local\Programs\Python\Python37\DLLs\Scripts\virtualenv.exe"
    # sys.executable = ("F:\Local\Programs\Python\Python37\python.exe")
    # print(sys.executable)
    # cmdBySystem(cmd, cmd, "error")
    pass
