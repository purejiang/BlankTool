# -*- coding:utf-8 -*-

import os
from PySide2.QtCore import Qt
from aab.bundltool_builder import BundleToolBuilder
from apk.apk_tools import ApkTools
from common.constant import BUNDLE_TOOL_PATH, CACHE_PATH
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from ui.progressbar_dialog import ProgressBarDialog
from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile


class InstallDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/11

    安装 aab/apk 的弹出框

    """
    __UI_FILE = "./res/ui/install_dialog.ui"
    __QSS_FILE = "./res/qss/install_dialog.qss"

    def __init__(self, main_window):
        super(InstallDialog, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title("安装 aab/apk")
        self._ui.install_dialog_title_bar.addWidget(self.title_bar)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.install_path_btn.clicked.connect(self.__choose_file)
        self._ui.install_path_edt.textChanged.connect(self.__sync_file_path)
        self._ui.install_btn.clicked.connect(self.__show_progress)
        self._ui.install_btn.setEnabled(False)

    def keyPressEvent(self, e):
        # 键盘事件
        if e.key() == Qt.Key_Escape:
            # self.close()
            pass

    def __sync_file_path(self):
        file_path = self._ui.install_path_edt.text().strip()
        # 输入内容为空则不可点击
        if file_path is None or len(file_path) == 0:
            self._ui.install_btn.setEnabled(False)
        else:
            self._ui.install_btn.setEnabled(True)

    def __choose_file(self):
        file_path = chooseFile(self, "选取aab", "安卓应用文件 (*.aab *.apk)")
        self._ui.install_path_edt.setText(file_path)

    def __show_progress(self):
        self.progressbar_dialog = ProgressBarDialog(self, "安装应用", 0, 100, self.__install)
        self.progressbar_dialog.set_msg("安装中...")
        self.progressbar_dialog.show()
    
    def __install(self):
        file_path = self._ui.install_path_edt.text()
        file_name = FileHelper.filename(file_path)
        if FileHelper.getSuffix(file_path)==".aab":
            rebuilder = BundleToolBuilder(BUNDLE_TOOL_PATH, os.path.join(
                CACHE_PATH, "installing-{0}.apks".format(file_name)), os.path.join(CACHE_PATH, "installing-{0}.log".format(file_name)), None)
            rebuilder.install_aab(file_path)
        else:
            ApkTools.installApk(file_path)
        self.progressbar_dialog.set_msg("安装完成")
        
        

    # 关闭对话框
    def close_dialog(self):
        self.close()

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
