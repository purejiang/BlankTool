# -*- coding:utf-8 -*-

from viewmodel.adb_viewmodel import AdbViewModel
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
        self.__adb_viewmodel = AdbViewModel(self)

    def _setupListener(self):
        self.__adb_viewmodel.adb_restart_opreation.setListener(self.__onRestartAdbSuccess, self.__onRestartAdbProgress, self.__onRestartAdbFailure)
        self.__adb_viewmodel.adb_devices_opreation.setListener(self.__onGetDevicesSuccess, self.__onGetDevicesProgress, self.__onGetDevicesFailure)
        self._ui.pb_restart_adb.clicked.connect(self.__onRestartAdb)
        self._ui.cb_adb_devices.currentTextChanged.connect(self.__onDeviceChanged)
    
    def _onHide(self):
        pass
    
    def _onShow(self):
        self.__adb_viewmodel.adbDevices()

    def __onRestartAdb(self):
        self.__adb_viewmodel.adbRestart()
    
    def __onRestartAdbSuccess(self):
        self._ui.lb_restart_adb_status.setText("重连完成")
        self._ui.pb_restart_adb.setDisabled(False)

    def __onRestartAdbProgress(self, progress, message, other_info, is_success):
        self._ui.lb_restart_adb_status.setText("重连中：{0}%".format(progress))
        self._ui.pb_restart_adb.setDisabled(True)

    def __onRestartAdbFailure(self, code, message, other_info):
        self._ui.lb_restart_adb_status.setText("重连失败")
        self._ui.pb_restart_adb.setDisabled(False)
    
    def __onGetDevicesSuccess(self, device_dict):
        print("__onGetDevicesSuccess:"+str(device_dict))
        self._ui.cb_adb_devices.clear()
        for key in device_dict:
            self._ui.cb_adb_devices.addItem(device_dict[key], key)

    def __onGetDevicesProgress(self, progress, message, other_info, is_success):
        print("__onGetDevicesProgress:")

    def __onGetDevicesFailure(self, code, message, other_info):
        print("__onGetDevicesFailure:")
        self._ui.cb_adb_devices.clear()
    
    def __onDeviceChanged(self, text):
        print(text)
        self.__adb_viewmodel.selectDevice(text)




