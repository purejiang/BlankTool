# -*- coding:utf-8 -*-

import base64
from time import sleep
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap,QIcon
from viewmodel.blank_viewmodel import BlankViewModel
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar
from widget.base.base_window import BaseWindow
from widget.window_main import MainWindow

class InitWindow(BaseWindow):
    """

    @author: purejiang
    @created: 2022/4/12

    初始化页面，由于这一步还没有加载.rcc， 所以样式和ui只能通过py代码配置

    """
    __icon_str_base64 ="iVBORw0KGgoAAAANSUhEUgAAAIAAAACAAQMAAAD58POIAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAZQTFRFAAAA////pdmf3QAAAC5JREFUeJxjYBgFowAFsP//x/gfBD6MChAnAARAgQaUUBwVGBUYFRh6AqOArgAA1FAdN5gPDpQAAAAASUVORK5CYII="

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
        self.blank_viewmodel = BlankViewModel(self)

    def _setupListener(self):
        self.blank_viewmodel.init_app_opreation.setListener(self.__initAppSuccess, self.__initAppProgress, self.__initAppFailure)
        self.blank_viewmodel.initApp()

    def __initAppSuccess(self):
        self.__label.setText("初始化完成")
        self.__progress_bar.setValue(100)
        self._jump(MainWindow, None)

    def __initAppFailure(self, code, msg):
        self.__label.setText("error, code:{0} msg:{1}".format(code, msg))

    def __initAppProgress(self, progress: int, msg: str, des: str):
        self.__label.setText(msg)
        self.__progress_bar.setValue(progress)

