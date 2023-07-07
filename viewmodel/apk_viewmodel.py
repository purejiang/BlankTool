# -*- coding:utf-8 -*-

import os
from common.constant import Constant
from logic.apk_manager import ApkManager
from utils.other_util import currentTimeMillis
from viewmodel.base_viewmodel import BaseThread, Operation
from PySide6.QtCore import Signal

from vo.apk_info import ApkInfo
from vo.signer import SignerConfig

class ApkViewModel():
    """
    apk 相关操作

    @author: purejiang
    @created: 2022/7/29

    """
    _parse_apk_info = None
    
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        
        self.install_apk_operation = Operation()            # 安装 apk
        self.generate_info_operation = Operation()          # 生成 apk 信息文件
        self.depack_apk_operation = Operation()             # 反编译 apk
        self.generate_list_operation= Operation()           # 获取手机内 apk 列表
        self.pull_apk_operation = Operation()               # 导出手机内 apk
        self.repack_apk_operation = Operation()             # 重编译 apk
        self.parse_apk_operation = Operation()              # 解析并反编译 apk 

    def install(self, apk_path):
        install_thread = InstallApk(apk_path)
        self.install_apk_operation.loadThread(install_thread)
        self.install_apk_operation.start()

    # def generateApkInfo(self, apk_path):
    #     generate_apk_thread = GenerateApkInfo(apk_path)
    #     self.generate_info_operation.loadThread(generate_apk_thread)
    #     self.generate_info_operation.start()

    def parseApk(self, apk_path, is_pass_error_dex=True, is_only_res=True):
        parse_thread = ParseApk(apk_path, is_pass_error_dex, is_only_res)
        self.parse_apk_operation.loadThread(parse_thread)
        self.parse_apk_operation.start()
    
    def generateApkList(self, is_sys):
        generate_list_thread = GenerateApksList(is_sys)
        self.generate_list_operation.loadThread(generate_list_thread)
        self.generate_list_operation.start()
    
    def pullApk(self, pakcage_name, in_phone_path):
        pull_apk_thread = PullApk(pakcage_name, in_phone_path)
        self.pull_apk_operation.loadThread(pull_apk_thread)
        self.pull_apk_operation.start()

    def repack(self, repackage_path, output_apk_path, is_support_aapt2, signer_config:SignerConfig):
        repack_thread = RepackageAndSign(repackage_path, output_apk_path, is_support_aapt2, signer_config)
        self.repack_apk_operation.loadThread(repack_thread)
        self.repack_apk_operation.start()

class InstallApk(BaseThread):
    """
    安装 apk
    """

    def __init__(self, apk_path):
        super().__init__()
        self._apk_path = apk_path

    def run(self):
        result = ApkManager.installApk(self._apk_path, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "安装失败")

# class GenerateApkInfo(BaseThread):
#     """
#     生成解析 apk 信息文件
#     """
#     _success_signal = Signal(str)
    
#     def __init__(self, apk_path):
#         QThread.__init__(self)
#         self.apk_path = apk_path

#     def run(self):
#         file_name = new_file_name(FileHelper.filename(self.apk_path, False), FileHelper.md5(self.apk_path))
#         info_file = os.path.join(Constant.Path.AAPT_INFO_CACHE_PATH, "{0}.info".format(file_name))
#         if FileHelper.fileExist(info_file):
#             FileHelper.delFile(info_file)
#         result = ApkManager.aapt_apk_info(self.apk_path, info_file)
#         if result:
#             self._success_signal.emit(info_file)
#         else:
#             self._failure_signal.emit(Constant.ErrorCode.PARSE_APK_FAILEURE, "解析失败")


class ParseApk(BaseThread):
    """
    解析并反编 apk
    """
    _success_signal = Signal(ApkInfo)

    def __init__(self, apk_path, is_pass_error_dex, is_only_res):
        super().__init__()
        self.apk_path = apk_path
        self.is_pass_error_dex = is_pass_error_dex
        self.is_only_res = is_only_res

    def run(self):
        result, apk_info = ApkManager.parseApk(self.apk_path, self.is_pass_error_dex, self.is_only_res, self._progressCallback)
        if result:
            self._success_signal.emit(apk_info)
        else:
            self._failure_signal.emit(Constant.ErrorCode.PARSE_APK_FAILEURE, "分析失败")

class GenerateApksList(BaseThread):
    """
    生成手机内 apk 列表信息文件
    """
    _success_signal = Signal(str)

    def __init__(self, is_sys):
        super().__init__(self)
        self.is_sys = is_sys

    def run(self):
        info_file = os.path.join(Constant.Path.ADB_INFO_CACHE_PATH, "{0}_apks_info.txt").format(currentTimeMillis())
        result = ApkManager.getApkListInfo(info_file, self.is_sys, self._progressCallback)
        if result:
            self._success_signal.emit(info_file)
        else:
            self._failure_signal.emit(0, "生成 apk list 信息文件失败")
            
class PullApk(BaseThread):
    """
    导出手机内 apk
    """
    _success_signal = Signal(str)

    def __init__(self, package_name, in_phone_path):
        super().__init__(self)
        self.in_phone_path = in_phone_path
        self.package_name = package_name

    def run(self):
        target_file = os.path.join(Constant.Path.PULL_APK_CACHE_PATH, "{0}.apk".format(self.package_name))
        result = ApkManager.pull_apk(self.in_phone_path, target_file)
        if result:
            self._success_signal.emit(target_file)
        else:
            self._failure_signal.emit(0, "导出 apk 失败")

class RepackageAndSign(BaseThread):
    """
    重编译 apk
    """
    _success_signal = Signal(str)
    def __init__(self, repackage_path, output_apk_path, is_support_aapt2, ks_config):
        super().__init__()
        self.repackage_path = repackage_path
        self.output_apk_path = output_apk_path
        self.is_support_aapt2 = is_support_aapt2
        self.ks_config = ks_config

    def run(self):
        result = ApkManager.repack(self.repackage_path, self.output_apk_path, self.is_support_aapt2, self.ks_config, self._progressCallback)
        if result:
            self._success_signal.emit(self.output_apk_path)
        else:
            self._failure_signal.emit(0, "重编译 apk 失败")