# -*- coding:utf-8 -*-
from ui.base_widget import BaseWidget


class SmallTitilBar(BaseWidget):
    """

    @author: purejiang
    @created: 2022/10/10

    小标题栏/ dialog 上的标题栏

    """
    __UI_FILE = "./res/ui/small_title_bar_widget.ui"
    __QSS_FILE = "./res/qss/small_title_bar_widget.qss"

    def __init__(self, main_window) -> None:
        super(SmallTitilBar, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
    
    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        self._ui.close_window_btn.clicked.connect(self.__on_click_close)
    
    def set_title(self, title):
        self._ui.normal_title_bar_label.setText(title)
    
    def __on_click_close(self):
        self._win.close()