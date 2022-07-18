# -*- coding:utf-8 -*-

import os


class ApkInfo:
    """
    @author: purejiang
    @created: 2022/7/14

    apk 相关信息的数据对象

    """
    def __init__(self, apk_path, app_name, icon, package_name, version_code,
                 version_name, target_version, min_version, abis, langs, output_path=None):
        """
        :param apk_path: apk 路径
        :param app_name: app 名称
        :param icon: icon 的路径
        :param package_name: 包名
        :param version_code: 版本号
        :param version_name: 版本名
        :param target_version: 目标版本
        :param min_version: 最小版本
        :param abis: 支持的架构
        :param langs: 支持的语言
        :param output_path: 反编后的路径，可为空
        """
        self.apk_path = apk_path
        self.app_name = app_name
        self.output_path = output_path
        if output_path!= None:
            self.icon = os.path.join(output_path, icon)
        else:
            self.icon = icon
        self.package_name = package_name
        self.version_code = version_code
        self.version_name = version_name
        self.target_version = target_version
        self.min_version = min_version
        self.abis = abis
        self.langs = langs

    def __str__(self):
        return str(self.__dict__)