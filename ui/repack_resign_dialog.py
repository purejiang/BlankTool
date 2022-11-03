# -*- coding:utf-8 -*-

from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from ui.repack_widget import RePackWidget
from ui.resign_widget import ReSignWidget

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
    
    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.repack_resign_dialog_title_bar.addWidget(self.title_bar)
        self.__show_repack_widget()
       
    def _setup_qss(self):
        self.setWindowTitle(self.__TITLE)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.repack_dir_btn.clicked.connect(self.__show_repack_widget)
        self._ui.resign_apk_btn.clicked.connect(self.__show_resign_widget)
    
    def __show_repack_widget(self):
        for i in range(self._ui.repackage_layout.count()):
            self._ui.repackage_layout.itemAt(i).widget().deleteLater()
        self._ui.repackage_layout.addWidget(RePackWidget(self))
        
    def __show_resign_widget(self):
        for i in range(self._ui.repackage_layout.count()):
            self._ui.repackage_layout.itemAt(i).widget().deleteLater()
        self._ui.repackage_layout.addWidget(ReSignWidget(self))
        
