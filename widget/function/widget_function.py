# -*- coding:utf-8 -*-

from abc import abstractmethod
from widget.base.base_widget import BaseWidget


class FunctionWidget(BaseWidget):
    """

    @author: purejiang
    @created: 2023/4/20

    功能页的基类
    """

    def __init__(self, main_window, ui_file, qss_file) -> None:
        super(FunctionWidget, self).__init__(main_window, ui_file, qss_file)