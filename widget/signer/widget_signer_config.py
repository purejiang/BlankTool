# -*- coding:utf-8 -*-

from viewmodel.signer_viewmodel import SignerViewModel
from widget.function.widget_function import FunctionWidget
from widget.signer.dialog_signer_config import SignerConfigDialog
from widget.signer.listwidget_signer import SignerListWidget

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

    def _onPreShow(self):
        self.signer_viewmodel = SignerViewModel(self)
        self.__listwidget_signers = SignerListWidget()
        self._ui.layout_signers.addWidget(self.__listwidget_signers)

    def _setupListener(self):
        self._ui.btn_add_signer.clicked.connect(self.__showAddSignerDialog)

        self.signer_viewmodel.all_operation.setListener(self.__allSignerSuccess, self.__allSignerProgress, self.__allSignerFailure)
        self.signer_viewmodel.add_operation.setListener(self.__addSignerSuccess, self.__addSignerProgress, self.__addSignerFailure)

    def __showAddSignerDialog(self):
        self._add_signer_dialog = SignerConfigDialog(self, self.__changedListener)
        self._add_signer_dialog.show()
    
    def _entry(self):
        self.signer_viewmodel.allSigners()

    def __allSignerSuccess(self, signer_list):
        SignerViewModel._signer_list = signer_list
        self.__listwidget_signers.loadList(signer_list)

    def __allSignerProgress(self, progress, title, des):
        pass

    def __allSignerFailure(self, code, msg):
        pass

    def __changedListener(self, signer):
        print(signer.__dict__)
        self.signer_viewmodel.addSigner(signer)
        
    def __addSignerSuccess(self):
        self.signer_viewmodel.allSigners()

    def __addSignerProgress(self, progress, title, des):
        pass

    def __addSignerFailure(self, code, msg):
        pass