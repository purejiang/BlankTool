# -*- coding:utf-8 -*-

import traceback
from common.cmd import CMD
from utils.file_helper import FileHelper
from utils.other_util import write_print
from vo.apk_info import ApkInfo

class ApkManager(object):
    """

    @author: purejiang
    @created: 2022/7/14

    .apk 相关的功能管理

    """

    @classmethod
    def install_apk(cls, apk_path, loguer = None):
        """
        安装 apk

        :param apk_path: apk 路径
        :param progress_callback: 执行进度
        :param loguer: 日志工具，可空

        """
        write_print(loguer, "install {0} ...".format(apk_path))
        cmd_result = CMD.installApk(apk_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def depackage(cls, apktool_path, apk_path, output_dir, is_pass_dex=False, is_only_res=False, loguer = None):
        """
        反编 apk

        :param apktool_path: apktool 路径
        :param apk_path: apk 路径
        :param output_dir: 反编后目录
        :param is_pass_dex: 是否忽略错误的 dex, 默认不忽略
        :param is_only_res: 是否只反编译资源文件, 默认编译所有
        :param loguer: 日志工具，可空

        """
        write_print(loguer, "depackage {0} ...".format(apk_path))
        cmd_result = CMD.depackage(apktool_path, apk_path, output_dir, is_pass_dex, is_only_res)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def repackage(cls, apktool_path, dir_path, output_apk_path, is_support_aapt2=False, loguer=None):
        """
        重编译目录

        :param apktool_ver: apktool 版本
        :param dir_path: 需要重编的目录
        :param output_apk_path: 重编后输出的 apk 路径
        :param is_support_aapt2: 重编译过程中是否支持 aapt2, 默认不支持

        """
        write_print(loguer, "repackage {0} ...".format(dir_path))
        cmd_result = CMD.repackage(apktool_path, dir_path, output_apk_path, is_support_aapt2)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]
    
    @classmethod
    def aapt_apk_info(cls, apk_path, info_file_path, loguer=None):
        """
        获取本地的 apk 信息

        :param apk_path: apk 路径
        :param info_file_path: 输出信息的文件
        :param loguer: 日志工具

        """
        write_print(loguer, "aapt2 get {0} 's info ...".format(apk_path))

        cmd_result = CMD.apkInfoByAapt(apk_path, info_file_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def get_apk_list_info(cls, info_file_path, is_sys, loguer=None):
        """
        获取手机上的 apk 列表

        :param info_file_path: 输出信息的文件
        :param is_sys: 是否只输出系统的应用
        :param loguer: 日志工具

        """
        write_print(loguer, "get all apks in phone...")
        cmd_result = CMD.inPhoneApkList(info_file_path, False, True, is_sys)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def get_inphone_path(cls, package_name, info_file_path, loguer=None):
        """
        获取 apk 在手机上的安装目录

        :param package_name: 包名
        :param info_file_path: 输出信息的文件
        :param loguer: 日志工具

        """
        write_print(loguer, "get {0}'s path ...".format(package_name))
        cmd_result = CMD.inPhonePath(package_name, info_file_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]

    @classmethod
    def pull_apk(cls, in_phone_path, target_path, loguer=None):
        """
        通过 adb 命令将指定路径下的 apk 拉到 pc

        :param package_name: 包名
        :param loguer: 日志工具

        """
        write_print(loguer, "pull apk ...")
        cmd_result = CMD.pullApk(in_phone_path, target_path)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]
    
    @classmethod
    def parseApkInfo(cls, info_file, apk_path, depackage_path):
        def get_value(info_content, target_property):
            return info_content.split(target_property)[1:][0].split("'")[1:2][0]
    
        def get_list(info_content, target_property, last_tag):
            content = info_content.split(target_property)[1:][0]
            if last_tag !="":
                content = content.split(last_tag)[:1][0]
            return content.replace("'","").strip().replace(" ", ", ")
        content = FileHelper.fileContent(info_file)
        try:    
            apk_name = get_value(content, "application: label=")
            apk_icon = get_value(content, "icon=")
            package_name = get_value(content, "package: name=")
            version_code = get_value(content, "versionCode=")
            version_name = get_value(content, "versionName=")
            min_version =get_value(content, "sdkVersion:")
            target_version = get_value(content, "targetSdkVersion:")
            abis = get_list(content, "native-code:", "\n")
            langs = get_list(content, "locales:", "\n")
            return True, ApkInfo(apk_path, apk_name, apk_icon, package_name, version_code, version_name, target_version, min_version, abis, langs, depackage_path)
        except Exception as e:
            return False, "exce:\n{0}".format(traceback.format_exc())
    
    @classmethod
    def parseApkListInfo(cls, info_file):
        content = FileHelper.fileContent(info_file)
        apk_list = []
        pack_infos = content.strip("package:").replace("\n", "").split("package:")
        for pack_info in pack_infos:
            apk_list.append((pack_info.split(".apk=")[1], pack_info.split(".apk=")[0]+".apk"))
        return apk_list
    