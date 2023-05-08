# -*- coding:utf-8 -*-

from logic.bundle_manager import BundleManager

from viewmodel.base_viewmodel import BaseThread, Operation

class AabViewModel():
    """
    apk 相关操作

    @author: purejiang
    @created: 2022/7/29

    """
    def __init__(self, parent) -> None:
        super(AabViewModel, self).__init__()
        self.parent = parent
        self.install_aab_operation = Operation()            # 安装 aab
        self.apk2aab_operation = Operation()                # apk 转 aab


    def install(self, aab_path, signer_config):
        install_aab_thread = InstallAAB(aab_path, signer_config)
        self.install_aab_operation.loadThread(install_aab_thread)
        self.install_aab_operation.start()
    
        

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
            self._failure_signal.emit(0, "安装失败")

