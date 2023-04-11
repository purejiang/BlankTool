# -*- coding:utf-8 -*-

from viewmodel.signer_viewmodel import SignerViewModel
from PySide6.QtWidgets import QListWidget,QMenu,QListWidgetItem
from PySide6.QtCore import Qt
from vo.signer import SignerConfig
from widget.signer.dialog_signer_config import SignerConfigDialog


class SignerListItem(QListWidgetItem):

    def __init__(self, signer:SignerConfig):
        super().__init__()
        self.setText(signer.signer_name)
        # 添加自定义属性
        self.data1 = signer

class SignerListWidget(QListWidget):
    """

    @author: purejiang
    @created: 2022/3/31

    自定义的签名列表

    """

    def __init__(self) -> None:
        super(SignerListWidget, self).__init__()
        self._initView()
        self._setupListener()

    def _initView(self):
        self.signer_viewmodel = SignerViewModel(self)
        # 启用自定义上下文菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__show_context_menu)

    def _setupListener(self):
        self.signer_viewmodel.all_operation.setListener(self.__allSignerSuccess, self.__allSignerProgress, self.__allSignerFailure)
        self.signer_viewmodel.modify_operation.setListener(self.__modifySignerSuccess, self.__modifySignerProgress, self.__modifySignerFailure)

    def __delItem(self):
        item = self.takeItem(self.currentRow())
        self.signer_viewmodel.delSigner(item.data1.signer_id)
        del item
    
    def loadList(self, sigenr_list):
        self.clear()
        for signer in sigenr_list:
            signer_item = SignerListItem(signer)
            self.addItem(signer_item)

    def __allSignerSuccess(self, sigenr_list):
        self.loadList(sigenr_list)

    def __allSignerProgress(self, progress, title, des):
        pass

    def __allSignerFailure(self, code, msg):
        pass
        
    def __topItem(self, item):
        pass

    def __upItem(self, item):
        pass

    def __downItem(self, item):
        pass
    
    def __modifySignerSuccess(self):
        self.signer_viewmodel.allSigners()

    def __modifySignerProgress(self, progress, title, des):    
        pass

    def __modifySignerFailure(self, code, msg):    
        pass

    def __modifyItem(self, item):
        self._add_signer_dialog = SignerConfigDialog(self, self.__changedListener, item.data1)
        self._add_signer_dialog.show()

    def __changedListener(self, signer):
        self.signer_viewmodel.modifySigner(signer)

    def __show_context_menu(self, point):
        current_item = self.currentItem()
        item = self.itemAt(point)
        if item is None:
            return
        if not current_item:
            return
        # 创建 QMenu 对象
        menu = QMenu(self)

        # 添加菜单项
        modify_action = menu.addAction("编辑") 
        del_action = menu.addAction("删除") 
        up_action = menu.addAction("上移") 
        down_action = menu.addAction("下移") 
        top_action = menu.addAction("置顶")

        # 显示菜单
        action = menu.exec_(self.mapToGlobal(point))

        # 处理选择的菜单项
        if action == modify_action:
            self.__modifyItem(self.currentItem())
        elif action == del_action:
            self.__delItem()
        elif action == top_action:
           self.__topItem(self.currentItem())
        elif action == up_action:
           self.__upItem(self.currentItem())
        elif action == down_action:
            self.__downItem(self.currentItem())