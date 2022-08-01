# -*- coding:utf-8 -*-
import os
from common.constant import ADB_INFO_CACHE_PATH
from manager.apk_manager import ApkManager
from ui.base_widget import BaseWidget
from utils.file_helper import FileHelper
from utils.work_thread import SUCCESS, WorkThread


class PullApkItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2022/7/21

    pull apk 展示的 apk 列表的 item
    """
    __UI_FILE = "./res/ui/pull_apk_item_widget.ui"
    __QSS_FILE = "./res/qss/pull_apk_item_widget.qss"

    def __init__(self, main_window, package_name) -> None:
        self.__package_name = package_name
        super(PullApkItemWidget, self).__init__(main_window)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self._ui.pull_package_name_label.setText(self.__package_name)
    
    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        self._ui.pull_apk_btn.clicked.connect(self.__start_pull)

    def __start_pull(self):
        self.__inphone_thread = WorkThread(self.__get_inphone_path)
        self.__inphone_thread._state.connect(self.__sig_out)
        self.__inphone_thread.start()

    def __get_inphone_path(self):
        self.__info_file = os.path.join(ADB_INFO_CACHE_PATH, "{0}_inphone_path.txt").format(self.__package_name)
        self.__path_result = ApkManager.get_inphone_path(self.__package_name, self.__info_file)
    
    def __sig_out(self, state):
        if state==SUCCESS:
            # 获取路径完成
            self.__inphone_thread.terminate()
            if self.__path_result:            
                self.__pull_thread = WorkThread(self.__pull_apk)
                self.__pull_thread._state.connect(self.__sig_out2)
                self.__pull_thread.start()  
            else:
                self._ui.pull_apk_btn.setText("获取手机内路径失败")
    
    def __pull_apk(self):
        self.__new_dir = os.path.join(ADB_INFO_CACHE_PATH, "pull_apks")
        if not FileHelper.fileExist(self.__new_dir):
            FileHelper.createDir(self.__new_dir)
        self.__new_apk= os.path.join(self.__new_dir, "{0}.apk".format(self.__package_name))
        inphone_path = FileHelper.fileContent(self.__info_file).replace("package:", "").strip()
        self.__pull_result = ApkManager.pull_apk(inphone_path, self.__new_apk)

    def __sig_out2(self, state):
        if state==SUCCESS:
        # 获取路径完成
            self.__pull_thread.terminate()
            if self.__pull_result:            
                self._ui.pull_apk_btn.setText("导出成功") 
            else:
                self._ui.pull_apk_btn.setText("导出失败")