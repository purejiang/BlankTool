# -*- coding:utf-8 -*-

from PySide6.QtCore import Qt
from abc import abstractmethod
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget

from widget.base.base_ui import BaseUi


class BaseWidget(QWidget, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的控件

    """
    __PRESSED = Signal([QWidget, QMouseEvent])

    def __init__(self, main_window, ui_file, qss_file):
        self._win = main_window
        super(BaseWidget, self).__init__()
        self._initView(ui_file, qss_file)
        self._onPreShow()
        self._setupListener()
    
    def _initView(self, ui_file, qss_file):
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 加载全局默认风格的qss，以及自定义的qss（可覆盖默认的）
        if ui_file is not None:
            self._loadUi(ui_file)
        if qss_file is not None:
            qss_str = "{0}\n{1}".format(self._loadQss(self._BASE_QSS_FILE), self._loadQss(qss_file))
            self.setStyleSheet(qss_str)

    def _mousePressEvent(self, event):
        self.__PRESSED.emit(self, event)
    
    @abstractmethod
    def _onPreShow(self):
        pass

    @abstractmethod
    def _setupListener(self):
        pass
