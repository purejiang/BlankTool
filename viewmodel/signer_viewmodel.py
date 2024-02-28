# -*- coding:utf-8 -*-

from PySide6.QtCore import Signal
from logic.signer_manager import SignerManager

from viewmodel.base_viewmodel import BaseThread, Operation
from vo.signer import SignerConfig

class SignerViewModel():
    """
    签名的相关操作

    @author: purejiang
    @created: 2022/8/1

    """

    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.add_operation = Operation()                 # 添加签名
        self.del_operation = Operation()                 # 删除签名
        self.modify_operation = Operation()              # 修改签名
        self.get_operation = Operation()                 # 获取签名
        self.all_operation = Operation()                 # 获取所有签名
    
    def addSigner(self, signer_config):
        add_thread = AddSigner(signer_config)
        self.add_operation.loadThread(add_thread)
        self.add_operation.start()
    
    def delSigner(self, signer_id):
        del_thread = DelSigner(signer_id)
        self.del_operation.loadThread(del_thread)
        self.del_operation.start()
    
    def getSigner(self, signer_id):
        get_thread = GetSigner(signer_id)
        self.get_operation.loadThread(get_thread)
        self.get_operation.start()

    def modifySigner(self, signer_config):
        modify_thread = ModifySigner(signer_config)
        self.modify_operation.loadThread(modify_thread)
        self.modify_operation.start()

    def allSigners(self):
        all_thread = AllSignerList()
        self.all_operation.loadThread(all_thread)
        self.all_operation.start()
 
    
class AddSigner(BaseThread):
    """
    添加 keystore
    """
    def __init__(self, signer_config):
        super().__init__()
        self.signer_config = signer_config

    def run(self):
        result = SignerManager.addKeystore(self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "添加失败", "")

class DelSigner(BaseThread):
    """
    删除签名
    """

    def __init__(self, configer_id):
        super().__init__()
        self.configer_id = configer_id

    def run(self):
        result = SignerManager.delSigner(self.configer_id, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "删除失败", "")

class ModifySigner(BaseThread):
    """
    修改签名
    """

    def __init__(self, signer_config):
        super().__init__()
        self.signer_config = signer_config

    def run(self):
        result = SignerManager.modifySigner(self.signer_config, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "修改失败", "")
        
class GetSigner(BaseThread):
    """
    获取签名
    """

    def __init__(self, signer_config_id):
        super().__init__()
        self.signer_config_id = signer_config_id
        self._success_signal = Signal(SignerConfig)

    def run(self):
        result, ks_config = SignerManager.getSigner(self.signer_config_id, self._progressCallback)
        if result:
            self._success_signal.emit(ks_config)
        else:
            self._failure_signal.emit(0, "获取失败", "")
            
class AllSignerList(BaseThread):
    """
    获取签名列表
    """
    _success_signal = Signal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        signer_list = SignerManager.allSigners(self._progressCallback)
        if signer_list!=None:
            self._success_signal.emit(signer_list)
        else:
            self._failure_signal.emit(0, "获取失败", "")