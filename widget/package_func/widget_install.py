# -*- coding:utf-8 -*-
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseFile
from viewmodel.aab_viewmodel import AabViewModel
from viewmodel.apk_viewmodel import ApkViewModel

from widget.custom.toast import Toast
from widget.function.widget_function import FunctionWidget
from widget.step_info.widget_step_info import StepInfoWidget


class InstallWidget(FunctionWidget):
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

    def __install(self):
        # 清除list中的item
        self.__widget_install_step_info._clear()

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
        self.__widget_install_step_info.loadStep(currentTime(), "安装 APK 成功", "", True)
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __apkInstallFailure(self, code, message, other_info):
        self.__widget_install_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __apkInstallPrgress(self, progress, message, other_info, is_success):
        self.__widget_install_step_info.loadStep(currentTime(), message, other_info, is_success)

    def __aabInstallSuccess(self):
        self.__widget_install_step_info.loadStep(currentTime(), "安装 AAB 成功", "", True)
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __aabInstallFailure(self, code, message, other_info):
        self.__widget_install_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 允许点击
        self._ui.btn_select_install.setEnabled(True)
        self._ui.btn_install.setEnabled(True)

    def __aabInstallPrgress(self, progress, message, other_info, is_success):
        self.__widget_install_step_info.loadStep(currentTime(), message, other_info, is_success)

    def _entry(self):
        return super()._entry()
