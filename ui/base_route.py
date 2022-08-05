# -*- coding:utf-8 -*-
from abc import abstractmethod

from PySide2.QtGui import Qt,QIcon
from PySide2.QtWidgets import QMainWindow
from ui.base_ui import BaseUi

class BaseRoute(QMainWindow, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的窗口

    """
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
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
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
