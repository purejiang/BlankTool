# -*- coding:utf-8 -*-

from widget.base.base_widget import BaseWidget

class MainTitilBar(BaseWidget):
    """

    @author: purejiang
    @created: 2023/2/21

    mainWidnow 上的标题栏

    """
    __UI_FILE = "./res/ui/widget_main_widow_titlebar.ui"
    __QSS_FILE = "./res/qss/widget_main_widow_titlebar.qss"

    def __init__(self, main_window) -> None:
        super(MainTitilBar, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)

    def _onPreShow(self):
        pass

    def _setupListener(self):
        self._ui.btn_close_window.clicked.connect(self.__onWindowClose)
        self._ui.btn_tool_setting.clicked.connect(self.__onOpenSetting)
        self._ui.btn_min_window.clicked.connect(self.__onWindowMin)

    def setTitle(self, title):
        self._ui.lb_main_widow_titlebar.setText(title)

    
    def __onWindowClose(self):
        """
        关闭程序
        """
        self._win.close()


    def __onOpenSetting(self):
        """
        打开设置
        """
        pass

    def __onWindowMin(self):
        """
        最小化窗口
        """
        self._win.showMinimized()