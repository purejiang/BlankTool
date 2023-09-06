# -*- coding: utf-8 -*-
from typing import Union

from .base_cmd import BaseCMD

class BundleCMD(BaseCMD):

    @classmethod
    def compileZip(cls, res_dir, output_zip):
        """
        aapt2 编译资源目录到zip

        :param aapt2: aapt2
        :param res_dir: 资源目录，res
        :param output_zip: 输出的zip文件

        [ aapt2 文件] compile --dir [ res 路径] -o [生成资源的 zip ]
        """
        win_cmd = "aapt2 compile --dir {0} -o {1}".format(res_dir, output_zip)
        linux_cmd=""
        mac_cmd=""
        return cls.run(win_cmd, linux_cmd, mac_cmd)
    
    @classmethod
    def linkRes(cls, zip_path, android_jar, manifest_file, min_ver, target_ver, compile_ver, ver_code, ver_name, output_base_apk):
        """
        链接资源(AAPT2 会将各种编译后的资源链接到一个 APK 中)

        :param zip_path: 资源的 .zip
        :param output_base_apk: 输出的 base.apk 路径
        :param android_jar: android.jar 文件
        :param manifest_file: manifest 文件
        :param min_ver: 最小版本
        :param target_ver: 目标版本
        :param ver_code: 版本号
        :param ver_name: 版本名

        [ aapt2 文件] link --proto-format [资源的 zip ] -o [输出的 base.apk] -I [ android.jar 文件] --manifest [ manifest 文件] --min-sdk-version [最小版本] --target-sdk-version [目标版本] --version-code [版本号] --version-name [版本名]
        """
        win_cmd = "aapt2 link --proto-format \"{0}\" -o \"{1}\" -I \"{2}\" --manifest \"{3}\" --min-sdk-version {4} --target-sdk-version {5} --version-code {6} --version-name {7}".format( 
             zip_path, output_base_apk, android_jar, manifest_file, min_ver, target_ver, ver_code, ver_name)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def linkResByDir(cls, android_jar, manifest_file, output_base_apk):
        """
        链接资源(AAPT2 会将各种编译后的资源链接到一个 APK 中)
        :param aapt2: aapt2
        :param output_base_apk: 输出的 base.apk
        :param manifest_file: 文件
        :param android_jar: android.jar

        [ aapt2 文件] link --proto-format [资源的 dir ] -o [输出的 base.apk] -I [ android.jar 文件] --auto-add-overlay
        """
        win_cmd = "aapt2 link --proto-format -o {0} -I {1} --manifest {2} --auto-add-overlay".format(
             output_base_apk, android_jar, manifest_file)
        linux_cmd=""
        mac_cmd=""
        return cls.run(win_cmd, linux_cmd, mac_cmd)

    @classmethod
    def signBundle(cls, signer_tool, aab_file, keystore, store_password, key_password, alias):
        """
        签名aab

        jarsigner -digestalg SHA1 -sigalg SHA1withRSA -keystore [keystore 文件] -storepass [store password] -keypass [key password] [aab 文件] [store alias]
        """
        win_cmd = "{0} -digestalg SHA1 -sigalg SHA1withRSA -keystore {1} -storepass {2} -keypass {3} {4} {5}".format(
            signer_tool, keystore, store_password, key_password, aab_file, alias)
        linux_cmd=""
        mac_cmd=""
        return cls.run(win_cmd, linux_cmd, mac_cmd)


    @classmethod
    def smali2dex(cls, smali_jar_path, smali_dir, dex_path):
        """
        smali 文件夹转 .dex 文件

        :param smali_jar_path: smali.jar 路径
        :param dex_path: 输出的 .dex 文件
        :param smali_dir: smali 文件夹

        java -jar [ smali.jar ] assemble -o [ .dex 文件] [ smali 文件夹]
        """
        all_cmd = "java -jar \"{0}\" assemble -o \"{1}\" \"{2}\"".format(
            smali_jar_path, dex_path, smali_dir)
        return cls.run(all_cmd, all_cmd, all_cmd)

    @classmethod
    def buildBundle(cls, bundle_tool_path, base_zip, output_aab):
        """
        构建 appbundle 

        :param bundle_tool_path: bundletool.jar 路径
        :param base_zip:  base.zip 文件
        :param output_aab:  输出的 .aab 

        java -jar [ bundletool.jar ] build-bundle --modules [ base.zip 文件] --output=[输出的 .aab ]
        """
        all_cmd = "java -jar \"{0}\" build-bundle --modules \"{1}\" --output=\"{2}\"".format(
            bundle_tool_path, base_zip, output_aab)
        return cls.run(all_cmd, all_cmd, all_cmd)
    
    @classmethod
    def gradleBundle(cls):
        """
        Gradle 打包

        win: gradle.bat bundle
        linux: gradle bundle
        
        """
        all_cmd = "gradle bundleRelease"
        return cls.run(all_cmd, all_cmd, all_cmd)

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
            keystore_str = " --ks=\"{0}\" --ks-pass=pass:{1} --ks-key-alias={2} --key-pass=pass:{3}".format(
                keystore_config["store_file"], keystore_config["store_password"], keystore_config["key_alias"], keystore_config["key_password"])
        all_cmd = "java -jar \"{0}\" build-apks --bundle \"{1}\" --output \"{2}\" {3}".format(
            bundletool_path, aab_path, output_apks_path, keystore_str)
        return cls.run(all_cmd, all_cmd, all_cmd)

    @classmethod
    def installApks(cls, bundletool_path, apks_path):
        """
        安装 .apks

        :param bundletool_path: bundletool 文件路径
        :param apks_path: apks 文件路径

        java -jar [ bundletool 文件] install-apks --apks [ .apks 文件]  --adb= [ .adb 文件]
        """
        all_cmd = "java -jar \"{0}\" install-apks --apks \"{1}\"".format(
            bundletool_path, apks_path)
        return cls.run(all_cmd, all_cmd, all_cmd)

    @classmethod
    def compileZip(cls, res_path, output_zip_path):
        """
        将资源编译为 zip

        :param aapt2_path: aapt2 文件路径
        :param res_path: 资源文件夹
        :param output_zip_path: 生成资源的 zip

        [ aapt2 文件] compile --dir [ res 路径] -o [生成资源的 .zip ]
        """
        win_cmd = "aapt2 compile --dir \"{0}\" -o \"{1}\"".format(
             res_path, output_zip_path)
        linux_cmd = ""
        mac_cmd = ""
        return cls.run(win_cmd, linux_cmd, mac_cmd)