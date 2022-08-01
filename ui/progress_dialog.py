# -*- coding:utf-8 -*-


from time import sleep
import time
from PySide2.QtCore import Qt
from ui.base_dialog import BaseDialog


class ProgressDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/7/12

    通用的进度条弹出框，不执行操作，只做展示

    """
    __UI_FILE = "./res/ui/progressbar_dialog.ui"
    __QSS_FILE = "./res/qss/progressbar_dialog.qss"
    def __init__(self, main_window, title, close_func, min_value=0, max_value=100):
        self.__title = title
        self.__min_value = min_value
        self.__max_value = max_value
        self.__close_func = close_func
        super(ProgressDialog, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self._ui.progressbar_title_label.setText(self.__title)
        self._ui.progress_bar.setMinimum(self.__min_value)
        self._ui.progress_bar.setMaximum(self.__max_value)
        self._ui.progress_bar.setVisible(True)
        self._ui.progress_confirm_btn.setVisible(False)
        

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.progress_confirm_btn.clicked.connect(self.close)

    def keyPressEvent(self, e):
        # 键盘事件
        # if e.key() == Qt.Key_Escape:
        #     self.close()
        pass

    def dismiss(self):
        time.sleep(3)
        self.close()
        if self.__close_func:
            print("close_func()")
            self.__close_func()

    def progress_callback(self, progress=None, msg=None):
        if progress:
            self.__set_progress(progress)
        if msg:
            self.__set_msg(msg)
    
    def showEnd(self, confirm_msg, func=None):
        self.__close_func = func
        self._ui.progress_bar.setVisible(False)
        self._ui.progress_confirm_btn.setVisible(True)
        self._ui.progress_confirm_btn.setText(confirm_msg)

    def __set_progress(self, value):
        print("progress_bar.setvalue:"+str(value))
        self._ui.progress_bar.setValue(value)
    
    def __set_msg(self, msg):
        print("progress_bar.setText:"+str(msg))
        self._ui.progressbar_message_label.setText(msg)
            

            
            