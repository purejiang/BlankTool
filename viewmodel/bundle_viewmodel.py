# -*- coding:utf-8 -*-

from PySide6.QtCore import Signal
from logic.bundle_manager import BundleManager

from viewmodel.base_viewmodel import BaseThread, Operation

class BundleViewModel():
    """
    aab 相关操作

    @author: purejiang
    @created: 2022/7/29

    """
    def __init__(self, parent) -> None:
        super(BundleViewModel, self).__init__()
        self.parent = parent
        self.install_aab_operation = Operation()            # 安装 aab
        self.install_apks_operation = Operation()            # 安装 apks
        self.apk2aab_operation = Operation()                # apk 转 aab


    def install(self, aab_path, signer_config):
        install_aab_thread = InstallAAB(aab_path, signer_config)
        self.install_aab_operation.loadThread(install_aab_thread)
        self.install_aab_operation.start()
    
    def installApks(self, apks_file):
        install_apks_thread = InstallApks(apks_file)
        self.install_apks_operation.loadThread(install_apks_thread)
        self.install_apks_operation.start()

    def apk2aab(self, apk_file, ver_config, signer_config):
        apk2aab_thread = Apk2aab(apk_file, ver_config, signer_config)
        self.apk2aab_operation.loadThread(apk2aab_thread)
        self.apk2aab_operation.start()
        

class InstallAAB(BaseThread):
    """
    安装 aab
    """

    def __init__(self, aab_path, signer_config):
        super().__init__()
        self.aab_path = aab_path
        self.signer_config = signer_config

    def run(self):
        result = BundleManager.install_aab(self.aab_path, self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "安装失败", "")

class InstallApks(BaseThread):
    """
    安装 apks
    """

    def __init__(self, apks_file):
        super().__init__()
        self.apks_file = apks_file

    def run(self):
        result = BundleManager.install_apks(self.apks_file, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "安装失败", "")

class Apk2aab(BaseThread):
    """
    apk 转 aab
    """
    _success_signal = Signal(str)

    def __init__(self, apk_file, ver_config, signer_config):
        super().__init__()
        self.apk_file = apk_file
        self.ver_config = ver_config
        self.signer_config = signer_config

    def run(self):
        result, aab_path = BundleManager.apk2aab(self.apk_file, self.ver_config, self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit(aab_path)
        else:
            self._failure_signal.emit(0, "apk 转 aab失败", "")

