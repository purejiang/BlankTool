# -*- coding:utf-8 -*-


from PySide2.QtCore import Qt,QSize
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from PySide2.QtWidgets import QListWidgetItem
from ui.pull_apk_item_widget import PullApkItemWidget
from utils.file_helper import FileHelper


class PullApkDialog(BaseDialog):
    """
    @author: purejiang
    @created: 2022/7/20

    有拉取 apk 功能的弹出框

    """
    __UI_FILE = "./res/ui/pull_apk_dialog.ui"
    __QSS_FILE = "./res/qss/pull_apk_dialog.qss"

    def __init__(self, application, info_file) -> None:
        super(PullApkDialog, self).__init__(application)
        self.__info_file = info_file
        self.__parseInfo()

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title("Pull Apk")
        self._ui.pull_apk_dialog_title_bar.addWidget(self.title_bar)

    def _setup_qss(self):
        # 禁止其他界面响应
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        pass

    def __parseInfo(self):
        self.__get_package_name(FileHelper.fileContent(self.__info_file))

    def __get_package_name(self, info_content):
        package_name_list = info_content.strip("package:").replace("\n", "").split("package:")
        for package_name in package_name_list:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(540, 40))
            widget = PullApkItemWidget(self, package_name)  # 调用上面的函数获取对应
            self._ui.apk_list.addItem(item)  # 添加item
            self._ui.apk_list.setItemWidget(item, widget)  # 为item设置widget