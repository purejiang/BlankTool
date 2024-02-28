# -*- coding:utf-8 -*-
import os
from common.context import Context
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseDir, chooseFile
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
        self.__is_support_aapt2 = False
        self.__is_resign_apk = False

    def _onHide(self):
        pass
    
    def _onShow(self):
        self.__getsignerList()

    def __getsignerList(self):
        self.__showSignerVersions(self.__used_signer_version_list)
        if Context.ALL_SIGNER_LIST!=None:
            self.__showSignerConfigs(Context.ALL_SIGNER_LIST)
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
        self._ui.btn_repack_or_sign_apk.clicked.connect(self.__startRepackOrReSign)
        self._ui.btn_jump_to_repack_path.clicked.connect(self.__jumpToRepackPath)
        self._ui.ckb_support_aapt2.stateChanged.connect(self.__isSupportAapt2)
        self._ui.ckb_is_resign_apk.stateChanged.connect(self.__isResignApk)
        self.__apk_viewmodel.repack_dir_operation.setListener(self.__repackSuccess, self.__repackProgress, self.__repackFailure)
        self.__apk_viewmodel.resign_apk_operation.setListener(self.__repackSuccess, self.__repackProgress, self.__repackFailure)
        self.__signer_viewmodel.all_operation.setListener(self.__loadSignersSuccess, self.__loadSignersProgress, self.__loadSignersFailure)
       
    def __loadSignersSuccess(self, signer_list):
        self.__showSignerConfigs(signer_list)

    def __loadSignersProgress(self, progress, message, other_info,  is_success):
        pass

    def __loadSignersFailure(self, code, message, other_info):
        pass

    def __isSupportAapt2(self, checked):
        self.__is_support_aapt2 = checked

    def __isResignApk(self, checked):
        self.__is_resign_apk = checked
        if self.__is_resign_apk:
            self._ui.ckb_support_aapt2.setDisabled(True)
            self._ui.ckb_support_aapt2.setChecked(False)
            self._ui.btn_repack_or_sign_apk.setText("重签")
        else:
            self._ui.ckb_support_aapt2.setDisabled(False)
            self._ui.btn_repack_or_sign_apk.setText("重编")

    def __chooseFile(self):
        if self.__is_resign_apk:
            file_path = chooseFile(self, "选取 Apk", "安卓应用文件 (*.apk)")
        else:
            file_path = chooseDir(self, "需要重编的目录")
        self._ui.edt_repack_dir_path.setText(file_path)
    
    def __startRepackOrReSign(self):
        self.__widget_repack_step_info.clearAll()
        repack_file_path = self._ui.edt_repack_dir_path.text()
        self.__ouput_apk_path = os.path.join(FileHelper.parentDir(repack_file_path), "repack_"+FileHelper.filename(repack_file_path)+".apk")
        if not FileHelper.fileExist(repack_file_path) or repack_file_path=="":
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        # 获取用户选择的项的索引
        signer_index = self._ui.cb_choose_signer_config.currentIndex()
        version_index = self._ui.cb_choose_signer_version.currentIndex()
        if self.__is_resign_apk:
            self.__apk_viewmodel.reSign(repack_file_path, self.__ouput_apk_path, self.__used_signer_version_list[version_index], self.__used_signer_config_list[signer_index])
        else:    
            self.__apk_viewmodel.repack(repack_file_path, self.__ouput_apk_path, self.__is_support_aapt2, self.__used_signer_version_list[version_index], self.__used_signer_config_list[signer_index])
        # 禁止点击
        self._ui.widget_repack_fuction_bar.setDisabled(True)
        self._ui.btn_jump_to_repack_path.setVisible(False)

    def __jumpToRepackPath(self):
        if self.__ouput_apk_path!=None:
            FileHelper.showInExplorer(self.__ouput_apk_path)

    def __repackSuccess(self, apk_info):
        self.apk_info = apk_info
        self.__widget_repack_step_info.loadStep(currentTime(), "重编/重签成功", "", True)
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        self._ui.btn_jump_to_repack_path.setVisible(True)

    def __repackProgress(self, progress, message, other_info, is_success):
        self.__widget_repack_step_info.loadStep(currentTime(), message, other_info, is_success)

    def __repackFailure(self, code, message, other_info):
        self.__widget_repack_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        
