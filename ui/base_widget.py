# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt
from abc import abstractmethod
from PySide2.QtCore import Signal
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QWidget

from ui.base_ui import BaseUi


class BaseWidget(QWidget, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的控件

    """
    pressed = Signal([QWidget, QMouseEvent])

    def __init__(self, main_window):
        super(BaseWidget, self).__init__()
        self._win = main_window
        self._on_pre_show()
        self._setup_qss()
        self._setup_listener()
        
    def _loadQss(self, qss_file):
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(super()._loadQss(qss_file))

    def _mousePressEvent(self, event):
        self.pressed.emit(self, event)
    
    @abstractmethod
    def _on_pre_show(self):
        pass

    @abstractmethod
    def _setup_qss(self):
        pass

    @abstractmethod
    def _setup_listener(self):
        pass
