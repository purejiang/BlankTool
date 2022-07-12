# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from abc import abstractmethod
from PySide2.QtCore import Signal
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QDialog

from ui.base_ui import BaseUi


class BaseDialog(QDialog, BaseUi):

    pressed = Signal([QDialog, QMouseEvent])

    def __init__(self, main_window):
        super(BaseDialog, self).__init__()
        self.win = main_window
        self._on_pre_show()
        self._setup_qss()
        self._setup_listener()
        
    def _loadQss(self, qss_file):
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
