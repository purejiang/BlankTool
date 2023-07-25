# -*- coding:utf-8 -*-

import os
import re
import traceback
from typing import Union
from common.cmd import CMD
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.j_loger import JLoger
from vo.apk_info import ApkInfo


class ApkManager():
    """

    @author: purejiang
    @created: 2022/7/14

    .apk 相关的功能管理

    """
    loger = JLoger()

    @classmethod
    def installApk(cls, apk_path, progress_callback):
        """
        安装 apk

        :param apk_path: apk 路径
        :param progress_callback: 执行进度

        """
        progress_callback(30, "开始安装 apk：" + apk_path, "", True)
        cmd_result = CMD.installApk(apk_path)
        cls.loger.info(cmd_result[1])
        progress_callback(90, "执行完成" , cmd_result[1], cmd_result[0])
        return cmd_result[0]

    @classmethod
    def parseApk(cls, apk_path, is_pass_dex, is_only_res, callback_progress)->Union[bool, None or ApkInfo]:
        """
        解析并反编译 APK 全流程

        :param apktool_path: apktool 路径
        :param apk_path: APK 路径
        :param is_pass_dex: 是否忽略错误的 dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有

        """
        # 第一步，初始化解析工具
        callback_progress(5, "开始执行" , "", True)    
        md5 = FileHelper.md5(apk_path)
        md5_name = "{0}_{1}".format(FileHelper.filename(apk_path, False), md5)
        info_file = os.path.join(
            Constant.Path.AAPT_INFO_CACHE_PATH, "{0}.info".format(md5_name))
        depack_output_dir = os.path.join(
            Constant.Path.PARSE_CACHE_PATH, md5_name)
        callback_progress(15, "初始化解析工具" , "", True)    

        # 第二步，通过 aapt 生成解析文件
        aapt_info_result = cls.__aapt_apk_info(apk_path, info_file)
        callback_progress(25, "AAPT 生成解析文件：" + info_file, aapt_info_result[1], aapt_info_result[0])
        if not aapt_info_result[0]:
            return False, None   

        # 第三步，解析文件中 APK 信息
        parse_apk_info_result = cls.__parse_apk_info(info_file, apk_path, depack_output_dir)
        callback_progress(35, "读取解析文件：" + info_file, "", parse_apk_info_result!=None)
        if parse_apk_info_result==None:
            return False, None
        
        # 第四步，反编译 APK
        depack_result = cls.__depackage(Constant.Re.APKTOOL_PATH, apk_path, depack_output_dir, is_pass_dex, is_only_res)
        callback_progress(55, "反编译 APK 到：" + depack_output_dir, depack_result[1], depack_result[0])
        if not depack_result[0]:
            return False, None
        
        # 第五步，keytool 分析 APK
        signer_info_result = cls.__parseSignerInfo(Constant.Re.KEYTOOL_PATH, depack_output_dir)
        if signer_info_result[0]:
            parse_apk_info_result.signer_sha1 = signer_info_result[1]
            parse_apk_info_result.signer_sha256 = signer_info_result[2]

        signer_md5_result = cls.__parseSignermd5(Constant.Re.KEYTOOL_PATH, depack_output_dir)
        if signer_md5_result[0]:
            parse_apk_info_result.signer_md5 = signer_md5_result[1]
        
        callback_progress(75, "keytool 分析 APK：" + apk_path, "{0}\n{1}".format(signer_info_result[1], signer_md5_result[1]), True)
        if not signer_info_result[0] and not signer_md5_result[0]:
            return False, None

        # 第六步，生成 APK 分析结果
        callback_progress(95, "生成 APK 分析结果", "", True)
        parse_apk_info_result.icon = cls.__parse_icon(depack_output_dir)
        parse_apk_info_result.md5 = md5
        return True, parse_apk_info_result
    
    @classmethod
    def repack(cls, repack_dir_path, output_apk_path, is_support_aapt2, ks_config, callback_progress):
        tmp_apk_path = os.path.join(FileHelper.parentDir(output_apk_path), "tmp_"+FileHelper.filename(output_apk_path))
        callback_progress(10, "开始执行重编译", "", True)
        # 第一步，重编译,生成未签名的 APK
        repack_tmp_apk_result = cls.__repack(Constant.Re.APKTOOL_PATH, repack_dir_path, tmp_apk_path, is_support_aapt2)
        callback_progress(30, "重编译，生成未签名 APK：" + output_apk_path, repack_tmp_apk_result[1], repack_tmp_apk_result[0])
        if not repack_tmp_apk_result[0]:
            cls.loger.info(repack_tmp_apk_result[1])
            return False
        
        # 第二步，重签名 APK
        sign_result = cls.__sign(Constant.Re.JARSIGNER_PATH, tmp_apk_path, output_apk_path, ks_config)
        callback_progress(60, "重签名 APK：" + output_apk_path, sign_result[1], sign_result[0])
        return sign_result[0]
        
    @classmethod
    def parseApkListInfo(cls, info_file):
        content = FileHelper.fileContent(info_file)
        apk_list = []
        pack_infos = content.strip("package:").replace(
            "\n", "").split("package:")
        for pack_info in pack_infos:
            apk_list.append(
                (pack_info.split(".apk=")[1], pack_info.split(".apk=")[0]+".apk"))
        return apk_list
    
    @classmethod
    def __parseSignermd5(cls, keytool_path, depack_path):
        msg=""
        signer_dir = os.path.join(depack_path, "original"+os.path.sep+"META-INF")
        md5_str = ""
        for file in FileHelper.getChild(signer_dir):
            if file.endswith(".RSA"):
                result = cls.__getSignerMd5(keytool_path, os.path.join(signer_dir, file))
                msg+="{}/n".format(result[1])
                if result[0]:
                    md5_str = result[1].split("(stdin)= ")[1]
                    return True, md5_str
        return False, msg
    
    @classmethod
    def __parseSignerInfo(cls, keytool_path, depack_path):
        msg=""
        signer_dir = os.path.join(depack_path, "original"+os.path.sep+"META-INF")
        sha1_str = ""
        sha256_str = ""
        for file in FileHelper.getChild(signer_dir):
            if file.endswith(".RSA"):
                result = cls.__getSignerInfo(keytool_path, os.path.join(signer_dir, file))
                msg+="{}/n".format(result[1])
                if result[0]:
                    sha1_list = re.findall("SHA1: (.*?)\n", result[1])
                    for sha1 in sha1_list:
                        if sha1!=None :
                            sha1_str += "{}\n".format(sha1)
                    sha256_list = re.findall("SHA256: (.*?)\n", result[1])
                    for sha256 in sha256_list:
                        if sha256!=None:
                            sha256_str+= "{}\n".format(sha256)
                    return (False, sha1_str, sha256_str)
        return (False, msg, "")

    @classmethod
    def __getSignerInfo(cls, keytool_path, rsa_path)->Union[bool, str]:
        """
        获取 rsa 文件的签名信息

        :param keytool_path: keytool 路径
        :param rsa_path: rsa 路径

        """
        cls.loger.info("keytool 获取 {0} 信息...".format(rsa_path))
        cmd_result = CMD.apkSignerByKeyTool(keytool_path, rsa_path)
        return cmd_result
    
    @classmethod
    def __getSignerMd5(cls, keytool_path, rsa_path)->Union[bool, str]:
        """
        获取 rsa 文件的签名md5

        :param keytool_path: keytool 路径
        :param rsa_path: rsa 路径

        """
        cls.loger.info("keytool 获取 {0} MD5...".format(rsa_path))
        cmd_result = CMD.apkSignerMd5ByKeyTool(keytool_path, rsa_path)
        return cmd_result
    
    @classmethod
    def __depackage(cls, apktool_path, apk_path, output_dir, is_pass_dex, is_only_res)->Union[bool, str]:
        """
        反编 apk

        :param apktool_path: apktool 路径
        :param apk_path: apk 路径
        :param output_dir: 反编后目录
        :param is_pass_dex: 是否忽略错误的 dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有

        """
        cls.loger.info("depackage {0} ...".format(apk_path))
        cmd_result = CMD.depackage(
            apktool_path, apk_path, output_dir, is_pass_dex, is_only_res)
        return cmd_result

    @classmethod
    def __aapt_apk_info(cls, apk_path, info_file_path)->Union[bool, str]:
        """
        获取本地的 apk 信息

        :param apk_path: apk 路径
        :param info_file_path: 输出信息的文件

        """
        cls.loger.info("aapt2 get {0}'s info ...".format(apk_path))
        cmd_result = CMD.apkInfoByAapt(apk_path, info_file_path)
        return cmd_result

    @classmethod
    def __repack(cls, apktool_path, dir_path, output_apk_path, is_support_aapt2):
        """
        重编译目录

        :param apktool_ver: apktool 版本
        :param dir_path: 需要重编的目录
        :param output_apk_path: 重编后输出的 apk 路径
        :param is_support_aapt2: 重编译过程中是否支持 aapt2, 默认不支持

        """
        cls.loger.info("repackage {0} ...".format(dir_path))
        cmd_result = CMD.repackage(apktool_path, dir_path, output_apk_path, is_support_aapt2)
        return cmd_result

    @classmethod
    def getApkListInfo(cls, info_file_path, is_sys):
        """
        获取手机上的 apk 列表

        :param info_file_path: 输出信息的文件
        :param is_sys: 是否只输出系统的应用

        """
        cls.loger.info("get all apks in phone...")
        cmd_result = CMD.inPhoneApkList(info_file_path, False, True, is_sys)
        return cmd_result

    @classmethod
    def getInphonePath(cls, package_name, info_file_path):
        """
        获取 apk 在手机上的安装目录

        :param package_name: 包名
        :param info_file_path: 输出信息的文件

        """
        cls.loger.info("get {0}'s path ...".format(package_name))
        cmd_result = CMD.inPhonePath(package_name, info_file_path)
        return cmd_result

    @classmethod
    def pullApk(cls, in_phone_path, target_path):
        """
        通过 adb 命令将指定路径下的 apk 拉到 pc

        :param package_name: 包名

        """
        cls.loger.info("pull apk ...")
        cmd_result = CMD.pullApk(in_phone_path, target_path)
        return cmd_result

    @classmethod
    def __sign(cls, signer_path, origin_apk_path, output_apk_path, signer_config):
        """
        对 apk 签名

        :param apk_path: 未签名的 apk 路径
        :param out_path: 签名后的 apk 输出的路径
        :param signer_config: 签名信息

        """
        cls.loger.info("sign {0} ...".format(origin_apk_path))
        cmd_result = CMD.signApk(signer_path, origin_apk_path, output_apk_path, signer_config)
        return cmd_result

    @classmethod
    def __parse_apk_info(cls, info_file, apk_path, depackage_path)->None or ApkInfo:
        def get_value(info_content, target_property):
            try:
                return info_content.split(target_property)[1:][0].split("'")[1:2][0]
            except Exception as e:
                cls.loger.warning("exce:\n{0}".format(traceback.format_exc()))
                return ""

        def get_list(info_content, target_property, last_tag):
            try:
                content = info_content.split(target_property)[1:][0]
                if last_tag != "":
                    content = content.split(last_tag)[:1][0]
                return content.replace("'", "").strip().replace(" ", ", ")
            except Exception as e:
                cls.loger.warning("exce:\n{0}".format(traceback.format_exc()))
                return ""
            
        content = FileHelper.fileContent(info_file)
        app_name = get_value(content, "application: label=")
        apk_icon = os.path.join(depackage_path, get_value(content, "icon="))
        package_name = get_value(content, "package: name=")
        version_code = get_value(content, "versionCode=")
        version_name = get_value(content, "versionName=")
        min_version = get_value(content, "sdkVersion:")
        target_version = get_value(content, "targetSdkVersion:")
        abis = get_list(content, "native-code:", "\n")
        langs = get_list(content, "locales:", "\n")
        return ApkInfo(apk_path, app_name, apk_icon, package_name, version_code, version_name, target_version, min_version, abis, langs, depackage_path)

        
    @classmethod
    def __parse_icon(cls, depack_path):
        content = FileHelper.fileContent(
            os.path.join(depack_path, "AndroidManifest.xml"))
        # 非贪婪模式，取第一个
        icon_name_list = re.findall("android:icon=\"(.*?)\"", content)
        try:
            if len(icon_name_list) > 0:
                icon_name = icon_name_list[0].split("/")[1]
            res_dir_name = icon_name_list[0].split("/")[0].replace("@", "")
            res_dir_list = []
            for res_dir in FileHelper.getChild(os.path.join(depack_path, "res"), FileHelper.TYPE_DIR):
                if res_dir_name in res_dir:
                    res_dir_list.append(res_dir)
            for file in FileHelper.getChild(res_dir_list[-1], FileHelper.TYPE_FILE):
                if icon_name in file and (FileHelper.getSuffix(file) == ".png" or FileHelper.getSuffix(file) == ".jpg"):
                    return os.path.abspath(file)
        except Exception as e:
            return None
