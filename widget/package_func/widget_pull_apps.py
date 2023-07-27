# -*- coding:utf-8 -*-

from viewmodel.apk_viewmodel import ApkViewModel
from widget.custom.toast import Toast
from widget.function.widget_function import FunctionWidget
from widget.package_func.widget_app_items import AppListWidget


class PullAppsWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/3/3

    拉取设备中 Apk 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_pull_apps.ui"
    __QSS_FILE = "./res/qss/widget_pull_apps.qss"

    def __init__(self, main_window) -> None:
        super(PullAppsWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__app_list = None

    def _entry(self):
        pass
    
    def _onPreShow(self):
        self.__apk_viewmodel = ApkViewModel(self)
        self.__app_list_widget = AppListWidget()
        self._ui.layout_pull_app_content.addWidget(self.__app_list_widget)
        # 禁止点击
        self._ui.btn_search_app.setDisabled(True)
        self._ui.edt_search_pull_app.setDisabled(True)
    
    def _setupListener(self):
        self.__apk_viewmodel.generate_list_operation.setListener(self.__generateListSuccess, self.__generateListProgress, self.__generateListFailure)
        self._ui.btn_get_apps.clicked.connect(self.__getApps)
        self._ui.btn_search_app.clicked.connect(self.__search)

    def __getApps(self):
        self.__app_list_widget.clear()
        self.__apk_viewmodel.generateApkList(False)

    def __search(self):
        keyword = self._ui.edt_search_pull_app.text()
        if keyword =="":
            toast = Toast(self)
            toast.make_text("输入不能为空", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        if self.__app_list!=None:
            self.__app_list_widget.clear()
            index = 0
            for app in self.__app_list:
                if keyword in app[0]:
                    self.__app_list_widget.loadApk(index, app)
                index+=1
        else:
            toast = Toast(self)
            toast.make_text("请连接手机", Toast.toast_left(self), Toast.toast_top(self), times=3)

    def __generateListSuccess(self, app_list):
        # 开放点击
        self._ui.btn_search_app.setDisabled(False)
        self._ui.edt_search_pull_app.setDisabled(False)
        self.__app_list = app_list
        self._ui.btn_get_apps.setText("加载")
        index = 0
        for app in app_list:
            self.__app_list_widget.loadApk(index, app)
            index+=1


    def __generateListProgress(self, progress, message, other_info, is_success):
        self._ui.btn_get_apps.setText("加载应用中，{0}%...".format(progress))

    def __generateListFailure(self, message, other_info):
        self._ui.btn_get_apps.setText("加载失败,重试")