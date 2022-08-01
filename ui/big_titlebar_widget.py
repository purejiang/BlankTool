# -*- coding:utf-8 -*-


from ui.base_widget import BaseWidget

class BigTitilBar(BaseWidget):
    """

    @author: purejiang
    @created: 2022/7/3

    widnow 上的标题栏

    """
    __UI_FILE = "./res/ui/big_title_bar_widget.ui"
    __QSS_FILE = "./res/qss/big_title_bar_widget.qss"

    def __init__(self, main_window) -> None:
        super(BigTitilBar, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
    
    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        self._ui.close_window_btn.clicked.connect(self.__on_click_close)
        self._ui.min_window_btn.clicked.connect(self.__on_click_min)
        self._ui.max_window_btn.clicked.connect(self.__on_click_max)

    def set_title(self, title):
        self._ui.big_title_bar_label.setText(title)

    def __on_click_close(self):
        self._win.close()

    def __on_click_max(self):
        if self._win.isMaximized():
            self._win.showNormal()
        else:
            self._win.showMaximized()

    def __on_click_min(self):
        self._win.showMinimized()