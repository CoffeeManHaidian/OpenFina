import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidgetItem, QSpinBox,
    QCheckBox, QComboBox, QMessageBox, QHeaderView)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from models.voucher import VoucherManager
from utils.subject import SubjectLookup
from utils.logger import get_logger, log_event
from utils.theme import material_widget_style

logger = get_logger()


def compute_totals(rows):
    """计算各列的合计值。纯函数，可独立测试。"""
    totals = {
        "begin_debit": 0.0, "begin_credit": 0.0,
        "current_debit": 0.0, "current_credit": 0.0,
        "end_debit": 0.0, "end_credit": 0.0,
    }
    for row in rows:
        for key in totals:
            totals[key] += row.get(key, 0.0)
    return totals


class GeneralLedgerView(QWidget):
    def __init__(self, user_info):
        super().__init__()

        self.user_info = user_info
        self.bookset_db_path = user_info["bookset_db_path"]
        log_event(
            logger,
            "初始化总分类账窗口",
            enterprise_name=user_info.get("enterprise_name", user_info.get("company", "")),
            db_path=self.bookset_db_path,
        )
        self.subjectLookup = SubjectLookup(self.bookset_db_path)

        self.setupUi()
        self.setStyle()

    def setupUi(self):
        self.setWindowTitle("总分类账")
        self.resize(1200, 640)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(8, 8, 8, 8)
        mainLayout.setSpacing(6)

        # ---- 筛选第一行：基本过滤条件 ----
        row1 = QWidget()
        row1Layout = QHBoxLayout(row1)
        row1Layout.setContentsMargins(0, 0, 0, 0)

        row1Layout.addWidget(QLabel("会计期间"))
        self.yearStartSpin = QSpinBox()
        self.yearStartSpin.setRange(2000, 2100)
        self.yearStartSpin.setValue(QDate.currentDate().year())
        self.monthStartSpin = QSpinBox()
        self.monthStartSpin.setRange(1, 12)
        self.monthStartSpin.setValue(QDate.currentDate().month())
        row1Layout.addWidget(self.yearStartSpin)
        row1Layout.addWidget(QLabel("年"))
        row1Layout.addWidget(self.monthStartSpin)
        row1Layout.addWidget(QLabel("月"))
        row1Layout.addWidget(QLabel("至"))
        self.yearEndSpin = QSpinBox()
        self.yearEndSpin.setRange(2000, 2100)
        self.yearEndSpin.setValue(QDate.currentDate().year())
        self.monthEndSpin = QSpinBox()
        self.monthEndSpin.setRange(1, 12)
        self.monthEndSpin.setValue(QDate.currentDate().month())
        row1Layout.addWidget(self.yearEndSpin)
        row1Layout.addWidget(QLabel("年"))
        row1Layout.addWidget(self.monthEndSpin)
        row1Layout.addWidget(QLabel("月"))

        row1Layout.addSpacing(20)
        row1Layout.addWidget(QLabel("科目范围"))
        self.subjectFromEdit = QSpinBox()
        self.subjectFromEdit.setRange(0, 9999)
        self.subjectFromEdit.setSpecialValueText("")
        self.subjectFromEdit.setMinimumWidth(70)
        self.subjectToEdit = QSpinBox()
        self.subjectToEdit.setRange(0, 9999)
        self.subjectToEdit.setSpecialValueText("")
        self.subjectToEdit.setMinimumWidth(70)
        row1Layout.addWidget(self.subjectFromEdit)
        row1Layout.addWidget(QLabel("至"))
        row1Layout.addWidget(self.subjectToEdit)

        row1Layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.queryBtn = QPushButton("查询")
        self.queryBtn.clicked.connect(self.on_query)
        self.queryBtn.setFixedWidth(80)
        row1Layout.addWidget(self.queryBtn)

        mainLayout.addWidget(row1)

        # ---- 筛选第二行：通用过滤条件 ----
        row2 = QWidget()
        row2Layout = QHBoxLayout(row2)
        row2Layout.setContentsMargins(0, 0, 0, 0)

        row2Layout.addWidget(QLabel("账簿"))
        self.bookCombo = QComboBox()
        self.bookCombo.addItem("默认账簿")
        self.bookCombo.setEnabled(False)
        row2Layout.addWidget(self.bookCombo)

        row2Layout.addSpacing(16)
        row2Layout.addWidget(QLabel("币别"))
        self.currencyCombo = QComboBox()
        self.currencyCombo.addItem("人民币")
        self.currencyCombo.setEnabled(False)
        row2Layout.addWidget(self.currencyCombo)

        row2Layout.addSpacing(16)
        row2Layout.addWidget(QLabel("科目级别"))
        self.levelCombo = QComboBox()
        self.levelCombo.addItem("全部", 0)
        self.levelCombo.addItem("1", 1)
        self.levelCombo.addItem("2", 2)
        self.levelCombo.addItem("3", 3)
        row2Layout.addWidget(self.levelCombo)

        row2Layout.addSpacing(16)
        self.noActivityCheck = QCheckBox("无发生额不显示")
        row2Layout.addWidget(self.noActivityCheck)

        row2Layout.addSpacing(12)
        self.zeroBalanceCheck = QCheckBox("余额为零且无发生额不显示")
        row2Layout.addWidget(self.zeroBalanceCheck)

        row2Layout.addSpacing(12)
        self.showAuxCheck = QCheckBox("显示核算维度明细")
        self.showAuxCheck.setEnabled(False)
        row2Layout.addWidget(self.showAuxCheck)

        row2Layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.balanceLabel = QLabel("")
        self.balanceLabel.setStyleSheet("font-weight: bold;")
        row2Layout.addWidget(self.balanceLabel)

        mainLayout.addWidget(row2)

        # ---- 表格 ----
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "科目编码", "科目名称",
            "期初借方", "期初贷方",
            "本期借方", "本期贷方",
            "期末借方", "期末贷方",
            "余额方向",
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setDefaultSectionSize(24)

        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)

    def setStyle(self):
        self.setStyleSheet(material_widget_style())

    def on_query(self):
        if not os.path.exists(self.bookset_db_path):
            QMessageBox.warning(self, "错误", "账套数据库不存在")
            return

        start_date = self._build_date(self.yearStartSpin.value(), self.monthStartSpin.value(), is_start=True)
        end_date = self._build_date(self.yearEndSpin.value(), self.monthEndSpin.value(), is_start=False)

        if start_date > end_date:
            QMessageBox.warning(self, "错误", "起始期间不能晚于结束期间")
            return

        subject_from = str(self.subjectFromEdit.value()) if self.subjectFromEdit.value() > 0 else ""
        subject_to = str(self.subjectToEdit.value()) if self.subjectToEdit.value() > 0 else ""
        level = self.levelCombo.currentData()

        self.voucherManage = VoucherManager(self.bookset_db_path)
        result = self.voucherManage.get_general_ledger(
            start_date, end_date,
            subject_code_from=subject_from,
            subject_code_to=subject_to,
            subject_level=level,
        )

        # 后过滤：无发生额不显示
        if self.noActivityCheck.isChecked():
            result = [r for r in result if r["current_debit"] != 0.0 or r["current_credit"] != 0.0]

        # 后过滤：余额为零且无发生额不显示
        if self.zeroBalanceCheck.isChecked():
            result = [r for r in result
                       if not (r["begin_debit"] == 0.0 and r["begin_credit"] == 0.0
                               and r["current_debit"] == 0.0 and r["current_credit"] == 0.0
                               and r["end_debit"] == 0.0 and r["end_credit"] == 0.0)]

        self._populate_table(result)

        if result:
            totals = compute_totals(result)
            balanced = (
                abs(totals["begin_debit"] - totals["begin_credit"]) < 0.01 and
                abs(totals["current_debit"] - totals["current_credit"]) < 0.01 and
                abs(totals["end_debit"] - totals["end_credit"]) < 0.01
            )
            if balanced:
                self.balanceLabel.setText("✓ 试算平衡")
                self.balanceLabel.setStyleSheet("color: #2e7d32; font-weight: bold;")
            else:
                self.balanceLabel.setText("✗ 试算不平衡！")
                self.balanceLabel.setStyleSheet("color: #c62828; font-weight: bold;")
        else:
            self.balanceLabel.setText("")

    def _build_date(self, year, month, is_start):
        if is_start:
            return QDate(year, month, 1).toString("yyyy-MM-dd")
        else:
            if month == 12:
                return QDate(year + 1, 1, 1).addDays(-1).toString("yyyy-MM-dd")
            return QDate(year, month + 1, 1).addDays(-1).toString("yyyy-MM-dd")

    def _populate_table(self, result):
        self.table.setRowCount(0)

        if not result:
            self.balanceLabel.setText("(无数据)")
            return

        self.table.setRowCount(len(result) + 1)  # +1 for totals row

        for i, row in enumerate(result):
            items = [
                (row["account_code"], Qt.AlignCenter),
                (row["account_name"], Qt.AlignLeft | Qt.AlignVCenter),
                (f"{row['begin_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (f"{row['begin_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (f"{row['current_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (f"{row['current_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (f"{row['end_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (f"{row['end_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
                (row.get("balance_direction", ""), Qt.AlignCenter),
            ]
            for j, (text, align) in enumerate(items):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)

        # 合计行
        totals = compute_totals(result)
        total_row = len(result)
        total_items = [
            ("合计", Qt.AlignCenter),
            ("", Qt.AlignLeft),
            (f"{totals['begin_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            (f"{totals['begin_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            (f"{totals['current_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            (f"{totals['current_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            (f"{totals['end_debit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            (f"{totals['end_credit']:.2f}", Qt.AlignRight | Qt.AlignVCenter),
            ("", Qt.AlignCenter),
        ]
        font = QFont()
        font.setBold(True)
        for j, (text, align) in enumerate(total_items):
            item = QTableWidgetItem(text)
            item.setTextAlignment(align)
            item.setFont(font)
            item.setFlags(Qt.ItemIsEnabled)
            item.setBackground(QColor("#f5f5f5"))
            self.table.setItem(total_row, j, item)


if __name__ == "__main__":
    app = QApplication([])
    window = GeneralLedgerView(
        {
            "username": "demo",
            "user_id": 1,
            "bookset_id": 1,
            "enterprise_name": "OpenFina",
            "company": "OpenFina",
            "fiscal_year": 2026,
            "bookset_db_path": "",
        }
    )
    window.show()
    app.exec()
