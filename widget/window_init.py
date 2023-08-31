# -*- coding:utf-8 -*-

import base64
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from viewmodel.app_viewmodel import AppViewModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from widget.base.base_window import BaseWindow
from widget.window_main import MainWindow


class InitWindow(BaseWindow):
    """

    @author: purejiang
    @created: 2022/4/12

    初始化页面，由于这一步还没有加载.rcc， 所以样式和ui只能通过py代码配置

    """
    __icon_str_base64 = "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"

    def __init__(self, application) -> None:
        super(InitWindow, self).__init__(application, None, None, None)
        self.__initView()

    def __initView(self):
        self._moveCenter()
        # 创建一个进度条
        self.__progress_bar = QProgressBar()

        self.__progress_bar.setMaximum(100)
        self.__progress_bar.setMinimum(0)
        self.__progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid gray;
                border-radius: 5px;
                background-color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #46A6FD;
                border-radius: 5px;
            }
        """)
        # 创建一个按钮
        self.__label = QLabel("应用初始化")
        self.__label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: "Microsoft YaHei";
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self.__label.setAlignment(Qt.AlignCenter)
        self.__progress_bar.setAlignment(Qt.AlignCenter)
        # 将进度条和按钮添加到主窗口中
        layout = QVBoxLayout()

        layout.addWidget(self.__label)
        layout.addWidget(self.__progress_bar)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        # 设置名称，可以在qss中引用到
        central_widget.setObjectName("init_widget")
        self.setCentralWidget(central_widget)
        self.setStyleSheet("""
            QWidget#init_widget {
                border-radius: 2px;
                min-width: 360px;
                min-height: 240px;
                background-color: #3D3D3D;
            }
        """)
        pixmap = QPixmap()
        image_bytes = base64.b64decode(self.__icon_str_base64)
        pixmap.loadFromData(image_bytes)
        self.setWindowIcon(QIcon(pixmap))

    def _onPreShow(self, data):
        self.app_viewmodel = AppViewModel(self)

    def _setupListener(self):
        self.app_viewmodel.init_app_opreation.setListener(
            self.__initAppSuccess, self.__initAppProgress, self.__initAppFailure)
        self.app_viewmodel.initApp()

    def __initAppSuccess(self):
        self.__label.setText("初始化完成")
        self.__progress_bar.setValue(100)
        self._jump(MainWindow, None)

    def __initAppFailure(self, code, msg):
        self.__label.setText("error, code:{0} msg:{1}".format(code, msg))

    def __initAppProgress(self, progress: int, message: str, other_info: str, is_success: bool):
        self.__label.setText(message)
        self.__progress_bar.setValue(progress)
