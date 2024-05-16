# -*- coding:utf-8 -*-

import json
import traceback
from common.config import UserConfig
from utils.file_helper import FileHelper
from utils.jlogger import JLogger
from utils.other_util import currentTimeNumber
from vo.signer import SignerConfig


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
    logger = JLogger()

    @classmethod
    def addKeystore(cls, curr_signer_config, progress_callback):
        """
        添加 keystore

        :param curr_signer_config: 当前签名配置

        """
        cls.logger.info("add keystore {0} ...".format(curr_signer_config.signer_file_path))
        file_md5 = FileHelper.md5(curr_signer_config.signer_file_path)
        curr_signer_config.file_md5 = file_md5
        curr_signer_config.create_time = currentTimeNumber()
        curr_signer_config.update_time = currentTimeNumber()

        is_exist = False
        max_id = 0
        signer_config_list =[]
        for exist_signer_config in cls.allSigners(progress_callback):
            if exist_signer_config.signer_id > max_id:
                max_id = exist_signer_config.signer_id

            if curr_signer_config.signer_name == exist_signer_config.signer_name or curr_signer_config.file_md5 == exist_signer_config.file_md5:
                cls.logger.info("{} is exist.".format(exist_signer_config.signer_name))
                is_exist = True
            signer_config_list.append(exist_signer_config.__dict__)

        if not is_exist:
            curr_signer_config.signer_id = max_id+1
            signer_config_list.append(curr_signer_config.__dict__)
        else:
            return False

        return FileHelper.writeContent(UserConfig.getPath().signer_file, json.dumps(signer_config_list))

    @classmethod
    def delSigner(cls, signer_id, progress_callback):
        """
        删除签名

        :param signer_id: 签名配置 id

        """
        cls.logger.info("del signer by id:{0} ...".format(signer_id))
        signer_data_list = json.loads(FileHelper.fileContent(UserConfig.getPath().signer_file))
        for signer_str in signer_data_list:
            signer = json2obj(signer_str, SignerConfig)
            if signer.signer_id == signer_id:
                signer_data_list.remove(signer_str)
        return FileHelper.writeContent(UserConfig.getPath().signer_file, json.dumps(signer_data_list))

    @classmethod
    def modifySigner(cls, curr_signer_config: SignerConfig, progress_callback):
        """
        修改签名

        :param curr_signer_config: 当前签名配置

        """
        cls.logger.info("modify keystore {0} ...".format(curr_signer_config.signer_name))
        all_signer_list = []
        for signer_config in cls.allSigners(None):
            if curr_signer_config.signer_id == signer_config.signer_id:
                curr_signer_config.update_time = currentTimeNumber()
                all_signer_list.append(curr_signer_config.__dict__)
            else:
                all_signer_list.append(signer_config.__dict__)
        cls.logger.info("writeContent: {0}".format(all_signer_list))        
        return FileHelper.writeContent(UserConfig.getPath().signer_file, json.dumps(all_signer_list))

    @classmethod
    def allSigners(cls, progress_callback) -> list:
        """
        获取所有的签名
        """
        cls.logger.info("get all signer ...")
        signer_list =[]
        try:
            if not FileHelper.fileExist(UserConfig.getPath().signer_file):
                with open(UserConfig.getPath().signer_file, 'w') as file:
                    pass
            signer_data_list = json.loads(FileHelper.fileContent(UserConfig.getPath().signer_file))
            for signer_str in signer_data_list:
                signer_list.append(json2obj(signer_str, SignerConfig))
            signer_list1 = sorted(signer_list, key=lambda x: x.update_time, reverse=True)
            signer_list2 = sorted(signer_list1, key=lambda x: x.sort)
            return signer_list2
        except Exception as e:
            cls.logger.warning(""+traceback.format_exc())
            return signer_list

    @classmethod
    def getSigner(cls, signer_id, progress_callback) -> SignerConfig:
        """
        获取签名

        :param signer_id: 签名配置 id

        """
        cls.logger.info("get signer by id: {}...".format(signer_id))
        signer_data_list = json.loads(FileHelper.fileContent(UserConfig.getPath().signer_file))
        for signer_str in signer_data_list:
            signer_config = json2obj(signer_str, SignerConfig)
            if signer_config.signer_id == signer_id:
                return signer_config
        return None
