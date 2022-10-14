# -*- coding:utf-8 -*-


from PySide2.QtCore import QSize
from manager.apk_manager import ApkManager
from ui.base_dialog import BaseDialog
from ui.normal_titlebar_widget import NormalTitilBar
from PySide2.QtWidgets import QListWidgetItem
from ui.pull_apk_item_widget import PullApkItemWidget


class PullApkDialog(BaseDialog):
    """
    @author: purejiang
    @created: 2022/7/20

    有拉取 apk 功能的弹出框

    """
    __UI_FILE = "./res/ui/pull_apk_dialog.ui"
    __QSS_FILE = "./res/qss/pull_apk_dialog.qss"
    __TITLE= "pull apk"
    
    def __init__(self, application, info_file) -> None:
        super(PullApkDialog, self).__init__(application)
        self.info_file = info_file
        self.widget_item_list=[]
        self.__init(info_file)

    def __init(self, info_file):
        self.pack_list = ApkManager.parseApkListInfo(info_file)
        self.__parse_list(self.pack_list)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = NormalTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.pull_apk_dialog_title_bar.addWidget(self.title_bar)
        

    def _setup_qss(self):
        self.setWindowTitle(self.__UI_FILE)
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        self._ui.package_searcher_btn.clicked.connect(self.__search_package)
    
    def __search_package(self):
        package_name = self._ui.package_searcher_edt.text().strip()
        result_list = [(pack, path) for pack, path in self.pack_list if package_name in pack]   
        self.__parse_list(result_list)
            

    def __parse_list(self, pack_list):
        print(pack_list)
        self._ui.apk_list.clear()
        for package_name, path in pack_list:
            list_widget_item = QListWidgetItem()  # 创建QListWidgetItem对象
            list_widget_item.setSizeHint(QSize(540, 40))
            widget = PullApkItemWidget(self, package_name, path)  # 调用上面的函数获取对应
            self._ui.apk_list.addItem(list_widget_item)  # 添加item
            self.widget_item_list.append(list_widget_item)
            self._ui.apk_list.setItemWidget(list_widget_item, widget)  # 为item设置widget


        