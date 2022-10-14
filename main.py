# -*- coding:utf-8 -*-

import os
import sys
from common.constant import Constant
from common.myapplication import MyApplication
from PySide2.QtCore import QResource
from ui.main_route import MainRoute
from utils.file_helper import FileHelper


if __name__ == '__main__':
    # 读取 .rcc s资源
    try:
        for file in FileHelper.getChild(os.path.join(Constant.AppPath.APP_PATH, Constant.AppPath.RESOURCE_PATH), FileHelper.TYPE_FILE):
            if FileHelper.getSuffix(file)==".rcc":
                QResource.registerResource(file)
    except Exception as e:
        print("load .rcc error.")
        
    os.chdir(sys.path[0]) 
    
    app = MyApplication(sys.argv)

    login_route = MainRoute(app)
    
    app.show(MainRoute)

    sys.exit(app.exec_())
