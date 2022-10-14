# -*- coding:utf-8 -*-


import json


class KeystoreConfig:
    """
    @author: purejiang
    @created: 2022/10/10

    签名相关信息的对象

    """
    def __init__(self, keystore_name, keystore_path, keystore_password, key_alias, key_password, step):
        """
        :keystore_name: 文件别名
        :param keystore_path: keystore 的路径
        :param keystore_password: keystore 密码
        :param key_alias: key 别名
        :param key_password: key 密码
        :param step: 默认使用的顺序
        """
        self.keystore_path = keystore_path
        self.keystore_password = keystore_password
        self.key_alias = key_alias
        self.key_password = key_password
        self.step = step
        self.keystore_name = keystore_name

    def __str__(self):
        return str(json.dumps(self.__dict__))
