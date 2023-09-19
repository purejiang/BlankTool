# -*- coding:utf-8 -*-

from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseFile
from viewmodel.bundle_viewmodel import BundleViewModel
from viewmodel.signer_viewmodel import SignerViewModel
from widget.function.widget_function import FunctionWidget
from widget.step_info.widget_step_info import StepInfoListWidget

class Apk2AabWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/4/11

    APK 转 AAB 功能页面
    """
    __UI_FILE = "./res/ui/widget_apk2aab.ui"
    __QSS_FILE = "./res/qss/widget_apk2aab.qss"

    def __init__(self, main_window) -> None:
        super(Apk2AabWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__used_signer_config_list = []
        self.__min_sdk_version = 11
        self.__max_sdk_version = 33
        self.__initView()

    def _entry(self):
        self.__showVersions(self.__min_sdk_version, self.__max_sdk_version)
        all_signer_list = SignerViewModel._signer_list
        if all_signer_list!=None:
            self.__showSignerConfigs(all_signer_list)
        else:
            self.__signer_viewmodel.allSigners()
    
    def __showSignerConfigs(self, all_signerconfig_list):
        self._ui.cb_apk2aab_choose_signer_config.clear()
        self.__used_signer_config_list.clear()
        for signer_config in all_signerconfig_list:
            if signer_config.is_used == True:
                self.__used_signer_config_list.append(signer_config)
                self._ui.cb_apk2aab_choose_signer_config.addItem(signer_config.signer_name, signer_config)

    def __showVersions(self, min_sdk_version, max_sdk_version):
        for version in range(min_sdk_version, max_sdk_version+1):
            self._ui.cb_choose_min_version.addItem(str(version), version)
            self._ui.cb_choose_target_version.addItem(str(version), version)
            self._ui.cb_choose_compile_version.addItem(str(version), version)

    def __initView(self):
        pass

    def _onPreShow(self):
        self.__aab_viewmodel = BundleViewModel(self)
        self.__signer_viewmodel = SignerViewModel(self)
        self.__widget_apk2aab_step_info = StepInfoListWidget()
        self._ui.layout_apk2aab_step_info.addWidget(self.__widget_apk2aab_step_info)
        self._ui.btn_jump_to_aab_path.setVisible(False)

    def _setupListener(self):
        self._ui.btn_select_apk2aab_aab.clicked.connect(self.__chooseFile)
        self._ui.btn_apk2aab.clicked.connect(self.__startApk2aab)
        self._ui.btn_jump_to_aab_path.clicked.connect(self.__jumpToAabPath)
        self.__aab_viewmodel.apk2aab_operation.setListener(self.__apk2aabSuccess, self.__apk2aabProgress, self.__apk2aabFailure)
        self.__signer_viewmodel.all_operation.setListener(self.__loadSignersSuccess, self.__loadSignersProgress, self.__loadSignersFailure)
    
    def __jumpToAabPath(self):
        if self.__aab_path!=None:
            FileHelper.showInExplorer(self.__aab_path)
            
    def __chooseFile(self):
        file_path = chooseFile(self, "选取 Apk", "安卓应用文件 (*.apk)")
        self._ui.edt_apk2aab_apk_path.setText(file_path)

    def __startApk2aab(self):
        self.__aab_path = None
        # 隐藏跳转按钮
        self._ui.btn_jump_to_aab_path.setVisible(False)
        # 清除list中的item
        self.__widget_apk2aab_step_info.clearAll()
        # 禁止点击
        self._ui.widget_apk2aab_fuction_bar.setDisabled(True)

        apk_file = self._ui.edt_apk2aab_apk_path.text()
        signer_index = self._ui.cb_apk2aab_choose_signer_config.currentIndex()
        target_version = self._ui.cb_choose_target_version.currentText()
        min_version = self._ui.cb_choose_min_version.currentText()
        compile_version = self._ui.cb_choose_compile_version.currentText()
        version_code = self._ui.edt_apk2aab_version_code.text()
        version_name = self._ui.edt_apk2aab_version_name.text()
        ver_config={}
        ver_config["min_ver"]=min_version
        ver_config["tar_ver"]=target_version
        ver_config["compile_ver"]=compile_version
        ver_config["ver_code"]=version_code
        ver_config["ver_name"]=version_name
        self.__aab_viewmodel.apk2aab(apk_file, ver_config, self.__used_signer_config_list[signer_index])

    def __loadSignersSuccess(self, signer_list):
        self.__showSignerConfigs(signer_list)

    def __loadSignersProgress(self, progress, message, other_info,  is_success):
        pass

    def __loadSignersFailure(self, code, message, other_info):
        pass

    def __apk2aabSuccess(self, aab_path):
        self.__aab_path = aab_path
        self.__widget_apk2aab_step_info.loadStep(currentTime(), "apk 转 aab 成功", "", True)
        # 恢复点击
        self._ui.widget_apk2aab_fuction_bar.setDisabled(False)
        self._ui.btn_jump_to_aab_path.setVisible(True)

    def __apk2aabProgress(self, progress, message, other_info, is_success):
        self.__widget_apk2aab_step_info.loadStep(currentTime(), message, other_info, is_success)

    def __apk2aabFailure(self, code, message, other_info):
        self.__widget_apk2aab_step_info.loadStep(currentTime(), "code:{0}, message:{1}".format(code, message), other_info, False)
        # 恢复点击
        self._ui.widget_apk2aab_fuction_bar.setDisabled(False)
        
        
