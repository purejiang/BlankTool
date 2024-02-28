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
        self.depack_apk_operation = Operation()             # 反编译 apk
        self.get_apps_operation= Operation()           # 获取手机内 apk 列表
        self.pull_apk_operation = Operation()               # 导出手机内 apk
        self.repack_dir_operation = Operation()             # 重编译目录
        self.resign_apk_operation = Operation()             # 重签 apk
        self.parse_apk_operation = Operation()              # 解析并反编译 apk 

    def install(self, apk_path):
        install_thread = InstallApk(apk_path)
        self.install_apk_operation.loadThread(install_thread)
        self.install_apk_operation.start()

    def parseApk(self, apk_path, is_pass_error_dex=False, is_only_res=False):
        parse_thread = ParseApk(apk_path, is_pass_error_dex, is_only_res)
        self.parse_apk_operation.loadThread(parse_thread)
        self.parse_apk_operation.start()
    
    def getApps(self, is_sys):
        get_apps_thread = GetApps(is_sys)
        self.get_apps_operation.loadThread(get_apps_thread)
        self.get_apps_operation.start()
    
    def pullApk(self, pakcage_name, in_phone_path):
        pull_apk_thread = PullApk(pakcage_name, in_phone_path)
        self.pull_apk_operation.loadThread(pull_apk_thread)
        self.pull_apk_operation.start()

    def repack(self, repackage_path, output_apk_path, is_support_aapt2, signer_version, signer_config):
        repack_thread = Repackage(repackage_path, output_apk_path, is_support_aapt2, signer_version, signer_config)
        self.repack_dir_operation.loadThread(repack_thread)
        self.repack_dir_operation.start()
    
    def reSign(self, origin_apk, output_apk, signer_version, signer_config):
        resign_thread = ReSign(origin_apk, output_apk, signer_version, signer_config)
        self.resign_apk_operation.loadThread(resign_thread)
        self.resign_apk_operation.start()

class InstallApk(BaseThread):
    """
    安装 apk
    """

    def __init__(self, apk_path:str):
        super().__init__()
        self._apk_path = apk_path

    def run(self):
        result = ApkManager.installApk(self._apk_path, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "安装失败", "")

class ParseApk(BaseThread):
    """
    解析并反编 apk
    """
    _success_signal = Signal(ApkInfo)

    def __init__(self, apk_path:str, is_pass_error_dex:bool, is_only_res:bool):
        super().__init__()
        self.apk_path = apk_path
        self.is_pass_error_dex = is_pass_error_dex
        self.is_only_res = is_only_res

    def run(self):
        result, apk_info = ApkManager.parseApk(self.apk_path, self.is_pass_error_dex, self.is_only_res, self._progressCallback)
        if result:
            self._success_signal.emit(apk_info)
        else:
            self._failure_signal.emit(Constant.ErrorCode.PARSE_APK_FAILEURE, "分析失败", "")

class GetApps(BaseThread):
    """
    生成手机内 app 信息列表
    """
    _success_signal = Signal(list)

    def __init__(self, is_sys:bool):
        super().__init__()
        self._is_sys = is_sys

    def run(self):
        result, app_list = ApkManager.getApps(self._is_sys, self._progressCallback)
        if result:
            self._success_signal.emit(app_list)
        else:
            self._failure_signal.emit(0, "生成 apk list 信息文件失败", "")
            
class PullApk(BaseThread):
    """
    导出手机内 apk
    """
    _success_signal = Signal(str)

    def __init__(self, package_name:str, in_phone_path:str):
        super().__init__()
        self.package_name = package_name
        self.in_phone_path = in_phone_path

    def run(self):
        result = ApkManager.pullApk(self.package_name, self.in_phone_path, self._progressCallback)
        if result[0]:
            self._success_signal.emit(result[1])
        else:
            self._failure_signal.emit(0, "导出 apk 失败", "")

class Repackage(BaseThread):
    """
    重编译目录为 Apk
    """
    _success_signal = Signal(str)
    
    def __init__(self, repack_dir:str, output_apk:str, is_support_aapt2:bool, signer_version:str, signer_config):
        super().__init__()
        self.repack_dir = repack_dir
        self.output_apk = output_apk
        self.is_support_aapt2 = is_support_aapt2
        self.signer_version = signer_version
        self.signer_config = signer_config

    def run(self):
        result = ApkManager.repack(self.repack_dir, self.output_apk, self.is_support_aapt2, self.signer_version, self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit(self.output_apk)
        else:
            self._failure_signal.emit(0, "重编译 apk 失败", "")

class ReSign(BaseThread):
    """
    重签 Apk
    """
    _success_signal = Signal(str)
    
    def __init__(self, origin_apk:str, output_apk:str, signer_version:str, signer_config):
        super().__init__()
        self.origin_apk = origin_apk
        self.output_apk = output_apk
        self.signer_version = signer_version
        self.signer_config = signer_config

    def run(self):
        result = ApkManager.signApk(self.origin_apk, self.output_apk, self.signer_version, self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit(self.output_apk)
        else:
            self._failure_signal.emit(0, "重签 apk 失败", "")