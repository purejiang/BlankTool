# -*- coding:utf-8 -*-

from common.config import AppConfig, UserConfig
from viewmodel.app_viewmodel import AppViewModel
from widget.custom.dialog_custom_small import SmallCustomDialog
from widget.custom.widget_small_dialog_msg_set import WidgetSmallDialogMsgSet
from widget.custom.widget_small_dialog_progress_set import WidgetSmallDialogProgressSet
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
        self.__clean_cache_dialog = SmallCustomDialog(self)
        app_info = AppConfig.getAppInfo()
        host = AppConfig.getHost()
        setting = UserConfig.getSetting()
        self._ui.lb_app_vesion_name.setText(app_info.version_name)
        self._ui.lb_app_vesion_code.setText(app_info.version_code)
        self._ui.lb_app_build_time.setText(app_info.build_time)
        self._ui.lb_app_mode.setText(app_info.mode)
        if setting.is_output_log:
            self._ui.ckb_is_output_log.setChecked(True)

        self._ui.lb_app_web_url.setText(host.office_website_url)

    def _setupListener(self):
        self.__app_viewmodel.get_chache_size_opreation.setListener(self.__onCacheSizeSuccess, self.__onCacheSizeProgress, self.__onCacheSizeFailure)
        self.__app_viewmodel.clean_cache_opreation.setListener(self.__onCleanSuccess, self.__onCleanProgress, self.__onCleanFailure)
        self._ui.pb_clean_cache.clicked.connect(self.__onShowCacheDialog)
        self._ui.ckb_is_output_log.stateChanged.connect(self.__onIsOutputLog)
    
        self.__clean_cache_dialog.setCloseListener(self.__onCloseCacheDialog)

    def __onIsOutputLog(self, checked):
        if checked:
            self.__app_viewmodel.setAppSetting({"is_output_log": True})
        else:
            self.__app_viewmodel.setAppSetting({"is_output_log": False})
    
    def _onHide(self):
        pass
    
    def _onShow(self):
        self.__analysisCache()
    
    def __analysisCache(self):
        if not self.__is_getsize_ing:
            self.__app_viewmodel.getCacheSize()
            self._ui.lb_cache_totle_size.setText("缓存分析中")
            self.__is_getsize_ing = True
            self._ui.pb_clean_cache.setDisabled(True)

    def __onShowCacheDialog(self):
        # 要传dialog才行，不能用self当父布局
        self._clean_cache_message_widget = WidgetSmallDialogMsgSet(self.__clean_cache_dialog)
        self._clean_cache_message_widget.message = "是否清理应用缓存"
        self.__clean_cache_dialog.content_widget = self._clean_cache_message_widget
        self.__clean_cache_dialog.title = "提示"
        self.__clean_cache_dialog.setConfirmListener("清理", self.__onCleanCache)
        self.__clean_cache_dialog.setCancelListener("取消", self.__onCloseCacheDialog)
        self.__clean_cache_dialog.show()

    def __onCloseCacheDialog(self):
        self.__clean_cache_dialog.close()
        self.__clean_cache_dialog.reject()

    def __onCleanCache(self):
        self._clean_cache_progress_widget = WidgetSmallDialogProgressSet(self.__clean_cache_dialog)
        self.__clean_cache_dialog.content_widget = self._clean_cache_progress_widget
        self.__clean_cache_dialog.title = "清理缓存"
        self.__clean_cache_dialog.setConfirmListener(None, None, False)
        self.__clean_cache_dialog.setCancelListener(None, None, False)
        self.__clean_cache_dialog.setCloseListener(None, False)
        self.__app_viewmodel.cleanCache()

    def __onCleanSuccess(self):
        self._clean_cache_message_widget = WidgetSmallDialogMsgSet(self.__clean_cache_dialog)
        self._clean_cache_message_widget.message = "清理完成"
        self.__clean_cache_dialog.content_widget = self._clean_cache_message_widget
        self.__clean_cache_dialog.setConfirmListener("确认", self.__onCloseCacheDialog, True)
        self.__analysisCache()

    def __onCleanProgress(self, progress, message, other_info, is_success):
        self._clean_cache_progress_widget.progress = progress
        self._clean_cache_progress_widget.bottom_msg = message
 
    def __onCleanFailure(self, code, message, other_info):
        self._clean_cache_message_widget = WidgetSmallDialogMsgSet(self.__clean_cache_dialog)
        self._clean_cache_message_widget.message = "清理失败 code:{0}, message:{1}".format(code, message)
        self.__clean_cache_dialog.content_widget = self._clean_cache_message_widget
        self.__clean_cache_dialog.setConfirmListener("确认", self.__onCloseCacheDialog, True)
    
    def __onCacheSizeSuccess(self, size_str):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText(size_str)
        self._ui.pb_clean_cache.setDisabled(False)

    def __onCacheSizeProgress(self, progress, message, other_info, is_success):
        pass

    def __onCacheSizeFailure(self, code, message, other_info):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText("error code:{0}, message:{1}".format(code, message))
        self._ui.pb_clean_cache.setDisabled(False)




