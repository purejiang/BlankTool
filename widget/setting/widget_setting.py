# -*- coding:utf-8 -*-

from common.constant import Constant
from viewmodel.app_viewmodel import AppViewModel
from widget.custom.dialog_normal import NormalDialog
from widget.function.widget_function import FunctionWidget

class SettingWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/4/10

    设置界面

    """
    __UI_FILE = "./res/ui/widget_setting.ui"
    __QSS_FILE = "./res/qss/widget_setting.qss"

    def __init__(self, main_window) -> None:
        super(SettingWidget, self).__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__is_getsize_ing = False

    def _onPreShow(self):
        self.__app_viewmodel = AppViewModel(self)
        self.__cleanCacheDialog = NormalDialog(self, "提示", "是否清理应用缓存")
        self._ui.lb_app_vesion_name.setText(Constant.AppInfo.VERSION_NAME)
        self._ui.lb_app_vesion_code.setText(Constant.AppInfo.VERSION_CODE)
        self._ui.lb_app_create_time.setText(Constant.AppInfo.CREATE_TIME)
        self._ui.lb_app_mode.setText(Constant.Setting.MODE)
        if Constant.Setting.iS_OUTPUT_LOG:
            self._ui.ckb_is_output_log.setChecked(True)
        self._ui.lb_app_web_url.setText(Constant.AppInfo.WEB_URL)

    def _setupListener(self):
        self.__app_viewmodel.get_chache_size_opreation.setListener(self.__getCacheSizeSuccess, self.__getCacheSizeProgress, self.__getCacheSizeFailure)
        self.__app_viewmodel.clean_cache_opreation.setListener(self.__cleanCacheSuccess, self.__cleanCacheProgress, self.__cleanCacheFailure)
        self.__app_viewmodel.adb_restart_opreation.setListener(self.__adbRestartSuccess, self.__adbRestartProgress, self.__adbRestartFailure)
        self._ui.pb_clean_cache.clicked.connect(self.__showCacheDialog)
        self._ui.pb_restart_adb.clicked.connect(self.__restartAdb)
        self._ui.ckb_is_output_log.stateChanged.connect(self.__isOutputLog)
        self.__refershCacheDialog()

    def __isOutputLog(self, checked):
        if checked:
            self.__app_viewmodel.setAppSetting({"is_output_log": True})
        else:
            self.__app_viewmodel.setAppSetting({"is_output_log": False})

    def __refershCacheDialog(self):
        self.__cleanCacheDialog.setConfirm("清理", self.__cleanCache)
        self.__cleanCacheDialog.setCancel("取消", self.__closeCacheDialog)
        
    def _entry(self):
        if not self.__is_getsize_ing:
            self.__app_viewmodel.getCacheSize()
            self._ui.lb_cache_totle_size.setText("缓存分析中")
            self.__is_getsize_ing = True

    def __restartAdb(self):
        self.__app_viewmodel.adbRestart()
  
    def __showCacheDialog(self):
        self.__refershCacheDialog()
        self.__cleanCacheDialog.show()

    def __closeCacheDialog(self):
        self.__cleanCacheDialog.close()

    def __cleanCache(self):
        self.__cleanCacheDialog.setConfirm("", None)
        self.__cleanCacheDialog.setCancel("", None)
        self.__app_viewmodel.cleanCache()

    def __cleanCacheSuccess(self):
        self.__cleanCacheDialog.setMessage("清理完成")
        self.__cleanCacheDialog.setConfirm("确认", self.__closeCacheDialog)
        self._entry()

    def __cleanCacheProgress(self, progress, message, other_info, is_success):
        self.__cleanCacheDialog.setMessage("{0}%:{1}".format(progress, message))
 
    def __cleanCacheFailure(self, code, message, other_info):
        self.__cleanCacheDialog.setMessage("清理失败 code:{0}, message:{1}".format(code, message))
        self.__cleanCacheDialog.setConfirm("确认", self.__closeCacheDialog)
    
    def __getCacheSizeSuccess(self, size_str):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText(size_str)

    def __getCacheSizeProgress(self, progress, message, other_info, is_success):
        pass

    def __getCacheSizeFailure(self, code, message, other_info):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText("error code:{0}, message:{1}".format(code, message))
    
    def __adbRestartSuccess(self):
        self._ui.lb_restart_adb_status.setText("重连完成")

    def __adbRestartProgress(self, progress, message, other_info, is_success):
        self._ui.lb_restart_adb_status.setText("重连中：{0}%".format(progress))

    def __adbRestartFailure(self, code, message, other_info):
        self._ui.lb_restart_adb_status.setText("重连失败")




