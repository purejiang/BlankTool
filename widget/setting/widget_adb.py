# -*- coding:utf-8 -*-

from viewmodel.app_viewmodel import AppViewModel
from widget.function.widget_function import FunctionWidget

class AdbWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2024/2/27

    ADB设置界面

    """
    __UI_FILE = "./res/ui/widget_adb.ui"
    __QSS_FILE = "./res/qss/widget_adb.qss"

    def __init__(self, main_window) -> None:
        super(AdbWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)

    def _onPreShow(self):
        self.__app_viewmodel = AppViewModel(self)

    def _setupListener(self):
        self.__app_viewmodel.adb_restart_opreation.setListener(self.__onRestartAdbSuccess, self.__onRestartAdbProgress, self.__onRestartAdbFailure)
        self._ui.pb_restart_adb.clicked.connect(self.__onRestartAdb)
    
    def hideEvent(self, event):
        print("AdbWidget:hideEvent")
    
    def showEvent(self, event):
        print("AdbWidget:showEvent")

    def __onRestartAdb(self):
        self.__app_viewmodel.adbRestart()
    
    def __onRestartAdbSuccess(self):
        self._ui.lb_restart_adb_status.setText("重连完成")
        self._ui.pb_restart_adb.setDisabled(False)

    def __onRestartAdbProgress(self, progress, message, other_info, is_success):
        self._ui.lb_restart_adb_status.setText("重连中：{0}%".format(progress))
        self._ui.pb_restart_adb.setDisabled(True)

    def __onRestartAdbFailure(self, code, message, other_info):
        self._ui.lb_restart_adb_status.setText("重连失败")
        self._ui.pb_restart_adb.setDisabled(False)




