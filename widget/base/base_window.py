# -*- coding:utf-8 -*-
from abc import abstractmethod

from PySide6.QtGui import QGuiApplication,Qt,QIcon
from PySide6.QtWidgets import QMainWindow
from widget.base.base_ui import BaseUi

class BaseWindow(QMainWindow, BaseUi):
    """

    @author: purejiang
    @created: 2022/7/7

    基础的窗口

    """
    def __init__(self, application, ui_file, qss_file, icon):
        super(BaseWindow, self).__init__()
        self._application = application
        # 鼠标位置偏移值
        self.__offset = None
        self._icon = icon
        self._initView(ui_file, qss_file)

    def _onMin(self):
        """
        窗口最小化
        """
        self.setWindowState(Qt.WindowMinimized)
    
    def _moveCenter(self):    
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _jump(self, to_window_clazz, data):
        self._application.jump(self, to_window_clazz, data)

    def _initView(self, ui_file, qss_file):
        self._application.addWindow(self)
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground) 
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        if ui_file is not None:
            self._loadUi(ui_file)
        if qss_file is not None:
            qss_str = "{0}\n{1}".format(super()._loadQss(self._BASE_QSS_FILE), super()._loadQss(qss_file))
            self.setStyleSheet(qss_str)
        if self._icon is not None:
            self.setWindowIcon(QIcon(self._icon))

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
    def _onPreShow(self, data):
        pass

    @abstractmethod
    def _onAfterShow(self, data):
        pass

    @abstractmethod
    def _onHide(self):
        pass

    @abstractmethod
    def _setupListener(self):
        pass

    def _onJumpFinish(self):
        pass

