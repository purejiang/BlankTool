# -*- coding:utf-8 -*-
import os
"""

@author: purejiang
@created: 2022/7/11

常量

"""
###### 使用的工具所在的路径 ######
BUNDLE_TOOL_PATH = os.path.abspath("./re/bundletool/bundletool-all-1.8.2.jar")
APK_TOOL_PATH = os.path.abspath("./re/apktool/apktool_2.6.1.jar")
ADB_PATH = os.path.abspath("./re/adb")
AAPT2_PATH = os.path.abspath("./re/aapt")
JAVA_PATH = os.path.abspath("./re/jre/bin")

###### 缓存目录 ######
CACHE_PATH = os.path.abspath("./cache")

###### 安装功能的缓存 ######
INSTALL_CACHE_PATH = os.path.join(CACHE_PATH, "install")
######apk 功能的缓存 ######
APK_CACHE_PATH = os.path.join(CACHE_PATH, "apk")
# 解析功能的缓存
PARSE_CACHE_PATH = os.path.join(APK_CACHE_PATH, "parse_apk")
# adb 信息文件的缓存
ADB_INFO_CACHE_PATH = os.path.join(APK_CACHE_PATH, "adb_info")
# 手机内导出的 apk 文件的缓存
PULL_APK_CACHE_PATH = os.path.join(APK_CACHE_PATH, "pull_apk")
# aapt 信息文件的缓存
AAPT_INFO_CACHE_PATH = os.path.join(APK_CACHE_PATH, "aapt_info")
###### aab 功能的缓存 ######
AAB_CACHE_PATH = os.path.join(CACHE_PATH, "aab")
###### Blank Tool 的缓存 ######
BLANK_CACHE_PATH = os.path.join(CACHE_PATH, "blank")

BASE_CACHE_LIST = [APK_CACHE_PATH, AAB_CACHE_PATH, BLANK_CACHE_PATH, INSTALL_CACHE_PATH]
APK_CACHE_LIST = [AAPT_INFO_CACHE_PATH, PARSE_CACHE_PATH, ADB_INFO_CACHE_PATH, PULL_APK_CACHE_PATH]

