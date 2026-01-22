from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QComboBox, QDateTimeEdit,
    QVBoxLayout, QHBoxLayout, QLabel)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor


class FilterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUi()

    def setupUi(self):
        """界面设计"""
        self.setWindowTitle("筛选条件")
        self.resize(800, 400)

        mainLayout = QVBoxLayout()

        current_date = QDateTime.currentDateTime()
        # 标题
        title = QLabel("条件")
        
        # 筛选条件
        self.conditionWidget = QWidget()
        conditionLayout = QVBoxLayout(self.conditionWidget)
        ## 会计期间
        periodSLayout = QHBoxLayout()
        startLb = QLabel("会计期间: ")
        self.yearSSpin = QDateTimeEdit()
        self.yearSSpin.setDisplayFormat("yyyy")
        self.yearSSpin.setDateTime(current_date)
        # self.yearSSpin.setReadOnly(True)
        self.monthSSpin = QDateTimeEdit()
        self.monthSSpin.setDisplayFormat("MM")
        self.monthSSpin.setDateTime(current_date)
        # self.monthSSpin.setReadOnly(True)
        ## 至
        periodELayout = QHBoxLayout()
        endLb = QLabel("至: ")
        self.yearESpin = QDateTimeEdit()
        self.yearESpin.setDisplayFormat("yyyy")
        self.yearESpin.setDateTime(current_date)
        # self.yearESpin.setReadOnly(True)
        self.monthESpin = QDateTimeEdit()
        self.monthESpin.setDisplayFormat("MM")
        self.monthESpin.setDateTime(current_date)
        # self.monthESpin.setReadOnly(True)
        
        # 布局
        ## 筛选条件布局
        ### 会计期间开始
        periodSLayout.addWidget(startLb)
        periodSLayout.addWidget(self.yearSSpin)
        periodSLayout.addWidget(self.monthSSpin)
        ### 会计期间结束
        periodELayout.addWidget(endLb)
        periodELayout.addWidget(self.yearESpin)
        periodELayout.addWidget(self.monthESpin)
        ### 会计期间
        conditionLayout.addLayout(periodSLayout)
        conditionLayout.addLayout(periodELayout)
        ## 主布局
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.conditionWidget)
        self.setLayout(mainLayout)