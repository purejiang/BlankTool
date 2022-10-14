# -*- coding:utf-8 -*-
import os
from PySide2.QtWidgets import QFileDialog

# 相对于父窗口偏移点距离，避免完全遮盖父窗口
OFFSET_X = 30
OFFSET_Y = 30

def toast_left(widget):
    return widget.geometry().x() + widget.size().width() / 2

def toast_top(widget):
    return widget.geometry().y() + widget.size().height() / 13

def chooseFile(window, title, type):
    file_path, file_type = QFileDialog.getOpenFileName(window, title, os.getcwd(), type)
    return file_path

def chooseDir(window, title):
    dir_path = QFileDialog.getExistingDirectory(window, title)
    return dir_path