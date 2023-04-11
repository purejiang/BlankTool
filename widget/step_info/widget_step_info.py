# -*- coding:utf-8 -*-

from PySide6.QtWidgets import QListWidget,QListWidgetItem
from widget.base.base_widget import BaseWidget


class StepInfoItemWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/3/7

    显示步骤信息的 item
    """
    __UI_FILE = "./res/ui/widget_item_step_info.ui"
    __QSS_FILE = "./res/qss/widget_item_step_info.qss"

    def __init__(self, main_window, title, time, des) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.title = title
        self.time = time
        self.ds = des
        self.__initView()
        

    def _onPreShow(self):
        pass

    def __initView(self):
        self._ui.lb_step_title.setText(self.title)
        self._ui.lb_step_time.setText(self.time)
        
    
    def _setupListener(self):
        pass


class StepInfoWidget(QListWidget):
    """

    @author: purejiang
    @created: 2023/3/23

    显示步骤信息总览的 QListWidget
    """

    def __init__(self) -> None:
        super(StepInfoWidget, self).__init__()
        self.__initView()
        self._setupListener()
        
    def __initView(self):
        pass

    def loadStep(self, title, date, des):
        list_widget_item = QListWidgetItem()  # 创建QListWidgetItem对象
        widget = StepInfoItemWidget(self, title, date, des)  # 调用上面的函数获取对应
        self.addItem(list_widget_item)  # 添加item
        self.setItemWidget(list_widget_item, widget)  # 为item设置widget
    
    def _clear(self):
        self.clear()

    def _setupListener(self):
        pass
