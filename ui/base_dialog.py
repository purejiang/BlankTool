# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt
from ui.base_ui import BaseUi
from abc import abstractmethod
from PySide2.QtCore import Signal
from PySide2.QtGui import QMouseEvent,QIcon
from PySide2.QtWidgets import QDialog

class BaseDialog(QDialog, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的弹出框

    """
    pressed = Signal([QDialog, QMouseEvent])

    def __init__(self, main_window):
        super(BaseDialog, self).__init__()
        self.win = main_window
        self.setWindowIcon(QIcon("./res/img/app_icon_small"))
        self._on_pre_show()
        self._setup_qss()
        self._setup_listener()
        
    def _loadQss(self, qss_file):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(super()._loadQss(qss_file))
        
    # 实现可拖动
    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()
    # 实现可拖动
    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)
    
    @abstractmethod
    def _on_pre_show(self):
        pass

    @abstractmethod
    def _setup_qss(self):
        pass

    @abstractmethod
    def _setup_listener(self):
        pass
