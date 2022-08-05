# -*- coding:utf-8 -*-
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDesktopWidget
from manager.blank_manager import BlankManager
from ui.aab_bar_widget import AabBarWidget
from ui.apk_bar_widget import ApkBarWidget
from ui.base_route import BaseRoute
from ui.big_titlebar_widget import BigTitilBar
from ui.other_bar_widget import OtherBarWidget


class MainRoute(BaseRoute):
    """

    @author: purejiang
    @created: 2022/7/2

    主页面

    """
    __UI_FILE = "./res/ui/main_route.ui"
    __QSS_FILE = "./res/qss/main_route.qss"
    __TITLE = "BlankTool"

    def __init__(self, application) -> None:
        super(MainRoute, self).__init__(application)
        # 工具的初始化
        BlankManager.init()

    def _on_pre_show(self, data):
        self._loadUi(self.__UI_FILE)
        self.__title_bar = BigTitilBar(self)
        self.__title_bar.set_title("Blank Tool v4.0")
        self._ui.main_title_bar.addWidget(self.__title_bar)
        self.__aab_bar = AabBarWidget(self)
        self._ui.aab_bar_layout.addWidget(self.__aab_bar)
        self.__apk_bar = ApkBarWidget(self)
        self._ui.apk_bar_layout.addWidget(self.__apk_bar)
        self.__other_bar = OtherBarWidget(self)
        self._ui.other_bar_layout.addWidget(self.__other_bar)
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        return super()._setup_listener()

    def _on_after_show(self, data):
        return super()._on_after_show(data)

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
