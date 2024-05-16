# -*- coding:utf-8 -*-
import json
import os
import sys
from utils.file_helper import FileHelper



APP_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
DATA_DIR = os.path.join(APP_DIR, "data")
CONFIG_DIR = os.path.join(APP_DIR, "config")
OTHER_DIR = os.path.join(APP_DIR, "other")


DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIR, "default_config.json")

class Config(object):
    def __init__(self, config_file) -> None:
        self._config_file = config_file
        self._params = self.loadConfig(config_file)

    def loadConfig(self, config_file):
        return json.loads(FileHelper.fileContent(config_file).replace("${root}", APP_DIR.replace("\\","\\\\")))   

    def commit(self):
        FileHelper.writeContent(self._config_file, json.dumps(self._params))

class AppInfo(Config):
    ###### App 信息 ######

    def __init__(self, config_file) -> None:
        super().__init__(config_file)
        self.params = self._params["app_info"]

    @property
    def app_name(self):
        return self.params["app_name"]
    
    @app_name.setter
    def app_name(self, value):
        self.params["app_name"] = value
        self.commit()

    @property
    def version_name(self):
        return self.params["version_name"]
    
    @version_name.setter
    def version_name(self, value):
        self.params["version_name"] = value
        self.commit()

    @property
    def version_code(self):
        return self.params["version_code"]
    
    @version_code.setter
    def version_code(self, value):
        self.params["version_code"] = value
        self.commit()

    @property
    def build_time(self):
        return self.params["build_time"]
    
    @build_time.setter
    def build_time(self, value):
        self.params["build_time"] = value
        self.commit()

    @property
    def mode(self):
        return self.params["mode"]
    
    @mode.setter
    def mode(self, value):
        self.params["mode"] = value
        self.commit()

class Host(Config):
    ###### host 信息 ######

    def __init__(self, config_file) -> None:
        super().__init__(config_file)
        self.params = self._params["host"]

    @property
    def init(self):
        return self.params["init"]
    
    @init.setter
    def init(self, value):
        self.params["init"] = value
        self.commit()

    @property
    def check_update(self):
        return self.params["check_update"]
    
    @check_update.setter
    def check_update(self, value):
        self.params["check_update"] = value
        self.commit()

    @property
    def login(self):
        return self.params["login"]
    
    @login.setter
    def login(self, value):
        self.params["login"] = value
        self.commit()

    @property
    def office_website_url(self):
        return self.params["office_website_url"]
    
    @office_website_url.setter
    def office_website_url(self, value):
        self.params["office_website_url"] = value
        self.commit()

class AppConfig:
    """
    @author: purejiang
    @created: 2024/4/16

    应用配置管理
    """
    __APP_CONFIG_PATH = os.path.join(CONFIG_DIR, "app_config.json")

    @classmethod
    def getConfigFile(cls):
        return cls.__APP_CONFIG_PATH

    @classmethod
    def getAppInfo(cls)->AppInfo:
        return AppInfo(cls.__APP_CONFIG_PATH)

    @classmethod
    def getHost(cls)->Host:
        return Host(cls.__APP_CONFIG_PATH)    

class Setting(Config):
    ###### 应用设置 ######
    def __init__(self, config_file) -> None:
        super().__init__(config_file)
        self.params = self._params["setting"]

    @property
    def is_output_log(self):
        return self.params["app"]["is_output_log"]
    
    @is_output_log.setter
    def is_output_log(self, value):
        self.params["app"]["is_output_log"] = value
        self.commit()

    @property
    def theme(self):
        return self.params["app"]["theme"]
    
    @theme.setter
    def theme(self, value):
        self.params["app"]["theme"] = value
        self.commit()

    @property
    def choose_first(self):
        return self.params["adb"]["choose_first"]
    
    @choose_first.setter
    def choose_first(self, value):
        self.params["adb"]["choose_first"] = value
        self.commit()

class Path(Config):
    ###### path 配置 ######
    def __init__(self, config_file) -> None:
        super().__init__(config_file)
        self.params = self._params["path"]

    ###### re ######
    @property
    def bundletool(self):
        return self.params["re"]["bundletool"]
    
    @bundletool.setter
    def bundletool(self, value):
        self.params["re"]["bundletool"] = value
        self.commit()

    @property
    def apktool(self):
        return self.params["re"]["apktool"]
    
    @apktool.setter
    def apktool(self, value):
        self.params["re"]["apktool"] = value
        self.commit()

    @property
    def jarsigner(self):
        return self.params["re"]["jarsigner"]
    
    @jarsigner.setter
    def jarsigner(self, value):
        self.params["re"]["jarsigner"] = value
        self.commit()

    @property
    def apksigner(self):
        return self.params["re"]["apksigner"]
    
    @apksigner.setter
    def apksigner(self, value):
        self.params["re"]["apksigner"] = value
        self.commit()

    @property
    def keytool(self):
        return self.params["re"]["keytool"]
    
    @keytool.setter
    def keytool(self, value):
        self.params["re"]["keytool"] = value
        self.commit()

    @property
    def zipalign(self):
        return self.params["re"]["zipalign"]
    
    @zipalign.setter
    def zipalign(self, value):
        self.params["re"]["zipalign"] = value
        self.commit()
        
    @property
    def android_jar(self):
        return self.params["re"]["android_jar"]
    
    @android_jar.setter
    def android_jar(self, value):
        self.params["re"]["android_jar"] = value
        self.commit()

    @property
    def smali_jar(self):
        return self.params["re"]["smali_jar"]
    
    @smali_jar.setter
    def smali_jar(self, value):
        self.params["re"]["smali_jar"] = value
        self.commit()

    @property
    def adb_path(self):
        return self.params["re"]["adb_path"]
    
    @adb_path.setter
    def adb_path(self, value):
        self.params["re"]["adb_path"] = value
        self.commit()

    @property
    def aapt2_path(self):
        return self.params["re"]["aapt2_path"]
    
    @aapt2_path.setter
    def aapt2_path(self, value):
        self.params["re"]["aapt2_path"] = value
        self.commit()

    @property
    def java_path(self):
        return self.params["re"]["java_path"]
    
    @java_path.setter
    def java_path(self, value):
        self.params["re"]["java_path"] = value
        self.commit()

    ###### cache ######    
    @property
    def setting_cache(self):
        return self.params["cache"]["setting_cache"]
    
    @setting_cache.setter
    def setting_cache(self, value):
        self.params["cache"]["setting_cache"] = value
        self.commit()

    @property
    def install_cache(self):
        return self.params["cache"]["install_cache"]
    
    @install_cache.setter
    def install_cache(self, value):
        self.params["cache"]["install_cache"] = value
        self.commit()

    @property
    def parse_apk_cache(self):
        return self.params["cache"]["parse_apk_cache"]
    
    @parse_apk_cache.setter
    def parse_apk_cache(self, value):
        self.params["cache"]["parse_apk_cache"] = value
        self.commit()

    @property
    def adb_cache(self):
        return self.params["cache"]["adb_cache"]
    
    @adb_cache.setter
    def adb_cache(self, value):
        self.params["cache"]["adb_cache"] = value
        self.commit()

    @property
    def pull_apk_cache(self):
        return self.params["cache"]["pull_apk_cache"]
    
    @pull_apk_cache.setter
    def pull_apk_cache(self, value):
        self.params["cache"]["pull_apk_cache"] = value
        self.commit()

    @property
    def aapt_cache(self):
        return self.params["cache"]["aapt_cache"]
    
    @aapt_cache.setter
    def aapt_cache(self, value):
        self.params["cache"]["aapt_cache"] = value
        self.commit()

    @property
    def aab_cache(self):
        return self.params["cache"]["aab_cache"]
    
    @aab_cache.setter
    def aab_cache(self, value):
        self.params["cache"]["aab_cache"] = value
        self.commit()

    ###### data ######  
    @property
    def log_data(self):
        return self.params["data"]["log_data"]
    
    @log_data.setter
    def log_data(self, value):
        self.params["data"]["log_data"] = value
        self.commit()

    @property
    def signer_file(self):
        return self.params["data"]["signer_file"]
    
    @signer_file.setter
    def signer_file(self, value):
        self.params["data"]["signer_file"] = value
        self.commit()
     
    ###### res ###### 
    @property
    def res(self):
        return self.params["res"]
    
    @res.setter
    def res(self, value):
        self.params["res"] = value
        self.commit()

    ###### other ###### 
    @property
    def assets_res_manifest_file(self):
        return self.params["other"]["assets_res_manifest_file"]
    
    @assets_res_manifest_file.setter
    def assets_res_manifest_file(self, value):
        self.params["other"]["assets_res_manifest_file"] = value
        self.commit()
    

class UserConfig:
    """
    @author: purejiang
    @created: 2024/4/16

    用户自定义配置
    """
    __USER_CONFIG_PATH = os.path.join(DATA_DIR, "user_config.json")

    @classmethod
    def getConfigFile(cls):
        return cls.__USER_CONFIG_PATH
    
    @classmethod
    def getSetting(cls)->Setting:
        return Setting(cls.__USER_CONFIG_PATH)
    
    @classmethod
    def getPath(cls)->Path:
        if not FileHelper.fileExist(cls.__USER_CONFIG_PATH):
            FileHelper.copyFile(DEFAULT_CONFIG_PATH, cls.__USER_CONFIG_PATH)
        return Path(cls.__USER_CONFIG_PATH)
    
    @classmethod
    def getAllRe(cls)->list:
        path = cls.getPath()
        app_re_paths = []
        app_re_paths.append(path.apksigner)
        app_re_paths.append(path.adb_path)
        app_re_paths.append(path.aapt2_path)
        app_re_paths.append(path.android_jar)
        app_re_paths.append(path.smali_jar)
        app_re_paths.append(path.zipalign)
        app_re_paths.append(path.jarsigner)
        app_re_paths.append(path.java_path)
        app_re_paths.append(path.keytool)
        app_re_paths.append(path.apktool)
        app_re_paths.append(path.bundletool)
        return app_re_paths
    
    @classmethod
    def getAllCache(cls)->list:
        path = cls.getPath()
        app_caches = []
        app_caches.append(path.aab_cache)
        app_caches.append(path.adb_cache)
        app_caches.append(path.aapt_cache)
        app_caches.append(path.install_cache)
        app_caches.append(path.setting_cache)
        app_caches.append(path.pull_apk_cache)
        app_caches.append(path.parse_apk_cache)
        return app_caches