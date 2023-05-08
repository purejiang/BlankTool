
from PySide6.QtWidgets import QApplication

from widget.base.base_window import BaseWindow

class MyApplication(QApplication):
    """

    @author: purejiang
    @created: 2022/7/7

    """
    def __init__(self, sysargs):
        super(MyApplication, self).__init__(sysargs)
        self.window_list = []
        self.current_window = None

    def addWindow(self, window:BaseWindow):
        if window not in self.window_list:
            self.window_list.append(window)

    def jump(self, from_window:BaseWindow, to_window_clazz, data=None):
        to_window = None
        for window in self.window_list:
            if isinstance(window, to_window_clazz):
                to_window = window
               
        if to_window is None:
            to_window = to_window_clazz(self)
            self.addWindow(to_window)

        if from_window:
            from_window._onHide()
            from_window.close()

        to_window._onPreShow(data)
        to_window.show()
        to_window._setupListener()
        to_window._onAfterShow(data)
        self.current_window = to_window

    def showClazz(self, window_clazz):
        self.jump(None, window_clazz)