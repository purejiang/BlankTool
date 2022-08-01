
from PySide2.QtWidgets import QApplication


class MyApplication(QApplication):
    """

    @author: purejiang
    @created: 2022/7/7

    """
    def __init__(self, sysargs):
        super(MyApplication, self).__init__(sysargs)
        self.window_list = []
        self.current_window = None

    def addWindow(self, window):
        self.window_list.append(window)

    def jump2Window(self, from_window, to_window_clazz, data=None):
        for window in self.window_list:
            if isinstance(window, to_window_clazz):
                window._on_pre_show(data)
                window._setup_qss()
                window.show()
                window._setup_listener()
                window._on_after_show(data)
                self.current_window = window
                if from_window:
                    from_window.on_hide()
                    from_window.close()
                window._onJumpFinish()

    def show(self, window):
        self.jump2Window(None, window)