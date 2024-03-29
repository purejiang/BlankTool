# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from PySide6.QtCore import Qt
from widget.base.base_ui import BaseUi, MyUiLoad
from abc import abstractmethod
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent,QGuiApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QFile, QIODevice, QMetaObject

class BaseDialog(QDialog, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的弹出框

    """
    pressed = Signal([QDialog, QMouseEvent])

    _BASE_QSS_FILE = "./res/qss/widget_base.qss"

    def __init__(self, parent, ui_file, qss_file):
        super(BaseDialog, self).__init__()
        self._parent = parent
        self._initView(ui_file, qss_file)
        self._onPreShow()
        self._setupListener()
        self.__offset = None
        
    def _initView(self, ui_file, qss_file):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        # 设置这个不会在任务栏新建选项卡，而且能全屏拖动
        self.setWindowFlags(Qt.FramelessWindowHint| self.windowFlags() | Qt.Tool)
        if ui_file is not None:
            self._loadUi(ui_file)
        if qss_file is not None:
            qss_str = "{0}\n{1}".format(super()._loadQss(self._BASE_QSS_FILE), super()._loadQss(qss_file))
            self.setStyleSheet(qss_str)
    
    def _moveCenter(self):    
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 获取鼠标相对于窗口位置的偏移值
            self.__offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.__offset is not None:
            # 移动窗口
            self.move(event.globalPos() - self.__offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 释放鼠标
            self.__offset = None

    def keyPressEvent(self, e):
        # 键盘事件
        if e.key() == Qt.Key_Escape:
            # self.close()
            pass
    
    @abstractmethod
    def _onPreShow(self):
        pass

    @abstractmethod
    def _setupListener(self):
        pass
