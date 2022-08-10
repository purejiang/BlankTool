# -*- coding:utf-8 -*-

import os
from common.constant import INSTALL_CACHE_PATH
from manager.bundle_manager import BundleManager
from utils.file_helper import FileHelper
from utils.loguer import Loguer
from viewmodel.viewmodel_signal import ViewModelSignal

from PySide2.QtCore import QThread, Signal

class AabViewModel(object):
    """
    apk 相关操作

    @author: purejiang
    @created: 2022/7/29

    """
    def __init__(self, parent) -> None:
        super(AabViewModel, self).__init__()
        self.parent = parent
        self.install_aab_success = ViewModelSignal()        # 安装 aab 成功
        self.install_aab_progress = ViewModelSignal()       # 安装 aab 进度
        self.install_aab_failure = ViewModelSignal()        # 安装 aab 失败

    def install(self, aab_path, keystore_config):
        install_aab_thread = InstallAAB(self.parent, aab_path, keystore_config)
        install_aab_thread.success.connect(self.install_aab_success.to_method())
        install_aab_thread.install_progress.connect(self.install_aab_progress.to_method())
        install_aab_thread.failure.connect(self.install_aab_failure.to_method())
        install_aab_thread.start()
        

class InstallAAB(QThread):
    """
    安装 aab
    """
    success = Signal()
    install_progress = Signal(int, str)
    failure = Signal(int, str)

    def __init__(self, parent, aab_path, keystore_config):
        super().__init__(parent)
        self.aab_path = aab_path
        self.keystore_config = keystore_config

    def run(self):
        md5 = FileHelper.md5(self.aab_path)
        apks_path = os.path.join(INSTALL_CACHE_PATH, "{0}.apks".format(md5))
        loguer = Loguer(os.path.join(INSTALL_CACHE_PATH, "{0}.log".format(md5)))
        result = BundleManager.install_aab(self.aab_path, apks_path, self.keystore_config, loguer, self.progress_callback)
        print("result:"+str(result))
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "安装失败")

    def progress_callback(self, progress, msg):
        self.install_progress.emit(progress, msg)

