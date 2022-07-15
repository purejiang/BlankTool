# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt

from ui.base_widget import BaseWidget
from ui.parse_apk_dialog import ParseApkDialog

class ApkBarWidget(BaseWidget):

    __UI_FILE = "./res/ui/apk_bar_widget.ui"
    __QSS_FILE = "./res/qss/apk_bar_widget.qss"

    def __init__(self, application) -> None:
        super(ApkBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.apk_info_btn.clicked.connect(self.__on_parse_apk)
    
    def __on_parse_apk(self):
        self.parse_apk_dialog = ParseApkDialog(self)
        self.parse_apk_dialog.show()
