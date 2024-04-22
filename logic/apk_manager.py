# -*- coding:utf-8 -*-

import os
import re
import traceback
from typing import Union
from cmd_util.adb_cmd import AdbCMD
from cmd_util.apk_cmd import ApkCMD
from common.config import UserConfig
from common.context import Context
from utils.file_helper import FileHelper
from utils.jlogger import JLogger
from utils.other_util import currentTimeMillis, currentTimeNumber
from vo.apk_info import ApkInfo
from vo.signer import SignerConfig


class ApkManager():
    """

    @author: purejiang
    @created: 2022/7/14

    .apk 相关的功能管理

    """
    @classmethod
    def installApk(cls, apk_path, progress_callback):
        """
        安装 apk

        :param apk_path: apk 路径
        :param progress_callback: 执行进度

        """
        logger = JLogger(log_name="install_apk_{0}.log".format(currentTimeNumber()), save_file=True)
        progress_callback(30, "开始安装 apk：" + apk_path, "", True)
        cmd_result = AdbCMD.adbInstallApk(apk_path, Context.DEFAULT_ADB_DEVICE)
        logger.info(cmd_result[1])
        progress_callback(90, "执行完成" , cmd_result[1], cmd_result[0])
        return cmd_result[0]

    @classmethod
    def parseApk(cls, apk_path, is_pass_dex, is_only_res, progress_callback)->Union[bool, None or ApkInfo]:
        """
        解析并反编译 APK 全流程

        :param apktool_path: apktool 路径
        :param apk_path: APK 路径
        :param is_pass_dex: 是否忽略错误的 dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有

        """
        user_path_config = UserConfig.getPath()

        logger = JLogger(log_name="parse_apk_{0}.log".format(currentTimeNumber()), save_file=True)
        # 第一步，初始化解析工具
        progress_callback(5, "开始执行" , "", True)    
        md5 = FileHelper.md5(apk_path)
        md5_name = "{0}_{1}".format(FileHelper.filename(apk_path, False), md5)
        info_file = os.path.join(user_path_config.aapt_cache, "{0}.info".format(md5_name))
        depack_output_dir = os.path.join(user_path_config.parse_apk_cache, md5_name)
        progress_callback(15, "初始化解析工具完成" , "", True)    

        # 第二步，通过 aapt 生成解析文件
        aapt_info_result = ApkCMD.aaptApkInfo(apk_path, info_file)
        logger.info("cmd:"+aapt_info_result[2]+", result:"+aapt_info_result[1])
        progress_callback(25, "AAPT 生成解析文件：" + info_file, aapt_info_result[1], aapt_info_result[0])
        if not aapt_info_result[0]:
            return False, None   

        # 第三步，解析文件中 APK 信息
        parse_apk_info_result = cls.parseApkInfo(info_file, apk_path, depack_output_dir, logger)
        progress_callback(35, "读取解析文件：" + info_file, "", parse_apk_info_result!=None)
        if parse_apk_info_result==None:
            return False, None
        
        # 第四步，反编译 APK
        depack_result = ApkCMD.depackage(user_path_config.apktool, apk_path, depack_output_dir, is_pass_dex, is_only_res,)
        logger.info("cmd:"+depack_result[2]+", result:"+depack_result[1])
        progress_callback(55, "反编译 APK 到：" + depack_output_dir, depack_result[1], depack_result[0])
        if not depack_result[0]:
            return False, None
        
        # 第五步，keytool 分析 APK
        signer_info_result = cls.parseSignerInfo(user_path_config.keytool, depack_output_dir, logger)
        if signer_info_result[0]:
            parse_apk_info_result.signer_sha1 = signer_info_result[1]
            parse_apk_info_result.signer_sha256 = signer_info_result[2]

        signer_md5_result = cls.parseSignermd5(user_path_config.keytool, depack_output_dir, logger)
        if signer_md5_result[0]:
            parse_apk_info_result.signer_md5 = signer_md5_result[1]
        
        progress_callback(75, "keytool 分析 APK：" + apk_path, "{0}\n{1}".format(signer_info_result[1], signer_md5_result[1]), True)
        if not signer_info_result[0] and not signer_md5_result[0]:
            return False, None

        # 第六步，生成 APK 分析结果
        progress_callback(95, "生成 APK 分析结果", "", True)
        parse_apk_info_result.icon = cls.getIcon(depack_output_dir, logger)
        parse_apk_info_result.md5 = md5
        return True, parse_apk_info_result
    
    @classmethod
    def repack(cls, repack_dir_path, output_apk, is_support_aapt2, signer_version, signer_config:SignerConfig, progress_callback):
        user_path_config = UserConfig.getPath()
        logger = JLogger(log_name="repack_{0}.log".format(currentTimeNumber()), save_file=True)
        tmp_apk = os.path.join(FileHelper.parentDir(output_apk), "tmp_"+FileHelper.filename(output_apk))
        # 第一步，清理工作空间
        progress_callback(0, "清理工作空间", "", True)
        if FileHelper.fileExist(tmp_apk):
            FileHelper.delFile(tmp_apk)
            logger.info("del file:"+tmp_apk)
        if FileHelper.fileExist(output_apk):
            FileHelper.delFile(output_apk)
            logger.info("del file:"+output_apk)

       # 第二步，重编译,生成未签名的 APK     
        repack_tmp_apk_result = ApkCMD.repack(user_path_config.apktool, repack_dir_path, tmp_apk, is_support_aapt2)
        logger.info("cmd:"+repack_tmp_apk_result[2]+", result:"+repack_tmp_apk_result[1])
        progress_callback(40, "重编译，生成未签名 APK：" + output_apk, repack_tmp_apk_result[1], repack_tmp_apk_result[0])
        if not repack_tmp_apk_result[0]:
            logger.info(repack_tmp_apk_result[1])
            return False
        
        # 第三步，重签名 APK
        sign_result = cls.__signApk(tmp_apk, output_apk, signer_config, signer_version, logger)
        progress_callback(70, "重签名 APK：" + output_apk, sign_result[1], sign_result[0])
        logger.info("signer_version:"+signer_version+",cmd:"+sign_result[2]+", result:"+sign_result[1])
        return sign_result[0]

    
    @classmethod
    def signApk(cls, origin_apk, output_apk, signer_version, signer_config:SignerConfig, progress_callback):
        logger = JLogger(log_name="repack_{0}.log".format(currentTimeNumber()), save_file=True)
        tmp_apk = os.path.join(FileHelper.parentDir(output_apk), "tmp_"+FileHelper.filename(output_apk))
        
        # 第一步，清理工作空间
        progress_callback(0, "清理工作空间", "", True)
        if FileHelper.fileExist(tmp_apk):
            FileHelper.delFile(tmp_apk)
            logger.info("del file:"+tmp_apk)
        if FileHelper.fileExist(output_apk):
            FileHelper.delFile(output_apk)
            logger.info("del file:"+output_apk)
        
        FileHelper.copyFile(origin_apk, tmp_apk, True)
        
        # 第二步，重签名 APK
        sign_result = cls.__signApk(tmp_apk, output_apk, signer_config, signer_version, logger)
        progress_callback(70, "重签名 APK：" + output_apk, sign_result[1], sign_result[0])
        logger.info("signer_version:"+signer_version+",cmd:"+sign_result[2]+", result:"+sign_result[1]+", bool:"+str(sign_result[0]))
        return sign_result[0]

    @classmethod
    def __signApk(cls, origin_apk, output_apk, signer_config, signer_version, logger):
        user_path_config = UserConfig.getPath()

        signer_config_dict={}
        signer_config_dict["signer_file_path"]=signer_config.signer_file_path
        signer_config_dict["signer_pwd"]=signer_config.signer_pwd
        signer_config_dict["signer_key_pwd"]=signer_config.signer_key_pwd
        signer_config_dict["signer_alias"]=signer_config.signer_alias
        
        if signer_version=="v2":
            tmp_apk = os.path.join(FileHelper.parentDir(origin_apk), "unsign_"+FileHelper.filename(origin_apk))
            zip_result = ApkCMD.zipalign(user_path_config.zipalign, origin_apk, tmp_apk)
            if zip_result:
                result = ApkCMD.signV2(user_path_config.apksigner, tmp_apk, output_apk, signer_config_dict)
        elif signer_version=="v1":
            tmp_apk = os.path.join(FileHelper.parentDir(origin_apk), "unzipalign_"+FileHelper.filename(origin_apk))
            sign_result = ApkCMD.signV1(user_path_config.jarsigner, origin_apk, tmp_apk, signer_config_dict)
            if sign_result:
                result = ApkCMD.zipalign(user_path_config.zipalign, tmp_apk, output_apk)
        return result

    @classmethod
    def getApps(cls, is_sys, progress_callback):
        """
        获取手机上的 app 列表

        :param is_sys: 是否只包含系统应用
        :param progress_callback: 进度回调

        """

        logger = JLogger(log_name="get_apps_info_{0}.log".format(currentTimeNumber()), save_file=True)
        # 输出信息的文件
        user_path_config = UserConfig.getPath()
        target_info_file  = os.path.join(user_path_config.adb_cache, "{0}_apks_info.txt").format(currentTimeMillis())
        # 第一步，导出所有应用信息
        progress_callback(10, "开始执行", "", True)
        logger.info("get all apps in phone...")
        cmd_result = AdbCMD.getAppsByAdb(target_info_file, False, True, is_sys, Context.DEFAULT_ADB_DEVICE)
        progress_callback(50, "获取手机应用信息", cmd_result[1], cmd_result[0])
        if not cmd_result[0]:
            return False, None
        # 第二步，解析应用信息
        app_list = cls.parseApkListInfo(target_info_file)
        progress_callback(80, "解析手机应用信息", "", True)
        return True, app_list
    
    @classmethod
    def pullApk(cls, package_name, in_phone_path, progress_callback):
        """
        通过 adb 命令将指定路径下的 apk 拉到 pc

        :param package_name: 包名
        :param in_phone_path: 指定路径

        """
        logger = JLogger(log_name="pull_apk_{0}.log".format(currentTimeNumber()), save_file=True)
        user_path_config = UserConfig.getPath()
        target_file = os.path.join(user_path_config.pull_apk_cache, "{0}.apk".format(package_name))
        logger.info("pull apk ...")
        progress_callback(10, "开始执行", "", True)
        cmd_result = AdbCMD.pullApkByAdb(in_phone_path, target_file, Context.DEFAULT_ADB_DEVICE)
        print(cmd_result)
        progress_callback(80, "导出完成", "", True)
        
        return cmd_result[0], target_file
    
    @classmethod
    def parseApkListInfo(cls, info_file):
        content = FileHelper.fileContent(info_file)
        apk_list = []
        pack_infos = content.strip("package:").replace("\n", "").split("package:")
        for pack_info in pack_infos:
            apk_list.append(
                (pack_info.split(".apk=")[1], pack_info.split(".apk=")[0]+".apk"))
        return apk_list
    
    @classmethod
    def parseSignermd5(cls, keytool_path, depack_path, logger):
        msg=""
        signer_dir = os.path.join(depack_path, "original"+os.path.sep+"META-INF")
        md5_str = ""
        for file in FileHelper.getChild(signer_dir):
            if file.endswith(".RSA"):
                result = ApkCMD.getSignerMd5(keytool_path, os.path.join(signer_dir, file))
                logger.info("cmd:"+result[2]+", result:"+result[1])
                msg+="{}/n".format(result[1])
                if result[0]:
                    md5_str = result[1].split("(stdin)= ")[1]
                    return True, md5_str
        return False, msg
    
    @classmethod
    def parseSignerInfo(cls, keytool_path, depack_path, logger):
        msg=""
        signer_dir = os.path.join(depack_path, "original"+os.path.sep+"META-INF")
        sha1_str = ""
        sha256_str = ""
        for file in FileHelper.getChild(signer_dir):
            if file.endswith(".RSA"):
                result = ApkCMD.getSignerInfo(keytool_path, os.path.join(signer_dir, file))
                logger.info("cmd:"+result[2]+", result:"+result[1])
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
                    return (True, sha1_str, sha256_str)
        return (False, msg, "")
    
    @classmethod
    def parseApkInfo(cls, info_file, apk_path, depackage_path, logger)->None or ApkInfo:
        def get_value(info_content, target_property):
            try:
                return info_content.split(target_property)[1:][0].split("'")[1:2][0]
            except Exception as e:
                logger.warning("exce:\n{0}".format(traceback.format_exc()))
                return ""

        def get_list(info_content, target_property, last_tag):
            try:
                content = info_content.split(target_property)[1:][0]
                if last_tag != "":
                    content = content.split(last_tag)[:1][0]
                return content.replace("'", "").strip().replace(" ", ", ")
            except Exception as e:
                logger.warning("exce:\n{0}".format(traceback.format_exc()))
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
    def getIcon(cls, depack_path, logger):
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
                if icon_name in file and (FileHelper.getSuffix(file) == ".png" or FileHelper.getSuffix(file) == ".jpg" or FileHelper.getSuffix(file) == ".webp"):
                    return os.path.abspath(file)
        except Exception as e:
            return None

