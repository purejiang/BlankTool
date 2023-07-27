# -*- coding:utf-8 -*-
from PySide6.QtGui import QPixmap
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
    __SUCCESS_IMG = "./res/img/ic_step_success"
    __FAILED_IMG = "./res/img/ic_step_failed"
    __INFO_IMG = "./res/img/ic_step_info"

    def __init__(self, main_window, time, message, other_info, is_success) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self._message = message
        self._time = time
        self._other_info = other_info
        self._is_success = is_success
        self.__initView()
        

    def _onPreShow(self):
        pass

    def __initView(self):
        self._ui.lb_step_title.setText(self._message)
        self._ui.lb_step_time.setText(self._time)
        if self._is_success==None:
            pixmap = QPixmap(self.__INFO_IMG)
        elif self._is_success:
            pixmap = QPixmap(self.__SUCCESS_IMG)
        else:
            pixmap = QPixmap(self.__FAILED_IMG)

        self._ui.lb_step_info_icon.setPixmap(pixmap)
        
    
    def _setupListener(self):
        pass


class StepInfoListWidget(QListWidget):
    """

    @author: purejiang
    @created: 2023/3/23

    显示步骤信息总览的 QListWidget
    """

    def __init__(self) -> None:
        super(StepInfoListWidget, self).__init__()
        self.__initView()
        self._setupListener()
        
    def __initView(self):
        pass

    def loadStep(self, time, message, other_info, is_success):
        # 创建QListWidgetItem对象
        list_widget_item = QListWidgetItem()
        # 调用上面的函数获取对应
        widget = StepInfoItemWidget(self, message, time, other_info, is_success)
        # 添加item
        self.addItem(list_widget_item) 
        # 为item设置widget
        self.setItemWidget(list_widget_item, widget)  
        # 滑动到底部
        self.scrollToBottom()
    
    def _clear(self):
        self.clear()

    def _setupListener(self):
        pass
