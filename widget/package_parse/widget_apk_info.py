# -*- coding:utf-8 -*-

from PySide6.QtWidgets import QTableWidgetItem,QHeaderView,QLabel
from viewmodel.apk_viewmodel import ApkViewModel
from PySide6.QtGui import QPixmap

from vo.apk_info import ApkInfo

from widget.function.widget_function import FunctionWidget


class ApkInfoWidget(FunctionWidget):
    """

    @author: purejiang
    @created: 2023/3/16

    Apk 信息对应的主页
    """
    __UI_FILE = "./res/ui/widget_apk_info.ui"
    __QSS_FILE = "./res/qss/widget_apk_info.qss"

    def __init__(self, main_window) -> None:
        super().__init__(main_window, self.__UI_FILE, self.__QSS_FILE)
        self.__initView()

    def _onPreShow(self):
        pass

    def _entry(self):
        if ApkViewModel._parse_apk_info !=None:
            self._ui.lb_notic_please_update_apk.setVisible(False)
            self._ui.tw_apk_info_table.setVisible(True)
            self.__showApkInfo(ApkViewModel._parse_apk_info)
        else:
            self._ui.lb_notic_please_update_apk.setVisible(True)
            self._ui.tw_apk_info_table.setVisible(False)
    
    def _setupListener(self):
        pass

    def __showApkInfo(self, apk_info:ApkInfo):
        table = self._ui.tw_apk_info_table
        data_set = self.__apkinfo2data(apk_info)
        columb_count=2
        row_count=len(data_set)
        table.setRowCount(row_count)
        table.setColumnCount(columb_count)
        table.setHorizontalHeaderLabels(["属性", "值"])
        # 宽度
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # 将第二列的 ResizeMode 设置为 Stretch
        table.setColumnWidth(0, table.columnWidth(1)/2) # 将第一列宽度设置为第二列宽度的一半

        # 隐藏行号
        table.verticalHeader().setHidden(True)
        table.verticalHeader().resizeSection(0, 60)
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                if row == 0 and col == 1:
                    image = QPixmap(apk_info.icon)
                    label = QLabel()
                    label.setPixmap(image)
                    label.setScaledContents(True)
                    label.setMaximumSize(48, 48)  # 设置最大尺寸为50*50
                    table.setCellWidget(row, col, label)
                else:
                    tableItem = QTableWidgetItem(data_set[row][col])
                    table.setItem(row, col, tableItem)


    def __apkinfo2data(self, apkinfo:ApkInfo):
        dataset = []
        dataset.append(["icon", apkinfo.icon])
        dataset.append(["app name", apkinfo.app_name])
        dataset.append(["apk path", apkinfo.apk_path])
        dataset.append(["package name", apkinfo.package_name])
        dataset.append(["version code", apkinfo.version_code])
        dataset.append(["version name", apkinfo.version_name])
        dataset.append(["target sdk version", apkinfo.target_version])
        dataset.append(["min sdk version", apkinfo.min_version])
        dataset.append(["abis", apkinfo.abis])
        dataset.append(["langs", apkinfo.langs])
        dataset.append(["md5", apkinfo.md5])
        dataset.append(["signer md5", apkinfo.signer_md5])
        dataset.append(["signer sha1", apkinfo.signer_sha1])
        dataset.append(["signer sha256", apkinfo.signer_sha256])
        return dataset

    def __initView(self):
        pass
    