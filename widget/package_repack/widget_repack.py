# -*- coding:utf-8 -*-
import os
from utils.file_helper import FileHelper
from utils.other_util import currentTime
from utils.ui_utils import chooseDir
from viewmodel.apk_viewmodel import ApkViewModel
from viewmodel.signer_viewmodel import SignerViewModel
from widget.base.base_widget import BaseWidget
from widget.custom.toast import Toast
from widget.function.widget_function import FunctionWidget
from widget.step_info.widget_step_info import StepInfoWidget



class RepackApkWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/2/23

    解析 Apk 功能对应的主页
    """
    __UI_FILE = "./res/ui/widget_repack.ui"
    __QSS_FILE = "./res/qss/widget_repack.qss"

    def __init__(self, main_window) -> None:
        super(RepackApkWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__initView()
        self.__signer_list=[]

    def __initView(self):
        pass

    def _entry(self):
        self.__signer_viewmodel.allSigners()

    def _onPreShow(self):
        self.__apk_viewmodel = ApkViewModel(self)
        self.__signer_viewmodel = SignerViewModel(self)
        self.__widget_repack_step_info = StepInfoWidget()
        self.layout_repack_step_info.addWidget(self.__widget_repack_step_info)
        self._ui.btn_jump_to_repack_path.setVisible(False)
        
    def _setupListener(self):
        self._ui.btn_select_repack_apk.clicked.connect(self.__chooseFile)
        self._ui.btn_repack_apk.clicked.connect(self.__startRepack)
        self._ui.btn_jump_to_repack_path.clicked.connect(self.__jumpToRepackPath)
        self.__signer_viewmodel.all_operation.setListener(self.__loadSignersSuccess, self.__loadSignersProgress, self.__loadSignersFailure)
        self.__apk_viewmodel.repack_apk_operation.setListener(self.__repackSuccess, self.__repackProgress, self.__repackFailure)

    def __loadSignersSuccess(self, signer_list):
        self._ui.cb_signers.clear()
        self.__signer_list = []
        if signer_list!=None:
            for signer in signer_list:
                if signer.is_used == True:
                    self.__signer_list.append(signer)
                    self._ui.cb_signers.addItem(signer.signer_name, signer)

    def __loadSignersProgress(self, progress, title, des):
        pass

    def __loadSignersFailure(self, code, msg):
        pass

    def __chooseFile(self):
        repack_dir_path = chooseDir(self, "需要重编的目录")
        self._ui.edt_repack_dir_path.setText(repack_dir_path)
        
    
    def __startRepack(self):
        self.__widget_repack_step_info._clear()
        repack_dir_path = self._ui.edt_repack_dir_path.text()
        self.__ouput_apk_path = os.path.join(FileHelper.parentDir(repack_dir_path), FileHelper.filename(repack_dir_path)+".apk")
        if not FileHelper.fileExist(repack_dir_path) or repack_dir_path=="":
            toast = Toast(self)
            toast.make_text("请输入正确的路径", Toast.toast_left(self), Toast.toast_top(self), times=3)
            return
        # 获取用户选择的项的索引
        index = self._ui.cb_signers.currentIndex()
        self.__apk_viewmodel.repack(repack_dir_path, self.__ouput_apk_path, True, self.__signer_list[index])
        # 禁止点击
        self._ui.widget_repack_fuction_bar.setDisabled(True)
        self._ui.btn_jump_to_repack_path.setVisible(False)

    def __jumpToRepackPath(self):
        if self.__ouput_apk_path!=None:
            FileHelper.showInExplorer(self.__ouput_apk_path)

    def __repackSuccess(self, apk_info):
        self.apk_info = apk_info
        self.__widget_repack_step_info.loadStep("重编成功", currentTime(), "")
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        self._ui.btn_jump_to_repack_path.setVisible(True)

    def __repackProgress(self, progress, title, des):
        self.__widget_repack_step_info.loadStep(title, currentTime(), "")

    def __repackFailure(self, code, msg):
        self.__widget_repack_step_info.loadStep("code:{0}, msg:{1}".format(code, msg), currentTime(), "")
        # 恢复点击
        self._ui.widget_repack_fuction_bar.setDisabled(False)
        
