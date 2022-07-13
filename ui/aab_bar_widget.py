# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt

from ui.base_widget import BaseWidget
from ui.install_dialog import InstallDialog

class AabBarWidget(BaseWidget):

    __UI_FILE = "./res/ui/aab_bar_widget.ui"
    __QSS_FILE = "./res/qss/aab_bar_widget.qss"

    def __init__(self, application) -> None:
        super(AabBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)

    def _setup_qss(self):
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        pass
