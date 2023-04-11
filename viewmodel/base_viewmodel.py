# -*- coding:utf-8 -*-

from PySide6.QtCore import QThread, Signal

"""
线程相关操作

@author: purejiang
@created: 2023/3/13

"""

class BaseThread(QThread):
    _success_signal = Signal()
    _progress_signal = Signal(int, str, str)
    _failure_signal = Signal(int, str)

    def __init__(self):
        super().__init__()

    def _progressCallback(self, progress, msg, des):
        self._progress_signal.emit(progress, msg, des)

class ViewModelSignal():
    """
    用于转发QtThread的回调通知到函数中

    """
    def __init__(self):
        self.func_list = []

    def connect(self, func):
        self.func_list.append(func)

    def disconnect(self, func):
        self.func_list.remove(func)

    def to_method(self):
        return self.onCall

    def onCall(self, *args):
        for func in self.func_list:
            func(*args)

class Operation(object):

    def __init__(self) -> None:
        super().__init__()
        self.success = ViewModelSignal()
        self.progress = ViewModelSignal() 
        self.failure = ViewModelSignal()
    
    def setListener(self, success_listner , progress_listner, failure_listner):
        self.success.connect(success_listner)
        self.progress.connect(progress_listner)
        self.failure.connect(failure_listner)
    
    def loadThread(self, thread:BaseThread):
        self._thread = thread
    
    def start(self):
        self._thread._success_signal.connect(self.success.to_method())
        self._thread._progress_signal.connect(self.progress.to_method())
        self._thread._failure_signal.connect(self.failure.to_method())
        self._thread.start()