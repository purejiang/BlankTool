# -*-coding:utf-8 -*-

import os
import traceback
from cmd_util.bundle_cmd import BundleCMD
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.jloger import JLogger
from utils.other_util import currentTime

class BundleManager():
    """
    @author: purejiang
    @created: 2022/7/13

    .aab 相关的功能管理

    """
    loger = JLogger()

    @classmethod
    def install_aab(cls, aab_path, signer_config, progress_callback):
        apks_path = os.path.join(Constant.Path.INSTALL_CACHE_PATH, "{0}.apks".format(FileHelper.filename(aab_path, False)))
        cls.loger.info("开始安装 aab，时间："+ currentTime())
        try:
            if FileHelper.fileExist(apks_path):
                FileHelper.delFile(apks_path)
            progress_callback(10, "清理输出目录...", "", True)

            
            aab2apks_result = BundleCMD.aab2Apks(Constant.Re.BUNDLETOOL_PATH, aab_path, apks_path, signer_config)
            progress_callback(30, "aab 转 apks...", aab2apks_result[1], aab2apks_result[0])
            if not aab2apks_result[0]:
                return False
            
            
            install_apks_result = BundleCMD.installApks(Constant.Re.BUNDLETOOL_PATH, apks_path)
            progress_callback(70, "安装 apks...", install_apks_result[1], install_apks_result[0])
            if not install_apks_result[0]:
                return False
            return True
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return False
        
    @classmethod
    def install_apks(cls, apks_file, progress_callback):
        cls.loger.info("开始安装 apks，时间："+ currentTime())
        try:
        
            progress_callback(30, "安装 apks...", "", True)
            install_apks_result = BundleCMD.installApks(Constant.Re.BUNDLETOOL_PATH, apks_file)
            progress_callback(70, "安装 apks完成", install_apks_result[1], install_apks_result[0])
            if not install_apks_result[0]:
                return False
            return True
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return False