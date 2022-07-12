# -*- coding:utf-8 -*-


from PySide2.QtCore import QThread, Signal


class WorkThread(QThread):
    _state = Signal(int)
    """
    执行耗时方法的线程
    
    """
    def __init__(self, func):
        QThread.__init__(self)
        self.__func = func

    # 线程运行时获取apk信息并通过pub与主线程交互
    def run(self):
        self.__func()
        self._state.emit(1)
