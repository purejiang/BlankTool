# -*- coding:utf-8 -*-

from PySide2.QtCore import QFile, QIODevice, QMetaObject
from PySide2.QtUiTools import QUiLoader

class BaseUi():

    def __init__(self):
        self._ui = None

    def _loadQss(self, qss_file):
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