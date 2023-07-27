# -*-coding:utf-8 -*-

import os
import traceback
from common.cmd import CMD
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.j_loger import JLoger
from utils.other_util import currentTime

class BundleManager():
    """
    @author: purejiang
    @created: 2022/7/13

    .aab 相关的功能管理

    """
    loger = JLoger()
    
    @classmethod
    def __aab2apks(cls, bundletool_path, aab_path, apks_path, signer_config):
        """
        .aab 转 .apks
        :param bundletool_path: bundletool 文件路径
        :param aab_path: aab 文件路径
        :param output_apks_path: 输出的 apks 路径
        """
        cls.loger.info("aab2apks...")
        cmd_result = CMD.aab2Apks(bundletool_path, aab_path, apks_path, signer_config)
        return cmd_result

    @classmethod
    def __install_apks(cls, bundletool_path, apks_path):
        """
        安装 .apks
        :param bundletool_path: bundletool 文件路径
        :param apks_path: 要安装的 apks 路径
        """
        cls.loger.info("install apks...")
        cmd_result = CMD.installApks(bundletool_path, apks_path)
        return cmd_result

    @classmethod
    def install_aab(cls, aab_path, signer_config, progress_callback):
        apks_path = os.path.join(Constant.Path.INSTALL_CACHE_PATH, "{0}.apks".format(FileHelper.filename(aab_path, False)))
        cls.loger.info("开始安装 aab，时间："+ currentTime())
        try:
            if FileHelper.fileExist(apks_path):
                FileHelper.delFile(apks_path)
            progress_callback(10, "清理输出目录...", "", True)

            
            aab2apks_result = cls.__aab2apks(Constant.Re.BUNDLETOOL_PATH, aab_path, apks_path, signer_config)
            progress_callback(30, "aab 转 apks...", aab2apks_result[1], aab2apks_result[0])
            if not aab2apks_result[0]:
                return False
            
            
            install_apks_result = cls.__install_apks(Constant.Re.BUNDLETOOL_PATH, apks_path)
            progress_callback(70, "安装 apks...", install_apks_result[1], install_apks_result[0])
            if not install_apks_result[0]:
                return False
            return True
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return False