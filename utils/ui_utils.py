# -*- coding:utf-8 -*-
import os
from PySide2.QtWidgets import QFileDialog

def chooseFile(window, title, type):
    file_name, file_type = QFileDialog.getOpenFileName(window, title, os.getcwd(), type)
    return file_name