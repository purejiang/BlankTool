# -*- coding:utf-8 -*-

from widget.function.widget_function import FunctionWidget


class PullApksWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/3/3

    拉取设备中 Apk 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_pull_apks.ui"
    __QSS_FILE = "./res/qss/widget_pull_apks.qss"

    def __init__(self, main_window) -> None:
        super(PullApksWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)

    def _entry(self):
        pass
    
    def _onPreShow(self):
        self._loadUi(self.__UI_FILE)
    
    def _setupListener(self):
        pass
