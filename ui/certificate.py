import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QDate, QSize, Qt
from PySide6.QtGui import QColor, QFont, QKeySequence, QShortcut

from models.data import Voucher, VoucherDetail
from models.voucher import VoucherManager
from ui.cal import DatePickerDialog
from ui.clickableLabel import ClickableLabel
from ui.subject import SubjectWindow
from utils.logger import get_logger, log_event
from utils.theme import material_widget_style

logger = get_logger()


class Certification(QWidget):
    def __init__(self, user_info, func):
        super().__init__()
        self.user_info_dict = user_info
        self.username = user_info["username"]
        self.company = user_info.get("enterprise_name") or user_info.get("company", "")
        self.fiscal_year = user_info.get("fiscal_year")
        self.bookset_db_path = user_info["bookset_db_path"]
        self.func = func
        self.current_date = QDate.currentDate()
        self.current_voucher = None
        self.voucherManager = VoucherManager(self.bookset_db_path)
        log_event(
            logger,
            "初始化凭证窗口",
            username=self.username,
            enterprise_name=self.company,
            bookset_id=user_info.get("bookset_id", ""),
            func=self.func,
            db_path=self.bookset_db_path,
        )

        self.subjectWidget = SubjectWindow(self.bookset_db_path)
        self.summaryItems = []
        self.subjectClasses = []
        self.subjects = []
        self.user_info()
        self.setupUI()
        self.setStyleSheet(material_widget_style())
        self.init_slot()

    def user_info(self):
        """获取用户信息"""
        date_str = self.current_date.toString("yyyy年MM期")

        fiscal_label = f"{self.fiscal_year}年度" if self.fiscal_year else ""
        self.companyLb = f"{self.company} {fiscal_label}".strip()
        self.voucherLb = f"总账: {date_str}"
        self.post = ""
        self.preparer = ""
        self.review = ""
        self.cashier = ""
        self.approve = ""

    def setupUI(self):
        """设置表格UI"""
        title_map = {
            1: "凭证录入",
            2: "凭证查询",
            3: "凭证过账",
            4: "双敲审核",
        }
        self.setWindowTitle(title_map.get(self.func, "记账凭证"))
        self.resize(900, 600)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)

        self.titleWidget = QWidget()
        titleLayout = QVBoxLayout(self.titleWidget)
        titleLayout.setSpacing(0)
        labelLayout = QHBoxLayout()
        labelLayout.setSpacing(0)
        self.titleWidget.setMinimumSize(QSize(700, 100))
        self.titleWidget.setMaximumSize(QSize(16777215, 100))
        self.titleWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.titleWidget.setStyleSheet(
            """
            QWidget {
                background-color: rgb(255, 255, 255);
            }
            """
        )

        self.title = QLabel("通用记账凭证")
        self.title.setStyleSheet(
            """
            QLabel {
                font-family: "宋体";
                font-size: 24px;
                font-weight: bold;
                color: rgb(0, 128, 0);
                text-decoration: underline double;
                qproperty-alignment: AlignCenter;
            }
            """
        )
        titleLayout.addSpacerItem(QSpacerItem(1400, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        titleLayout.addWidget(self.title)
        titleLayout.addSpacerItem(QSpacerItem(1400, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self.dateLabel = QLabel("业务日期 ")
        self.dateLabel.setStyleSheet(
            """
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
            """
        )
        self.voucher_date = self.current_date
        self.dateBtnLabel = ClickableLabel()
        self.update_date_label(self.voucher_date, self.dateBtnLabel)
        self.dateBtnLabel.setStyleSheet(
            """
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
            """
        )

        self.created_time = self.current_date
        self.datetimeBtnLabel = ClickableLabel()
        self.update_date_label(self.created_time, self.datetimeBtnLabel)
        self.datetimeBtnLabel.setStyleSheet(
            """
            QLabel {
                font-family: "宋体";
                font-size: 16px;
                color: rgb(0, 128, 0);
                qproperty-alignment: AlignCenter;
            }
            """
        )

        labelLayout.addWidget(self.dateLabel)
        labelLayout.addWidget(self.dateBtnLabel)
        labelLayout.addSpacerItem(QSpacerItem(1200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        labelLayout.addWidget(self.datetimeBtnLabel)
        labelLayout.addSpacerItem(QSpacerItem(1400, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.voucherWidget = QWidget()
        voucherLayout = QVBoxLayout(self.voucherWidget)
        self.voucherWidget.setMinimumSize(QSize(200, 100))
        self.voucherWidget.setMaximumSize(QSize(200, 100))
        self.voucherWidget.setStyleSheet(
            """
            QWidget {
                background-color: rgb(255,255,255);
            }
            """
        )
        self.voucherWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        typeLayout = QHBoxLayout()
        self.type_lb = QLabel("凭证字")
        typeLayout.addWidget(self.type_lb)
        self.typeCombo = QComboBox()
        self.typeCombo.setMinimumSize(100, 30)
        self.typeCombo.setMaximumSize(100, 30)
        self.typeCombo.setEditable(True)
        self.typeCombo.addItems(["记账凭证", "收款凭证", "支付凭证", "转账凭证"])
        typeLayout.addWidget(self.typeCombo)

        numberLayout = QHBoxLayout()
        self.number_lb = QLabel("凭证号")
        numberLayout.addWidget(self.number_lb)
        self.numberCombo = QComboBox()
        self.numberCombo.setMinimumSize(100, 30)
        self.numberCombo.setMaximumSize(100, 30)
        self.numberCombo.setEditable(True)
        numberLayout.addWidget(self.numberCombo)
        self.refresh_number_combo()

        voucherLayout.addLayout(typeLayout)
        voucherLayout.addLayout(numberLayout)
        titleLayout.addLayout(labelLayout)

        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["摘要", "科目", "借方金额", "贷方金额"])
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.reset_table_rows()

        self.topWidget = QWidget()
        topLayout = QHBoxLayout()
        self.topWidget.setMinimumSize(QSize(0, 60))

        self.btnSave = QPushButton(self.topWidget)
        self.btnSave.setObjectName("保存")
        button_text = "保存"
        if self.func == 3:
            button_text = "过账"
        elif self.func == 4:
            button_text = "审核"
        self.btnSave.setText(button_text)
        self.btnSave.setMinimumSize(QSize(40, 40))
        self.btnSave.setStyleSheet(
            """
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
            """
        )
        topLayout.addWidget(self.btnSave)
        topLayout.addSpacing(10)

        self.btnCancel = QPushButton(self.topWidget)
        self.btnCancel.setObjectName("取消")
        self.btnCancel.setText("关闭" if self.func in (2, 3, 4) else "取消")
        self.btnCancel.setMinimumSize(QSize(40, 40))
        self.btnCancel.setStyleSheet(
            """
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
            """
        )
        topLayout.addWidget(self.btnCancel)
        topLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.lowerWidget = QWidget()
        lowerLayout = QHBoxLayout(self.lowerWidget)
        lowerLayout.setSpacing(12)
        self.preparerLb = QLabel("制单")
        self.preparerEdit = QLineEdit(self.preparer)
        self.preparerEdit.setPlaceholderText("请输入制单人")
        self.reviewLb = QLabel("审核")
        self.reviewEdit = QLineEdit(self.review)
        self.reviewEdit.setPlaceholderText("请输入审核人")
        self.postLb = QLabel("过账")
        self.postEdit = QLineEdit(self.post)
        self.postEdit.setPlaceholderText("请输入过账人")
        self.cashierLb = QLabel("出纳")
        self.cashierEdit = QLineEdit(self.cashier)
        self.cashierEdit.setReadOnly(True)
        self.approveLb = QLabel("核准")
        self.approveEdit = QLineEdit(self.approve)
        self.approveEdit.setReadOnly(True)
        lowerLayout.addWidget(self.create_person_field(self.preparerLb, self.preparerEdit), 1)
        lowerLayout.addWidget(self.create_person_field(self.reviewLb, self.reviewEdit), 1)
        lowerLayout.addWidget(self.create_person_field(self.postLb, self.postEdit), 1)
        lowerLayout.addWidget(self.create_person_field(self.cashierLb, self.cashierEdit), 1)
        lowerLayout.addWidget(self.create_person_field(self.approveLb, self.approveEdit), 1)

        self.bottomWidget = QWidget()
        bottomLayout = QHBoxLayout(self.bottomWidget)
        bottomLayout.addWidget(QLabel(self.companyLb))
        bottomLayout.addWidget(QLabel(self.voucherLb))

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

        if self.func in (2, 3, 4):
            self.typeCombo.setEnabled(False)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            if self.func in (3, 4):
                self.btnSave.setEnabled(False)
            else:
                self.btnSave.hide()
                self.numberCombo.setEnabled(False)

        self.preparerEdit.setReadOnly(self.func != 1)
        self.reviewEdit.setReadOnly(self.func not in (1, 4))
        self.postEdit.setReadOnly(self.func not in (1, 3))

    def init_slot(self):
        """绑定信号与槽"""
        if self.func != 2:
            self.dateBtnLabel.clicked.connect(self.show_date_picker)
        if self.func not in (2, 3, 4):
            self.datetimeBtnLabel.clicked.connect(self.show_datetime_picker)
        self.table.itemChanged.connect(self.on_itemChanged)

        if self.func == 1:
            self.subShortcut = QShortcut(QKeySequence(Qt.Key_F2), self)
            self.subShortcut.activated.connect(self.select_subject)
            self.subjectWidget.subFunc.connect(self.get_subject)

        self.btnSave.clicked.connect(self.on_btnSave_clicked)
        self.btnCancel.clicked.connect(self.on_btnCancel_clicked)

        if self.func in (2, 3, 4):
            self.numberCombo.currentIndexChanged.connect(self.load_voucher)

    def refresh_number_combo(self):
        """刷新凭证号列表"""
        self.numberCombo.blockSignals(True)
        self.numberCombo.clear()

        if self.func == 1:
            next_number = self.voucherManager.update_voucher_no(self.voucher_date)
            self.numberCombo.addItem(str(next_number))
            log_event(logger, "初始化凭证号", func=self.func, numbers=next_number)
        elif self.func in (2, 3, 4):
            numbers = self.voucherManager.load_voucher_no(self.voucher_date)
            self.numberCombo.addItems(numbers)
            self.numberCombo.setCurrentIndex(-1)
            log_event(logger, "加载凭证号列表", func=self.func, count=len(numbers))

        self.numberCombo.blockSignals(False)

    def reset_table_rows(self):
        """恢复默认表格内容"""
        self.table.clearContents()
        for row in range(self.table.rowCount() - 1):
            subjectItem = QTableWidgetItem("按F2")
            subjectItem.setForeground(QColor(150, 150, 150))
            subjectItem.setBackground(QColor(240, 240, 240))
            subjectItem.setFlags(subjectItem.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, subjectItem)
        self.update_totals(0.0, 0.0)

    def update_footer_labels(self, voucher=None):
        """更新底部人名输入框信息"""
        if voucher is None:
            reviewer = ""
            poster = ""
            preparer = ""
        else:
            reviewer = voucher.reviewer or ""
            poster = voucher.poster or ""
            preparer = voucher.preparer or ""

        self.review = reviewer
        self.post = poster
        self.preparer = preparer
        self.reviewEdit.setText(self.review)
        self.postEdit.setText(self.post)
        self.preparerEdit.setText(self.preparer)
        self.cashierEdit.setText(self.cashier)
        self.approveEdit.setText(self.approve)

    def create_person_field(self, label, editor):
        """创建底部签名字段容器"""
        field_widget = QWidget()
        field_layout = QHBoxLayout(field_widget)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(6)
        editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        field_layout.addWidget(label)
        field_layout.addWidget(editor, 1)
        return field_widget

    def get_person_values(self):
        """获取底部人名输入框内容"""
        return (
            self.preparerEdit.text().strip(),
            self.reviewEdit.text().strip(),
            self.postEdit.text().strip(),
        )

    def update_review_action(self):
        """根据审核状态刷新按钮"""
        if self.func != 4:
            return

        if self.current_voucher is None:
            self.btnSave.setText("审核")
            self.btnSave.setEnabled(False)
            return

        if self.current_voucher.poster:
            self.btnSave.setText("已过账")
            self.btnSave.setEnabled(False)
            return

        if self.current_voucher.reviewer:
            if self.current_voucher.reviewer_account == self.username:
                self.btnSave.setText("取消审核")
                self.btnSave.setEnabled(True)
            else:
                self.btnSave.setText("已审核")
                self.btnSave.setEnabled(False)
            return

        self.btnSave.setText("审核")
        self.btnSave.setEnabled(True)

    def update_post_action(self):
        """根据过账状态刷新按钮"""
        if self.func != 3:
            return

        if self.current_voucher is None:
            self.btnSave.setText("过账")
            self.btnSave.setEnabled(False)
            return

        if self.current_voucher.poster:
            if self.current_voucher.poster_account == self.username:
                self.btnSave.setText("取消过账")
                self.btnSave.setEnabled(True)
            else:
                self.btnSave.setText("已过账")
                self.btnSave.setEnabled(False)
            return

        if not self.current_voucher.reviewer:
            self.btnSave.setText("待审核")
            self.btnSave.setEnabled(False)
            return

        self.btnSave.setText("过账")
        self.btnSave.setEnabled(True)

    def on_itemChanged(self, item):
        """单元格内容改变时触发"""
        if item.row() < self.table.rowCount() - 1:
            self.calculate_totals()

    def calculate_totals(self):
        """计算借方和贷方金额合计"""
        self.debit_total = 0.0
        self.credit_total = 0.0

        for row in range(self.table.rowCount() - 1):
            debit_value = self.table.item(row, 2)
            credit_value = self.table.item(row, 3)

            if debit_value and debit_value.text():
                self.debit_total += float(debit_value.text().replace(",", ""))
            if credit_value and credit_value.text():
                self.credit_total += float(credit_value.text().replace(",", ""))

        self.update_totals(self.debit_total, self.credit_total)

    def update_totals(self, debit_total, credit_total):
        """更新合计"""
        last_row = self.table.rowCount() - 1
        total_item = QTableWidgetItem("合计")
        total_item.setFont(QFont("Arial", 10, QFont.Bold))
        total_item.setBackground(QColor(240, 240, 240))
        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 0, total_item)

        subject_item = QTableWidgetItem("")
        subject_item.setBackground(QColor(240, 240, 240))
        subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 1, subject_item)

        debit_item = QTableWidgetItem(f"{debit_total:,.2f}")
        debit_item.setBackground(QColor(240, 240, 240))
        debit_item.setFlags(debit_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 2, debit_item)

        credit_item = QTableWidgetItem(f"{credit_total:,.2f}")
        credit_item.setBackground(QColor(240, 240, 240))
        credit_item.setFlags(credit_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(last_row, 3, credit_item)

    def update_date_label(self, date, label):
        """更新凭证日期标签的显示"""
        label.setText(date.toString("yyyy年MM月dd日"))

    def show_date_picker(self):
        """选择凭证日期"""
        log_event(logger, "打开业务日期选择器", current_date=self.voucher_date.toString("yyyy-MM-dd"))
        dateDialog = DatePickerDialog(self.voucher_date, self.dateBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()

    def show_datetime_picker(self):
        """选择会计时间"""
        log_event(logger, "打开会计时间选择器", current_date=self.created_time.toString("yyyy-MM-dd"))
        dateDialog = DatePickerDialog(self.created_time, self.datetimeBtnLabel)
        dateDialog.date_selected.connect(self.select_date)
        dateDialog.exec()

    def select_date(self, date, label):
        """选择日期并更新"""
        if label == self.dateBtnLabel:
            self.voucher_date = date
            self.update_date_label(date, self.dateBtnLabel)
            self.current_voucher = None
            self.reset_table_rows()
            self.update_footer_labels()
            self.update_post_action()
            self.update_review_action()
            self.refresh_number_combo()
            log_event(logger, "更新业务日期", func=self.func, voucher_date=self.voucher_date.toString("yyyy-MM-dd"))
        elif label == self.datetimeBtnLabel:
            self.created_time = date
            self.update_date_label(date, self.datetimeBtnLabel)
            log_event(logger, "更新会计时间", created_time=self.created_time.toString("yyyy-MM-dd"))

    def select_subject(self):
        """选择会计科目"""
        if self.func != 1:
            return
        if self.table.currentColumn() == 1 and self.table.hasFocus():
            if hasattr(self, "subjectWidget") and self.subjectWidget.isVisible():
                self.subjectWidget.raise_()
                self.subjectWidget.activateWindow()
                return

            log_event(logger, "打开科目选择窗口", row=self.table.currentRow(), column=self.table.currentColumn())
            self.subjectWidget.show()

    def get_subject(self, code, name):
        """获取会计科目类和会计科目"""
        self.subjectStr = f"{code} {name}"
        log_event(logger, "写入科目到凭证明细", row=self.table.currentRow(), code=code, name=name)
        self.table.setItem(self.table.currentRow(), 1, QTableWidgetItem(self.subjectStr))

    def on_btnSave_clicked(self):
        if self.func == 2:
            self.close()
            return
        if self.func == 3:
            self.on_post_clicked()
            return
        if self.func == 4:
            self.on_review_clicked()
            return

        preparer, reviewer, poster = self.get_person_values()
        if not preparer:
            QMessageBox.warning(self, "错误", "请填写制单人")
            return

        number = self.voucher_date.toString("yyyy-MM") + "-{:0>4d}".format(int(self.numberCombo.currentText()))
        voucher = Voucher(
            voucher_id=self.numberCombo.currentText(),
            voucher_no=number,
            voucher_type=self.typeCombo.currentText(),
            voucher_date=self.voucher_date.toString("yyyy-MM-dd"),
            attach_count=0,
            preparer=preparer,
            reviewer=reviewer or None,
            reviewer_account=None,
            poster=poster or None,
            poster_account=None,
            attention=None,
            created_time=self.created_time.toString("yyyy-MM-dd"),
        )
        log_event(logger, "开始保存凭证", voucher_no=number, voucher_type=voucher.voucher_type, username=self.username, company=self.company)

        for row in range(self.table.rowCount() - 1):
            debit_value = self.table.item(row, 2)
            credit_value = self.table.item(row, 3)
            debit_amount = float(debit_value.text().replace(",", "")) if debit_value and debit_value.text() else 0.0
            credit_amount = float(credit_value.text().replace(",", "")) if credit_value and credit_value.text() else 0.0

            if debit_amount or credit_amount:
                subject_item = self.table.item(row, 1)
                summary_item = self.table.item(row, 0)
                if subject_item is None or not subject_item.text() or " " not in subject_item.text():
                    QMessageBox.warning(self, "错误", "存在未填写完整的会计科目")
                    return

                detail = VoucherDetail(
                    line_no=row,
                    account_code=subject_item.text().split(" ")[0],
                    account_name=subject_item.text().split(" ", 1)[1],
                    debit_amount=debit_amount,
                    credit_amount=credit_amount,
                    summary=summary_item.text() if summary_item else "",
                )
                voucher.details.append(detail)

        log_event(
            logger,
            "凭证保存数据准备完成",
            voucher_no=voucher.voucher_no,
            detail_count=len(voucher.details),
            debit_total=f"{self.debit_total:.2f}",
            credit_total=f"{self.credit_total:.2f}",
        )

        try:
            index = self.voucherManager.save_voucher(voucher)
            log_event(logger, "凭证保存成功", voucher_id=index, voucher_no=voucher.voucher_no, detail_count=len(voucher.details))
            QMessageBox.information(self, "成功", f"凭证{index}保存成功！")
        except Exception as e:
            logger.exception("凭证保存失败")
            QMessageBox.critical(self, "错误", f"凭证保存失败{str(e)}")

        self.close()

    def on_review_clicked(self):
        """审核或取消审核"""
        if self.current_voucher is None:
            QMessageBox.warning(self, "提示", "请先选择需要审核的凭证")
            return

        voucher_no = self.current_voucher.voucher_no
        reviewer_name = self.reviewEdit.text().strip() or (self.current_voucher.reviewer or "")
        try:
            if self.current_voucher.reviewer:
                self.voucherManager.cancel_review(voucher_no, self.username)
                action_text = "取消审核"
            else:
                if not reviewer_name:
                    QMessageBox.warning(self, "提示", "请先填写审核人")
                    return
                self.voucherManager.review_voucher(voucher_no, reviewer_name, self.username)
                action_text = "审核"

            self.current_voucher = self.voucherManager.search_voucher(voucher_no)
            self.populate_voucher(self.current_voucher)
            log_event(
                logger,
                "凭证审核状态更新完成",
                voucher_no=voucher_no,
                action=action_text,
                reviewer=reviewer_name,
                reviewer_account=self.username,
            )
            QMessageBox.information(self, "成功", f"凭证 {voucher_no} {action_text}成功！")
        except ValueError as exc:
            log_event(
                logger,
                "凭证审核失败",
                level=30,
                voucher_no=voucher_no,
                reviewer=reviewer_name,
                reviewer_account=self.username,
                reason=str(exc),
            )
            QMessageBox.warning(self, "提示", str(exc))
        except Exception as exc:
            logger.exception("凭证审核失败")
            QMessageBox.critical(self, "错误", f"凭证审核失败: {exc}")

    def on_post_clicked(self):
        """过账或取消过账"""
        if self.current_voucher is None:
            QMessageBox.warning(self, "提示", "请先选择需要过账的凭证")
            return

        voucher_no = self.current_voucher.voucher_no
        poster_name = self.postEdit.text().strip() or (self.current_voucher.poster or "")
        try:
            if self.current_voucher.poster:
                self.voucherManager.cancel_post(voucher_no, self.username)
                action_text = "取消过账"
            else:
                if not poster_name:
                    QMessageBox.warning(self, "提示", "请先填写过账人")
                    return
                self.voucherManager.post_voucher(voucher_no, poster_name, self.username)
                action_text = "过账"

            self.current_voucher = self.voucherManager.search_voucher(voucher_no)
            self.populate_voucher(self.current_voucher)
            log_event(
                logger,
                "凭证过账状态更新完成",
                voucher_no=voucher_no,
                action=action_text,
                poster=poster_name,
                poster_account=self.username,
            )
            QMessageBox.information(self, "成功", f"凭证 {voucher_no} {action_text}成功！")
        except ValueError as exc:
            log_event(
                logger,
                "凭证过账失败",
                level=30,
                voucher_no=voucher_no,
                poster=poster_name,
                poster_account=self.username,
                reason=str(exc),
            )
            QMessageBox.warning(self, "提示", str(exc))
        except Exception as exc:
            logger.exception("凭证过账失败")
            QMessageBox.critical(self, "错误", f"凭证过账失败: {exc}")

    def on_btnCancel_clicked(self):
        log_event(logger, "取消凭证编辑", username=self.username, company=self.company, func=self.func)
        self.close()

    def populate_voucher(self, voucher):
        """将凭证数据回显到界面"""
        self.current_voucher = voucher
        self.reset_table_rows()

        voucher_date = QDate.fromString(voucher.voucher_date, "yyyy-MM-dd")
        if voucher_date.isValid():
            self.voucher_date = voucher_date
            self.update_date_label(self.voucher_date, self.dateBtnLabel)

        if voucher.created_time:
            created_date = QDate.fromString(str(voucher.created_time)[:10], "yyyy-MM-dd")
            if created_date.isValid():
                self.created_time = created_date
                self.update_date_label(self.created_time, self.datetimeBtnLabel)

        self.typeCombo.setCurrentText(voucher.voucher_type or "记账凭证")
        self.update_footer_labels(voucher)

        for row, detail in enumerate(voucher.details):
            self.table.setItem(row, 0, QTableWidgetItem(detail.summary or ""))

            subject = f"{detail.account_code} {detail.account_name}"
            subject_item = QTableWidgetItem(subject)
            subject_item.setFlags(subject_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, subject_item)

            self.table.setItem(row, 2, QTableWidgetItem(str(detail.debit_amount or 0)))
            self.table.setItem(row, 3, QTableWidgetItem(str(detail.credit_amount or 0)))

        for row in range(len(voucher.details), self.table.rowCount() - 1):
            subjectItem = QTableWidgetItem("按F2")
            subjectItem.setForeground(QColor(150, 150, 150))
            subjectItem.setBackground(QColor(240, 240, 240))
            subjectItem.setFlags(subjectItem.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, subjectItem)

        self.calculate_totals()
        self.update_post_action()
        self.update_review_action()

    def load_voucher(self):
        """加载已录入的凭证"""
        if self.numberCombo.currentIndex() == -1 or not self.numberCombo.currentText():
            self.current_voucher = None
            self.reset_table_rows()
            self.update_footer_labels()
            self.update_post_action()
            self.update_review_action()
            return

        number = self.voucher_date.toString("yyyy-MM-") + self.numberCombo.currentText()
        log_event(logger, "加载凭证", voucher_no=number, username=self.username, company=self.company, func=self.func)
        voucher = self.voucherManager.search_voucher(number)
        if voucher is None:
            log_event(logger, "凭证不存在", level=30, voucher_no=number)
            self.current_voucher = None
            self.update_footer_labels()
            self.update_post_action()
            self.update_review_action()
            return

        self.populate_voucher(voucher)
        log_event(
            logger,
            "凭证加载完成",
            voucher_no=number,
            detail_count=len(voucher.details),
            reviewer=voucher.reviewer or "",
            poster=voucher.poster or "",
        )

    def load_voucher_by_number(self, voucher_no):
        """根据完整凭证号加载凭证详情"""
        voucher = self.voucherManager.search_voucher(voucher_no)
        if voucher is None:
            raise ValueError(f"凭证 {voucher_no} 不存在")

        voucher_date = QDate.fromString(voucher.voucher_date, "yyyy-MM-dd")
        if voucher_date.isValid():
            self.voucher_date = voucher_date
            self.update_date_label(self.voucher_date, self.dateBtnLabel)
            self.refresh_number_combo()

        voucher_suffix = voucher_no.split("-")[-1]
        if self.numberCombo.findText(voucher_suffix) == -1:
            self.numberCombo.addItem(voucher_suffix)
        self.numberCombo.setCurrentText(voucher_suffix)
        self.populate_voucher(voucher)


if __name__ == "__main__":
    app = QApplication([])
    demo_user = {"username": "demo", "company": "OpenFina"}
    window = Certification(demo_user, 3)
    window.show()
    app.exec()



