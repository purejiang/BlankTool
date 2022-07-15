# -*- coding:utf-8 -*-

import os
from PySide2.QtCore import Qt
from aab.bundltool_tools import BundleTools
from apk.apk_tools import ApkTools
from common.constant import ADB_PATH, BUNDLE_TOOL_PATH, CACHE_PATH, INSTALL_CACHE_PATH
from ui.toast import Toast
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from ui.progressbar_dialog import ProgressBarDialog
from utils.file_helper import FileHelper
from utils.loguer import Loguer
from utils.other_util import currentTimeMillis
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
        self.left = self.geometry().x() + self.size().width() / 2
        self.top = self.geometry().y() + self.size().height() / 13

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
        file_path = self._ui.install_path_edt.text()
        print(file_path)
        if not FileHelper.fileExist(file_path):
            toast = Toast(self)
            toast.make_text("请输入正确的路径", self.left, self.top, times=3)
            return
        self.progressbar_dialog = ProgressBarDialog(self, "安装应用", 0, 100, self.__install)
        self.progressbar_dialog.progress_callback(msg="安装中...")
        self.progressbar_dialog.show()
    
    def __install(self):
        file_path = self._ui.install_path_edt.text()
        file_name = FileHelper.filename(file_path)
        if FileHelper.getSuffix(file_path)==".aab":
            apks_path = os.path.join(INSTALL_CACHE_PATH, "installing-{0}.apks".format(file_name))
            loguer = Loguer(os.path.join(INSTALL_CACHE_PATH, "bundletool_{0}.log".format(currentTimeMillis())))  
            BundleTools.install_aab(BUNDLE_TOOL_PATH, ADB_PATH, file_path, apks_path, None, loguer, self.progressbar_dialog.progress_callback)
        else:
            result = ApkTools.install_apk(ADB_PATH, file_path) 
            if result:
                 self.progressbar_dialog.progress_callback(100, "apk 安装成功")
            else:
                self.progressbar_dialog.progress_callback(100, "apk 安装失败")

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
