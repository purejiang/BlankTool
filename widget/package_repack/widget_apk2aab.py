# -*- coding:utf-8 -*-

from widget.function.widget_function import FunctionWidget

class Apk2AabWidget(FunctionWidget):
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

    def _entry(self):
        pass
    
    def __initView(self):
        pass

    def _onPreShow(self):
        pass
        
    def _setupListener(self):
        pass