# -*- coding:utf-8 -*-

import os
from PySide2.QtGui import QMovie
from PySide2.QtCore import Qt
from apk.apk_tools import ApkTools
from common.constant import AAPT_PATH, APK_TOOL_PATH, CACHE_PATH, PARSE_CACHE_PATH
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from utils.file_helper import FileHelper
from utils.work_thread import WorkThread
from vo.apk_info import ApkInfo
from PySide2.QtWidgets import QGraphicsOpacityEffect
class ApkInfoDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/14

    其他工具

    """

    __UI_FILE = "./res/ui/apk_info_dialog.ui"
    __QSS_FILE = "./res/qss/apk_info_dialog.qss"
    __LOADING_FILE ="./res/img/loading.gif"

    def __init__(self, main_window, apk_path, info_file_path, is_depackage=False) -> None:
        super(ApkInfoDialog, self).__init__(main_window)
        self.__apk_path = apk_path
        self.__info_file_path = info_file_path
        self.__is_depackage = is_depackage
        self.__depackage_path = os.path.join(PARSE_CACHE_PATH, FileHelper.md5(self.__apk_path))
        self.__result = None
        self.__parse_info()

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title("apk 信息")
        self._ui.apk_info_title_bar.addWidget(self.title_bar)
        self.__loading_movie = QMovie(self.__LOADING_FILE)
        self._ui.depackage_statue.clicked.connect(self.__depackage_click)
        self._ui.depackage_loading_view.setVisible(False)
       
    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.more_info_btn.clicked.connect(self.__show_more_info)

    def __show_more_info(self):
        self.__open_more_info = not self.__open_more_info

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
    
    def __parse_info(self):
        content =""
        with open(self.__info_file_path, "r+", encoding="utf-8") as f:
            content = str(f.read())
        apk_name = self.__get_value(content, "application: label=")
        apk_icon = self.__get_value(content, "icon=")
        package_name = self.__get_value(content, "package: name=")
        version_code = self.__get_value(content, "versionCode=")
        version_name = self.__get_value(content, "versionName=")
        min_version = self.__get_value(content, "sdkVersion:")
        target_version = self.__get_value(content, "targetSdkVersion:")
        abis = self.__get_list(content, "native-code:", "\n")
        langs = self.__get_list(content, "locales:", "\n")
        self.__apk_info = ApkInfo(self.__apk_path, apk_name, apk_icon, package_name, version_code, version_name, target_version, min_version, abis, langs)
        self.__show_info()
        self.__init_depackage(self.__is_depackage)

    def __init_depackage(self, is_depackage):
        if is_depackage:
            self._ui.depackage_loading_view.setVisible(True)
            # 设置加载动态
            self._ui.depackage_loading_view.setMovie(self.__loading_movie)
            self.__thread = WorkThread(self.__depackage)
            self.__thread._state.connect(self.__sig_out)
            self._ui.depackage_statue.setText("反编译中...")
            self._ui.depackage_statue.setEnabled(False)
            self.__loading_movie.start()
            self.__thread.start()
        else:
            self._ui.depackage_statue.setText("开始反编译")
            self._ui.depackage_statue.setEnabled(True)

    def __depackage(self):
        self.__result = ApkTools.depackage(APK_TOOL_PATH, self.__apk_path, self.__depackage_path)
    
    def __sig_out(self, state):
        if state==1:
            self.__thread.terminate()
            self.__loading_movie.stop()
            if self.__result:            
                self._ui.depackage_statue.setText("反编译路径")
            else:
                self._ui.depackage_statue.setText("重新反编译")
            self._ui.depackage_statue.setEnabled(True)
            self._ui.depackage_loading_view.setVisible(False)

    def __depackage_click(self):
        if self.__result:
            os.startfile(self.__depackage_path)
        else:
           self.__init_depackage(True)

    def __show_info(self):
        self._ui.app_name.setText(self.__apk_info.aap_name)
        self._ui.package_name.setText(self.__apk_info.package_name)
        self._ui.apk_path.setText(self.__apk_info.apk_path)
        self._ui.version_name.setText(self.__apk_info.version_name)
        self._ui.version_code.setText(self.__apk_info.version_code)
        self._ui.target_version.setText(self.__apk_info.target_version)
        self._ui.min_version.setText(self.__apk_info.min_version)
        self._ui.abis.setText(self.__apk_info.abis)
        self._ui.langs.setText(self.__apk_info.langs)

    def __get_value(self, info_content, target_property):
        return info_content.split(target_property)[1:][0].split("'")[1:2][0]
    
    def __get_list(self, info_content, target_property, last_tag):
        content = info_content.split(target_property)[1:][0]
        if last_tag !="":
            content = content.split(last_tag)[:1][0]
        return content.replace("'","").strip().replace(" ", ", ")
        
        
        
