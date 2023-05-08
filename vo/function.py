# -*- coding:utf-8 -*-


from widget.function.widget_function import FunctionWidget




class Function:
    """
    @author: purejiang
    @created: 2022/7/14

    功能列表分类

    """
    def __init__(self, name:str, icon_path:str, function_widget:FunctionWidget):
        """
        :param name: 标题
        :param icon_path: icon
        :param function_widget: 功能页
        """
        self.name = name
        self.icon_path = icon_path
        self.function_widget = function_widget

    def __str__(self):
        return str(self.__dict__)
    
class FunctionType:
    """
    @author: purejiang
    @created: 2023/4/20

    功能列表总类

    """
    def __init__(self, name:str, icon:str, fucntion_list:list[Function]):
        """
        :param name: 标题
        :param icon: icon
        :param fucntion_list: 功能数组
        """
        self.name = name
        self.icon = icon
        self.fucntion_list = fucntion_list

    def __str__(self):
        return str(self.__dict__)
