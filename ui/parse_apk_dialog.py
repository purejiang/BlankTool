# -*- coding:utf-8 -*-

import os
import time
from PySide2.QtCore import Qt
from common.constant import AAPT_INFO_CACHE_PATH
from ui.progress_dialog import ProgressDialog
from ui.toast import Toast
from ui.apk_info_dialog import ApkInfoDialog
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile
from viewmodel.apk_viewmodel import ApkViewModel


class ParseApkDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/13

    解析 .apk 的弹出框

    """
    __UI_FILE = "./res/ui/parse_apk_dialog.ui"
    __QSS_FILE = "./res/qss/parse_apk_dialog.qss"
    __TITLE= "Pull Apk"

    def __init__(self, main_window):
        super(ParseApkDialog, self).__init__(main_window)
        self.left = self.geometry().x() + self.size().width() / 2
        self.top = self.geometry().y() + self.size().height() / 13
        self.is_depackage = False

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.parse_apk_dialog_title_bar.addWidget(self.title_bar)
        self.apk_viewmodel = ApkViewModel(self)
        self.progress_dialog = ProgressDialog(self, "解析 apk", self.__jump_to_apk_info)
        self.progress_dialog.progress_callback(msg="解析中...")

    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.apk_viewmodel.generate_info_success.connect(self.__parse_success)
        self.apk_viewmodel.generate_info_failure.connect(self.__parse_failure)

        # view
        self._ui.parse_apk_path_btn.clicked.connect(self.__choose_file)
        self._ui.parse_apk_btn.clicked.connect(self.__parse)

        self._ui.parse_apk_path_edt.textChanged.connect(self.__sync_file_path)
        self._ui.depackage_apk_check.stateChanged.connect(self.__check_depackage)

        self._ui.parse_apk_btn.setEnabled(False)

    def keyPressEvent(self, e):
        pass

    def __check_depackage(self, state):
        if state == Qt.Checked:
            self.is_depackage = True
        else:
            self.is_depackage = False

    def __sync_file_path(self):
        content = self._ui.parse_apk_path_edt.text().strip()
        # 输入内容为空则不可点击
        if content is None or len(content) == 0:
            self._ui.parse_apk_btn.setEnabled(False)
        else:
            self._ui.parse_apk_btn.setEnabled(True)

    def __choose_file(self):
        self._ui.parse_apk_path_edt.setText(
            chooseFile(self, "选取 apk", "Apks (*.apk)"))

    def __parse(self):
        self.progress_dialog.show()
        self.apk_path = self._ui.parse_apk_path_edt.text()
        if not FileHelper.fileExist(self.apk_path):
            toast = Toast(self)
            toast.make_text("请输入正确的路径", self.left, self.top, times=3)
            return
        
        self.info_file_path = os.path.join(AAPT_INFO_CACHE_PATH, "{0}_info.txt").format(FileHelper.md5(self.apk_path))
        self.apk_viewmodel.generate_apk_info(self.apk_path, self.info_file_path)

    def __parse_success(self):
        self.progress_dialog.progress_callback(100, "apk 解析成功")
        self.progress_dialog.dismiss()
    
    def __parse_failure(self):
        self.progress_dialog.progress_callback(100, "apk 解析失败")
        self.progress_dialog.showEnd("确认")
        
    def __jump_to_apk_info(self):
            self.apk_info_dialog = ApkInfoDialog(
                self, self.apk_path, self.info_file_path, self.is_depackage)
            self.apk_info_dialog.show()