# -*- coding:utf-8 -*-
from common.constant import Constant
from widget.base.base_window import BaseWindow
from widget.function.widget_function import FunctionWidget
from widget.function.widget_function_tab_bar import FunctionTabBarWidget
from widget.widget_main_widow_titlebar import MainTitilBar


class MainWindow(BaseWindow):
    """

    @author: purejiang
    @created: 2022/2/21

    主页面

    """
    __UI_FILE = "./res/ui/window_main.ui"
    __QSS_FILE = "./res/qss/window_main.qss"
    __ICON = "./res/img/app_icon_small"
    __TITLE = Constant.AppInfo.APP_NAME

    def __init__(self, application) -> None:
        super(MainWindow, self).__init__(application, self.__UI_FILE, self.__QSS_FILE, self.__ICON)

    def _onPreShow(self, data):
        self._moveCenter()
        self.setWindowTitle(Constant.AppInfo.APP_NAME)
        self.__title_bar = MainTitilBar(self)
        self.__title_bar.setTitle(self.__TITLE)
        self.__function_tab_bar = FunctionTabBarWidget(self.__itemClickCallback)
        self._ui.layout_main_window_title_bar.addWidget(self.__title_bar)
        self._ui.layout_function_bar.addWidget(self.__function_tab_bar)

    def _setupListener(self):
        pass

    def _onAfterShow(self, data):
       pass

    def __itemClickCallback(self, content_widget:FunctionWidget):
        for i in range(self._ui.layout_main_content.count()):
            self._ui.layout_main_content.itemAt(i).widget().setVisible(False)
        content_widget.setVisible(True)
        content_widget._entry()
        self._ui.layout_main_content.addWidget(content_widget)
