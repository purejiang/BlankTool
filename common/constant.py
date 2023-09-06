# -*- coding:utf-8 -*-
import json
import os
import sys
from utils.file_helper import FileHelper
"""

@author: purejiang
@created: 2022/7/11

常量

"""
APP_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
DATA_PATH = os.path.join(APP_PATH, "data")
CONFIG_PATH = os.path.join(APP_PATH, "config")
class Config:
    
    APP_CONFIG_PATH = os.path.join(CONFIG_PATH, "app_config.json")
    DEFAULT_CONFIG_PATH = os.path.join(CONFIG_PATH, "default_config.json")  
    APP_CONFIG_JSON= json.loads(FileHelper.fileContent(APP_CONFIG_PATH).replace("\./", APP_PATH))
    DEFAULT_CONFIG_JSON = json.loads(FileHelper.fileContent(DEFAULT_CONFIG_PATH).replace("\\./", APP_PATH))
    
    @classmethod
    def parseAppConfig(cls, key):
        return cls.APP_CONFIG_JSON[key]

    @classmethod
    def parseDefaultConfig(cls, key):
        return cls.DEFAULT_CONFIG_JSON[key]
class Constant:
    class AppInfo:
        ###### App 信息 ######
        __APP_INFO = Config.parseAppConfig("app_info")
        APP_NAME = __APP_INFO["app_name"]
        VERSION_NAME = __APP_INFO["version_name"]
        VERSION_CODE = __APP_INFO["version_code"]
        CREATE_TIME = __APP_INFO["create_time"]
        WEB_URL = __APP_INFO["web_url"]

    class Setting:
        ###### App 信息 ######
        __SETTING = Config.parseAppConfig("setting")
        iS_OUTPUT_LOG = __SETTING["is_output_log"]
        MODE = __SETTING["mode"]

    class Re:
        ###### 使用的工具所在的路径 ######
        __RE = Config.parseDefaultConfig("path")["re"]
        BUNDLETOOL_PATH = os.path.abspath(__RE["bundletool_path"])
        APKTOOL_PATH = os.path.abspath(__RE["apktool_path"])
        KEYTOOL_PATH = os.path.abspath(__RE["keytool_path"])
        JARSIGNER_PATH = os.path.abspath(__RE["jarsigner_path"])
        APKSIGNER_PATH = os.path.abspath(__RE["apksigner_path"])
        ADB_PATH = os.path.abspath(__RE["adb_path"])
        AAPT2_PATH = os.path.abspath(__RE["aapt2_path"])
        ANDROID_JAR_PATH = os.path.abspath(__RE["android_jar_path"])
        SMALI_JAR_PATH = os.path.abspath(__RE["smali_jar_path"])
        JAVA_PATH = os.path.abspath(__RE["java_path"])
        ALL_RE_PATH_LIST = [BUNDLETOOL_PATH, APKTOOL_PATH, KEYTOOL_PATH, JARSIGNER_PATH, ADB_PATH, AAPT2_PATH, JAVA_PATH]

    class Path:
        ###### 数据目录 ######
        __DATA= Config.parseDefaultConfig("path")["data"]
        DATA_PATH = os.path.abspath(__DATA["base_data"])
        SIGNER_DATA_FILE = os.path.abspath(__DATA["signer_data"])
        
        ###### 缓存目录 ######
        __CACHE = Config.parseDefaultConfig("path")["cache"]
        CACHE_PATH = os.path.abspath(__CACHE["base_cache"])
        # 安装功能的缓存
        INSTALL_CACHE_PATH = os.path.abspath(__CACHE["install_cache"])
        # 解析功能的缓存
        PARSE_CACHE_PATH = os.path.abspath(__CACHE["parse_apk_cache"])
        # 解析后的信息文件名，在反编的目录下
        PAESE_APK_INFO_FILE_NAME = "parse_apk_info.json"
        # adb 信息文件的缓存
        ADB_INFO_CACHE_PATH = os.path.abspath(__CACHE["adb_cache"])
        # 手机内导出的 apk 文件的缓存
        PULL_APK_CACHE_PATH = os.path.abspath(__CACHE["pull_apk_cache"])
        # aapt 信息文件的缓存
        AAPT_INFO_CACHE_PATH = os.path.abspath(__CACHE["aapt_cache"])
        # aab 功能的缓存
        AAB_CACHE_PATH = os.path.abspath(__CACHE["aab_cache"])
        # Blank Tool 的缓存
        SETTING_CACHE_PATH = os.path.abspath(__CACHE["setting_cache"])

        ###### RCC资源目录 ######
        RESOURCE_PATH = os.path.abspath(Config.parseDefaultConfig("path")["res"])

        ALL_CACHE_PATH_LIST = [ADB_INFO_CACHE_PATH, AAB_CACHE_PATH, SETTING_CACHE_PATH, AAPT_INFO_CACHE_PATH, INSTALL_CACHE_PATH, PARSE_CACHE_PATH, PULL_APK_CACHE_PATH,]
        ALL_OTHER_PATH_LIST = [RESOURCE_PATH]

    class ErrorCode:
        CREATE_APK_LIST_INFO_FILE_FAILEURE = 10001
        PARSE_APK_FAILEURE = 40001
        
    class Signer:
        USED_SIGNERS = "used_signers"
        USENESS_SIGNERS = "useness_signers"
        SIGNER_FILE_PATH = os.path.join(DATA_PATH, "signer.json")

    class Aab:
        ASSETS_RES_MANIFEST = os.path.join(DATA_PATH, "assets_res_default_AndroidManifest.xml")