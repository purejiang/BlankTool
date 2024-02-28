# -*- coding:utf-8 -*-

import os
from common.constant import Constant

from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseFile

from viewmodel.apk_viewmodel import ApkViewModel
from vo.apk_info import ApkInfo

from widget.custom.toast import Toast
from widget.function.widget_function import FunctionWidget
from widget.step_info.widget_step_info import StepInfoListWidget


class ParseApkWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/2/23

    解析 Apk 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_parse_apk.ui"
    __QSS_FILE = "./res/qss/widget_parse_apk.qss"

    def __init__(self, main_window) -> None:
        super(ParseApkWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.apk_info:ApkInfo = None
        self.__is_pass_dex =False
        self.__is_only_res =False

    def _onHide(self):
        pass
    
    def _onShow(self):
        pass
        
    def _onPreShow(self):
        self.apk_viewmodel = ApkViewModel(self)
        self._ui.pb_depack_progress.setVisible(False)
        self.__widget_parse_step_info = StepInfoListWidget()
        self.layout_parse_step_info.addWidget(self.__widget_parse_step_info)
    
    def _setupListener(self):
        self._ui.btn_select_apk.clicked.connect(self.__chooseFile)
        self._ui.btn_parse_apk.clicked.connect(self.__startParse)
        self._ui.btn_depack_dir_path.clicked.connect(self.__openDepackDirPath)

        self.apk_viewmodel.parse_apk_operation.setListener(self.__parseApkSuccess, self.__parseApkProgress, self.__parseApkFailure),
        self._ui.ckb_pass_dex.stateChanged.connect(self.__isPassDex)
        self._ui.ckb_only_res.stateChanged.connect(self.__isOnlyRes)

    def __isPassDex(self, checked):
        self.__is_pass_dex = checked

    def __isOnlyRes(self, checked):
        self.__is_only_res = checked

    def __chooseFile(self):
        file_path = chooseFile(self, "选取 Apk", "安卓应用文件 (*.apk)")
        self._ui.edt_parse_apk_path.setText(file_path)
    
    def __startParse(self):
        ApkViewModel._parse_apk_info = None
        self.apk_info = None
        # 清除list中的item
        self.__widget_parse_step_info.clearAll()
        apk_path = self._ui.edt_parse_apk_path.text()
        if not FileHelper.fileExist(apk_path) or apk_path=="":
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        # 展示进度条
        self._ui.pb_depack_progress.setValue(0)
        self._ui.pb_depack_progress.setVisible(True)
        self._ui.btn_depack_dir_path.setVisible(False)
        # 禁止点击
        self._ui.widget_parse_apk_fuction_bar.setDisabled(True)
        self.apk_viewmodel.parseApk(apk_path, self.__is_pass_dex, self.__is_only_res)

    def __parseApkSuccess(self, apk_info):
        self.apk_info = apk_info
        ApkViewModel._parse_apk_info = apk_info
        self.__widget_parse_step_info.loadStep("分析成功", currentTime(), "", True)
        # 恢复点击
        self._ui.widget_parse_apk_fuction_bar.setDisabled(False)
        # 隐藏进度条
        self._ui.pb_depack_progress.setValue(100)
        self._ui.pb_depack_progress.setVisible(False)
        self._ui.btn_depack_dir_path.setVisible(True)

    def __parseApkProgress(self, progress, message, other_info, is_success):
        self._ui.pb_depack_progress.setValue(progress)
        self.__widget_parse_step_info.loadStep(currentTime(), message, other_info, is_success)

    def __parseApkFailure(self, code, message, other_info):
        self.__widget_parse_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 恢复点击
        self._ui.widget_parse_apk_fuction_bar.setDisabled(False)
        # 隐藏进度条
        self._ui.pb_depack_progress.setValue(100)
        self._ui.pb_depack_progress.setVisible(False)
        self._ui.btn_depack_dir_path.setVisible(True)
    
    def __openDepackDirPath(self):
        if self.apk_info!=None:
            FileHelper.showInExplorer(self.apk_info.output_path)
        else:
            FileHelper.showInExplorer(Constant.Path.PARSE_CACHE_PATH)