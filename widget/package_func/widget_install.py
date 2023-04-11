# -*- coding:utf-8 -*-
import os
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseFile
from viewmodel.aab_viewmodel import AabViewModel
from viewmodel.apk_viewmodel import ApkViewModel

from widget.base.base_widget import BaseWidget
from widget.custom.toast import Toast
from widget.step_info.widget_step_info import StepInfoWidget


class InstallWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/3/3

    安装 Apk/Aab 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_install.ui"
    __QSS_FILE = "./res/qss/widget_install.qss"

    def __init__(self, main_window) -> None:
        super(InstallWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)

    def _onPreShow(self):
        self.__apk_viewmodel = ApkViewModel(self)
        self.__aab_viewmodel = AabViewModel(self)
        self.__widget_install_step_info = StepInfoWidget()
        self.layout_install_step_info.addWidget(self.__widget_install_step_info)
        
    def _setupListener(self):
        self._ui.btn_select_install.clicked.connect(self.__chooseFile)
        self._ui.btn_install.clicked.connect(self.__install)

        self.__apk_viewmodel.install_apk_operation.setListener(self.__apkInstallSuccess, self.__apkInstallPrgress, self.__apkInstallFailure)
        self.__aab_viewmodel.install_aab_operation.setListener(self.__aabInstallSuccess, self.__aabInstallPrgress, self.__aabInstallFailure)
    
    def __chooseFile(self):
        file_path = chooseFile(self, "选取 Apk/aab", "安卓应用文件 (*.aab *.apk)")
        self._ui.edt_install_path.setText(file_path)
        # 清除list中的item
        self.__widget_install_step_info._clear()

    def __install(self):
        file_path = self._ui.edt_install_path.text()
        if not FileHelper.fileExist(file_path) or file_path=="":
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        if FileHelper.getSuffix(file_path) == ".aab":
            self.__aab_viewmodel.install(file_path, None)
        else:
             self.__apk_viewmodel.install(file_path)
       
        # 禁止点击
        self._ui.btn_select_install.setEnabled(False)
        self._ui.btn_install.setEnabled(False)

    def __apkInstallSuccess(self):
        self.__widget_install_step_info.loadStep("安装 APK 成功", currentTime(), "")
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __apkInstallFailure(self, code, msg):
        self.__widget_install_step_info.loadStep("code:{0}, msg:{1}".format(code, msg), currentTime(), "")
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __apkInstallPrgress(self, progress, title, des):
        self.__widget_install_step_info.loadStep(title, currentTime(), des)

    def __aabInstallSuccess(self):
        self.__widget_install_step_info.loadStep("安装 AAB 成功", currentTime(), "")
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __aabInstallFailure(self, code, msg):
        self.__widget_install_step_info.loadStep("code:{0}, msg:{1}".format(code, msg), currentTime(), "")
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __aabInstallPrgress(self, progress, title, des):
        self.__widget_install_step_info.loadStep(title, currentTime(), des)
