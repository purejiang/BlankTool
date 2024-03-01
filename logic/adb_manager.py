# -*- coding:utf-8 -*-

import re
import traceback
from cmd_util.adb_cmd import AdbCMD
from common.context import Context
from utils.jloger import JLogger
from utils.other_util import currentTimeNumber


class AdbManager():
    """

    @author: purejiang
    @created: 2024/2/27

    ADB相关的功能管理

    """
    @classmethod
    def reStartAdb(cls, progress_callback):
        """
        adb重连
        """
        loger = JLogger(log_name="restart_adb_{0}.log".format(currentTimeNumber()), save_file=True)
        loger.info("开始adb重连")
        progress_callback(50, "重连中...", "", True)
        result = AdbCMD.adbKillServer()
        if not result[0]:
            return False
        return AdbCMD.adbStartServer()[0]
    
    @classmethod
    def devices(cls, progress_callback):
        """
        获取连接adb的设备
        """
        try:
            loger = JLogger(log_name="devices_adb_{0}.log".format(currentTimeNumber()), save_file=True)
            loger.info("开始获取连接adb的设备")
            progress_callback(50, "获取中...", "", True)
            result = AdbCMD.adbDevices()
            if result[0]:
                return True, cls.parseDevices(result[1], loger)
        except Exception as e:
            loger.warning("获取连接adb的设备失败："+traceback.format_exc())   
            return False, None
        return result[0], None
    

    @classmethod
    def selectDevice(cls, device_info, progress_callback):
        """
        选择adb连接的设备
        """
        if Context.ALL_ADB_DEVICES==None:
            Context.DEFAULT_ADB_DEVICE = None
            return False
        for key, value in Context.ALL_ADB_DEVICES.items():
            if device_info == value:
                Context.DEFAULT_ADB_DEVICE = key
        return True

    
    @classmethod
    def parseDevices(cls, devices_info, loger)->dict:
        device_dict ={}
        loger.info("解析："+devices_info)
        devices = re.findall("(.*?)\s+device product:(.*?) model:(.*?) device:(.*?) transport_id:(.*)", devices_info, re.M|re.I)
        if devices:
            for device in devices:
                device_dict[device[0].strip()] = "{0}-{1}-{2}-{3}".format(device[1].strip(), device[2].strip(), device[3].strip(), device[4].strip())
            Context.ALL_ADB_DEVICES = device_dict
        else:
            Context.ALL_ADB_DEVICES = None
        Context.DEFAULT_ADB_DEVICE = None
        return device_dict