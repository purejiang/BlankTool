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
        self.application = application
        self.application.addWindow(self)
        self.Move = True
        self._loadUi(ui_file)
        self._loadQss(qss_file)
        self.setWindowIcon(QIcon(icon))

    def _onMin(self):
        """
        窗口最小化
        """
        self.setWindowState(Qt.WindowMinimized)
    
    def _moveCenter(self):    # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _jump2Window(self, from_window, to_window_clazz, data):
        self.application.jump2Window(from_window, to_window_clazz, data)

    def _loadQss(self, qss_file):
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground) 
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(super()._loadQss(qss_file))

    def keyPressEvent(self, e):
        # 键盘事件
        if e.key() == Qt.Key_Escape:
            # self.close()
            pass

    def mousePressEvent(self, event):
        # 鼠标点击事件
        if event.button() == Qt.LeftButton:
            # 设定bool为True
            self.Move = True
            # 记录起始点坐标
            self.Point = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 鼠标移动事件，左键+移动=拖动
        if Qt.LeftButton and self.Move:
            # 移动窗口到鼠标的坐标点
            self.move(QMouseEvent.globalPos() - self.Point)
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):
        # 结束事件
        self.Move = False
    
    
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

