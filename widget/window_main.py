# -*- coding:utf-8 -*-
from common.constant import Constant
from widget.base.base_window import BaseWindow
from widget.function.widget_function_tab_bar import FuctionListItem, FunctionTabBarWidget
from widget.widget_main_widow_titlebar import MainTitleBar


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
        self.current_item = None

    def _onPreShow(self, data):
        super()._onPreShow(data)
        self.setWindowTitle(Constant.AppInfo.APP_NAME)
        self.__title_bar = MainTitleBar(self)
        self.__title_bar.setTitle(self.__TITLE)
        self.__function_tab_bar = FunctionTabBarWidget()
        self.__function_tab_bar.setItemClickCallback(self.__itemClickCallback)
        self._ui.layout_main_window_title_bar.addWidget(self.__title_bar)
        self._ui.layout_function_bar.addWidget(self.__function_tab_bar)

    def _setupListener(self):
        pass

    def _onAfterShow(self, data):
        # 设置第一项为当前选定项，并模拟点击该项
        self.__function_tab_bar.clickItem(0, 0)

    def __itemClickCallback(self, item:FuctionListItem):
        if item==self.current_item and item.func.function_widget.isVisible:
            return
        self.__hideContentWidget()
        self.current_item = item
        self._ui.layout_main_content.addWidget(item.func.function_widget)
        item.func.function_widget.setVisible(True)
    
    def __hideContentWidget(self):
        for i in range(self._ui.layout_main_content.count()):
            item_widget = self._ui.layout_main_content.itemAt(i).widget()
            if item_widget.isVisible():
                self._ui.layout_main_content.itemAt(i).widget().setVisible(False)
