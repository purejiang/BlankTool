# -*- coding:utf-8 -*-


class Function:
    """
    @author: purejiang
    @created: 2022/7/14

    列表功能类

    """
    def __init__(self, title:str, icon:str, widget_list:list):
        """
        :param title: 标题
        :param icon: icon
        :param widgets: 包含的控件
        """
        self.title = title
        self.icon = icon
        self.widget_list = widget_list

    def __str__(self):
        return str(self.__dict__)
