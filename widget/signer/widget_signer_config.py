# -*- coding:utf-8 -*-

from common.context import Context
from viewmodel.signer_viewmodel import SignerViewModel
from widget.custom.dialog_custom_big import BigCustomDialog
from widget.function.widget_function import FunctionWidget
from widget.signer.listwidget_signer import SignerListWidget
from widget.signer.widget_signer_config_set import SignerConfigSetWidget

class SignerConfigWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2022/3/24

    签名配置主界面

    """
    __UI_FILE = "./res/ui/widget_signer_config.ui"
    __QSS_FILE = "./res/qss/widget_signer_config.qss"

    def __init__(self, main_window) -> None:
        super(SignerConfigWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
    
    def _onHide(self):
        pass
    
    def _onShow(self):
        self.signer_viewmodel.allSigners()

    def _onPreShow(self):
        self.signer_viewmodel = SignerViewModel(self)
        self.__listwidget_signers = SignerListWidget()
        self._ui.layout_signers.addWidget(self.__listwidget_signers)

        self._add_signer_dialog = BigCustomDialog(self)
        self._add_signer_dialog.title = "添加签名"

    def _setupListener(self):
        self._ui.btn_add_signer.clicked.connect(self.__onShowAddSignerDialog)

        self.signer_viewmodel.all_operation.setListener(self.__allSignerSuccess, self.__allSignerProgress, self.__allSignerFailure)
        self.signer_viewmodel.add_operation.setListener(self.__addSignerSuccess, self.__addSignerProgress, self.__addSignerFailure)

        self._add_signer_dialog.setConfirmListener("添加", self.__onConfirm)
        self._add_signer_dialog.setCancelListener("取消", self.__onClose)
        self._add_signer_dialog.setCloseListener(self.__onClose)

    def __onShowAddSignerDialog(self):
        self._add_widget_signer_config_set = SignerConfigSetWidget(self)
        self._add_signer_dialog.content_widget =  self._add_widget_signer_config_set
        self._add_signer_dialog.show()

    def __allSignerSuccess(self, signer_list):
        Context.ALL_SIGNER_LIST = signer_list
        self.__listwidget_signers.loadList(signer_list)

    def __allSignerProgress(self, progress, title, des):
        pass

    def __allSignerFailure(self, code, msg):
        pass

    def __onConfirm(self):
        new_signer = self._add_widget_signer_config_set.getSigner()
        self.signer_viewmodel.addSigner(new_signer)
        self._add_signer_dialog.close()
    
    def __onClose(self):
        self._add_signer_dialog.close()

    def __addSignerSuccess(self):
        self.signer_viewmodel.allSigners()

    def __addSignerProgress(self, progress, title, des):
        pass

    def __addSignerFailure(self, code, msg):
        pass