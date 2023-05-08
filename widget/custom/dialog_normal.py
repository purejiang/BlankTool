# -*- coding:utf-8 -*-

from widget.base.base_dialog import BaseDialog



class NormalDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/4/21

    普通弹窗


    """
    __UI_FILE = "./res/ui/dialog_normal.ui"
    __QSS_FILE = "./res/qss/dialog_normal.qss"
    __ICON = "./res/img/app_icon_small"

    def __init__(self, main_window, title, msg) -> None:
        super(NormalDialog, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE, self.__ICON)
        self.__title = title
        self.__msg = msg
        self.__initView()
        self.__confirm_listener=None
        self.__cancel_listener=None

    def _onPreShow(self):
        self._moveCenter()   

    def setTitle(self, str):
        self._ui.lb_dialog_title.setText(str)

    def setMessage(self, str):
        self._ui.lb_dialog_msg.setText(str)
    
    def setCancel(self, str, listener):
        self.__cancel_listener= listener
        if str=="":
            self._ui.btn_dialog_cancel.setVisible(False)
            return
        self._ui.btn_dialog_cancel.setVisible(True)
        self._ui.btn_dialog_cancel.setText(str)

    def setConfirm(self, str, listener):
        self.__confirm_listener= listener
        if str=="":
            self._ui.btn_dialog_confirm.setVisible(False)
            return
        self._ui.btn_dialog_confirm.setVisible(True)
        self._ui.btn_dialog_confirm.setText(str)

    def __confirmListener(self):
        if self.__confirm_listener:
            self.__confirm_listener()

    def __cancelListener(self):
        if self.__cancel_listener:
            self.__cancel_listener()

    def __initView(self):
        self._ui.lb_dialog_title.setText(self.__title)
        self._ui.lb_dialog_msg.setText(self.__msg)

    def _setupListener(self):
        self._ui.btn_dialog_confirm.clicked.connect(self.__confirmListener)
        self._ui.btn_dialog_cancel.clicked.connect(self.__cancelListener)