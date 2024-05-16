# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_setting.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(764, 571)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 771, 571))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(24, 12, 24, 12)
        self.widget_setting = QWidget(self.verticalLayoutWidget)
        self.widget_setting.setObjectName(u"widget_setting")
        self.verticalLayoutWidget_2 = QWidget(self.widget_setting)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 721, 551))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(24, 12, 24, 12)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.lb_cache_totle_size = QLabel(self.verticalLayoutWidget_2)
        self.lb_cache_totle_size.setObjectName(u"lb_cache_totle_size")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_cache_totle_size.sizePolicy().hasHeightForWidth())
        self.lb_cache_totle_size.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lb_cache_totle_size)

        self.pb_clean_cache = QPushButton(self.verticalLayoutWidget_2)
        self.pb_clean_cache.setObjectName(u"pb_clean_cache")
        sizePolicy.setHeightForWidth(self.pb_clean_cache.sizePolicy().hasHeightForWidth())
        self.pb_clean_cache.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pb_clean_cache)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(24, 12, 24, 12)
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.ckb_is_output_log = QCheckBox(self.verticalLayoutWidget_2)
        self.ckb_is_output_log.setObjectName(u"ckb_is_output_log")

        self.horizontalLayout_2.addWidget(self.ckb_is_output_log)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(24, 12, 24, 12)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.lb_app_vesion_name = QLabel(self.verticalLayoutWidget_2)
        self.lb_app_vesion_name.setObjectName(u"lb_app_vesion_name")
        sizePolicy2.setHeightForWidth(self.lb_app_vesion_name.sizePolicy().hasHeightForWidth())
        self.lb_app_vesion_name.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.lb_app_vesion_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(24, 12, 24, 12)
        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.lb_app_vesion_code = QLabel(self.verticalLayoutWidget_2)
        self.lb_app_vesion_code.setObjectName(u"lb_app_vesion_code")
        sizePolicy2.setHeightForWidth(self.lb_app_vesion_code.sizePolicy().hasHeightForWidth())
        self.lb_app_vesion_code.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.lb_app_vesion_code)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(24, 12, 24, 12)
        self.label_5 = QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.lb_app_build_time = QLabel(self.verticalLayoutWidget_2)
        self.lb_app_build_time.setObjectName(u"lb_app_build_time")
        sizePolicy2.setHeightForWidth(self.lb_app_build_time.sizePolicy().hasHeightForWidth())
        self.lb_app_build_time.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.lb_app_build_time)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(24, 12, 24, 12)
        self.label_7 = QLabel(self.verticalLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_7)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.lb_app_mode = QLabel(self.verticalLayoutWidget_2)
        self.lb_app_mode.setObjectName(u"lb_app_mode")
        sizePolicy2.setHeightForWidth(self.lb_app_mode.sizePolicy().hasHeightForWidth())
        self.lb_app_mode.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.lb_app_mode)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(24, 12, 24, 12)
        self.label_9 = QLabel(self.verticalLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.label_9)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.lb_app_web_url = QLabel(self.verticalLayoutWidget_2)
        self.lb_app_web_url.setObjectName(u"lb_app_web_url")
        sizePolicy2.setHeightForWidth(self.lb_app_web_url.sizePolicy().hasHeightForWidth())
        self.lb_app_web_url.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.lb_app_web_url)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(7, 7)

        self.verticalLayout.addWidget(self.widget_setting)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u7f13\u5b58\u5927\u5c0f\uff1a", None))
        self.lb_cache_totle_size.setText("")
        self.pb_clean_cache.setText(QCoreApplication.translate("Form", u"\u6e05\u7406\u7f13\u5b58", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u5f00\u542f\u65e5\u5fd7\u8f93\u51fa", None))
        self.ckb_is_output_log.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u5e94\u7528\u7248\u672c\u540d\uff1a", None))
        self.lb_app_vesion_name.setText(QCoreApplication.translate("Form", u"version_name", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5e94\u7528\u7248\u672c\u53f7\uff1a", None))
        self.lb_app_vesion_code.setText(QCoreApplication.translate("Form", u"version_code", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u51fa\u5305\u65f6\u95f4\uff1a", None))
        self.lb_app_build_time.setText(QCoreApplication.translate("Form", u"time", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u6a21\u5f0f\uff1a", None))
        self.lb_app_mode.setText(QCoreApplication.translate("Form", u"mode", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u5b98\u7f51\uff1a", None))
        self.lb_app_web_url.setText(QCoreApplication.translate("Form", u"url", None))
    # retranslateUi

