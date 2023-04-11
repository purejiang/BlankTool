# -*- coding:utf-8 -*-

import json
import traceback
from typing import Union
from utils.file_helper import FileHelper
from utils.b_loger import Loger
from utils.other_util import currentTimeNumber
from vo.signer import SignerConfig



USED_SIGNERS = "used_signers"
USENESS_SIGNERS = "useness_signers"
SIGNER_FILE = "./data/signer.json"

def json2obj(class_dict ,clazz):
    result = clazz()
    result.__dict__ = class_dict
    return result

def json2obj(class_dict ,clazz):
    result = clazz()
    result.__dict__ = class_dict
    return result

class SignerManager():
    """

    @author: purejiang
    @created: 2022/10/10

    签名相关的功能管理

    """
    loger = Loger()

    @classmethod
    def addKeystore(cls, curr_signer_config, progress_callback):
        """
        添加 keystore

        :param keystore_info: keystore 信息

        """
        cls.loger.info("add keystore {0} ...".format(curr_signer_config.signer_file_path))
        file_md5 = FileHelper.md5(curr_signer_config.signer_file_path)
        curr_signer_config.file_md5 = file_md5
        curr_signer_config.create_time = currentTimeNumber()
        curr_signer_config.update_time = currentTimeNumber()

        is_exist = False
        max_id = 0
        signer_config_list =[]
        for signer_config in cls.allSigners(None):
            if signer_config.signer_id > max_id:
                max_id = signer_config.signer_id

            if curr_signer_config.signer_name == signer_config.signer_name or curr_signer_config.file_md5 == signer_config.file_md5:
                cls.loger.info("{} is exist.".format(signer_config.signer_name))
                is_exist = True
            signer_config_list.append(signer_config.__dict__)

        if not is_exist:
            curr_signer_config.signer_id = max_id+1
            signer_config_list.append(curr_signer_config.__dict__)
        else:
            return False

        return FileHelper.writeContent(SIGNER_FILE, json.dumps(signer_config_list))

    @classmethod
    def delSigner(cls, signer_id, progress_callback):
        """
        删除 signer

        :param signer_config: signer 信息

        """
        cls.loger.info("del signer by id:{0} ...".format(signer_id))
        signer_data_list = json.loads(FileHelper.fileContent(SIGNER_FILE))
        for signer_str in signer_data_list:
            signer = json2obj(signer_str, SignerConfig)
            if signer.signer_id == signer_id:
                signer_data_list.remove(signer_str)
        return FileHelper.writeContent(SIGNER_FILE, json.dumps(signer_data_list))

    @classmethod
    def modifySigner(cls, curr_signer_config: SignerConfig, progress_callback):
        """
        修改 signer

        :param signer_config: signer 信息

        """
        cls.loger.info("modify keystore {0} ...".format(curr_signer_config.signer_name))
        all_signer_list = []
        for signer_config in cls.allSigners(None):
            if curr_signer_config.signer_id == signer_config.signer_id:
                curr_signer_config.update_time = currentTimeNumber()
                all_signer_list.append(curr_signer_config.__dict__)
            else:
                all_signer_list.append(signer_config.__dict__)
        cls.loger.info("writeContent: {0}".format(all_signer_list))        
        return FileHelper.writeContent(SIGNER_FILE, json.dumps(all_signer_list))

    @classmethod
    def allSigners(cls, progress_callback) -> list or None:
        """
        获取所有的 keystore config

        """
        cls.loger.info("get all signer ...")
        try:
            signer_list =[]
            signer_data_list = json.loads(FileHelper.fileContent(SIGNER_FILE))
            for signer_str in signer_data_list:
                signer_list.append(json2obj(signer_str, SignerConfig))

            signer_list.sort(key=lambda x: x.sort, reverse=True)
            return signer_list
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return None

    @classmethod
    def getSigner(cls, signer_id, progress_callback) -> SignerConfig:
        cls.loger.info("get signer by id: {}...".format(signer_id))
        signer_data_list = json.loads(FileHelper.fileContent(SIGNER_FILE))
        for signer_str in signer_data_list:
            signer_config = json2obj(signer_str, SignerConfig)
            if signer_config.signer_id == signer_id:
                return signer_config
        return None
