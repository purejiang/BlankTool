# -*- coding:utf-8 -*-

import sys
from common.myapplication import MyApplication
from widget.window_init import InitWindow



if __name__ == '__main__':

        app = MyApplication(sys.argv)

        MyApplication.showClazz(app, InitWindow)

        sys.exit(app.exec())