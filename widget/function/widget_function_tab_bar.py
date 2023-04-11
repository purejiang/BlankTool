# -*- coding:utf-8 -*-
from PySide6.QtGui import QIcon
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtWidgets import QListWidget, QListWidgetItem,QScrollArea

from widget.base.base_widget import BaseWidget
from widget.package_func.widget_install import InstallWidget
from widget.function.widget_item_function import FuctionItemWidget
from widget.package_parse.widget_parse_apk import ParseApkWidget
from widget.package_parse.widget_apk_info import ApkInfoWidget
from widget.package_func.widget_pull_apks import PullApksWidget
from widget.package_repack.widget_apk2aab import Apk2AabWidget
from widget.package_repack.widget_repack import RepackApkWidget
from widget.setting.widget_setting import SettingWidget
from widget.signer.widget_signer_config import SignerConfigWidget


class FunctionTabBarWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/3/9

    安装 Apk/Aab 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_function_tab_bar.ui"
    __QSS_FILE = "./res/qss/widget_function_tab_bar.qss"

    def __init__(self, main_window, item_click_callback) -> None:
        super(FunctionTabBarWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__item_click_callback = item_click_callback
        self.__apk_parse_widget = ParseApkWidget(self)
        self.__apk_parse_result_widget = ApkInfoWidget(self)
        self.__install_apk_widget = InstallWidget(self)
        self.__pull_apk_widget = PullApksWidget(self)
        self.__repack_apk_widget = RepackApkWidget(self)
        self.__apk2aab_widget = Apk2AabWidget(self)
        self.__signer_config_widget = SignerConfigWidget(self)
        self.__setting_widget = SettingWidget(self)
        self.__function_all_dict = {}
        self.__widgets_dict = {}
        self.__list_widget_list = []
        self.__initView()

    def _onPreShow(self):
        self._ui.toolbox_functions.removeItem(0)

    def __initView(self):
        android_parse_dict ={"icon": "./res/img/app_icon_small", "widgets":{"APK/AAB 解析":self.__apk_parse_widget, "APK 解析结果": self.__apk_parse_result_widget}}
        package_func_dict = {"icon": "./res/img/app_icon_small", "widgets":{"APK/AAB 安装":self.__install_apk_widget, "APK 拉取":self.__pull_apk_widget}}
        pakage_repack_dict = {"icon": "./res/img/app_icon_small", "widgets":{"APK 重编":self.__repack_apk_widget, "APK 转 AAB":self.__apk2aab_widget}}
        other_dict ={"icon": "./res/img/app_icon_small", "widgets":{"签名配置": self.__signer_config_widget, "设置":self.__setting_widget}}
        
        self.__function_all_dict["安卓分析"] = android_parse_dict
        self.__function_all_dict["包体功能"] = package_func_dict
        self.__function_all_dict["包体重编"] = pakage_repack_dict
        self.__function_all_dict["其他"] = other_dict
        for type_name in self.__function_all_dict:
            widgets = self.__function_all_dict[type_name]["widgets"]
            list_widget = self.__createListWidget(widgets)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(list_widget)
            self._ui.toolbox_functions.addItem(scroll, QIcon(self.__function_all_dict[type_name]["icon"]), type_name)
            self.__widgets_dict.update(widgets)
            self.__list_widget_list.append(list_widget)
            
            
        # 设置第一项为当前选定项，并模拟点击该项
        first_item = self.__list_widget_list[0].item(0)
        self.__list_widget_list[0].setCurrentItem(first_item, QItemSelectionModel.SelectCurrent)
        self.__list_widget_list[0].itemClicked.emit(first_item)

    def __createListWidget(self, widgets):
        functions_list_widget = MyListWidget(self)
        for widget_name in widgets:
            list_item = QListWidgetItem(widget_name)  # 创建QListWidgetItem对象
            function_item_widget = FuctionItemWidget(self, "", widget_name)
            functions_list_widget.addItem(list_item)  # 添加item
            functions_list_widget.setItemWidget(list_item, function_item_widget)
        functions_list_widget.itemClicked.connect(self.__itemClickCallback)
        return functions_list_widget
            

    def __itemClickCallback(self, item):
        for list_widget in self.__list_widget_list:
            if list_widget!=self.sender():
                list_widget.clearSelection()
        for widget_name in self.__widgets_dict:
            if widget_name==item.text():
                self.__item_click_callback(self.__widgets_dict[item.text()])
                if item.text()=="APK 解析结果":
                    self.__apk_parse_result_widget.receiveApkInfo(self.__apk_parse_widget.apk_info)
                if item.text()=="APK 重编":
                    self.__repack_apk_widget.refersh()
                if item.text()=="签名配置":
                    self.__signer_config_widget.refersh()
                break
    
    def _setupListener(self):
        pass

class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            current_item = self.currentItem()
            if current_item:
                current_item.setSelected(True)
        else:
            super().mousePressEvent(event)
