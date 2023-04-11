# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from PySide6.QtCore import Qt
from widget.base.base_ui import BaseUi
from abc import abstractmethod
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent,QIcon,QGuiApplication
from PySide6.QtWidgets import QDialog

class BaseDialog(QDialog, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的弹出框

    """
    pressed = Signal([QDialog, QMouseEvent])

    def __init__(self, main_window, ui_file, qss_file, icon):
        super(BaseDialog, self).__init__()
        self._win = main_window
        self.setWindowIcon(QIcon(icon))
        self._loadUi(ui_file)
        self._loadQss(qss_file)
        self._onPreShow()
        self._setupListener()
        self.move_press=0
        
    def _loadQss(self, qss_file):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(super()._loadQss(qss_file))
    
    def _moveCenter(self):    # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 实现可拖动
    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    # 实现可拖动
    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
    
    @abstractmethod
    def _onPreShow(self):
        pass

    @abstractmethod
    def _setupListener(self):
        pass
