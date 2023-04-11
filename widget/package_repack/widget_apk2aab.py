# -*- coding:utf-8 -*-
import os
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseDir
from viewmodel.apk_viewmodel import ApkViewModel
from viewmodel.signer_viewmodel import SignerViewModel
from widget.base.base_widget import BaseWidget
from widget.custom.toast import Toast
from widget.step_info.widget_step_info import StepInfoWidget



class Apk2AabWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/4/11

    APK 转 AAB 功能页面
    """
    __UI_FILE = "./res/ui/widget_apk2aab.ui"
    __QSS_FILE = "./res/qss/widget_apk2aab.qss"

    def __init__(self, main_window) -> None:
        super(Apk2AabWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__initView()


    def __initView(self):
        pass

    def _onPreShow(self):
        pass
        
    def _setupListener(self):
        pass