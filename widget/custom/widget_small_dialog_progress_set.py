# -*- coding:utf-8 -*-



from widget.base.base_widget import BaseWidget


class WidgetSmallDialogProgressSet(BaseWidget):
    """

    @author: purejiang
    @created: 2024/2/5

    小dialog，进度条


    """
    __UI_FILE = "./res/ui/widget_small_dialog_progress_set.ui"
    __QSS_FILE = "./res/qss/widget_small_dialog_progress_set.qss"

    def __init__(self, main_window) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__top_msg = None
        self.__bottom_msg = None
        self.__progress = 0
        self.__initView()

    def _onPreShow(self):
        self._ui.lb_small_progress_dialog_top_msg.setVisible(False)
        self._ui.lb_small_progress_dialog_bottom_msg.setVisible(False)

    def __initView(self):
        pass

    def _setupListener(self):
        pass
    
    @property
    def progress(self):
        return self.__progress
    
    @progress.setter
    def progress(self, value):
        self.__progress = value
        self._ui.pb_small_progress_dialog.setValue(value)
    
    @property
    def top_msg(self):
        return self.__top_msg
    
    @top_msg.setter
    def top_msg(self, value):
        self.__top_msg = value
        self._ui.lb_small_progress_dialog_top_msg.setVisible(True)
        self._ui.lb_small_progress_dialog_top_msg.setText(value)

    @property
    def bottom_msg(self):
        return self.__bottom_msg
    
    @bottom_msg.setter
    def bottom_msg(self, value):
        self.__bottom_msg = value
        self._ui.lb_small_progress_dialog_bottom_msg.setVisible(True)
        self._ui.lb_small_progress_dialog_bottom_msg.setText(value)


