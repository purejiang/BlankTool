# -*- coding:utf-8 -*-

from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile
from vo.signer import SignerConfig
from widget.base.base_dialog import BaseDialog
from widget.custom.toast import Toast



class SignerConfigDialog(BaseDialog):
    """

    @author: purejiang
    @created: 2022/3/24

    签名配置弹窗


    """
    __UI_FILE = "./res/ui/dialog_signer_config.ui"
    __QSS_FILE = "./res/qss/dialog_signer_config.qss"
    __ICON = "./res/img/app_icon_small"

    def __init__(self, main_window, changed_listener, signer=None) -> None:
        super(SignerConfigDialog, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE, self.__ICON)
        self.__changed_listener = changed_listener
        self.__signer = signer
        self.__initView()

    def _onPreShow(self):
        self._moveCenter()
    
    def __initView(self):
        if self.__signer!=None:
            self._ui.edt_signer_name.setText(self.__signer.signer_name)
            self._ui.edt_signer_file_path.setText(self.__signer.signer_file_path)
            self._ui.edt_signer_pwd.setText(self.__signer.signer_pwd)
            self._ui.edt_signer_key_pwd.setText(self.__signer.signer_key_pwd)
            self._ui.edt_signer_key_alias.setText(self.__signer.signer_alias)

    def _setupListener(self):
        self._ui.btn_signer_confirm.clicked.connect(self.__comfirm)
        self._ui.btn_signer_cancel.clicked.connect(self.__cancel)
        self._ui.btn_signer_file.clicked.connect(self.__chooseFile)

    def __comfirm(self):
        signer_name = self._ui.edt_signer_name.text()
        signer_file_path = self._ui.edt_signer_file_path.text()
        signer_pwd = self._ui.edt_signer_pwd.text()
        signer_key_pwd = self._ui.edt_signer_key_pwd.text()
        signer_alias = self._ui.edt_signer_key_alias.text()
 
        info_list = [signer_name, signer_file_path, signer_pwd, signer_key_pwd, signer_alias]
        for i in range(len(info_list)):
            if info_list[i]=="":
                toast = Toast(self)
                toast.make_text("第 {} 项不能为空".format(i+1), Toast.toast_left(self), Toast.toast_top(self), times=3)
                return
        if not FileHelper.fileExist(signer_file_path):
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)  
            return
        if self.__signer!=None:
            signer = self.__signer
        else:
            signer = SignerConfig()
        signer.signer_name = signer_name
        signer.signer_file_path = signer_file_path
        signer.signer_pwd = signer_pwd
        signer.signer_key_pwd = signer_key_pwd
        signer.signer_alias = signer_alias
        self.__changed_listener(signer)
        self.close()

    def __cancel(self):
        self.close()
    
    def __chooseFile(self):    
        file_path = chooseFile(self, "选取签名文件", "签名文件 (*.jks *.keystore)")
        self._ui.edt_signer_file_path.setText(file_path)