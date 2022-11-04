# -*- coding:utf-8 -*-

import os
from time import time
from common.constant import Constant
from ui.base_widget import BaseWidget
from ui.choose_file_widget import ChooseFileWidget
from ui.progress_dialog import ProgressDialog
from ui.signer_dialog import SignerDialog
from utils.file_helper import FileHelper
from viewmodel.apk_viewmodel import ApkViewModel
from viewmodel.signer_viewmodel import SignerViewModel

class ReSignWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/10/25

    重签名 apk 的界面

    """
    __UI_FILE = "./res/ui/resign_widget.ui"
    __QSS_FILE = "./res/qss/resign_widget.qss"

    def __init__(self, main_window):
        super(ReSignWidget, self).__init__(main_window)
        self.__refersh()
        self.keystore_config=None

    def __refersh(self):
        self.signer_viewmodel.get_keystores()

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.choose_resign_apk_path_widget = ChooseFileWidget(self, "重签名 apk", "选择 apk 文件", self.__resign_path_change, "Apk (*.apk)")
        self._ui.choose_resign_apk_path_layout.addWidget(self.choose_resign_apk_path_widget)
        self._ui.resign_btn.setEnabled(False)
        self.signer_viewmodel = SignerViewModel(self)
        
    def __resign_path_change(self, path):
        if path is None or len(path) == 0:
            self._ui.resign_btn.setEnabled(False)
        else:
            self.resign_apk_path = path
            self._ui.resign_btn.setEnabled(True)
    
    def __show_signer(self):
        self.signer_dialog = SignerDialog(self, self.__refersh)
        self.signer_dialog.show()

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.signer_viewmodel.get_keystores_success.connect(self.__get_keystores_success)
        self.signer_viewmodel.get_keystores_failure.connect(self.__get_keystores_failure)

        self.signer_viewmodel.sign_success.connect(self.__resign_apk_success)
        self.signer_viewmodel.sign_failure.connect(self.__resign_apk_failure)

        # view
        self._ui.resign_btn.clicked.connect(self.__resign)
        self._ui.show_signer_btn.clicked.connect(self.__show_signer)
    
    def __resign(self):
        final_apk_path = os.path.join(FileHelper.parentDir(self.resign_apk_path), FileHelper.filename(self.resign_apk_path, False)+"_signed.apk")
        self.signer_viewmodel.sign(self.resign_apk_path, final_apk_path, self.keystore_config)
        self.progressbar_dialog = ProgressDialog(self, "重签名 apk", None)
        self.progressbar_dialog.progress_callback(msg="重签名中...")
        self.progressbar_dialog.show()

    def __get_keystores_success(self, list):
        if len(list)>0:
            self.keystore_config = list[0]
            self._ui.keystore_name_edt.setText(list[0].keystore_name)

    def __get_keystores_failure(self, code, msg):
        pass

    def __resign_apk_success(self):
        self.progressbar_dialog.progress_callback(100, "重签名 apk 成功")
        self.progressbar_dialog.showEnd("确认")

    def __resign_apk_failure(self, code, msg):
        self.progressbar_dialog.progress_callback(50, "{0} : {1}".format(code, msg))
        self.progressbar_dialog.showEnd("确认")
    