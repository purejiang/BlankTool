# -*- coding:utf-8 -*-

import os
from PySide2.QtCore import Qt
from manager.bundle_manager import BundleManager
from common.constant import INSTALL_CACHE_PATH
from ui.progress_dialog import ProgressDialog
from ui.toast import Toast
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from utils.file_helper import FileHelper
from utils.loguer import Loguer
from utils.ui_utils import chooseFile
from viewmodel.aab_viewmodel import AabViewModel
from viewmodel.apk_viewmodel import ApkViewModel


class InstallDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/11

    安装 aab/apk 的弹出框

    """
    __UI_FILE = "./res/ui/install_dialog.ui"
    __QSS_FILE = "./res/qss/install_dialog.qss"
    __TITLE = "Install"

    def __init__(self, main_window):
        super(InstallDialog, self).__init__(main_window)
        self.left = self.geometry().x() + self.size().width() / 2
        self.top = self.geometry().y() + self.size().height() / 13

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.install_dialog_title_bar.addWidget(self.title_bar)
        self.progressbar_dialog = ProgressDialog(self, "安装应用", None)
        self.progressbar_dialog.progress_callback(msg="安装中...")
        # apk相关
        self.apk_viewmodel = ApkViewModel(self)
        # aab相关
        self.aab_viewmodel = AabViewModel(self)

    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.apk_viewmodel.install_apk_success.connect(self.__install_success)
        self.apk_viewmodel.install_apk_failure.connect(self.__insatll_failure)

        self.aab_viewmodel.install_aab_success.connect(self.__install_success)
        self.aab_viewmodel.install_aab_progress.connect(self.__install_progress)
        self.aab_viewmodel.install_aab_failure.connect(self.__insatll_failure)
        # view
        self._ui.install_path_btn.clicked.connect(self.__choose_file)
        self._ui.install_path_edt.textChanged.connect(self.__sync_file_path)
        self._ui.install_btn.clicked.connect(self.__install)
        self._ui.install_btn.setEnabled(False)

    def keyPressEvent(self, e):
        # 键盘事件
        if e.key() == Qt.Key_Escape:
            # self.close()
            pass

    def __install_success(self):
        self.progressbar_dialog.progress_callback(100, "安装成功")
        self.progressbar_dialog.showEnd("确认")

    def __insatll_failure(self):
        self.progressbar_dialog.progress_callback(100, "安装失败")
        self.progressbar_dialog.showEnd("确认")

    def __install_progress(self, progress, msg):
        self.progressbar_dialog.progress_callback(progress, msg)
        
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

    def __install(self):
        file_path = self._ui.install_path_edt.text()
        if not FileHelper.fileExist(file_path):
            toast = Toast(self)
            toast.make_text("请输入正确的路径", self.left, self.top, times=3)
            return

        self.progressbar_dialog.show()

        if FileHelper.getSuffix(file_path) == ".aab":
            md5 = FileHelper.md5(file_path)
            apks_path = os.path.join(INSTALL_CACHE_PATH, "{0}.apks".format(md5))
            loguer = Loguer(os.path.join(INSTALL_CACHE_PATH, "{0}.log".format(md5)))
            self.aab_viewmodel.install(file_path, apks_path, None, loguer)
        else:
            self.apk_viewmodel.install(file_path)
