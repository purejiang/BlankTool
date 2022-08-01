# -*- coding:utf-8 -*-

from PySide2.QtCore import QFile, QIODevice, QMetaObject
from PySide2.QtUiTools import QUiLoader

class BaseUi():
    """

    @author: purejiang
    @created: 2022/7/7

    基础的 UI，实现解析 .qss 文件和动态加载 .ui 文件

    """
    def __init__(self):
        self._ui = None

    def _loadQss(self, qss_file):
        """
        解析 qss 文件
        """
        qfile = QFile(qss_file)
        if qfile.open(QIODevice.ReadOnly):
            byteArrayStyleSheet = qfile.readAll()
            qfile.close()
            return str(byteArrayStyleSheet, encoding='utf-8')
            

    def _loadUi(self, ui_file):
        """
        加载 ui 文件
        """
        self._ui = MyUiLoad().loadUi(ui_file, self)


class MyUiLoad(QUiLoader):
    __baseInstance =None
    """
    将 .ui 转换 widget 的链接到原有的widget 上，使得在原有的 widget 里可以通过 self.xxx 去实现功能
    """

    def createWidget(self, classname, parent=None, name=""):
        if parent is None and self.__baseInstance is not None:
            widget = self.__baseInstance
        else:
            widget = super(MyUiLoad, self).createWidget(classname, parent, name)
            if self.__baseInstance is not None:
                setattr(self.__baseInstance, name, widget)
        return widget
    
    def loadUi(self, ui_file, base_instance=None):
        self.__baseInstance = base_instance 
        widget = self.load(ui_file)
        QMetaObject.connectSlotsByName(widget)
        return widget