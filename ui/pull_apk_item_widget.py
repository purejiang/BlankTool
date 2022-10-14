# -*- coding:utf-8 -*-
import os

from ui.base_widget import BaseWidget
from utils.file_helper import FileHelper
from viewmodel.apk_viewmodel import ApkViewModel


class PullApkItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/7/21

    pull apk 展示的 apk 列表的 item
    """
    __UI_FILE = "./res/ui/pull_apk_item_widget.ui"
    __QSS_FILE = "./res/qss/pull_apk_item_widget.qss"

    def __init__(self, main_window, package_name, path) -> None:
        self.package_name = package_name
        self.path = path
        self.is_output = False
        super(PullApkItemWidget, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self._ui.pull_package_name_edt.setText(self.package_name)
        self._ui.pull_apk_staute_btn.setText("未导出")
        self.apk_viewmodel = ApkViewModel(self)
    
    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        # 事件
        self.apk_viewmodel.pull_apk_success.connect(self.__pull_success)
        self.apk_viewmodel.pull_apk_failure.connect(self.__pull_failure)

        # view
        self._ui.pull_apk_btn.clicked.connect(self.__pull_apk)


    def __pull_apk(self):
        if self.is_output:
            os.startfile(FileHelper.parentDir(self.output_file))
        else:
            self._ui.pull_apk_staute_btn.setText("导出中...")
            self._ui.pull_apk_btn.setEnabled(False)
            self.apk_viewmodel.pull_apk(self.package_name, self.path)
    
    def __pull_success(self, output_file):
        self._ui.pull_apk_btn.setEnabled(True)
        self._ui.pull_apk_staute_btn.setText("已导出")
        self.output_file = output_file
        self.is_output =True
        self._ui.pull_apk_btn.setText("打开")

    def __pull_failure(self, code, msg):
        self._ui.pull_apk_btn.setEnabled(True)
        self._ui.pull_apk_staute_btn.setText("{0} : {1}".format(code, msg)) 
        self.is_output =False
