# -*- coding:utf-8 -*-

import sys
from common.myapplication import MyApplication
from widget.window_main import MainWindow


if __name__ == '__main__':

        app = MyApplication(sys.argv)

        login_route = MainWindow(app)
        
        app.show(MainWindow)

        sys.exit(app.exec())