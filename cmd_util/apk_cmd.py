# -*- coding: utf-8 -*-
from typing import Union

from .base_cmd import BaseCMD

class ApkCMD(BaseCMD):
    
    @classmethod
    def aaptApkInfo(cls, apk_path, output_info_file)->Union[bool, str]:        
        """
        aapt 获取 apk 信息

        :param apk_path: 需要获取信息的 .apk 文件路径
        :param output_info_file: 存储信息的文件路径

        aapt dump badging xxx.apk
        """
        win_cmd = "aapt2 dump badging \"{0}\" >> \"{1}\"".format(apk_path, output_info_file)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def getSignerInfo(cls, keytool_path, rsa_path)->Union[bool, str]:
        """
        通过 keytool 获取 apk 的签名信息

        :param keytool_path: keytool 路径
        :param rsa_path: .RSA 文件路径

        win: keytool.exe -printcert (-jarfile [.apk 文件] | -file [RSA 文件])
        linux: keytool -printcert (-jarfile [.apk 文件] | -file [RSA 文件])

        """
        all_cmd = "\"{0}\" -printcert -file \"{1}\"".format(keytool_path, rsa_path)
        return cls.run(all_cmd, all_cmd, all_cmd)
    
    @classmethod
    def getSignerMd5(cls, keytool_path, rsa_path)->Union[bool, str]:
        """
        通过 keytool 获取 apk 的签名md5

        :param keytool_path: keytool 路径
        :param rsa_path: .RSA 文件路径

        win: keytool.exe -printcert (-jarfile [.apk 文件] | -file [RSA 文件]) | openssl dgst -md5 
        linux: keytool -printcert (-jarfile [.apk 文件] | -file [RSA 文件]) | openssl dgst -md5 

        """
        all_cmd = "\"{0}\" -printcert -file \"{1}\" | openssl dgst -md5 ".format(keytool_path, rsa_path)
        return cls.run(all_cmd, all_cmd, all_cmd)
    
    @classmethod
    def depackage(cls, apktool_path, apk_path, output_dir, is_pass_dex, is_only_res)->Union[bool, str]:
        """
        反编 .apk

        :param apktool_path: apktool 路径
        :param apk_path: .apk 路径
        :param output_dir: 反编后目录
        :param is_pass_dex: 是否忽略错误的 .dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有

        java -jar [ apktool 文件] [-s (可选)] d [--only-main-classes (可选)] [需要反编的 .apk 文件] -o [反编后输出的目录]
        """
        pass_dex = ""
        if is_pass_dex:
            pass_dex = " --only -main-classes"
        
        s = ""
        if is_only_res:
            s = " -s"
        all_cmd = "java -jar \"{0}\"{1} d{2} \"{3}\" -o \"{4}\"".format(
            apktool_path, s, pass_dex, apk_path, output_dir)
        return cls.run(all_cmd, all_cmd, all_cmd)

    @classmethod
    def repack(cls, apktool, origin_dir, output_apk, is_support_aapt2):
        """
        重编译目录

        :param apktool: apktool 路径
        :param origin_dir: 需要重编的目录
        :param output_apk: 重编后输出的 .apk 路径
        :param is_support_aapt2: 重编译过程中是否支持 aapt2, 默认不支持

        java -jar [ apktool 文件] b [--use-aapt2 (可选)] [需要重编的目录] -f -o [重编后的 .apk 路径]
        """
        aapt2 = ""
        if is_support_aapt2:
            aapt2 = " --use-aapt2"
        all_cmd = "java -jar \"{0}\" b{1} \"{2}\" -f -o \"{3}\"".format(
            apktool, aapt2, origin_dir, output_apk)
        return cls.run(all_cmd, all_cmd, all_cmd)

    @classmethod
    def signV1(cls, jarsigner, origin_apk, output_apk, signer_config):
        """
        jarsigner 签名

        :param kwargs: 签名配置 ['ks_path'], ['ksw'], ['kw'], ['final_apk'], ['new_apk'], ['kalias']

        """
        win_cmd = "\"{0}\" -keystore \"{1}\" -storepass \"{2}\" -keypass \"{3}\" -digestalg SHA1 -sigalg MD5withRSA -signedjar \"{4}\" \"{5}\" \"{6}\"".format(
            jarsigner, signer_config["signer_file_path"], signer_config["signer_pwd"], signer_config["signer_key_pwd"], output_apk, origin_apk, signer_config["signer_alias"])
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def signV2(cls, apksigner, origin_apk, output_apk, signer_config):
        """
        apksigner 签名

        :param kwargs: 签名配置 ['ks_path'], ['ksw'], ['kw'], ['final_apk'], ['new_apk'], ['kalias']

        java -jar [APKSIGNER_PATH] -v --out [SAVED_APK_PATH] --ks [KEYSTORE_PATH] --ks-pass pass:[KS_PASS] --key-pass pass:[KEY_PASS] --ks-key-alias [ALIAS_NAME] [APK_FILE_PATH]

        """
        win_cmd = "java -jar \"{0}\" sign -v --out \"{1}\" --ks \"{2}\" --ks-pass pass:\"{3}\" --key-pass pass:\"{4}\" --ks-key-alias \"{5}\" \"{6}\"".format(
            apksigner, output_apk, signer_config["signer_file_path"], signer_config["signer_pwd"], signer_config["signer_key_pwd"], signer_config["signer_alias"], origin_apk)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
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
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def apk2jarByenjarify(cls, enjarify_path, apk_path, output_jar_path):
        """
        反编 apk 为 jar（使用 enjarify）

        :param enjarify_path: enjarify 工具的路径
        :param apk_path: .apk 文件路径
        :param output_jar_path: 输出的 .jar 路径

        python [ enjarify 的 debug.py 文件] -o [ .jar 输出路径] [源 .apk 文件]
        """
        all_cmd = "python {0}/debug.py -o \"{1}\" \"{2}\"".format(
            enjarify_path, output_jar_path, apk_path)
        
        return cls.run(all_cmd, all_cmd, all_cmd)

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
        for dex_path in dexs_list:
            win_cmd = "{0}/d2j-dex2jar.bat \"{1}\" -o \"{2}\"".format(
                dex2jar_path, dex_path, output_jar_path)
            linux_cmd = "{0}/d2j-dex2jar \"{1}\" -o \"{2}\"".format(
                dex2jar_path, dex_path, output_jar_path)
            mac_cmd = ""
            cmd_result = cls.run(win_cmd, linux_cmd, mac_cmd)
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
        win_cmd = "{0}/d2j-dex2jar.bat \"{1}\" -o \"{2}\"".format(
            dex2jar_path, apk_path, output_jar_path)
        linux_cmd = "{0}/d2j-dex2jar \"{1}\" -o \"{2}\"".format(
            dex2jar_path, apk_path, output_jar_path)
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
