# -*- coding:utf-8 -*-

import os
import time
from PySide2.QtCore import Qt
from common.constant import PARSE_CACHE_PATH
from ui.choose_file_widget import ChooseFileWidget
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
        self.apk_path = ""

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.parse_apk_dialog_title_bar.addWidget(self.title_bar)
        self.choose_parse_apk_path_widget = ChooseFileWidget(self, "选择 Apk", "选择 apk", "Apk (*.apk)", self.__parse_apk_path_change)
        self._ui.choose_parse_apk_path_layout.addWidget(self.choose_parse_apk_path_widget)
        self.apk_viewmodel = ApkViewModel(self)

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
        self._ui.parse_apk_btn.clicked.connect(self.__parse)

        self._ui.depackage_apk_check.stateChanged.connect(self.__check_depackage)
        self._ui.depack_root_dir_btn.clicked.connect(self.__open_depack_root_dir)
        self._ui.parse_apk_btn.setEnabled(False)

    def keyPressEvent(self, e):
        pass

    def __open_depack_root_dir(self):
        os.startfile(PARSE_CACHE_PATH)

    def __check_depackage(self, state):
        if state == Qt.Checked:
            self.is_depackage = True
        else:
            self.is_depackage = False

    def __parse_apk_path_change(self, path):
        # 输入内容为空则不可点击
        if path is None or len(path) == 0:
            self._ui.parse_apk_btn.setEnabled(False)
        else:
            self.apk_path = path
            self._ui.parse_apk_btn.setEnabled(True)

    def __parse(self):
        if not self.choose_parse_apk_path_widget.check():
            toast = Toast(self)
            toast.make_text("请输入正确的路径", self.left, self.top, times=3)
            return
        self.progress_dialog = ProgressDialog(self, "解析 apk", self.__jump_to_apk_info)
        self.progress_dialog.progress_callback(msg="解析中...")
        self.progress_dialog.show()
        # 在此处去掉耗时操作，比如获取 apk 文件的 md5
        self.apk_viewmodel.generate_apk_info(self.apk_path)

    def __parse_success(self, info_file_path):
        self.info_file_path = info_file_path
        self.progress_dialog.progress_callback(100, "apk 解析成功")
        self.progress_dialog.dismiss()
    
    def __parse_failure(self, code, msg):
        self.progress_dialog.progress_callback(100, "{0} : {1}".format(code, msg))
        self.progress_dialog.showEnd("确认")
        
    def __jump_to_apk_info(self):
        self.apk_info_dialog = ApkInfoDialog(self, self.apk_path, self.info_file_path, self.is_depackage)
        # 相对于父窗口偏移点距离，避免完全遮盖父窗口
        self.apk_info_dialog.move(self.geometry().x()+30, self.geometry().y()+30)
        self.apk_info_dialog.show()