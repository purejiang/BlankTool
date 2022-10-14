# -*- coding:utf-8 -*-

from manager.signer_manager import SignerManager
from viewmodel.viewmodel_signal import ViewModelSignal
from PySide2.QtCore import QThread, Signal

class SignerViewModel(object):
    """
    签名的相关操作

    @author: purejiang
    @created: 2022/8/1

    """
    def __init__(self, parent) -> None:
        super(SignerViewModel, self).__init__()
        self.parent = parent
        self.add_keystore_success = ViewModelSignal()       # 添加签名成功
        self.add_keystore_failure = ViewModelSignal()       # 添加签名失败
        self.del_keystore_success = ViewModelSignal()       # 删除签名成功
        self.del_keystore_failure = ViewModelSignal()       # 删除签名失败
        self.get_keystores_success = ViewModelSignal()      # 获取签名列表成功
        self.get_keystores_failure = ViewModelSignal()      # 获取签名列表失败
        self.sign_success = ViewModelSignal()               # 签名成功
        self.sign_failure = ViewModelSignal()               # 签名失败
    
    def add_keystore(self, keystore_config):
        add_thread = AddKeyStore(self.parent, keystore_config)
        add_thread.success.connect(self.add_keystore_success.to_method())
        add_thread.failure.connect(self.add_keystore_failure.to_method())
        add_thread.start()
    
    def del_keystore(self, keystore_config):
        del_thread = DelKeyStore(self.parent, keystore_config)
        del_thread.success.connect(self.del_keystore_success.to_method())
        del_thread.failure.connect(self.del_keystore_failure.to_method())
        del_thread.start()
    
    def get_keystores(self):
        get_thread = GetKeyStoreList(self.parent)
        get_thread.success.connect(self.get_keystores_success.to_method())
        get_thread.failure.connect(self.get_keystores_failure.to_method())
        get_thread.start()
    
    def sign(self, apk_path, output_path, keystore_config):
        sign_thread = Sign(self.parent, apk_path, output_path, keystore_config)
        sign_thread.success.connect(self.sign_success.to_method())
        sign_thread.failure.connect(self.sign_failure.to_method())
        sign_thread.start()   
    
class AddKeyStore(QThread):
    """
    添加 keystore
    """
    success = Signal()
    failure = Signal(int, str)

    def __init__(self, parent, keystore_config):
        super().__init__(parent)
        self.keystore_config = keystore_config

    def run(self):
        result = SignerManager.addKeystore(self.keystore_config)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "添加失败")

    def progress_callback(self, progress, msg):
        self.install_progress.emit(progress, msg)

class DelKeyStore(QThread):
    """
    删除 keystore
    """
    success = Signal()
    failure = Signal(int, str)

    def __init__(self, parent, keystore_info):
        super().__init__(parent)
        self.keystore_info = keystore_info

    def run(self):
        result = SignerManager.delKeystore(self.keystore_info)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "删除失败")

class GetKeyStoreList(QThread):
    """
    获取 keystore 列表
    """
    success = Signal(list)
    failure = Signal(int, str)

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        result, list = SignerManager.getKeystores()
        if result:
            self.success.emit(list)
        else:
            self.failure.emit(0, "获取失败")
    
class Sign(QThread):
    """
    签名
    """
    success = Signal()
    failure = Signal(int, str)

    def __init__(self, parent, apk_path, out_path, keystore_config):
        super().__init__(parent)
        self.apk_path = apk_path
        self.out_path = out_path
        self.keystore_config = keystore_config

    def run(self):
        result = SignerManager.sign(self.apk_path, self.out_path, self.keystore_config)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "签名失败")
