import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QLabel, QComboBox, QMessageBox)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QFont, QColor, QShortcut, QKeySequence

from ui.calendar import DatePickerDialog
from ui.clickableTabel import ClickableLabel
from models.voucher import VoucherManager
from ui.subject import SubjectWindow
from models.data import Voucher, VoucherDetail


class Certification(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = QDate.currentDate()
        current_month = self.current_date.toString("yyyyMM")
        self.voucherManager = VoucherManager(rf"data\{current_month}.db")

        self.subjectWidget = SubjectWindow()
        self.summaryItems = []
        self.subjectClasses = []
        self.subjects = []
        self.user_info()
        self.setupUI()
        self.init_slot()

    def user_info(self):
        """获取用户信息"""
        date_str = self.current_date.toString("yyyy年MM期")

        self.companyLb = f"Open公司"
        self.voucherLb = f"{date_str}"
        self.review = ""
        self.post = ""
        self.cashier = ""
        self.preparer = f"张三"
        self.approve = ""

    def setupUI(self):
        """设置表格UI"""
        # title and size
        self.setWindowTitle("记账凭证")
        self.resize(900, 600)
        # 移除最大化按钮标志，只保留最小化和关闭按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)

        ## 标题栏
        self.titleWidget = QWidget()
        titleLayout = QVBoxLayout(self.titleWidget)
        titleLayout.setSpacing(0)
        # titleLayout.setContentsMargins(0, 0, 0, 0)
        labelLayout = QHBoxLayout()
        labelLayout.setSpacing(0)
        # labelLayout.setContentsMargins(0, 0, 0, 0)
        self.titleWidget.setMinimumSize(QSize(700,100))
        self.titleWidget.setMaximumSize(QSize(16777215,100))
        self.titleWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.titleWidget.setStyleSheet("""
            QWidget {
            background-color: rgb(255, 255, 255);
        }""")
        # self.titleWidget.setLayout(titleLayout)

        # 标题
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
        titleSpacer1 = QSpacerItem(1400, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        titleLayout.addSpacerItem(titleSpacer1)
        titleLayout.addWidget(self.title)
        titleSpacer2 = QSpacerItem(1400, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        titleLayout.addSpacerItem(titleSpacer2)

        # 凭证日期
        self.dateLabel = QLabel("业务日期 ")
        self.dateLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)
        self.voucher_date = self.current_date
        self.dateBtnLabel = ClickableLabel()
        self.update_date_label(self.voucher_date, self.dateBtnLabel)
        self.dateBtnLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)

        # 创建/修改时间
        self.created_time = self.current_date
        self.datetimeBtnLabel = ClickableLabel()
        self.update_date_label(self.created_time, self.datetimeBtnLabel)
        self.datetimeBtnLabel.setStyleSheet("""
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
        """)
        
        # 标题布局
        labelLayout.addWidget(self.dateLabel)
        labelLayout.addWidget(self.dateBtnLabel)
        labelSpacer1 = QSpacerItem(1200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        labelLayout.addSpacerItem(labelSpacer1)
        labelLayout.addWidget(self.datetimeBtnLabel)
        labelSpacer2 = QSpacerItem(1400, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        labelLayout.addSpacerItem(labelSpacer2)

        ## 凭证信息
        self.voucherWidget = QWidget()
        voucherLayout = QVBoxLayout(self.voucherWidget)
        self.voucherWidget.setMinimumSize(QSize(200,100))
        self.voucherWidget.setMaximumSize(QSize(200,100))
        self.voucherWidget.setStyleSheet("""
            QWidget {
                background-color: rgb(255,255,255);
            }
            """)
        self.voucherWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.voucherWidget.setLayout(voucherLayout)
        
        # 凭证字
        typeLayout = QHBoxLayout()
        self.type_lb = QLabel("凭证字")
        typeLayout.addWidget(self.type_lb)
        self.typeCombo = QComboBox()
        self.typeCombo.setMinimumSize(100, 30)
        self.typeCombo.setMaximumSize(100, 30)
        self.typeCombo.setEditable(True)
        self.typeCombo.addItems(["记账凭证","收款凭证","支付凭证","转账凭证"])
        typeLayout.addWidget(self.typeCombo)

        # 凭证号
        numberLayout = QHBoxLayout()
        self.number_lb = QLabel("凭证号")
        numberLayout.addWidget(self.number_lb)
        self.numberCombo = QComboBox()
        self.numberCombo.setMinimumSize(100, 30)
        self.numberCombo.setMaximumSize(100, 30)
        self.numberCombo.setEditable(True)
        numberLayout.addWidget(self.numberCombo)

        voucherLayout.addLayout(typeLayout)
        voucherLayout.addLayout(numberLayout)
        titleLayout.addLayout(labelLayout)

        ## 设置表头
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["摘要","科目","借方金额","\u2713","贷方金额","\u2713"]
        )

        ## 设置默认行高为 40 像素
        self.table.verticalHeader().setDefaultSectionSize(40)

        # 为第5列和第7列（索引4和6）在每一数据行（不含合计行）添加复选框
        for r in range(self.table.rowCount() - 1):
            left_cb = QTableWidgetItem()
            left_cb.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            left_cb.setCheckState(Qt.Unchecked)
            self.table.setItem(r, 3, left_cb)

            right_cb = QTableWidgetItem()
            right_cb.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            right_cb.setCheckState(Qt.Unchecked)
            self.table.setItem(r, 5, right_cb)
        
        # 设置科目为不可编辑，并设置提示
        for row in range(self.table.rowCount() - 1):
            subjectItem = QTableWidgetItem("按F2")
            subjectItem.setForeground(QColor(150, 150, 150))
            subjectItem.setBackground(QColor(240, 240, 240))
            subjectItem.setFlags(subjectItem.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, subjectItem)

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
        topLayout = QHBoxLayout()
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
        topLayout.addWidget(self.btnSave)
        topLayout.addSpacing(10)

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
        topLayout.addWidget(self.btnCancel)  
        
        topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        topLayout.addItem(topSpacer)

        ## 凭证尾
        self.lowerWidget = QWidget()
        lowerLayout = QHBoxLayout(self.lowerWidget)
        # 审核
        self.reviewLb = QLabel(f"审核: {self.review}")
        # 过账
        self.postLb = QLabel(f"过账: {self.post}")
        # 出纳
        self.cashierLb = QLabel(f"出纳: {self.cashier}")
        # 制单
        self.preparerLb = QLabel(f"制单: {self.preparer}")
        # 核准
        self.approveLb = QLabel(f"核准: {self.approve}")

        # 凭证尾布局
        lowerLayout.addWidget(self.reviewLb)
        lowerLayout.addWidget(self.postLb)
        lowerLayout.addWidget(self.cashierLb)
        lowerLayout.addWidget(self.preparerLb)
        lowerLayout.addWidget(self.approveLb)

        ## 底部状态栏
        self.bottomWidget = QWidget()
        bottomLayout = QHBoxLayout(self.bottomWidget)

        # 登录信息（未录入）
        companyLb = QLabel(self.companyLb)
        voucherLb = QLabel(f"总账: {self.voucherLb}")

        # 底部布局
        bottomLayout.addWidget(companyLb)
        bottomLayout.addWidget(voucherLb)

        ## 布局
        upperLayout = QHBoxLayout()
        upperLayout.setSpacing(0)
        upperLayout.addWidget(self.titleWidget)
        upperLayout.addWidget(self.voucherWidget)

        mainLayout.addLayout(topLayout) 
        mainLayout.addSpacing(10)
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(self.table) 
        mainLayout.addWidget(self.lowerWidget)
        mainLayout.addWidget(self.bottomWidget)    

        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        self.dateBtnLabel.clicked.connect(self.show_date_picker)
        self.datetimeBtnLabel.clicked.connect(self.show_datetime_picker)
        self.table.itemChanged.connect(self.on_itemChanged)

        # F2 打开会计科目选择窗口（全局快捷键，父对象为当前窗口）
        self.subShortcut = QShortcut(QKeySequence(Qt.Key_F2), self)
        self.subShortcut.activated.connect(self.select_subject)

        # 获取会计科目
        self.subjectWidget.subFunc.connect(self.get_subject)

        # 保存/取消凭证
        self.btnSave.clicked.connect(self.on_btnSave_clicked)
        self.btnCancel.clicked.connect(self.on_btnCancel_clicked)
        # 查询已录入的凭证
        # self.numberCombo.currentIndexChanged.connect(self.search_voucher)

    def on_itemChanged(self, item):
        """单元格内容改变时触发"""
        # 判断是否为合计行
        if item.row() < self.table.rowCount() - 1:
            self.calculate_totals()

    def calculate_totals(self):
        """计算借方和贷方金额合计"""
        self.debit_total = 0.0       # 借方金额
        self.credit_total = 0.0      # 贷方金额

        for row in range(self.table.rowCount() - 1):
            debit_value = self.table.item(row, 2)
            credit_value = self.table.item(row, 4)

            if debit_value and debit_value.text():
                debit_value = float(debit_value.text().replace(",", ""))
                self.debit_total += debit_value      # 计算借方金额
            if credit_value and credit_value.text():
                credit_value = float(credit_value.text().replace(",", ""))
                self.credit_total += credit_value    # 计算贷方金额   

        self.update_totals(self.debit_total, self.credit_total)     

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
        """选择凭证日期"""
        dateDialog = DatePickerDialog(self.created_time, self.dateBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()
    
    def show_datetime_picker(self):
        """选择会计事件"""
        dateDialog = DatePickerDialog(self.created_time, self.datetimeBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()

    def select_date(self, date, label):
        """选择日期并更新"""
        if label == self.dateBtnLabel:
            self.voucher_date = date
            self.update_date_label(date, self.dateBtnLabel)
        elif label == self.datetimeBtnLabel:
            self.created_time = date
            self.update_date_label(date, self.datetimeBtnLabel)

    def select_subject(self):
        """选择会计科目——按 F2 打开，会复用已打开窗口并置顶"""
        # 检查当前列是否为第二列且表格有焦点
        if self.table.currentColumn() == 1 and self.table.hasFocus():
            # 如果窗口已打开，则置顶并激活
            if hasattr(self, "subjectWidget") and self.subjectWidget.isVisible():
                self.subjectWidget.raise_()
                self.subjectWidget.activateWindow()
                return

            # 显示窗口
            self.subjectWidget.show()

    def get_subject(self, code, name):
        """获取会计科目类和会计科目"""
        self.subjectStr = f"{code} {name}"

        # 显示会计科目
        currentRow = self.table.currentRow()
        self.table.setItem(currentRow, 1, QTableWidgetItem(self.subjectStr))

    def on_btnSave_clicked(self):
        """保存凭证"""
        # 获取凭证内容
        voucher = Voucher(
            voucher_id=self.numberCombo.currentText(),
            voucher_no=self.numberCombo.currentText(),
            voucher_type=self.typeCombo.currentText(),
            voucher_date=self.dateBtnLabel.text(),
            attach_count=0,
            preparer=self.preparer,
            reviewer=None,
            attention=None,
            created_time=self.created_time
        )

        for row in range(self.table.rowCount() - 1):
            debit_value, credit_value = "", ""
            debit_value = self.table.item(row, 2)
            credit_value = self.table.item(row, 4)
            if debit_value and debit_value.text():
                debit_value = float(debit_value.text().replace(",", ""))
            if credit_value and credit_value.text():
                credit_value = float(credit_value.text().replace(",", ""))  

            if debit_value != 0.0 or credit_value != 0.0:
                detail = VoucherDetail(
                    line_no=row,
                    account_code=self.table.item(row, 1).text().split(" ")[0],
                    account_name=self.table.item(row, 1).text().split(" ")[1],
                    debit_amount=debit_value,
                    credit_amount=credit_value,
                    summary=self.table.item(row, 0).text(),
                )
                voucher.details.append(detail)
            else:
                pass

        try:
            index = self.voucherManager.save_voucher(voucher)
            QMessageBox.information(self, "成功", f"凭证{index:0>4d}保存成功！")
        except Exception as e:
            print(f"凭证保存失败{str(e)}")
            QMessageBox.critical(self, "错误", f"凭证保存失败{str(e)}")

        # 关闭窗口
        self.close()

    def on_btnCancel_clicked(self):
        self.close()

    def search_voucher(self):
        """加载以录入的凭证"""
        index = self.numberCombo.currentText()
        voucher = self.voucherManager.search_voucher(index)
        
        # 业务日期
        self.dateBtnLabel.setText(voucher.voucher_date)
        # 制单人
        self.preparerLb.setText(voucher.preparer)
        for row in range(len(voucher.details)):
            detail = voucher.details[row]
            # 摘要
            self.table.setItem(row, 0, QTableWidgetItem(detail.summary))
            # 科目
            subject = f"{detail.account_code} {detail.account_name}"
            self.table.setItem(row, 1, QTableWidgetItem(subject))
            # 借方金额
            self.table.setItem(row, 2, QTableWidgetItem(str(detail.debit_amount)))
            # 贷方金额
            self.table.setItem(row, 4, QTableWidgetItem(str(detail.credit_amount)))


if __name__ == "__main__":
    app = QApplication([])
    window = Certification()
    
    window.show()
    app.exec()