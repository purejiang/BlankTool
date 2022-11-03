# -*- coding:utf-8 -*-

import json
import os
from common.cmd import CMD
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.other_util import write_print
from vo.keystore_config import KeystoreConfig


class SignerManager(object):
    """

    @author: purejiang
    @created: 2022/10/10

    签名相关的功能管理

    """
    signer_data_path  = os.path.join(Constant.Data.DATA_PATH, "signer.json")
    signer_data_key = "keystore_config"

    @classmethod
    def addKeystore(cls, keystore_config, loguer = None):
        """
        添加 keystore

        :param keystore_info: keystore 信息
        :param loguer: 日志工具，可空

        """
        write_print(loguer, "add keystore {0} ...".format(keystore_config.keystore_name))
        if keystore_config.keystore_path =="":
            return False

        keystore_dict = json.loads(FileHelper.fileContent(cls.signer_data_path))
        if keystore_config.keystore_name in keystore_dict:
            write_print(loguer, "{} is exist.".format(keystore_config.keystore_name))
        keystore_dict[keystore_config.keystore_name] = str(keystore_config)
        return FileHelper.writeContent(cls.signer_data_path, json.dumps(keystore_dict))

    @classmethod
    def delKeystore(cls, keystore_config, loguer = None):
        """
        删除 keystore

        :param keystore_info: keystore 信息
        :param loguer: 日志工具，可空

        """
        write_print(loguer, "del keystore {0} ...".format(keystore_config.keystore_name))
        keystore_dict = json.loads(FileHelper.fileContent(cls.signer_data_path))
        keystore_dict.pop(keystore_config.keystore_name)
        return FileHelper.writeContent(cls.signer_data_path, json.dumps(keystore_dict))

    @classmethod
    def getKeystores(cls, loguer=None):
        """
        获取 keystore

        :param loguer: 日志工具，可空

        """
        write_print(loguer, "get keystores ...")
        try:
            keystore_dict = json.loads(FileHelper.fileContent(cls.signer_data_path))
            keystore_config_list =[]
            for keystore in keystore_dict.values():
                keystore_json = json.loads(keystore)
                keystore_config = KeystoreConfig(keystore_json["keystore_name"], keystore_json["keystore_path"], keystore_json["keystore_password"], keystore_json["key_alias"], keystore_json["key_password"], keystore_json["step"])
                keystore_config_list.append(keystore_config)
            keystore_config_list.sort(key=lambda x:x.step, reverse=True)
            return True, keystore_config_list
        except Exception as e:
            write_print(loguer, str(e))
            return False

    @classmethod
    def sign(cls, apk_path, out_path, keystore_config, loguer=None):
        """
        对 apk 签名

        :param apk_path: 未签名的 apk 路径
        :param out_path: 签名后的 apk 输出的路径
        :param keystore_info: keystore 信息
        :param loguer: 日志工具，可空

        """
        write_print(loguer, "sign {0} ...".format(apk_path))
        cmd_result = CMD.signApk(Constant.Re.JARSIGNER_PATH, apk_path, out_path, keystore_config)
        write_print(loguer, cmd_result[1])
        return cmd_result[0]