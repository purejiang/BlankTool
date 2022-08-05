# -*- coding:utf-8 -*-

import sys
from common.myapplication import MyApplication

from ui.main_route import MainRoute


if __name__ == '__main__':
    app = MyApplication(sys.argv)

    login_route = MainRoute(app)
    
    app.show(MainRoute)

    sys.exit(app.exec_())
