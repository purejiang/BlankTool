# -*- coding:utf-8 -*-

class ApkInfo:
    """
    @author: purejiang
    @created: 2022/7/14

    apk 相关信息的数据对象

    """
    def __init__(self, apk_path, aap_name, icon, package_name, version_code,
                 version_name, target_version, min_version, abis, langs, output_path=None):
        """
        :param apk_path: apk 路径
        :param aap_name: app 
        :param icon: 反编后目录
        :param package_name: 是否忽略错误的 dex, 默认不忽略
        :param version_code: 是否只反编译资源文件, 默认编译所有
        :param version_name: 是否只反编译资源文件, 默认编译所有
        :param target_version: 是否只反编译资源文件, 默认编译所有
        :param min_version: 是否只反编译资源文件, 默认编译所有
        :param abis: 是否只反编译资源文件, 默认编译所有
        :param langs: 是否只反编译资源文件, 默认编译所有
        :param output_path: 反编后的路径，可为空
        """
        self.apk_path = apk_path
        self.aap_name = aap_name
        self.output_path = output_path
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