# -*- coding:utf-8 -*-
from abc import abstractmethod

from PySide2.QtGui import Qt,QIcon
from PySide2.QtWidgets import QMainWindow
from ui.base_ui import BaseUi

class BaseRoute(QMainWindow, BaseUi):

    def __init__(self, application):
        super(BaseRoute, self).__init__()
        self.application = application
        self.application.addWindow(self)
        self.setWindowIcon(QIcon("./res/img/app_icon_small"))

    def _onMin(self):
        """
        窗口最小化
        """
        self.setWindowState(Qt.WindowMinimized)

    def _jump2Window(self, from_window, to_window_clazz, data):
        self.application.jump_to_window(from_window, to_window_clazz, data)

    def _loadQss(self, qss_file):
         self.setStyleSheet(super()._loadQss(qss_file))

    @abstractmethod
    def _on_pre_show(self, data):
        pass

    @abstractmethod
    def _on_after_show(self, data):
        pass

    @abstractmethod
    def _onHide(self):
        pass

    @abstractmethod
    def _setup_qss(self):
        pass

    @abstractmethod
    def _setup_listener(self):
        pass

    def _onJumpFinish(self):
        pass
