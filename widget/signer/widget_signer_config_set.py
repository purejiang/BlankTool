# -*- coding:utf-8 -*-


from utils.file_helper import FileHelper
from utils.ui_utils import chooseFile
from vo.signer import SignerConfig
from widget.base.base_widget import BaseWidget

from widget.custom.toast import Toast



class SignerConfigSetWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2024/2/1

    签名配置的功能UI


    """
    __UI_FILE = "./res/ui/widget_signer_config_set.ui"
    __QSS_FILE = "./res/qss/widget_signer_config_set.qss"

    def __init__(self, main_window, signer=None) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__signer = signer
        self.__initView()

    def _onPreShow(self):
        pass
    
    def __initView(self):
        if self.__signer is None:
            return
        self._ui.edt_signer_name.setText(self.__signer.signer_name)
        self._ui.edt_signer_file_path.setText(self.__signer.signer_file_path)
        self._ui.edt_signer_pwd.setText(self.__signer.signer_pwd)
        self._ui.edt_signer_key_pwd.setText(self.__signer.signer_key_pwd)
        self._ui.edt_signer_key_alias.setText(self.__signer.signer_alias)
        self._ui.edt_signer_ext.setText(self.__signer.ext)
        self._ui.ckb_is_used_signer.setChecked(self.__signer.is_used)
        
    def setTitle(self, str):
        self._ui.lb_signer_config_dilaog_title.setText(str)

    def _setupListener(self):
        self._ui.btn_signer_file.clicked.connect(self.__onChooseFile)

    def getSigner(self):
        signer_name = self._ui.edt_signer_name.text()
        signer_file_path = self._ui.edt_signer_file_path.text()
        signer_pwd = self._ui.edt_signer_pwd.text()
        signer_key_pwd = self._ui.edt_signer_key_pwd.text()
        signer_alias = self._ui.edt_signer_key_alias.text()
        signer_ext = self._ui.edt_signer_ext.text()
        is_used = self._ui.ckb_is_used_signer.isChecked()
 
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
        signer.is_used = is_used
        signer.ext = signer_ext
        return signer

    def __onChooseFile(self):    
        file_path = chooseFile(self, "选取签名文件", "签名文件 (*.jks *.keystore)")
        self._ui.edt_signer_file_path.setText(file_path)