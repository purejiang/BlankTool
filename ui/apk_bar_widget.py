# -*- coding:utf-8 -*-


from ui.base_widget import BaseWidget
from ui.parse_apk_dialog import ParseApkDialog
from ui.progress_dialog import ProgressDialog
from ui.pull_apk_dialog import PullApkDialog
from ui.repack_resign_dialog import RePackReSignDialog
from viewmodel.apk_viewmodel import ApkViewModel

class ApkBarWidget(BaseWidget):
    """
    @author: purejiang
    @created: 2022/7/7

    .aab 相关的功能控件

    """
    __UI_FILE = "./res/ui/apk_bar_widget.ui"
    __QSS_FILE = "./res/qss/apk_bar_widget.qss"

    def __init__(self, application) -> None:
        super(ApkBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.apk_viewmodel = ApkViewModel(self)

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self.apk_viewmodel.generate_list_success.connect(self.__get_apks_success)
        self.apk_viewmodel.generate_list_failure.connect(self.__get_apks_failure)

        self._ui.apk_info_btn.clicked.connect(self.__on_parse_apk)
        self._ui.pull_apk_btn.clicked.connect(self.__get_apk_list)
        self._ui.repack_resign_btn.clicked.connect(self.__repack_resign)
    
    def __on_parse_apk(self):
        self.parse_apk_dialog = ParseApkDialog(self)
        self.parse_apk_dialog.show()

    def __repack_resign(self):
        self.repack_resign_dialog = RePackReSignDialog(self)
        self.repack_resign_dialog.show()

    def __get_apk_list(self):
        self.progressbar_dialog = ProgressDialog(self, "获取 apk 列表", None)
        self.progressbar_dialog.progress_callback(msg="获取中...")

        self.progressbar_dialog.show() 
        self.apk_viewmodel.generate_apk_list(False)

    def __get_apks_success(self, info_file):
        self.progressbar_dialog.progress_callback(100, "获取 apk 列表成功")
        self.progressbar_dialog.close()
        self.pull_dialog = PullApkDialog(self, info_file)
        self.pull_dialog.show()

    def __get_apks_failure(self, code, msg):
        self.progressbar_dialog.progress_callback(100, "{0} : {1}".format(code, msg))
        self.progressbar_dialog.showEnd("确认")

