# -*- coding:utf-8 -*-
from PySide6.QtCore import Signal
from logic.blank_manager import BlankManager
from viewmodel.base_viewmodel import BaseThread, Operation

class BlankViewModel():
    """
    程序的相关操作

    @author: purejiang
    @created: 2022/8/1

    """
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        
        self.init_app_opreation = Operation()           # 初始化应用
        self.get_chache_size_opreation = Operation()    # 获取缓存大小
        self.clean_cache_opreation = Operation()        # 清理缓存
        self.set_setting_opreation = Operation()        # 修改配置

    def initApp(self):
        init_app_thread = InitApp()
        self.init_app_opreation.loadThread(init_app_thread)
        self.init_app_opreation.start()

    def getCacheSize(self):
        get_chache_size_thread = GetCacheSize()
        self.get_chache_size_opreation.loadThread(get_chache_size_thread)
        self.get_chache_size_opreation.start()

    def cleanCache(self):
        clean_cache_thread = CleanCache()
        self.clean_cache_opreation.loadThread(clean_cache_thread)
        self.clean_cache_opreation.start()

    def setAppSetting(self, config:dict):
        set_setting_thread = SettingSetter(config)
        self.set_setting_opreation.loadThread(set_setting_thread)
        self.set_setting_opreation.start()


class SettingSetter(BaseThread):
    """
    修改配置
    """

    def __init__(self, config:dict):
        super().__init__()
        self._config = config

    def run(self):
        result = BlankManager.setSetting(self._config, self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "修改配置失败")

class CleanCache(BaseThread):
    """
    清理缓存
    """

    def __init__(self):
        super().__init__()

    def run(self):
        result = BlankManager.cleanCache(self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "清理缓存失败")

class GetCacheSize(BaseThread):
    """
    获取缓存大小
    """
    _success_signal = Signal(str)   

    def __init__(self):
        super().__init__()

    def run(self):
        result = BlankManager.getChache(self._progressCallback)
        if result:
            self._success_signal.emit(result)
        else:
            self._failure_signal.emit(0, "获取缓存失败")

class InitApp(BaseThread):
    """
    初始化应用
    """

    def __init__(self):
        super().__init__()

    def run(self):
        result = BlankManager.initApplication(self._progressCallback)
        if result:
            self._success_signal.emit()
        else:
            self._failure_signal.emit(0, "初始化应用失败")

            