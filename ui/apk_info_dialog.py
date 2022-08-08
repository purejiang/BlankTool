# -*- coding:utf-8 -*-

import os
from PySide2.QtGui import QMovie, QPixmap
from PySide2.QtCore import Qt

from common.constant import  APK_TOOL_PATH, PARSE_CACHE_PATH
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from utils.file_helper import FileHelper

from viewmodel.apk_viewmodel import ApkViewModel


class ApkInfoDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/15

    apk 信息展示的弹出框

    """

    __UI_FILE = "./res/ui/apk_info_dialog.ui"
    __QSS_FILE = "./res/qss/apk_info_dialog.qss"
    __LOADING_FILE ="./res/img/loading.gif"
    __TITLE ="Apk Info"

    def __init__(self, main_window, apk_path, info_file_path, is_depackage=False) -> None:
        super(ApkInfoDialog, self).__init__(main_window)
        self.apk_path = apk_path
        self.is_depackage = is_depackage
        self.info_file_path = info_file_path
        # 是否只反编资源
        self.is_only_res = False
        # 是否忽略错误的 dex
        self.is_pass_error_dex = False
        self.apk_info = None
        self.depack_success = False
        self.__init()

    def __init(self):
        self.apk_viewmodel.parse(self.info_file_path, self.apk_path)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.apk_info_title_bar.addWidget(self.title_bar)
        self.loading_movie = QMovie(self.__LOADING_FILE)
        self._ui.depackage_statue_btn.clicked.connect(self.__depackage_click)
        self._ui.depackage_loading_view.setVisible(False)
        self.apk_viewmodel = ApkViewModel(self)
       
    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self.apk_viewmodel.parse_info_success.connect(self.__get_info_success)
        self.apk_viewmodel.parse_info_failure.connect(self.__get_info_failure)
        self.apk_viewmodel.depack_apk_success.connect(self.__depack_success)
        self.apk_viewmodel.depack_apk_failure.connect(self.__depack_failure)

        self._ui.more_info_btn.clicked.connect(self.__show_more_info)

    def __show_more_info(self):
        self.__open_more_info = not self.__open_more_info

    def __depackage(self, depack_path):
        self.is_pass_error_dex = self._ui.pass_err_dex_check.isChecked()
        self.is_only_res = self._ui.only_res_check.isChecked()
        self.apk_viewmodel.depack(APK_TOOL_PATH, self.apk_path, depack_path, self.is_pass_error_dex, self.is_only_res)
    
    def __reset_depackage_ui(self, depackage_status, show_check):
        self._ui.depackage_statue_btn.setText(depackage_status)
        self._ui.depackage_statue_btn.setEnabled(True)
        if show_check:
            self._ui.pass_err_dex_check.setVisible(True)
            self._ui.only_res_check.setVisible(True)
        else:
            self._ui.pass_err_dex_check.setVisible(False)
            self._ui.only_res_check.setVisible(False)
        self._ui.depackage_loading_view.setVisible(False)
        self.loading_movie.stop()

    def __depack_success(self):
        self.__reset_depackage_ui("打开反编译路径", False)
        # 设置图片并自适应
        self._ui.app_icon.setPixmap(QPixmap(self.apk_info.icon))
        self._ui.app_icon.setScaledContents(True)
        self.depack_success = True
    
    def __depack_failure(self):
        self.__reset_depackage_ui("重新反编译", True)
        self.depack_success = False

    def __get_info_success(self, apk_info):
        self.apk_info = apk_info
        self.__show_info(apk_info) 
        if self.is_depackage:
            self.__show_start_depack()
            self.__depackage(apk_info.depack_path)
        else:
            self.__reset_depackage_ui("开始反编译", True)

    def __show_info(self, apk_info):
        self._ui.app_name.setText(apk_info.app_name)
        self._ui.package_name.setText(apk_info.package_name)
        self._ui.apk_file_path.setText(apk_info.apk_path)
        self._ui.version_name.setText(apk_info.version_name)
        self._ui.version_code.setText(apk_info.version_code)
        self._ui.target_version.setText(apk_info.target_version)
        self._ui.min_version.setText(apk_info.min_version)
        self._ui.abis.setText(apk_info.abis)
        self._ui.langs.setText(apk_info.langs)

    def __get_info_failure(self, msg):
        pass

    def __show_start_depack(self):
        self._ui.depackage_statue_btn.setText("反编译中...")
        self._ui.depackage_statue_btn.setEnabled(False)
        self._ui.pass_err_dex_check.setVisible(False)
        self._ui.only_res_check.setVisible(False)
        self._ui.depackage_loading_view.setMovie(self.loading_movie)
        self._ui.depackage_loading_view.setVisible(True)
        self.loading_movie.start()

    def __depackage_click(self):
        if self.depack_success:
            # 跳转到目录
            os.startfile(self.apk_info.depcak_path)
        else:
            self.__show_start_depack()
            self.__depackage(self.apk_info.depcak_path)


    
        
        
        
