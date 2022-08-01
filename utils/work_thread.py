# -*- coding:utf-8 -*-


from PySide2.QtCore import QThread, Signal

SUCCESS = 1001
class WorkThread(QThread):
    
    _state = Signal(int)
    """
    执行耗时方法的线程
    
    """
    def __init__(self, func):
        QThread.__init__(self)
        self.__func = func

    # 线程运行时
    def run(self):
        self.__func()
        self._state.emit(SUCCESS)
