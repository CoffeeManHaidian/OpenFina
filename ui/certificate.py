import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QLabel, QComboBox)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QFont, QColor, QShortcut, QKeySequence

from ui.calendar import DatePickerDialog
from ui.clickableTabel import ClickableLabel
from lib.voucher import VoucherManager
# from ui.


class Certification(QWidget):
    def __init__(self):
        super().__init__()
        self.voucherManager = VoucherManager()
        self.setupUI()
        self.init_slot()

    def setupUI(self):
        """设置表格UI"""
        # title and size
        self.setWindowTitle("记账凭证")
        self.resize(900, 600)
        # 移除最大化按钮标志，只保留最小化和关闭按钮
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.mainLayout = QVBoxLayout()

        ## 标题栏
        self.titleLayout = QVBoxLayout()
        self.labelLayout = QHBoxLayout()

        self.title = QLabel("通用记账凭证")
        self.title.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 24px;
                font-weight: bold;
                color: rgb(0, 128, 0);
                text-decoration: underline double;
                qproperty-alignment: AlignCenter;
            }
        """)
        self.titleLayout.addWidget(self.title)

        # 业务日期
        self.dateLabel = QLabel("业务日期 ")
        self.dateLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)
        self.date = QDate.currentDate()
        self.dateBtnLabel = ClickableLabel()
        self.update_date_label(self.date, self.dateBtnLabel)
        self.dateBtnLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)

        # 凭证日期
        self.datetime = QDate.currentDate()
        self.datetimeBtnLabel = ClickableLabel()
        self.update_date_label(self.datetime, self.datetimeBtnLabel)
        self.datetimeBtnLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)
        
        # 标题布局
        self.labelLayout.addWidget(self.dateLabel)
        self.labelLayout.addWidget(self.dateBtnLabel)
        titleSpacer1 = QSpacerItem(1400, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.labelLayout.addSpacerItem(titleSpacer1)
        self.labelLayout.addWidget(self.datetimeBtnLabel)
        titleSpacer2 = QSpacerItem(1400, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.labelLayout.addSpacerItem(titleSpacer2)

        # 凭证号 
        self.voucher_lb = QLabel("凭证号")
        self.labelLayout.addWidget(self.voucher_lb)
        self.voucher_combo = QComboBox()
        self.voucher_combo.setMinimumSize(100, 30)
        self.voucher_combo.setMaximumSize(100, 30)
        self.voucher_combo.setEditable(True)
        self.voucher_combo.addItems(self.voucherManager.get_voucher_history())
        self.labelLayout.addWidget(self.voucher_combo)

        self.titleLayout.addLayout(self.labelLayout)

        ## 设置表头
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["摘要","科目","借方金额","\u2713","贷方金额","\u2713"]
        )

        ## 设置默认行高为 40 像素
        self.table.verticalHeader().setDefaultSectionSize(40)

        ## 为第5列和第7列（索引4和6）在每一数据行（不含合计行）添加复选框
        for r in range(self.table.rowCount() - 1):
            left_cb = QTableWidgetItem()
            left_cb.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            left_cb.setCheckState(Qt.Unchecked)
            self.table.setItem(r, 3, left_cb)

            right_cb = QTableWidgetItem()
            right_cb.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            right_cb.setCheckState(Qt.Unchecked)
            self.table.setItem(r, 5, right_cb)

        self.update_totals(0.0, 0.0)

        ## 设置列宽
        # self.table.setItem(6, 0, QTableWidgetItem("合计"))
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        # 设置表格属性
        # self.table.setAlternatingRowColors(True)
        # self.table.setShowGrid(True)
        # self.table.verticalHeader().setVisible(False)

        ## 设置工具栏
        self.topWidget = QWidget()
        self.topLayout = QHBoxLayout()
        self.topWidget.setMinimumSize(QSize(0, 60))
        # self.topWidget.setMinimumSize(QSize(200, 40))

        self.btnSave = QPushButton(self.topWidget)
        self.btnSave.setObjectName("保存")
        self.btnSave.setText("保存")
        self.btnSave.setMinimumSize(QSize(40, 40))
        self.btnSave.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 255, 255);
                border:none;
            }
            QPushButton:hover {
                background-color: rgba(221, 221, 221, 1);
            }
            QPushButton:pressed {
                background-color: rgba(221, 221, 221, 0.8);
            }
        """)
        self.topLayout.addWidget(self.btnSave)

        self.btnCancel = QPushButton(self.topWidget)
        self.btnCancel.setObjectName("取消")
        self.btnCancel.setText("取消")
        self.btnCancel.setMinimumSize(QSize(40, 40))
        self.btnCancel.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 255, 255);
                border:none;
            }
            QPushButton:hover {
                background-color: rgba(221, 221, 221, 1);
            }
            QPushButton:pressed {
                background-color: rgba(221, 221, 221, 0.8);
            }
        """)
        self.topLayout.addWidget(self.btnCancel)  
        
        topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.topLayout.addItem(topSpacer)

        ## 布局
        self.mainLayout.addLayout(self.topLayout) 
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.table)     

        self.setLayout(self.mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        self.dateBtnLabel.clicked.connect(self.show_date_picker)
        self.datetimeBtnLabel.clicked.connect(self.show_datetime_picker)
        self.table.itemSelectionChanged.connect(self.calculate_totals)
        self.voucher_combo.currentTextChanged.connect(lambda: print(self.voucher_combo.currentText()))

    def calculate_totals(self):
        """计算借方和贷方金额合计"""
        debit_total = 0.0       # 借方金额
        credit_total = 0.0      # 贷方金额

        for row in range(self.table.rowCount() - 1):
            debit_value = self.table.item(row, 2)
            credit_value = self.table.item(row, 4)

            if debit_value and debit_value.text():
                debit_value = float(debit_value.text().replace(",", ""))
                debit_total += debit_value      # 计算借方金额
            if credit_value and credit_value.text():
                credit_value = float(credit_value.text().replace(",", ""))
                credit_total += credit_value    # 计算贷方金额   

        self.update_totals(debit_total, credit_total)     

    def update_totals(self, debit_total, credit_total):
        """更新合计"""
        # 
        last_row = self.table.rowCount() - 1
        total_item = QTableWidgetItem("合计")
        total_item.setFont(QFont("Arial", 10, QFont.Bold))
        total_item.setBackground(QColor(240, 240, 240))
        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)  # 设置为不可编辑
        self.table.setItem(last_row, 0, total_item)

        # 会计科目合计单元格
        subject_item = QTableWidgetItem("")
        subject_item.setBackground(QColor(240, 240, 240))
        subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 1, subject_item)

        # 借方金额合计
        debit_item = QTableWidgetItem(f"{debit_total:,.2f}")
        debit_item.setBackground(QColor(240, 240, 240))
        debit_item.setFlags(debit_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 2, debit_item)
        
        # 贷方金额合计
        credit_item = QTableWidgetItem(f"{credit_total:,.2f}")
        credit_item.setBackground(QColor(240, 240, 240))
        credit_item.setFlags(credit_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 4, credit_item)

        # 备注合计单元格
        note_item = QTableWidgetItem("")
        note_item.setBackground(QColor(240, 240, 240))
        note_item.setFlags(note_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 3, note_item)

        note_item = QTableWidgetItem("")
        note_item.setBackground(QColor(240, 240, 240))
        note_item.setFlags(note_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 5, note_item)

    def update_date_label(self, date, label):
        """更新凭证日期标签的显示"""
        date_str = date.toString("yyyy年MM月dd日")
        label.setText(f"{date_str}")

    def show_date_picker(self):
        """选择业务日期"""
        dateDialog = DatePickerDialog(self.datetime, self.dateBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()
    
    def show_datetime_picker(self):
        """选择业务日期"""
        dateDialog = DatePickerDialog(self.datetime, self.datetimeBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()

    def select_date(self, date, label):
        """选择日期并更新"""
        if label == self.dateBtnLabel:
            self.date = date
            self.update_date_label(date, self.dateBtnLabel)
        elif label == self.datetimeBtnLabel:
            self.datetime = date
            self.update_date_label(date, self.datetimeBtnLabel)

    def select_subject(self):
        """选择会计科目"""



if __name__ == "__main__":
    app = QApplication([])
    window = Certification()
    
    window.show()
    app.exec()