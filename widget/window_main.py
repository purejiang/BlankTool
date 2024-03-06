# -*- coding:utf-8 -*-
from common.constant import Constant
from widget.base.base_window import BaseWindow
from widget.custom.dialog_custom_small import SmallCustomDialog
from widget.custom.widget_small_dialog_msg_set import WidgetSmallDialogMsgSet
from widget.function.widget_function_tab_bar import FuctionListItem, FunctionTabBarWidget
from widget.widget_main_widow_titlebar import MainTitleBar


class MainWindow(BaseWindow):
    """

    @author: purejiang
    @created: 2022/2/21

    主页面

    """
    __UI_FILE = "./res/ui/window_main.ui"
    __QSS_FILE = "./res/qss/window_main.qss"
    __ICON = "./res/img/app_icon_small"
    __TITLE = Constant.AppInfo.APP_NAME

    def __init__(self, application) -> None:
        super(MainWindow, self).__init__(application, self.__UI_FILE, self.__QSS_FILE, self.__ICON)
        self.__current_item = None
        self.__close_window = False

    def _onPreShow(self, data):
        self.setWindowTitle(Constant.AppInfo.APP_NAME)
        self.__title_bar = MainTitleBar(self)
        self.__title_bar.setTitle(self.__TITLE)
        self.__function_tab_bar = FunctionTabBarWidget()
        self.__function_tab_bar.setItemClickCallback(self.__itemClickCallback)
        self._ui.layout_main_window_title_bar.addWidget(self.__title_bar)
        self._ui.layout_function_bar.addWidget(self.__function_tab_bar)
        
        self.__close_app_dialog = SmallCustomDialog(self)
        self.__close_app_dialog.title = "提示"

    def _setupListener(self):
        self.__close_app_dialog.setConfirmListener("关闭应用", self.__onCloseWindow)
        self.__close_app_dialog.setCancelListener("取消", self.__onCancelWindow)
        self.__close_app_dialog.setCloseListener(self.__onCancelWindow)

    def _onAfterShow(self, data):
        # 设置第一项为当前选定项，并模拟点击该项
        self.__function_tab_bar.clickItem(0, 0)

    def __itemClickCallback(self, item:FuctionListItem):
        if item==self.__current_item and item.func.function_widget.isVisible:
            return
        self.__hideContentWidget()
        self.__current_item = item
        self._ui.layout_main_content.addWidget(item.func.function_widget)
        item.func.function_widget.setVisible(True)
    
    def __hideContentWidget(self):
        for i in range(self._ui.layout_main_content.count()):
            item_widget = self._ui.layout_main_content.itemAt(i).widget()
            if item_widget.isVisible():
                self._ui.layout_main_content.itemAt(i).widget().setVisible(False)
    
    def __onCloseWindow(self):
        self.__close_app_dialog.close()
        self.__close_window = True
        self.close()
        
    def __onCancelWindow(self):
        self.__close_app_dialog.close()

    def __onShowCloseDialog(self):
        """
        显示关闭程序的dialog
        """

        self._close_message_widget = WidgetSmallDialogMsgSet(self)
        self._close_message_widget.message = "是否关闭应用"
        self.__close_app_dialog.content_widget = self._close_message_widget
        self.__close_app_dialog.show()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        if self.__close_window:
            self.__close_window = False
            event.accept()
        else:
            # 先不执行退出
            event.ignore()
            # 展示退出框
            self.__onShowCloseDialog()
