# -*- coding:utf-8 -*-

import os
from common.constant import Constant
from ui.base_widget import BaseWidget
from ui.choose_file_widget import ChooseFileWidget
from ui.progress_dialog import ProgressDialog
from ui.signer_dialog import SignerDialog
from utils.file_helper import FileHelper
from viewmodel.apk_viewmodel import ApkViewModel
from viewmodel.signer_viewmodel import SignerViewModel

class RePackWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/8/26

    重打包 apk 的界面

    """
    __UI_FILE = "./res/ui/repack_widget.ui"
    __QSS_FILE = "./res/qss/repack_widget.qss"

    def __init__(self, main_window):
        super(RePackWidget, self).__init__(main_window)
        self.__refersh()
        self.keystore_config=None

    def __refersh(self):
        self.signer_viewmodel.get_keystores()

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.choose_repack_path_widget = ChooseFileWidget(self, "重编路径", "选择重编译路径", self.__repack_path_change)
        self._ui.choose_repack_path_layout.addWidget(self.choose_repack_path_widget)
        self._ui.repack_btn.setEnabled(False)
        self.signer_viewmodel = SignerViewModel(self)
        self.apk_viewmodel = ApkViewModel(self)
        
    def __repack_path_change(self, path):
        if path is None or len(path) == 0:
            self._ui.repack_btn.setEnabled(False)
        else:
            self.repack_path = path
            self._ui.repack_btn.setEnabled(True)
    
    def __show_signer(self):
        self.signer_dialog = SignerDialog(self,  self.__refersh)
        self.signer_dialog.show()

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.signer_viewmodel.get_keystores_success.connect(self.__get_keystores_success)
        self.signer_viewmodel.get_keystores_failure.connect(self.__get_keystores_failure)

        self.apk_viewmodel.repack_apk_success.connect(self.__repack_apk_success)
        self.apk_viewmodel.repack_apk_failure.connect(self.__repack_apk_failure)

        self.signer_viewmodel.sign_success.connect(self.__sign_apk_success)
        self.signer_viewmodel.sign_failure.connect(self.__sign_apk_failure)
        # view
        self._ui.repack_btn.clicked.connect(self.__repack)
        self._ui.show_signer_btn.clicked.connect(self.__show_signer)
    
    def __repack(self):
        out_put_path = os.path.join(FileHelper.parentDir(self.repack_path), FileHelper.filename(self.repack_path)+".apk")
        self.apk_viewmodel.repack(Constant.Re.APK_TOOL_PATH, self.repack_path, out_put_path,False)
        self.progressbar_dialog = ProgressDialog(self, "重编译 apk", None)
        self.progressbar_dialog.progress_callback(msg="重编译中...")
        self.progressbar_dialog.show()

    def __get_keystores_success(self, list):
        if len(list)>0:
            self.keystore_config = list[0]
            self._ui.keystore_name_edt.setText(list[0].keystore_name)

    def __get_keystores_failure(self, code, msg):
        pass

    def __repack_apk_success(self, apk_path):
        self.progressbar_dialog.progress_callback(50, "重编译 apk 成功, 签名...")
        final_apk_path = os.path.join(FileHelper.parentDir(apk_path), FileHelper.filename(apk_path, False)+"_signed.apk")
        self.signer_viewmodel.sign(apk_path, final_apk_path, self.keystore_config)

    def __repack_apk_failure(self, code, msg):
        self.progressbar_dialog.progress_callback(50, "{0} : {1}".format(code, msg))
        self.progressbar_dialog.showEnd("确认")

    def __sign_apk_success(self,):
        self.progressbar_dialog.progress_callback(100, "签名 apk 成功")
        self.progressbar_dialog.showEnd("确认")


    def __sign_apk_failure(self, code, msg):
        self.progressbar_dialog.progress_callback(100, "{0} : {1}".format(code, msg))
        self.progressbar_dialog.showEnd("确认")
    