# -*- coding:utf-8 -*-

from PySide2.QtCore import QSize
from ui.add_keystore_dialog import AddKeystoreDialog
from ui.base_dialog import BaseDialog
from PySide2.QtWidgets import QListWidgetItem
from ui.signer_keystore_item_widget import SignerKeystoreItemWidget
from ui.small_titlebar_widget import SmallTitilBar
from utils.ui_utils import OFFSET_X, OFFSET_Y
from viewmodel.signer_viewmodel import SignerViewModel

class SignerDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/10/10

    签名配置的界面

    """
    __UI_FILE = "./res/ui/signer_dialog.ui"
    __QSS_FILE = "./res/qss/signer_dialog.qss"
    __TITLE= "signer"

    def __init__(self, main_window, close_listener):
        super(SignerDialog, self).__init__(main_window)
        self.widget_item_list=[]
        self.__refresh()
        self.close_listener = close_listener

    def _on_pre_show(self):
        self._loadUi(self.__UI_FILE)
        self.title_bar = SmallTitilBar(self)
        self.title_bar.set_title(self.__TITLE)
        self._ui.signer_dialog_title_bar.addWidget(self.title_bar)
        self.signer_viewmodel = SignerViewModel(self)

    def _setup_qss(self):
        self._loadQss(self.__QSS_FILE)

    def _setup_listener(self):
        # 事件
        self.signer_viewmodel.get_keystores_success.connect(self.__show_keystores)
        self.signer_viewmodel.get_keystores_failure.connect(self.__get_keystores_failure)

        # view
        self._ui.add_keystore_btn.clicked.connect(self.__add_keystore)
    
    def __add_keystore(self):
        self.add_keystore_dialog = AddKeystoreDialog(self, self.__refresh)
        # 相对于父窗口偏移点距离，避免完全遮盖父窗口
        self.add_keystore_dialog.move(self.geometry().x()+OFFSET_X, self.geometry().y()+OFFSET_Y)
        self.add_keystore_dialog.show()
    
    def __refresh(self):
        self.signer_viewmodel.get_keystores()
    
    def __show_keystores(self, list):
        self._ui.keystore_list.clear()
        for keystore_config in list:
            list_widget_item = QListWidgetItem()  # 创建QListWidgetItem对象
            list_widget_item.setSizeHint(QSize(430, 40))
            widget = SignerKeystoreItemWidget(self, keystore_config, self.__refresh)  # 调用上面的函数获取对应
            self._ui.keystore_list.addItem(list_widget_item)  # 添加item
            self.widget_item_list.append(list_widget_item)
            self._ui.keystore_list.setItemWidget(list_widget_item, widget)  # 为item设置widget

    def __get_keystores_failure(self, code, msg):
        pass

    def close(self):
        super().close()
        self.close_listener()
