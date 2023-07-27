# -*- coding:utf-8 -*-
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from utils.file_helper import FileHelper
from viewmodel.apk_viewmodel import ApkViewModel
from widget.base.base_widget import BaseWidget


class ApkItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/7/25

    显示apk信息的 item
    """
    __UI_FILE = "./res/ui/widget_item_pull_apps.ui"
    __QSS_FILE = "./res/qss/widget_item_pull_apps.qss"

    def __init__(self, main_window, id, app) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self._app = app
        self._id = id
        self._is_pulled = False
        self._target_file = ""
        self.__initView()

    def _onPreShow(self):
        self.__apk_viewmodel = ApkViewModel(self)

    def __initView(self):
        self._package_name = self._app[0]
        self._in_phone_path = self._app[1]
        pull_state = "未导出"
        
        self._ui.edt_pull_app_packagename.setText(self._package_name)
        self._ui.lb_pull_state.setText(pull_state)
        self._ui.lb_app_id.setText(str(self._id))

    def _setupListener(self):
        self.__apk_viewmodel.pull_apk_operation.setListener(self.__pullSuccess,self.__pullProgres,self.__pullFailure)
        self._ui.btn_pull_app.clicked.connect(self.__pullApk)
    
    def __pullSuccess(self, target_file):
        self._target_file = target_file
        self._is_pulled = True
        self._ui.lb_pull_state.setText("已导出")
        self._ui.btn_pull_app.setText("打开文件位置")

    def __pullProgres(self, progress, message, other_info, is_success):
        self._ui.lb_pull_state.setText("导出中：{0}%".format(progress))

    def __pullFailure(self, message, other_info):
        self._ui.lb_pull_state.setText("导出失败")

    def __pullApk(self):
        if not self._is_pulled:
            self.__apk_viewmodel.pullApk(self._package_name, self._in_phone_path)
        else:
            FileHelper.showInExplorer(self._target_file)

class AppListWidget(QListWidget):
    """

    @author: purejiang
    @created: 2023/7/25

    显示apk信息总览的 QListWidget
    """

    def __init__(self) -> None:
        super(AppListWidget, self).__init__()
        self.__initView()
        self._setupListener()

    def __initView(self):
        pass

    def loadApk(self, id, app):
        # 创建QListWidgetItem对象
        list_widget_item = QListWidgetItem()
        # 调用上面的函数获取对应
        widget = ApkItemWidget(self, id, app)
        # 添加item
        self.addItem(list_widget_item)
        # 为item设置widget
        self.setItemWidget(list_widget_item, widget)

    def _setupListener(self):
        pass
