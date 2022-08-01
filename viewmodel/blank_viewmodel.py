# -*- coding:utf-8 -*-

from manager.blank_manager import BlankManager
from manager.bundle_manager import BundleManager
from viewmodel.viewmodel_signal import ViewModelSignal

from PySide2.QtCore import QThread, Signal

class BlankViewModel(object):
    """
    程序的相关操作

    @author: purejiang
    @created: 2022/8/1

    """
    def __init__(self, parent) -> None:
        super(BlankViewModel, self).__init__()
        self.parent = parent
        self.clean_cache_success = ViewModelSignal()        # 清理缓存成功
        self.clean_cache_progress = ViewModelSignal()        # 清理缓存进度
        self.clean_cache_failure = ViewModelSignal()        # 清理缓存失败

    def clean_cache(self):
        clean_cache_thread = CleanCache(self.parent)
        clean_cache_thread.success.connect(self.clean_cache_success.to_method())
        clean_cache_thread.clean_progress.connect(self.clean_cache_progress.to_method())
        clean_cache_thread.failure.connect(self.clean_cache_failure.to_method())
        clean_cache_thread.start()
        
class CleanCache(QThread):
    """
    清理缓存
    """
    success = Signal()
    clean_progress = Signal(int, str)
    failure = Signal(int, str)

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        result = BlankManager.cleanCache(self.progress_callback)
        if result:
            self.success.emit()
        else:
            self.failure.emit(0, "清理缓存失败")
            
    def progress_callback(self, progress, msg):
        self.clean_progress.emit(progress, msg)
