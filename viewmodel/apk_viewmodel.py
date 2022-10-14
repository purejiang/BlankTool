# -*- coding:utf-8 -*-

import os
from common.constant import Constant
from manager.apk_manager import ApkManager
from utils.file_helper import FileHelper
from utils.other_util import currentTimeMillis
from viewmodel.viewmodel_signal import ViewModelSignal

from PySide2.QtCore import QThread, Signal

from vo.apk_info import ApkInfo

class ApkViewModel(object):
    """
    apk 相关操作

    @author: purejiang
    @created: 2022/7/29

    """
    def __init__(self, parent) -> None:
        super(ApkViewModel, self).__init__()
        self.parent = parent
        self.install_apk_success = ViewModelSignal()        # 安装 apk 成功
        self.install_apk_failure = ViewModelSignal()        # 安装 apk 失败
        self.generate_info_success = ViewModelSignal()      # 生成 apk 信息文件成功
        self.generate_info_failure = ViewModelSignal()      # 生成 apk 信息文件失败
        self.depack_apk_success = ViewModelSignal()         # 反编译 apk 成功
        self.depack_apk_failure = ViewModelSignal()         # 反编译 apk 失败
        self.parse_info_success = ViewModelSignal()         # 解析 apk 信息文件成功
        self.parse_info_failure = ViewModelSignal()         # 解析 apk 信息文件失败
        self.generate_list_success = ViewModelSignal()      # 获取手机内 apk 列表成功
        self.generate_list_failure = ViewModelSignal()      # 获取手机内 apk 列表失败
        self.pull_apk_success = ViewModelSignal()           # 导出手机内 apk 成功
        self.pull_apk_failure = ViewModelSignal()           # 导出手机内 apk 失败
        self.repack_apk_success = ViewModelSignal()         # 重编译 apk 成功
        self.repack_apk_failure = ViewModelSignal()         # 重编译 apk 失败
        
    def install(self, apk_path):
        install_thread = Install(self.parent, apk_path)
        install_thread.success.connect(self.install_apk_success.to_method())
        install_thread.failure.connect(self.install_apk_failure.to_method())
        install_thread.start()

    def generate_apk_info(self, apk_path):
        generate_apk_thread = GenerateApkInfo(self.parent, apk_path)
        generate_apk_thread.success.connect(self.generate_info_success.to_method())
        generate_apk_thread.failure.connect(self.generate_info_failure.to_method())
        generate_apk_thread.start()

    def depack(self, apktool_path, apk_path, output_path, is_pass_error_dex, is_only_res):
        depack_thread = Depack(self.parent, apktool_path, apk_path, output_path, is_pass_error_dex, is_only_res)
        depack_thread.success.connect(self.depack_apk_success.to_method())
        depack_thread.failure.connect(self.depack_apk_failure.to_method())
        depack_thread.start()

    def parse(self, info_file, apk_path):
        parse_thread = Parse(self.parent, info_file, apk_path)
        parse_thread.success.connect(self.parse_info_success.to_method())
        parse_thread.failure.connect(self.parse_info_failure.to_method())
        parse_thread.start()
    
    def generate_apk_list(self, is_sys):
        generate_list_thread = GenerateApksList(self.parent, is_sys)
        generate_list_thread.success.connect(self.generate_list_success.to_method())
        generate_list_thread.failure.connect(self.generate_list_failure.to_method())
        generate_list_thread.start()
    
    def pull_apk(self, pakcage_name, in_phone_path):
        pull_apk_thread = PullApk(self.parent, pakcage_name, in_phone_path)
        pull_apk_thread.success.connect(self.pull_apk_success.to_method())
        pull_apk_thread.failure.connect(self.pull_apk_failure.to_method())
        pull_apk_thread.start()

    def repack(self, apktool_path, repackage_path, out_put_path, is_support_aapt2):
        repack_thread = Repackage(self.parent, apktool_path, repackage_path, out_put_path, is_support_aapt2)
        repack_thread.success.connect(self.repack_apk_success.to_method())
        repack_thread.failure.connect(self.repack_apk_failure.to_method())
        repack_thread.start()
class Install(QThread):
    """
    安装 apk
    """
    success = Signal()
    failure = Signal(int, str)

    def __init__(self, parent, apk_path):
        super().__init__(parent)
        self._apk_path = apk_path

    def run(self):
        result = ApkManager.install_apk(self._apk_path)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "安装失败")

class GenerateApkInfo(QThread):
    """
    生成解析 apk 信息文件
    """
    success = Signal(str)
    failure = Signal(int, str)

    def __init__(self, parent, apk_path):
        QThread.__init__(self, parent)
        self.apk_path = apk_path

    def run(self):
        info_file = os.path.join(Constant.CachePath.AAPT_INFO_CACHE_PATH, "{0}_info.txt").format(FileHelper.md5(self.apk_path))
        if FileHelper.fileExist(info_file):
            FileHelper.delFile(info_file)
        result = ApkManager.aapt_apk_info(self.apk_path, info_file)
        if result:
            self.success.emit(info_file)
        else:
            self.failure.emit(0, "解析失败")

class Depack(QThread):
    """
    反编译 apk
    """
    success = Signal(str)
    failure = Signal(int, str)

    def __init__(self, parent, apktool_path, apk_path, out_put_path, is_pass_error_dex, is_only_res):
        QThread.__init__(self, parent)
        self.apk_path = apk_path
        self.apktool_path = apktool_path
        self.out_put_path = out_put_path
        self.is_pass_error_dex = is_pass_error_dex
        self.is_only_res = is_only_res

    def run(self):
        result = ApkManager.depackage(self.apktool_path, self.apk_path, self.out_put_path, self.is_pass_error_dex, self.is_only_res)
        if result:
            self.success.emit(ApkManager.parseIcon(self.out_put_path))
        else:
            FileHelper.delFile(self.out_put_path)
            self.failure.emit(0, "反编译失败")

class Parse(QThread):
    """
    展示 apk 信息文件
    """
    success = Signal(ApkInfo)
    failure = Signal(int, str)

    def __init__(self, parent, info_file, apk_path):
        QThread.__init__(self, parent)
        self.info_file = info_file
        self.apk_path = apk_path

    def run(self):
        depack_path = os.path.join(Constant.CachePath.PARSE_CACHE_PATH, FileHelper.md5(self.apk_path))
        result, apk_info = ApkManager.parseApkInfo(self.info_file, self.apk_path, depack_path)
        if result:
            self.success.emit(apk_info)
        else:
            self.failure.emit(0, "反编译失败")

class GenerateApksList(QThread):
    """
    生成手机内 apk 列表信息文件
    """
    success = Signal(str)
    failure = Signal(int, str)

    def __init__(self, parent, is_sys):
        QThread.__init__(self, parent)
        self.is_sys = is_sys

    def run(self):
        info_file = os.path.join(Constant.CachePath.ADB_INFO_CACHE_PATH, "{0}_apks_info.txt").format(currentTimeMillis())
        result = ApkManager.get_apk_list_info(info_file, self.is_sys)
        if result:
            self.success.emit(info_file)
        else:
            self.failure.emit(0, "生成 apk list 信息文件失败")
            
class PullApk(QThread):
    """
    导出手机内 apk
    """
    success = Signal(str)
    failure = Signal(int, str)

    def __init__(self, parent, package_name, in_phone_path):
        QThread.__init__(self, parent)
        self.in_phone_path = in_phone_path
        self.package_name = package_name

    def run(self):
        target_file = os.path.join(Constant.CachePath.PULL_APK_CACHE_PATH, "{0}.apk".format(self.package_name))
        result = ApkManager.pull_apk(self.in_phone_path, target_file)
        if result:
            self.success.emit(target_file)
        else:
            self.failure.emit(0, "导出 apk 失败")

class Repackage(QThread):
    """
    重编译 apk
    """
    success = Signal(str)
    failure = Signal(int, str)

    def __init__(self, parent, apktool_path, repackage_path, out_put_path, is_support_aapt2):
        QThread.__init__(self, parent)
        self.apktool_path = apktool_path
        self.repackage_path = repackage_path
        self.out_put_path = out_put_path
        self.is_support_aapt2 = is_support_aapt2

    def run(self):
        result = ApkManager.repackage(self.apktool_path, self.repackage_path, self.out_put_path, self.is_support_aapt2)
        if result:
            self.success.emit(self.out_put_path)
        else:
            self.failure.emit(0, "导出 apk 失败")