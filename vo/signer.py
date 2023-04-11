# -*- coding:utf-8 -*-
import json

class SignerConfig:
    """
    @author: purejiang
    @created: 2022/10/10

    签名相关信息的对象

    """

    def __init__(self):
        """
        :param signer_id: 签名信息的id
        :param file_md5: 签名文件的md5
        :param signer_name: 文件名
        :param signer_file_path: signer 的路径
        :param signer_pwd: signer 密码
        :param signer_alias: key 别名
        :param signer_key_pwd: key 密码
        :param create_time: 创建时间
        :param udpate_time: 更新时间
        :param sort: 排序的优先级
        :param is_used: 是否在使用列表中
        """
        self.signer_id = 0
        self.file_md5 = ""
        self.signer_name = ""
        self.signer_file_path = ""
        self.signer_pwd = ""
        self.signer_alias = ""
        self.signer_key_pwd = ""
        self.create_time = 0
        self.update_time = 0
        self.sort = 0
        self.is_used = False

    def __str__(self):
        return str(json.dumps(self.__dict__))