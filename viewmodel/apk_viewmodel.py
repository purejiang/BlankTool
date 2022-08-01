# -*- coding:utf-8 -*-

from manager.apk_manager import ApkManager
from viewmodel.viewmodel_signal import ViewModelSignal

from PySide2.QtCore import QThread, Signal

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

    def install(self, apk_path):
        install_thread = Install(self.parent,apk_path)
        install_thread.success.connect(self.install_apk_success.to_method())
        install_thread.failure.connect(self.install_apk_failure.to_method())
        install_thread.start()

    def generate_apk_info(self, apk_path, info_file):
        generate_apk_thread = GenerateApkInfo(self.parent, apk_path, info_file)
        generate_apk_thread.success.connect(self.generate_info_success.to_method())
        generate_apk_thread.failure.connect(self.generate_info_failure.to_method())
        generate_apk_thread.start()

    def depack(self, apktool_path, apk_path, output_path, is_pass_error_dex, is_only_res):
        depack_thread = Depack(self.parent, apktool_path, apk_path, output_path, is_pass_error_dex, is_only_res)
        depack_thread.success.connect(self.depack_apk_success.to_method())
        depack_thread.failure.connect(self.depack_apk_failure.to_method())
        depack_thread.start()

    def parse(self, info_file, apk_path, depack_path):
        parse_thread = Parse(self.parent, info_file, apk_path, depack_path)
        parse_thread.success.connect(self.parse_info_success.to_method())
        parse_thread.failure.connect(self.parse_info_failure.to_method())
        parse_thread.start()
    
    def generate_apk_list(self, info_file):
        generate_list_thread = GenerateApksList(self.parent, info_file)
        generate_list_thread.success.connect(self.generate_list_success.to_method())
        generate_list_thread.failure.connect(self.generate_list_failure.to_method())
        generate_list_thread.start()

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
    success = Signal()
    failure = Signal(int, str)

    def __init__(self, parent, apk_path, info_file):
        QThread.__init__(self, parent)
        self._apk_path = apk_path
        self._info_file = info_file

    def run(self):
        result = ApkManager.aapt_apk_info(self._apk_path, self._info_file)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "解析失败")

class Depack(QThread):
    """
    反编译 apk
    """
    success = Signal()
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
            self.success.emit()
        else:
            self.failure.emit(0, "反编译失败")

class Parse(QThread):
    """
    展示 apk 信息文件
    """
    success = Signal(object)
    failure = Signal(int, str)

    def __init__(self, parent, info_file, apk_path, depack_path):
        QThread.__init__(self, parent)
        self._info_file = info_file
        self._apk_path = apk_path
        self._depack_path = depack_path

    def run(self):
        result, info = ApkManager.parseApkInfo(self._info_file, self._apk_path, self._depack_path)
        if result:
            self.success.emit(info)
        else:
            self.failure.emit(0, "反编译失败")

class GenerateApksList(QThread):
    """
    生成手机内 apk 列表信息文件
    """
    success = Signal(list)
    failure = Signal(int, str)

    def __init__(self, parent, info_file):
        QThread.__init__(self, parent)
        self.info_file = info_file

    def run(self):
        result = ApkManager.get_apks(self.info_file)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "生成 apk list 信息文件失败")