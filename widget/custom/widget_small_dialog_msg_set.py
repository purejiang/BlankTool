# -*- coding:utf-8 -*-



from widget.base.base_widget import BaseWidget


class WidgetSmallDialogMsgSet(BaseWidget):
    """

    @author: purejiang
    @created: 2022/4/21

    小dialog，message


    """
    __UI_FILE = "./res/ui/widget_small_dialog_msg_set.ui"
    __QSS_FILE = "./res/qss/widget_small_dialog_msg_set.qss"

    def __init__(self, main_window) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__message = None
        self.__initView()

    def _onPreShow(self):
        pass

    def __initView(self):
        pass

    def _setupListener(self):
        pass
    
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, value):
        self.__message = value
        self._ui.lb_small_dialog_message.setText(self.__message)
