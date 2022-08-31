# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt
from ui.base_widget import BaseWidget
from ui.toast import Toast
from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile


class ChooseFileWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/8/26

    选择文件或者目录的自定义控件

    """
    __UI_FILE = "./res/ui/choose_file_widget.ui"
    __QSS_FILE = "./res/qss/choose_file_widget.qss"

    def __init__(self, main_window, btn_msg, title, type, change_linstener):
        super(ChooseFileWidget, self).__init__(main_window)
        self.title = title
        self.type = type
        self.change_linstener = change_linstener
        self.btn_msg = btn_msg
        self._init()

    def _init(self):
        self._ui.choose_file_btn.setText(self.btn_msg)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # view
        self._ui.choose_file_btn.clicked.connect(self.__choose_file)
        self._ui.choose_file_path_edt.textChanged.connect(self.__sync_file_path)

    def keyPressEvent(self, e):
        # 键盘事件
        if e.key() == Qt.Key_Escape:
            # self.close()
            pass
        
    def __sync_file_path(self):
        file_path = self._ui.choose_file_path_edt.text().strip()
        self.change_linstener(file_path)

    def __choose_file(self):
        file_path = chooseFile(self, self.title, self.type)
        self._ui.choose_file_path_edt.setText(file_path)

    def check(self):
        file_path = self._ui.choose_file_path_edt.text()
        return FileHelper.fileExist(file_path)
