# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from ui.repack_widget import RePackWidget

class RePackReSignDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/8/26

    重打包 apk 或者重签名 apk 的功能弹框

    """
    __UI_FILE = "./res/ui/repack_resign_dialog.ui"
    __QSS_FILE = "./res/qss/repack_resign_dialog.qss"
    __TITLE = "repack / resign"

    def __init__(self, main_window):
        super(RePackReSignDialog, self).__init__(main_window)
        pass
    
    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.repack_resign_dialog_title_bar.addWidget(self.title_bar)
        self.repack_widget = RePackWidget(self)
        self._ui.repackage_layout.addWidget(self.repack_widget)

       
    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        pass
