# -*- coding:utf-8 -*-

from widget.base.base_widget import BaseWidget


class FuctionItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/2/22

    主页面展示的功能列表的 item
    """
    __UI_FILE = "./res/ui/widget_item_function.ui"
    __QSS_FILE = "./res/qss/widget_item_function.qss"

    def __init__(self, main_window, icon, name) -> None:
        super(FuctionItemWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.icon = icon
        self.name = name
        self.__initView()

    def __initView(self):
        self._ui.lb_item_function_name.setText(self.name)

    def _onPreShow(self):
        pass

    def _setupListener(self):
        pass
