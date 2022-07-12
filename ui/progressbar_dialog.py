# -*- coding:utf-8 -*-

import time
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer
from ui.base_dialog import BaseDialog
from utils.work_thread import WorkThread


class ProgressBarDialog(BaseDialog):

    __UI_FILE = "./res/ui/progressbar_dialog.ui"
    __QSS_FILE = "./res/qss/progressbar_dialog.qss"

    def __init__(self, main_window, title, min_value, max_value, func):
        self.__title = title
        self.__func = func
        self.__min_value = min_value
        self.__max_value = max_value
        self.__thread = WorkThread(self.__func)
        self.__thread._state.connect(self.__sig_out)
        super(ProgressBarDialog, self).__init__(main_window)
        self.init()

    def init(self):
        self.__start_loader()

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self._ui.progressbar_title_label.setText(self.__title)
        self._ui.progress_bar.setMinimum(self.__min_value)
        self._ui.progress_bar.setMaximum(self.__max_value)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        pass

    def keyPressEvent(self, e):
        # 键盘事件
        # if e.key() == Qt.Key_Escape:
        #     self.close()
        pass

    def mousePressEvent(self, e):
        self.move_press = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        self.move(e.globalPos() - self.move_press)

    def set_progress(self, value):
        self._ui.progress_bar.setValue(value)
    
    def set_msg(self, msg):
        self._ui.progressbar_message_label.setText(msg)

    def __start_loader(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.__load_progress_bar)
        self.timer.start(600)

    def __load_progress_bar(self):
        self._ui.progress_bar.setValue(self._ui.progress_bar.value() + 1)  
        if self._ui.progress_bar.value()==5:
            self.__thread.start()

    def __sig_out(self, state):
        if state==1:
            if self._ui.progress_bar.value() < 100:
                self.set_progress(100)
            self.timer.stop()
            time.sleep(3)
            self.close()