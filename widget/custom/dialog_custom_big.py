# -*- coding:utf-8 -*-

from widget.base.base_dialog import BaseDialog



class BigCustomDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/4/21

    大弹窗


    """
    __UI_FILE = "./res/ui/dialog_custom_big.ui"
    __QSS_FILE = "./res/qss/dialog_custom_big.qss"

    def __init__(self, parent) -> None:
        super(BigCustomDialog, self).__init__(parent, self.__UI_FILE, self.__QSS_FILE)
        self.__title = None
        self.__content_widget = None
        self.__initView()
        self.__confirm_listener=None
        self.__cancel_listener=None
        self.__close_listener=None

    def _onPreShow(self):
        self._moveCenter()   

    def __initView(self):
        pass

    def _onPreShow(self):
        self._moveCenter()

    def __initView(self):
        pass

    def _setupListener(self):
        self._ui.btn_big_dialog_confirm.clicked.connect(self.__onConfirm)
        self._ui.btn_big_dialog_cancel.clicked.connect(self.__onCancel)
        self._ui.btn_big_dialog_close.clicked.connect(self.__onClose)

    @property
    def content_widget(self):
        return self.__content_widget
        
    @content_widget.setter
    def content_widget(self, value):
        if self.__content_widget:
            self.__content_widget.deleteLater()
        self.__content_widget = value
        self._ui.layout_big_dialog_main_set.addWidget(value)

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        self.__title = value
        self._ui.lb_big_dialog_title.setText(value)
    
    def setCancelListener(self, str, listener, is_show=True):
        self.__cancel_listener= listener
        self._ui.btn_big_dialog_cancel.setText(str)
        self._ui.btn_big_dialog_cancel.setVisible(is_show)
    
    def setConfirmListener(self, str, listener, is_show=True):
        self.__confirm_listener= listener
        self._ui.btn_big_dialog_confirm.setText(str)
        self._ui.btn_big_dialog_confirm.setVisible(is_show)
    
    def setCloseListener(self, listener, is_show=True):
        self.__close_listener = listener
        self._ui.btn_big_dialog_close.setVisible(is_show)

    def __onConfirm(self):
        if self.__confirm_listener:
            self.__confirm_listener()

    def __onCancel(self):
        if self.__cancel_listener:
            self.__cancel_listener()

    def __onClose(self):
        if self.__close_listener:
            self.__close_listener()

