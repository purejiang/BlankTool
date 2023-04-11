# -*- coding:utf-8 -*-
import os
from PySide6.QtWidgets import QFileDialog

def chooseFile(window, title, type):
    file_path, file_type = QFileDialog.getOpenFileName(window, title, os.getcwd(), type)
    return file_path

def chooseDir(window, title):
    dir_path = QFileDialog.getExistingDirectory(window, title)
    return dir_path