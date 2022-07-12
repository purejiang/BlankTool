# -*- coding:utf-8 -*-
"""

@author: purejiang
@created: 2021/8/25

文件处理

"""
import os
import re
import json
import math
import shutil
import struct
import hashlib
import zipfile


class FileType(object):
    """
    文件类型
    """
    @classmethod
    def __init__(self, sign, info):
        self.signature = sign
        self.info = info


class FileHelper(object):
    """
    文件操作工具类

    """
    UNIT_B = "B"
    UNIT_KB = "K"
    UNIT_MB = "M"
    UNIT_GB = "G"
    REGULAR_TIME = "time"
    REGULAR_NAME = "name"
    REGULAR_SIZE = "size"
    TYPE_DIR = "type_dir"
    TYPE_FILE = "type_file"
    TYPE_BOTH = "type_both"

    @classmethod
    def tozip(cls, dir_path, zip_file):
        """
        压缩文件

        :param dir_path: 需要压缩的文件夹
        :param zip_file: 压缩文件的路径
        """
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(dir_path):
                fpath = dirpath.replace(dir_path, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), fpath+filename)
        return True

    @classmethod
    def unzip(cls, zip_file, unnzip_dir):
        """
        解压 zip 文件

        :param zip_file: zip 文件的路径
        :param unnzip_dir: 解压的目录
        """
        with zipfile.ZipFile(zip_file, 'a') as zf:
            zf.extractall(unnzip_dir)

    @classmethod
    def zipDelFiles(cls, zip_file, del_files):
        """
        删除压缩文件里的文件

        :param zip_file: zip 文件的路径
        :param del_files: 需要删除的文件列表
        """
        zin = zipfile.ZipFile(zip_file, 'r')  # 读取对象
        new_zip_file = os.path.join(cls.parentDir(
            zip_file), "cache-{0}".format(cls.filename(zip_file)))
        zout = zipfile.ZipFile(new_zip_file, 'w')  # 被写入对象
        for item in zin.infolist():
            is_contains = False
            for del_name in del_files:
                if (item.filename.startswith(del_name)):  # 剔除要删除的文件
                    is_contains = True
                    break
            if not is_contains:
                buffer = zin.read(item.filename)
                zout.writestr(item, buffer)  # 把文件写入到新对象中
        zout.close()
        zin.close()
        shutil.move(new_zip_file, zip_file)  # 覆盖原文件

    @classmethod
    def fileExist(cls, file_path):
        """
        文件是否存在

        :param file_path: 文件的路径
        """
        return os.path.exists(os.path.abspath(file_path))

    @classmethod
    def file(cls, file_path):
        """
        文件路径获取文件对象

        :param file_path: 文件的路径
        """
        if cls.fileExist(file_path):
            return open(file_path, encoding="utf-8")
        else:
            return None

    @classmethod
    def isFile(cls, file_path):
        """
        判断是文件还是文件夹

        :param file_path: 文件的路径
        :return 文件返回 True，文件夹返回 False，不存在返回 None
        """
        if cls.fileExist(file_path):
            return os.path.isfile(os.path.abspath(file_path))
        else:
            return None

    @classmethod
    def createDir(cls, dir_path):
        """
        创建空文件夹

        :param dir_path: 文件夹
        :return 文件夹创建成功返回 True，已存在返回 False
        """
        if not cls.fileExist(dir_path):
            os.makedirs(dir_path)
            return True
        else:
            return False

    @classmethod
    def createFile(cls, file_path):
        """
        创建空文件

        :param dir_path: 文件夹
        :return 文件创建成功返回 True，已存在返回 False
        """
        if not cls.fileExist(file_path):
            with open(file_path, "w+"):
                return True
        else:
            return False

    @classmethod
    def delFile(cls, file_path):
        """
        删除文件或者文件夹

        :param file_path: 文件/文件夹
        """
        if cls.fileExist(file_path):
            if cls.isFile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
        else:
            raise FileExistsError(file_path+" is not exist.")

    @classmethod
    def rename(cls, file_path, new_name):
        """
        重命名文件或者文件夹

        :param file_path: 文件/文件夹
        :param new_name: 新名称
        """
        if cls.fileExist(file_path):
            os.renames(file_path, os.path.dirname(file_path).join(new_name))
        else:
            raise FileExistsError(file_path+" is not exist.")

    @classmethod
    def copyFile(cls, old_file, new_file, is_write=False):
        """
        复制文件或者文件夹

        :param old_file: 源文件
        :param new_file: 新文件
        :param is_write: 是否覆盖新文件，默认为 False
        """
        if not cls.fileExist(old_file):
            raise FileExistsError(old_file+" is not exist.")
        if  cls.fileExist(new_file) and not is_write:
            return
        if not cls.fileExist(cls.parentDir(new_file)):
            cls.createDir(cls.parentDir(new_file))
        if cls.isFile(old_file):
            # 如果新文件已经存在，则将其替换为源文件，否则将创建一个新文件
            shutil.copyfile(old_file, new_file)
        else:
            shutil.copytree(old_file, new_file)

    @classmethod
    def moveFile(cls, old_file, new_file, is_write=False):
        """
        移动文件或者文件夹

        :param old_file: 源文件
        :param new_file: 新文件
        :param is_write: 是否覆盖新文件，默认为 False
        """
        if not cls.fileExist(old_file):
            raise FileExistsError("old file is not exist.")
        if cls.fileExist(new_file) and is_write:
            cls.delFile(new_file)
        shutil.move(old_file, new_file)

    @classmethod
    def mergeDirs(cls, dirs, target_dir, is_write=False, is_delete=False):
        """
        合并多个文件夹

        :param dirs: 源文件夹列表
        :param target_dir: 合并后的新文件夹
        :param is_write: 是否覆盖新文件，默认为 False
        :param is_delete: 是否删除所有原文件夹，默认为 False

        """
        for old_dir in dirs:
            cls.mergeDir(old_dir, target_dir, is_write, is_delete)

    @classmethod
    def mergeDir(cls, old_dir, target_dir, is_write=False, is_delete=False):
        """
        合并两个文件夹

        :param old_dir: 源文件夹
        :param target_dir: 基准文件夹
        :param is_write: 是否覆盖基准文件夹里的文件，默认为 False
        :param is_delete: 是否删除原文件夹，默认为 False        
        """
        if not cls.fileExist(old_dir):
            raise FileExistsError("old dir is not exist.")
        for file in os.listdir(old_dir):
            old_file = os.path.join(old_dir, file)
            new_file = os.path.join(target_dir, file)
            cls.copyFile(old_file, new_file, is_write)
        if is_delete:  # 合并完成后再删除原文件夹
            cls.delFile(old_dir)

    @classmethod
    def diff(cls, first_dir, second_dir):
        """
        删除另一个文件夹中的同名文件

        :param first_dir: 源文件夹
        :param second_dir: 基准文件夹       
        """
        for file in os.listdir(first_dir):
            new_file = os.path.join(second_dir, file)
            if cls.fileExist(new_file):
                if cls.isFile(file):
                    cls.diff(os.path.join(first_dir, file), new_file)
                else:
                    cls.delFile(new_file)

    @classmethod
    def getSuffix(cls, file_path):
        """
        获取文件后缀

        :param file_path: 文件      
        """
        return os.path.splitext(file_path)[1]

    @classmethod
    def filename(cls, file_path, suffix=True):
        """
        获取文件名

        :param file_path: 文件   
        :param suffix: 是否带后缀，默认为 True   
        """
        if suffix:
            return os.path.basename(file_path)
        return os.path.splitext(os.path.basename(file_path))[0]

    @classmethod
    def fileContent(cls, file_path):
        """
        获取文件内容并返回为字符串

        :param file_path: 文件
        :return 文件内容字符串      
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @classmethod
    def fileSize(cls, file_path, unit):
        """
        获取文件大小，单位为字节

        :param file_path: 文件
        :param unit: 计量单位

        :return 携带计量单位的字符串，如"50 KB"，"50 GB"
        """
        size = os.path.getsize(file_path)
        if unit == cls.UNIT_B:
            return size
        elif unit == cls.UNIT_KB:
            return size / 1024.0
        elif unit == cls.UNIT_MB:
            return size / 1024.0 ** 2
        elif unit == cls.UNIT_GB:
            return size / 1024.0 ** 3

    @classmethod
    def getAllChild(cls, file_path, type, file_list=None):
        """
        获取文件夹下的所有文件/文件夹，递归

        :param file_path: 文件夹
        :param type: 获取的类型
        """
        if file_list is None:
            file_list = []
        if cls.fileExist(file_path):
            files = os.listdir(file_path)
            for file in files:
                temp_path = os.path.join(file_path, file)
                if cls.isFile(temp_path) and type is cls.TYPE_FILE:
                    file_list.append(temp_path)
                elif not cls.isFile(temp_path):
                    if type is cls.TYPE_DIR:
                        file_list.append(temp_path)
                    cls.getAllChild(temp_path, type, file_list)
            return file_list

    @classmethod
    def getChild(cls, file_path, type):
        """
        获取文件夹下的所有的文件/文件夹(不包括子目录)

        :param file_path: 文件夹
        :param type: 要获取的类型
        :return 文件/文件夹列表
        """
        if cls.fileExist(file_path):
            files = os.listdir(file_path)
            if type is cls.TYPE_FILE:
                return [os.path.join(file_path, file) for file in files if cls.isFile(file)]
            elif type is cls.TYPE_DIR:
                return [os.path.join(file_path, file) for file in files if not cls.isFile(file)]
            else:
                return [os.path.join(file_path, file) for file in files]

    @classmethod
    def sortFile(cls, dir_path, regular):
        """
        文件夹排序

        :param dir_path: 文件夹
        :param regular: 排序的类型（名称，时间，大小）
        """
        file_list = os.listdir(dir_path)
        if regular is cls.REGULAR_NAME:
            return sorted(file_list, key=lambda x: os.path.basename(os.path.join(dir_path, x)))
        elif regular is cls.REGULAR_SIZE:
            return sorted(file_list, key=lambda x: os.path.getsize(os.path.join(dir_path, x)))
        elif regular is cls.REGULAR_TIME:
            return sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(dir_path, x)))

    @classmethod
    def parentDir(cls, file_path):
        """
        获取文件的父目录的绝对路径
        """
        return os.path.abspath(os.path.dirname(file_path))

    @classmethod
    def checkSame(cls, first_file, second_file):
        """
        判断两个路径是否指向同一文件夹/文件
        """
        return os.path.samefile(first_file, second_file)

    @classmethod
    def checkSameFile(cls, first_file, second_file):
        """
        判断两个文件内容是否相同
        """
        content1 = ""
        content2 = ""
        with open(first_file, "r", encoding="utf-8") as file1:
            content1 = file1.readlines()
        with open(second_file, "r", encoding="utf-8") as file2:
            content2 = file2.readlines()
        return content1 == content2

    # 替换文件内容(支持正则式)
    @classmethod
    def replaceRe(cls, file_path, re_str, new_str):
        """
        替换文件内容(支持正则式)

        :param file_path: 文件
        :param re_str: 正则表达式
        :param new_str: 替换的新内容

        """
        with open(file_path, "r+", encoding="utf-8") as file:
            content = ""
            for line in file.readlines():
                content += line
            re.sub(re_str, new_str, content)
            file.write(content)

    @classmethod
    def replace(cls, file_path, kvs):
        """
        替换文件内容(不支持正则式)

        :param file_path: 文件
        :param re_str: 旧内容和新内容的 map
        """
        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read()
            for key in kvs:
                content = content.replace(str(key), str(kvs[key]))
            file.seek(0)
            file.truncate()
            file.write(content)

    @classmethod
    def md5(cls, file_path):
        """
        获取文件 MD5
        """
        return hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    @classmethod
    def bytes2hex(cls, bytes) -> str:
        """ 字节码转16进制 """
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    # 获取文件类型
    @classmethod
    def getFileType(cls, file_path):
        """
        根据文件特征值获取文件类型

        :param file_path: 文件
        :return FileType 对象
        """
        signature_list = json.loads(cls.fileContent(
            "file_signature.json"))  # 读取文件特征值文件
        with open(file_path, 'rb') as byte_file:  # 必须读取二进制数据
            sign = ''
            info = []
            for it in signature_list:  # 遍历整个列表
                numOfBytes = len(it['signature']) / 2  # 需要读多少字节
                byte_file.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
                bytes = struct.unpack_from("B" * math.ceil(numOfBytes),
                                           byte_file.read(math.ceil(numOfBytes)))  # 一个 "B" 表示一个字节
                if cls.bytes2hex(bytes) == it['signature']:
                    sign = it['signature']
                    if cls.getSuffix(file_path).lstrip(".") == it['extension'].lower():
                        info = [
                            {'ext': it['extension'].lower(), 'des':it['description']}]
                        break
                    else:
                        info.append(
                            {'ext': it['extension'].lower(), 'des': it['description']})
                return FileType(sign, info)

    @classmethod
    def delLongPathDir(cls, dir_path):
        """
        删除路径过长的文件夹

        :param dir_path: 文件夹
        """
        index = 0
        old_dir = dir_path
        try:
            while True:
                for file in cls.getChild(old_dir, cls.TYPE_DIR):
                    index += 1
                    new_dir = r"{0}\{1}".format(dir_path, index)
                    cls.moveFile(file, new_dir)
                old_dir = r"{0}\{1}".format(dir_path, index)
        except Exception as e:
            cls.delFile(dir_path)
