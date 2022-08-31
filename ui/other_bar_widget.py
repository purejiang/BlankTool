# -*- coding:utf-8 -*-

from manager.blank_manager import BlankManager

from ui.base_widget import BaseWidget
from ui.install_dialog import InstallDialog
from ui.progress_dialog import ProgressDialog
from viewmodel.blank_viewmodel import BlankViewModel

class OtherBarWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/7/13

    其他的功能控件

    """

    __UI_FILE = "./res/ui/other_bar_widget.ui"
    __QSS_FILE = "./res/qss/other_bar_widget.qss"

    def __init__(self, application) -> None:
        super(OtherBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.blank_viewmodel = BlankViewModel(self)

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        self.blank_viewmodel.clean_cache_success.connect(self.__clean_cache_success)
        self.blank_viewmodel.clean_cache_progress.connect(self.__clean_cache_progres)
        self.blank_viewmodel.clean_cache_failure.connect(self.__clean_cache_failue)

        self._ui.install_apk_aab_btn.clicked.connect(self.__install)
        self._ui.clean_cache_btn.clicked.connect(self.__clean_cache)

    def __install(self):
        self.install_dialog = InstallDialog(self)
        self.install_dialog.show()
    
    def __clean_cache(self):
        self.progressbar_dialog = ProgressDialog(self, "清理缓存", None)
        self.progressbar_dialog.progress_callback(msg="清理中...")
        self.progressbar_dialog.show()
        self.blank_viewmodel.clean_cache()

    def __clean_cache_progres(self, progress, msg):
        self.progressbar_dialog.progress_callback(progress, msg)

    def __clean_cache_success(self):
        self.progressbar_dialog.progress_callback(100, "清理缓存成功")
        self.progressbar_dialog.showEnd("确认")
            
    def __clean_cache_failue(self, code, msg):
        self.progressbar_dialog.progress_callback(100, "{0} : {1}".format(code, msg))
        self.progressbar_dialog.showEnd("确认")
