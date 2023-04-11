# -*- coding:utf-8 -*-

from logic.blank_manager import BlankManager
from viewmodel.base_viewmodel import BaseThread, Operation

from PySide6.QtCore import Signal

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

        self.clean_cache_opreation = Operation()        # 清理缓存

    def initApp(self):
        init_app_thread = InitApp()
        self.init_app_opreation.loadThread(init_app_thread)
        self.init_app_opreation.start()
    

    def cleanCache(self):
        clean_cache_thread = CleanCache()
        self.clean_cache_opreation.loadThread(clean_cache_thread)
        self.clean_cache_opreation.start()

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

            