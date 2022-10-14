# -*- coding:utf-8 -*-

from ui.base_dialog import BaseDialog
from ui.choose_file_widget import ChooseFileWidget
from ui.toast import Toast
from utils.file_helper import FileHelper
from utils.ui_utils import toast_left, toast_top
from viewmodel.signer_viewmodel import SignerViewModel
from vo.keystore_config import KeystoreConfig




class AddKeystoreDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/10/11

    添加 keystore

    """

    __UI_FILE = "./res/ui/add_keystore_dialog.ui"
    __QSS_FILE = "./res/qss/add_keystore_dialog.qss"
    __TITLE ="add keystore"

    def __init__(self, main_window) -> None:
        super(AddKeystoreDialog, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.signer_viewmodel = SignerViewModel(self)
        self.choose_keystore_path_widget = ChooseFileWidget(self, "签名路径", "选择签名文件", self.__keystore_path_change, "签名文件 (*.jks *.keystore)")
        self._ui.choose_keystore_path_layout.addWidget(self.choose_keystore_path_widget)
        
    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.signer_viewmodel.add_keystore_success.connect(self.__add_keystore_success)
        self.signer_viewmodel.add_keystore_failure.connect(self.__add_keystore_failure)
        # view
        self._ui.keystore_cancel_btn.clicked.connect(self.__close)
        self._ui.store_pwd_edt.textChanged.connect(self.__sync_file_path)
        self._ui.key_alias_edt.textChanged.connect(self.__sync_file_path)
        self._ui.key_pwd_edt.textChanged.connect(self.__sync_file_path)
        self._ui.keystore_add_btn.clicked.connect(self.__add)
        self._ui.keystore_add_btn.setEnabled(False)

    def __add(self):
        keystore_password = self._ui.store_pwd_edt.text().strip()
        key_alias = self._ui.key_alias_edt.text().strip()
        key_password = self._ui.key_pwd_edt.text().strip()
        info = KeystoreConfig(FileHelper.filename(self.keystore_path), self.keystore_path, keystore_password, key_alias, key_password, 0)
        self.signer_viewmodel.add_keystore(keystore_config=info)

    def __add_keystore_success(self):
        self.close()

    def __add_keystore_failure(self, code, msg):
        toast = Toast(self)
        toast.make_text("{0}, code:{1}".format(msg, code), toast_left(self), toast_top(self), times=3)

    def __keystore_path_change(self, path):
        # 输入内容为空则不可点击
        self.keystore_path = path
        self.__sync_file_path()

    def __sync_file_path(self):
        store_pwd = self._ui.store_pwd_edt.text().strip()
        key_alias = self._ui.key_alias_edt.text().strip()
        key_pwd = self._ui.key_pwd_edt.text().strip()
        # 输入内容为空则不可点击
        if store_pwd is None or len(store_pwd) == 0:
            self._ui.keystore_add_btn.setEnabled(False)
        elif key_alias is None or len(key_alias) == 0:
            self._ui.keystore_add_btn.setEnabled(False)
        elif key_pwd is None or len(key_pwd) == 0:
            self._ui.keystore_add_btn.setEnabled(False)
        elif self.keystore_path is None or len(self.keystore_path) == 0:
            self._ui.keystore_add_btn.setEnabled(False)
        else:
            self._ui.keystore_add_btn.setEnabled(True)

    def __close(self):
        self.close()


    
        
        
        
