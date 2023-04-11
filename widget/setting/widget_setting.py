# -*- coding:utf-8 -*-

from widget.base.base_widget import BaseWidget

class SettingWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/4/10

    设置界面

    """
    __UI_FILE = "./res/ui/widget_setting.ui"
    __QSS_FILE = "./res/qss/widget_setting.qss"

    def __init__(self, main_window) -> None:
        super(SettingWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)

    def _onPreShow(self):
        pass

    def _setupListener(self):
       pass