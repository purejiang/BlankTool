# -*- coding:utf-8 -*-

from PySide6.QtCore import Signal
from logic.adb_manager import AdbManager
from viewmodel.base_viewmodel import BaseThread, Operation

class AdbViewModel():
    """
    ADB的相关操作

    @author: purejiang
    @created: 2024/2/27

    """
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.adb_restart_opreation = Operation()        # ADB重连
        self.adb_devices_opreation = Operation()        # ADB读取设备列表
        self.select_adb_device_opreation = Operation()  # 选择ADB设备

    def adbRestart(self):
        adb_restart_thread = ADBRestart()
        self.adb_restart_opreation.loadThread(adb_restart_thread)
        self.adb_restart_opreation.start()
    
    def adbDevices(self):
        adb_devices_thread = AdbDevices()
        self.adb_devices_opreation.loadThread(adb_devices_thread)
        self.adb_devices_opreation.start()

    def selectDevice(self, device_info):
        select_device_thread = SelectDevice(device_info)
        self.select_adb_device_opreation.loadThread(select_device_thread)
        self.select_adb_device_opreation.start()

class ADBRestart(BaseThread):
    """
    ADB重连
    """

    def __init__(self):
        super().__init__()

    def run(self):
        result = AdbManager.reStartAdb(self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "ADB重连失败", "")

class AdbDevices(BaseThread):
    """
    ADB读取设备
    """
    _success_signal = Signal(dict)   

    def __init__(self):
        super().__init__()

    def run(self):
        result = AdbManager.devices(self._progressCallback)
        if result[0]:
            self._success_signal.emit(result[1])
        else:
            self._failure_signal.emit(0, "ADB读取设备失败", "")

class SelectDevice(BaseThread):
    """
    选择ADB设备
    """

    def __init__(self, device_info:str):
        super().__init__()
        self.device_info = device_info 

    def run(self):
        result = AdbManager.selectDevice(self.device_info, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "选择ADB设备失败", "")

            