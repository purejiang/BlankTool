# -*- coding:utf-8 -*-

from ui.base_widget import BaseWidget
from viewmodel.signer_viewmodel import SignerViewModel


class SignerKeystoreItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/10/14

    signer 签名列表的 item
    """
    __UI_FILE = "./res/ui/signer_keystore_item_widget.ui"
    __QSS_FILE = "./res/qss/signer_keystore_item_widget.qss"

    def __init__(self, main_window, keystore_config) -> None:
        super(SignerKeystoreItemWidget, self).__init__(main_window)
        self.main_window = main_window
        self.keystore_config = keystore_config
        self.init(keystore_config)

    def init(self, keystore_config):
        self._ui.keystore_name_edt.setText(keystore_config.keystore_name)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.signer_viewmodel = SignerViewModel(self)
    
    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        # 事件 

        # view
        self._ui.item_select_bt.clicked.connect(self.__select_keystore)
        self._ui.item_del_btn.clicked.connect(self.__del_keystore)
        self._ui.item_edit_btn.clicked.connect(self.__edit_keystore)
        
    def __edit_keystore(self):
        pass

    def __del_keystore(self):
        self.signer_viewmodel.del_keystore(self.keystore_config)
        self.close()

    def __select_keystore(self):
        self.keystore_config.step = 999
        self.signer_viewmodel.add_keystore(self.keystore_config)
        self.main_window.close()

