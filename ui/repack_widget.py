# -*- coding:utf-8 -*-


from PySide2.QtCore import Qt
from ui.base_widget import BaseWidget
from ui.choose_file_widget import ChooseFileWidget
from ui.toast import Toast
from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile

class RePackWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/8/26

    重打包 apk 的界面

    """
    __UI_FILE = "./res/ui/repack_widget.ui"
    __QSS_FILE = "./res/qss/repack_widget.qss"

    def __init__(self, main_window):
        super(RePackWidget, self).__init__(main_window)
        self.left = self.geometry().x() + self.size().width() / 2
        self.top = self.geometry().y() + self.size().height() / 13
        self.reapck_path=""
        self.keystore_path=""

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.choose_repack_path_widget = ChooseFileWidget(self, "重编路径", "选择重编译路径", "/", self.__repack_path_change)
        self._ui.choose_repack_path_layout.addWidget(self.choose_repack_path_widget)
        self.choose_keystore_path_widget = ChooseFileWidget(self, "签名文件", "选择签名文件", "签名文件 (*.jks *.keystore)", self.__keystore_path_change)
        self._ui.choose_keystore_path_layout.addWidget(self.choose_keystore_path_widget)
        self._ui.reapckage_btn.setEnabled(False)
        
    def __repack_path_change(self, path):
        if path is None or len(path) == 0:
            self._ui.reapckage_btn.setEnabled(False)
        else:
            self.reapck_path = path
            if len(self.keystore_path)!=0:
                self._ui.reapckage_btn.setEnabled(True)
    
    def __keystore_path_change(self, path):
        if path is None or len(path) == 0:
            self._ui.reapckage_btn.setEnabled(False)
        else:
            self.keystore_path = path
            if len(self.reapck_path)!=0:
                self._ui.reapckage_btn.setEnabled(True)

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.reapckage_btn.clicked.connect(self.__repack)
    
    def __repack(self):
        self.reapck_path
        self.keystore_path
        pass
