# -*- coding:utf-8 -*-
from PySide6.QtGui import QIcon
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtWidgets import QListWidget, QListWidgetItem,QScrollArea,QToolBox
from vo.function import Function, Functions
from widget.base.base_ui import BaseUi

from widget.base.base_widget import BaseWidget
from widget.package_func.widget_install import InstallWidget
from widget.package_parse.widget_parse_apk import ParseApkWidget
from widget.package_parse.widget_apk_info import ApkInfoWidget
from widget.package_func.widget_pull_apps import PullAppsWidget
from widget.package_repack.widget_apk2aab import Apk2AabWidget
from widget.package_repack.widget_repack import RepackApkWidget
from widget.setting.widget_adb import AdbWidget
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

    def __init__(self, func:Function) -> None:
        super(FuctionListItem, self).__init__()
        self.func = func


class FuctionListWidget(QListWidget):
    def __init__(self, func_list):
        super(FuctionListWidget, self).__init__()
        self.__func_list = func_list
        self.__initView()

    def __initView(self):
        for func in self.__func_list:
            func_item = FuctionListItem(func)
            func_item_widget = FuctionListItemWidget(self, func)
            self.addItem(func_item)  # 添加item
            self.setItemWidget(func_item, func_item_widget)

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

    def __init__(self) -> None:
        super(FunctionTabBarWidget, self).__init__()
        self.__listwidget_list = []
        self.__funcs_list = []
        self.__current_item = None
        self.__click_item_callback= None
        self.__onPreShow()
        self.__initView()
        

    def __onPreShow(self):
        qss_str = "{0}\n{1}".format(self._loadQss(self._BASE_QSS_FILE), self._loadQss(self.__QSS_FILE))
        self.setStyleSheet(qss_str)

    def __initView(self):
        apk_parse_function = Function("APK/AAB 解析", "", ParseApkWidget(self))
        apk_parse_result_function = Function("APK 解析结果", "", ApkInfoWidget(self))
        list1 = [apk_parse_function, apk_parse_result_function]
        analysis_funcs = Functions("安卓分析", "./res/img/analyse_img.png", list1)
        self.__funcs_list.append(analysis_funcs)

        install_function = Function("APK/AAB 安装", "", InstallWidget(self))
        pull_apk_function = Function("APK 拉取", "", PullAppsWidget(self))
        list2 = [install_function, pull_apk_function]
        package_funcs = Functions("包体功能", "./res/img/package_img.png", list2)
        self.__funcs_list.append(analysis_funcs)

        reapck_apk_function = Function("APK 重编", "", RepackApkWidget(self))
        apk2aab_function = Function("APK 转 AAB", "", Apk2AabWidget(self))
        list3 = [reapck_apk_function, apk2aab_function]
        repack_funcs = Functions("包体重编", "./res/img/android_img.png", list3)
        self.__funcs_list.append(analysis_funcs)

        signer_config_function = Function("签名配置", "", SignerConfigWidget(self))
        setting_function = Function("应用设置", "", SettingWidget(self))
        adb_function = Function("ADB设置", "", AdbWidget(self))
        list4 = [signer_config_function, setting_function, adb_function]
        other_funcs = Functions("其他", "./res/img/other_img.png", list4)
        self.__funcs_list.append(analysis_funcs)

        for func_type in [analysis_funcs, package_funcs, repack_funcs, other_funcs]:
            functions_list_widget = FuctionListWidget(func_type.func_list)
            functions_list_widget.itemClicked.connect(self.__onItemClick)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(functions_list_widget)
            self.addItem(scroll, QIcon(func_type.icon), func_type.name)
            self.__listwidget_list.append(functions_list_widget)

    def setItemClickCallback(self, click_item_callback):
        self.__click_item_callback = click_item_callback

    def clickItem(self, func_index, position):
        first_item = self.__listwidget_list[func_index].item(position)
        self.__listwidget_list[func_index].setCurrentItem(first_item, QItemSelectionModel.SelectCurrent)
        self.__listwidget_list[func_index].itemClicked.emit(first_item)

    def __onItemClick(self, item):
        for listwidget in self.__listwidget_list:
            if listwidget!=self.sender():
                listwidget.clearSelection()
        self.__current_item = item
        self.__click_item_callback(self.__current_item)
    
    def _setupListener(self):
        pass
