# -*- coding:utf-8 -*-

from viewmodel.blank_viewmodel import BlankViewModel
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
        self.__blank_viewmodel = BlankViewModel(self)
        self.__cleanCacheDialog = NormalDialog(self, "提示", "是否清理应用缓存")

    def _setupListener(self):
        self.__blank_viewmodel.get_chache_size_opreation.setListener(self.__getCacheSizeSuccess, self.__getCacheSizeProgress, self.__getCacheSizeFailure)
        self.__blank_viewmodel.clean_cache_opreation.setListener(self.__cleanCacheSuccess, self.__cleanCacheProgress, self.__cleanCacheFailure)
        self._ui.pb_clean_cache.clicked.connect(self.__showCacheDialog)
        self.__refershCacheDialog()

    def __refershCacheDialog(self):
        self.__cleanCacheDialog.setConfirm("清理", self.__cleanCache)
        self.__cleanCacheDialog.setCancel("取消", self.__closeCacheDialog)
        
    def _entry(self):
        if not self.__is_getsize_ing:
            self.__blank_viewmodel.getCacheSize()
            self._ui.lb_cache_totle_size.setText("缓存分析中")
            self.__is_getsize_ing = True
    
    def __showCacheDialog(self):
        self.__refershCacheDialog()
        self.__cleanCacheDialog.show()

    def __closeCacheDialog(self):
        self.__cleanCacheDialog.close()

    def __cleanCache(self):
        self.__cleanCacheDialog.setConfirm("", None)
        self.__cleanCacheDialog.setCancel("", None)
        self.__blank_viewmodel.cleanCache()

    def __cleanCacheSuccess(self):
        self.__cleanCacheDialog.setMessage("清理完成")
        self.__cleanCacheDialog.setConfirm("确认", self.__closeCacheDialog)
        self._entry()

    def __cleanCacheProgress(self, progress, title, des):
        self.__cleanCacheDialog.setMessage("{0}%:{1}".format(progress, title))
 
    def __cleanCacheFailure(self, code, msg):
        self.__cleanCacheDialog.setMessage("清理失败")
        self.__cleanCacheDialog.setConfirm("确认", self.__closeCacheDialog)
    
    def __getCacheSizeSuccess(self, size_str):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText(size_str)

    def __getCacheSizeProgress(self, progress, title, des):
        pass

    def __getCacheSizeFailure(self, code, msg):
        self.__is_getsize_ing = False
        self._ui.lb_cache_totle_size.setText("error, code:{0} msg:{1}".format(code, msg))