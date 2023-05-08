# -*- coding:utf-8 -*-
from PySide6.QtGui import QIcon
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtWidgets import QListWidget, QListWidgetItem,QScrollArea,QToolBox
from vo.function import Function, FunctionType
from widget.base.base_ui import BaseUi

from widget.base.base_widget import BaseWidget
from widget.function.widget_function import FunctionWidget
from widget.package_func.widget_install import InstallWidget
from widget.package_parse.widget_parse_apk import ParseApkWidget
from widget.package_parse.widget_apk_info import ApkInfoWidget
from widget.package_func.widget_pull_apks import PullApksWidget
from widget.package_repack.widget_apk2aab import Apk2AabWidget
from widget.package_repack.widget_repack import RepackApkWidget
from widget.setting.widget_setting import SettingWidget
from widget.signer.widget_signer_config import SignerConfigWidget


class FuctionListItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/2/22

    主页面展示的功能列表的 item
    """
    __UI_FILE = "./res/ui/widget_item_function.ui"
    __QSS_FILE = "./res/qss/widget_item_function.qss"

    def __init__(self, main_window, function:Function) -> None:
        super(FuctionListItemWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.icon_path = function.icon_path
        self.name = function.name
        self.function_widget = function.function_widget
        self.__initView()

    def __initView(self):
        self._ui.lb_item_function_name.setText(self.name)

    def _onPreShow(self):
        pass

    def _setupListener(self):
        pass

class FuctionListItem(QListWidgetItem):
    """

    @author: purejiang
    @created: 2023/4/20

    主页面展示的功能列表的 item
    """

    def __init__(self, function) -> None:
        super(FuctionListItem, self).__init__()
        self.function = function


class FuctionListWidget(QListWidget):
    def __init__(self, function_list, click_listener):
        super(FuctionListWidget, self).__init__()
        self.__loadList(function_list)
        self.itemClicked.connect(click_listener)

    def __loadList(self, function_list):
        for function in function_list:
            function_item = FuctionListItem(function)
            function_item_widget = FuctionListItemWidget(self, function)
            self.addItem(function_item)  # 添加item
            self.setItemWidget(function_item, function_item_widget)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            current_item = self.currentItem()
            if current_item:
                current_item.setSelected(True)
        else:
            super().mousePressEvent(event)


class FunctionTabBarWidget(QToolBox, BaseUi):
    """

    @author: purejiang
    @created: 2023/4/20

    功能列表
    """
    __QSS_FILE = "./res/qss/widget_function_tab_bar.qss"

    def __init__(self, item_click_callback) -> None:
        super(FunctionTabBarWidget, self).__init__()
        self.__item_click_callback = item_click_callback
        self.__listwidget_list=[]
        self.__onPreShow()
        self.__initView()

    def __onPreShow(self):
        qss_str = "{0}\n{1}".format(self._loadQss(self._BASE_QSS_FILE), self._loadQss(self.__QSS_FILE))
        self.setStyleSheet(qss_str)

    def __initView(self):
        apk_parse_function = Function("APK/AAB 解析", "", ParseApkWidget(self))
        apk_parse_result_function = Function("APK 解析结果", "", ApkInfoWidget(self))
        list1 = [apk_parse_function, apk_parse_result_function]
        self.__android_analysis = FunctionType("安卓分析", "./res/img/app_icon_small.png", list1)

        install_function = Function("APK/AAB 安装", "", InstallWidget(self))
        pull_apk_function = Function("APK 拉取", "", PullApksWidget(self))
        list2 = [install_function, pull_apk_function]
        self.__package_fc = FunctionType("包体功能", "./res/img/app_icon_small.png", list2)

        reapck_apk_function = Function("APK 重编", "", RepackApkWidget(self))
        apk2aab_function = Function("APK 转 AAB", "", Apk2AabWidget(self))
        list3 = [reapck_apk_function, apk2aab_function]
        self.__package_repack = FunctionType("包体重编", "./res/img/app_icon_small.png", list3)

        signer_config_function = Function("签名配置", "", SignerConfigWidget(self))
        setting_function = Function("应用设置", "", SettingWidget(self))
        list4 = [signer_config_function, setting_function]
        self.__other = FunctionType("其他", "./res/img/app_icon_small.png", list4)

        for function_type in [self.__android_analysis, self.__package_fc, self.__package_repack, self.__other]:
            functions_list_widget = FuctionListWidget(function_type.fucntion_list, self.__itemClickCallback)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(functions_list_widget)
            self.addItem(scroll, QIcon(function_type.icon), function_type.name)
            self.__listwidget_list.append(functions_list_widget)
        # 设置第一项为当前选定项，并模拟点击该项
        first_item = self.__listwidget_list[0].item(0)
        self.__listwidget_list[0].setCurrentItem(first_item, QItemSelectionModel.SelectCurrent)
        self.__listwidget_list[0].itemClicked.emit(first_item)


    def __itemClickCallback(self, item):
        for listwidget in self.__listwidget_list:
            if listwidget!=self.sender():
                listwidget.clearSelection()
        self.__item_click_callback(item.function.function_widget)
    
    def _setupListener(self):
        pass
