# -*- coding:utf-8 -*-
import os
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseDir
from viewmodel.apk_viewmodel import ApkViewModel
from viewmodel.signer_viewmodel import SignerViewModel
from widget.custom.toast import Toast
from widget.function.widget_function import FunctionWidget
from widget.step_info.widget_step_info import StepInfoListWidget



class RepackApkWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/2/23

    重编 Apk 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_repack.ui"
    __QSS_FILE = "./res/qss/widget_repack.qss"

    def __init__(self, main_window) -> None:
        super(RepackApkWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__used_signer_config_list = []
        self.__used_signer_version_list = ["v1", "v2"]
        self.__ckb_support_aapt2 = False
        self.__initView()

    def __initView(self):
        pass

    def _entry(self):
        self.__showSignerVersions(self.__used_signer_version_list)
        all_signer_list = SignerViewModel._signer_list
        if all_signer_list!=None:
            self.__showSignerConfigs(all_signer_list)
        else:
            self.__signer_viewmodel.allSigners()
    
    def __showSignerConfigs(self, all_signerconfig_list):
        self._ui.cb_choose_signer_config.clear()
        self.__used_signer_config_list.clear()
        for signer_config in all_signerconfig_list:
            if signer_config.is_used == True:
                self.__used_signer_config_list.append(signer_config)
                self._ui.cb_choose_signer_config.addItem(signer_config.signer_name, signer_config)

    def __showSignerVersions(self, all_signer_version_list):
        self._ui.cb_choose_signer_version.clear()
        for signer_version in all_signer_version_list:
            self._ui.cb_choose_signer_version.addItem(signer_version)

    def _onPreShow(self):
        self.__apk_viewmodel = ApkViewModel(self)
        self.__signer_viewmodel = SignerViewModel(self)
        self.__widget_repack_step_info = StepInfoListWidget()
        self._ui.layout_repack_step_info.addWidget(self.__widget_repack_step_info)
        self._ui.btn_jump_to_repack_path.setVisible(False)
        
    def _setupListener(self):
        self._ui.btn_select_repack_apk.clicked.connect(self.__chooseFile)
        self._ui.btn_repack_apk.clicked.connect(self.__startRepack)
        self._ui.btn_jump_to_repack_path.clicked.connect(self.__jumpToRepackPath)
        self._ui.ckb_support_aapt2.stateChanged.connect(self.__isSupportAapt2)
        self.__apk_viewmodel.repack_apk_operation.setListener(self.__repackSuccess, self.__repackProgress, self.__repackFailure)
        self.__signer_viewmodel.all_operation.setListener(self.__loadSignersSuccess, self.__loadSignersProgress, self.__loadSignersFailure)
       
    def __loadSignersSuccess(self, signer_list):
        self.__showSignerConfigs(signer_list)

    def __loadSignersProgress(self, progress, message, other_info,  is_success):
        pass

    def __loadSignersFailure(self, code, message, other_info):
        pass

    def __isSupportAapt2(self, checked):
        self.__ckb_support_aapt2 = checked

    def __chooseFile(self):
        repack_dir_path = chooseDir(self, "需要重编的目录")
        self._ui.edt_repack_dir_path.setText(repack_dir_path)
    
    def __startRepack(self):
        self.__widget_repack_step_info.clearAll()
        repack_dir_path = self._ui.edt_repack_dir_path.text()
        self.__ouput_apk_path = os.path.join(FileHelper.parentDir(repack_dir_path), FileHelper.filename(repack_dir_path)+".apk")
        if not FileHelper.fileExist(repack_dir_path) or repack_dir_path=="":
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        # 获取用户选择的项的索引
        signer_index = self._ui.cb_choose_signer_config.currentIndex()
        version_index = self._ui.cb_choose_signer_version.currentIndex()
        self.__apk_viewmodel.repack(repack_dir_path, self.__ouput_apk_path, self.__ckb_support_aapt2, self.__used_signer_version_list[version_index], self.__used_signer_config_list[signer_index])
        # 禁止点击
        self._ui.widget_repack_fuction_bar.setDisabled(True)
        self._ui.btn_jump_to_repack_path.setVisible(False)

    def __jumpToRepackPath(self):
        if self.__ouput_apk_path!=None:
            FileHelper.showInExplorer(self.__ouput_apk_path)

    def __repackSuccess(self, apk_info):
        self.apk_info = apk_info
        self.__widget_repack_step_info.loadStep(currentTime(), "重编成功", "", True)
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        self._ui.btn_jump_to_repack_path.setVisible(True)

    def __repackProgress(self, progress, message, other_info, is_success):
        self.__widget_repack_step_info.loadStep(currentTime(), message, other_info, is_success)

    def __repackFailure(self, code, message, other_info):
        self.__widget_repack_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        
