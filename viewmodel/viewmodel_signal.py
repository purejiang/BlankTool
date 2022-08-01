# -*- coding:utf-8 -*-

class ViewModelSignal(object):
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
        return self.on_call

    def on_call(self, *args):
        for func in self.func_list:
            func(*args)
