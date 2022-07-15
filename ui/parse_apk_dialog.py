# -*- coding:utf-8 -*-

import os
from PySide2.QtCore import Qt
from aab.bundltool_tools import BundleTools
from apk.apk_tools import ApkTools
from common.constant import AAPT_INFO_PATH, AAPT_PATH, APK_CACHE_PATH, APK_TOOL_PATH, BUNDLE_TOOL_PATH, CACHE_PATH, PARSE_CACHE_PATH
from ui.toast import Toast
from ui.apk_info_dialog import ApkInfoDialog
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from ui.progressbar_dialog import ProgressBarDialog
from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile


class ParseApkDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/13

    解析 apk 的弹出框

    """
    __UI_FILE = "./res/ui/parse_apk_dialog.ui"
    __QSS_FILE = "./res/qss/parse_apk_dialog.qss"

    def __init__(self, main_window):
        super(ParseApkDialog, self).__init__(main_window)
        self.left = self.geometry().x() + self.size().width() / 2
        self.top = self.geometry().y() + self.size().height() / 13
        self.__is_depackage = False

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title("解析 apk")
        self._ui.parse_apk_dialog_title_bar.addWidget(self.title_bar)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.parse_apk_path_btn.clicked.connect(self.__choose_file)
        self._ui.parse_apk_path_edt.textChanged.connect(self.__sync_file_path)
        self._ui.parse_apk_btn.clicked.connect(self.__show_progress)
        self._ui.depackage_apk_check.stateChanged.connect(self.__check_depackage)
        self._ui.parse_apk_btn.setEnabled(False)

    def keyPressEvent(self, e):
        pass

    def __check_depackage(self, state):
        if state == Qt.Checked:
            self.__is_depackage = True
        else:
            self.__is_depackage = False

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

    def __show_progress(self):
        self.__apk_path = self._ui.parse_apk_path_edt.text()
        if not FileHelper.fileExist(self.__apk_path):
            toast = Toast(self)
            toast.make_text("请输入正确的路径", self.left, self.top, times=3)
            return
        self.progressbar_dialog = ProgressBarDialog(
            self, "解析 apk", 0, 100, self.__parse_apk)
        self.progressbar_dialog._signal.connect(self.__show_apk_info)
        self.progressbar_dialog.progress_callback(msg="解析中...")
        self.progressbar_dialog.show()

    def __parse_apk(self):
        self.__info_file_path = os.path.join(AAPT_INFO_PATH, "{0}_info.txt").format(FileHelper.md5(self.__apk_path))
        result = ApkTools.aapt_apk_info(AAPT_PATH, self.__apk_path, self.__info_file_path)
        if result:
            self.progressbar_dialog.progress_callback(100, "apk 解析成功")
        else:
            self.progressbar_dialog.progress_callback(100, "apk 解析失败")

    def __show_apk_info(self, value):
        if value == "end":
            self.apk_info_dialog = ApkInfoDialog(
                self, self.__apk_path, self.__info_file_path, self.__is_depackage)
            self.apk_info_dialog.show()

    # 关闭对话框
    def close_dialog(self):
        self.close()

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
