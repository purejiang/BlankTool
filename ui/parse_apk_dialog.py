# -*- coding:utf-8 -*-

import os
from PySide2.QtCore import Qt
from aab.bundltool_builder import BundleToolBuilder
from common.constant import BUNDLE_TOOL_PATH, CACHE_PATH
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from utils.ui_utils import chooseFile


class install_aabDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/11

    安装 aab 的弹出框

    """
    __UI_FILE = "./res/ui/install_aab_dialog.ui"
    __QSS_FILE = "./res/qss/install_aab_dialog.qss"

    def __init__(self, main_window):
        super(install_aabDialog, self).__init__(main_window)
        self.is_to_apks = False

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title("安装 aab")
        self._ui.aab_dialog_title_bar.addWidget(self.title_bar)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        pass

    def keyPressEvent(self, e):
        pass

    def sync_file_path(self):
        content = self._ui.aab_path_edt.text().strip()
        # 输入内容为空则不可点击
        if content is None or len(content) == 0:
            self._ui.install_aab_btn.setEnabled(False)
        else:
            self._ui.install_aab_btn.setEnabled(True)

    def choose_file(self):
        filename = chooseFile(self, "选取aab", "AABs (*.aab)")
        self._ui.aab_path_edt.setText(filename)

    def install_aab(self):
        rebuilder = BundleToolBuilder(BUNDLE_TOOL_PATH, os.path.join(
            CACHE_PATH, "installing-apks.apks"), os.path.join(CACHE_PATH, "installing-apks.log"), None)
        filename = self._ui.aab_path_edt.text()
        if self.is_to_apks:
            rebuilder.aab2apks(filename)
        else:
            rebuilder.install_aab(filename)

    # 关闭对话框
    def close_dialog(self):
        self.close()

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
