import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from models.voucher import VoucherManager
from models.data import Voucher, VoucherDetail


class VoucherSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.voucherManage = VoucherManager()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("凭证汇总")
        self.resize(900, 600)

        mainLayout = QVBoxLayout()

        # 内容
        self.contentWidget = QWidget()
        contentLayout = QVBoxLayout(self.contentWidget)

        ## 会计时期
        periodLayout = QHBoxLayout()
        periodLb = QLabel("会计时期")
        periodSLb = QLabel("从第")
        self.periodComboS = QComboBox()         # 开始时期
        periodMLb = QLabel(" - 第")
        self.periodComboE = QComboBox()         # 结束时期
        periodELb = QLabel("期")

        self.periodComboS.addItems([str(i+1) for i in range(12)])
        self.periodComboE.addItems([str(i+1) for i in range(12)])
        self.periodComboS.setCurrentIndex(-1)
        self.periodComboE.setCurrentIndex(-1)

        ## 凭证类型
        typeLb = QLabel("凭证类型")
        self.typeCombo = QComboBox()
        self.typeCombo.addItems(["记账凭证","收款凭证","支付凭证","转账凭证"])
        self.typeCombo.setCurrentIndex(-1)

        ## 汇总表
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["科目","借方金额","贷方金额"])

        ## 设置列宽
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)

        # 内容布局
        ## 会计时期
        periodLayout.addWidget(periodLb)
        periodLayout.addWidget(periodSLb)
        periodLayout.addWidget(self.periodComboS)
        periodLayout.addWidget(periodMLb)
        periodLayout.addWidget(self.periodComboE)
        periodLayout.addWidget(periodELb)
        ## 凭证类型
        periodLayout.addWidget(typeLb)
        periodLayout.addWidget(self.typeCombo)
        ## 内容
        contentLayout.addLayout(periodLayout)
        contentLayout.addWidget(self.table)

        # 布局
        ## 内容
        mainLayout.addWidget(self.contentWidget)
        self.setLayout(mainLayout)

    def summary_voucher(self):
        """汇总符合条件的凭证信息"""
        start_time = self.periodComboS.currentText()
        end_time = self.periodComboE.currentText()

        


