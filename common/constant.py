# -*- coding:utf-8 -*-
import os

BUNDLE_TOOL_PATH = os.path.abspath("./re/bundletool/bundletool-all-1.8.2.jar")
APK_TOOL_PATH = os.path.abspath("./re/apktool/apktool_2.6.1.jar")
ADB_PATH = os.path.abspath("./re/adb/adb.exe")
AAPT_PATH = os.path.abspath("./re/aapt/aapt.exe")
CACHE_PATH = os.path.abspath("./cache")

INSTALL_CACHE_PATH = os.path.join(CACHE_PATH, "install")
APK_CACHE_PATH = os.path.join(CACHE_PATH, "apktool")
AAB_CACHE_PATH = os.path.join(CACHE_PATH, "aabtool")

PARSE_CACHE_PATH = os.path.join(APK_CACHE_PATH, "parse_apk")
ADB_INFO_PATH = os.path.join(APK_CACHE_PATH, "adb_info")
AAPT_INFO_PATH = os.path.join(APK_CACHE_PATH, "aapt_info")