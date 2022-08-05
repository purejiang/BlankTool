# -*- coding:utf-8 -*-



from ui.base_widget import BaseWidget


class AabBarWidget(BaseWidget):
    """
    @author: purejiang
    @created: 2022/7/7

    .aab 相关的功能控件

    """
    __UI_FILE = "./res/ui/aab_bar_widget.ui"
    __QSS_FILE = "./res/qss/aab_bar_widget.qss"

    def __init__(self, application) -> None:
        super(AabBarWidget, self).__init__(application)

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)
    
    def _setup_listener(self):
        pass
