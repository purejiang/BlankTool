# -*- coding:utf-8 -*-

from PySide2.QtCore import Qt
from common.constant import CACHE_PATH

from ui.base_widget import BaseWidget
from ui.install_dialog import InstallDialog
from ui.progressbar_dialog import ProgressBarDialog
from utils.file_helper import FileHelper

class OtherBarWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/7/13

    其他工具

    """

    __UI_FILE = "./res/ui/other_bar_widget.ui"
    __QSS_FILE = "./res/qss/other_bar_widget.qss"

    def __init__(self, application) -> None:
        super(OtherBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)

    def _setup_qss(self):
        # 设置 window 背景透明，如果设置 window 的颜色，在最小化和恢复的时候，左上角会有明显的系统 ui 闪现
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 去标题栏，状态栏
        self.setWindowFlag(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        self._ui.install_apk_aab_btn.clicked.connect(self.__on_install)
        self._ui.clean_cache_btn.clicked.connect(self.__on_clean_cache)

    def __on_install(self):
        self.install_dialog = InstallDialog(self)
        self.install_dialog.show()
    
    def __on_clean_cache(self):
        self.progressbar_dialog = ProgressBarDialog(self, "清理缓存", 0, 100, self.__clean_cache)
        self.progressbar_dialog.progress_callback(msg="清理中...")
        self.progressbar_dialog.show()
    
    def __clean_cache(self):
        try:
            FileHelper.delLongPathDir(CACHE_PATH)
            self.progressbar_dialog.progress_callback(100, msg="清理完成")
        except Exception as e:
            print(str(e))
            self.progressbar_dialog.progress_callback(100, msg="清理失败")
