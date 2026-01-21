import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidgetItem)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from models.voucher import VoucherManager
from models.data import Voucher, VoucherDetail


class VoucherSummary(QWidget):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setupUi()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("凭证汇总")
        self.resize(900, 600)

        mainLayout = QVBoxLayout()

        # 内容
        self.contentWidget = QWidget()
        contentLayout = QVBoxLayout(self.contentWidget)

        ## 会计时期
        periodLayout = QHBoxLayout()
        periodLb = QLabel("会计年度")
        self.yearCombo = QComboBox()            # 会计年度
        periodSLb = QLabel("从第")
        self.periodComboS = QComboBox()         # 开始时期
        periodMLb = QLabel(" -  第")
        self.periodComboE = QComboBox()         # 结束时期
        periodELb = QLabel("期")

        years = []
        for file in os.listdir("data"):
            if file.endswith("_vouchers.db"):
                years.append(file.split("_")[1])
        self.yearCombo.addItems(years)
        self.periodComboS.addItems([str(i+1) for i in range(12)])
        self.periodComboE.addItems([str(i+1) for i in range(12)])
        self.periodComboS.setCurrentIndex(0)
        self.periodComboE.setCurrentIndex(-1)

        ## 凭证类型
        typeLb = QLabel("凭证类型")
        self.typeCombo = QComboBox()
        self.typeCombo.addItems(["记账凭证","收款凭证","支付凭证","转账凭证"])
        self.typeCombo.setCurrentIndex(-1)

        ## 汇总表
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["科目","借方金额","贷方金额","科目余额"])

        ## 设置列宽
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)

        # 内容布局
        ## 会计时期
        periodLayout.addWidget(periodLb)
        periodLayout.addWidget(self.yearCombo)
        periodLayout.addWidget(periodSLb)
        periodLayout.addWidget(self.periodComboS)
        periodLayout.addWidget(periodMLb)
        periodLayout.addWidget(self.periodComboE)
        periodLayout.addWidget(periodELb)
        ## 凭证类型
        periodLayout.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        periodLayout.addWidget(typeLb)
        periodLayout.addWidget(self.typeCombo)
        ## 内容
        contentLayout.addLayout(periodLayout)
        contentLayout.addWidget(self.table)

        # 布局
        ## 内容
        mainLayout.addWidget(self.contentWidget)
        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        self.periodComboE.currentTextChanged.connect(self.summary_voucher)

    def summary_voucher(self, end_month):
        """汇总符合条件的凭证信息"""
        year = int(self.yearCombo.currentText())
        start_month = int(self.periodComboS.currentText())
        
        # 链接数据库
        self.database = f"data\{self.user_info['company']}_{year}_vouchers.db"
        self.voucherManage = VoucherManager(self.database)

        # 起止日期
        start_date = QDate(year, start_month, 1)
        end_date = QDate(year, int(end_month)+1, 1).addDays(-1)

        # 筛选凭证科目代码
        result = self.voucherManage.summary_subject(start_date, end_date)
        for i in range(len(result)):
            self.table.setRowCount(i+1)
            subjectItem = QTableWidgetItem(f"{result['account_code']}")
            subjectItem.setBackground(QColor(240, 240, 240))
            subjectItem.setFlags(subjectItem.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
            self.table.setItem(i, 0, subjectItem)

        # # 计算总额
        # debit_amount, credit_amount = self.voucherManage.summary_amount(start_date, end_date)
        # ## 展示借方总额
        # self.table.setRowCount(i+2)
        # sumdebitItem = QTableWidgetItem(f"{debit_amount}")
        # sumdebitItem.setBackground(QColor(240, 240, 240))
        # sumdebitItem.setFlags(sumdebitItem.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
        # self.table.setItem(i+1, 1, sumdebitItem)
        # ## 展示贷方总额
        # sumcreditItem = QTableWidgetItem(f"{credit_amount}")
        # sumcreditItem.setBackground(QColor(240, 240, 240))
        # sumcreditItem.setFlags(sumcreditItem.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
        # self.table.setItem(i+1, 2, sumcreditItem)
