# -*- coding:utf-8 -*-

import os
import sys
from common.myapplication import MyApplication

from ui.main_route import MainRoute


if __name__ == '__main__':
    os.chdir(sys.path[0]) 
    
    app = MyApplication(sys.argv)

    login_route = MainRoute(app)
    
    app.show(MainRoute)

    sys.exit(app.exec_())
