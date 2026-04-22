import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMenuBar,
    QMessageBox,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.voucher import VoucherManager
from ui.certificate import Certification
from ui.clickableLabel import ClickableLabel
from ui.subject import SubjectWindow
from utils.logger import get_logger, log_event
from utils.theme import material_widget_style

logger = get_logger()


class VoucherListDialog(QDialog):
    def __init__(self, user_info, parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.bookset_db_path = user_info["bookset_db_path"]
        self.voucherManager = VoucherManager(self.bookset_db_path)
        self.subjectSelector = SubjectWindow(self.bookset_db_path)
        self.period_date = QDate.currentDate()
        self.summary_keyword = ""
        self.account_keyword = ""
        self.detail_windows = []

        self.setup_ui()
        self.setStyleSheet(material_widget_style())
        self.init_menu()
        self.init_slot()
        self.refresh_list()

    def setup_ui(self):
        self.setWindowTitle("凭证列表")
        self.resize(980, 620)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 16)
        main_layout.setSpacing(10)

        self.menuBar = QMenuBar(self)
        self.menuBar.setMinimumHeight(34)
        self.menuBar.setStyleSheet("QMenuBar { min-height: 34px; }")
        main_layout.setMenuBar(self.menuBar)

        self.infoWidget = QWidget(self)
        info_layout = QHBoxLayout(self.infoWidget)
        info_layout.setContentsMargins(0, 0, 0, 0)

        self.periodLabel = ClickableLabel()
        self.filterLabel = QLabel()
        self.filterLabel.setStyleSheet("color: #5f6368;")
        self.periodLabel.setStyleSheet("color: #1a73e8; font-weight: 600;")

        info_layout.addWidget(self.periodLabel)
        info_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        info_layout.addWidget(self.filterLabel)

        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["凭证号", "业务日期", "凭证字", "摘要", "状态", "制单人", "审核/过账"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 130)
        self.table.setColumnWidth(1, 110)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 280)
        self.table.setColumnWidth(4, 90)
        self.table.setColumnWidth(5, 90)
        self.table.setColumnWidth(6, 140)

        self.tipLabel = QLabel("双击凭证可打开只读详情。")
        self.tipLabel.setStyleSheet("color: #5f6368;")

        main_layout.addWidget(self.infoWidget)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.tipLabel)

    def init_menu(self):
        filter_menu = self.menuBar.addMenu("筛选")

        self.summaryFilterAction = QAction("按摘要筛选", self)
        self.subjectFilterAction = QAction("按会计科目筛选", self)
        self.periodAction = QAction("切换会计期间", self)
        self.clearFilterAction = QAction("清除全部筛选", self)

        filter_menu.addAction(self.summaryFilterAction)
        filter_menu.addAction(self.subjectFilterAction)
        filter_menu.addSeparator()
        filter_menu.addAction(self.periodAction)
        filter_menu.addSeparator()
        filter_menu.addAction(self.clearFilterAction)

    def init_slot(self):
        self.summaryFilterAction.triggered.connect(self.prompt_summary_filter)
        self.subjectFilterAction.triggered.connect(self.prompt_subject_filter)
        self.periodAction.triggered.connect(self.prompt_period)
        self.clearFilterAction.triggered.connect(self.clear_filters)
        self.periodLabel.clicked.connect(self.prompt_period)
        self.table.itemDoubleClicked.connect(self.open_selected_voucher)

    def get_period_range(self):
        start_date = QDate(self.period_date.year(), self.period_date.month(), 1)
        if self.period_date.month() == 12:
            end_date = QDate(self.period_date.year() + 1, 1, 1).addDays(-1)
        else:
            end_date = QDate(self.period_date.year(), self.period_date.month() + 1, 1).addDays(-1)
        return start_date, end_date

    def update_labels(self):
        self.periodLabel.setText(f"会计期间: {self.period_date.toString('yyyy年MM期')}")
        filter_parts = []
        if self.summary_keyword:
            filter_parts.append(f"摘要: {self.summary_keyword}")
        if self.account_keyword:
            filter_parts.append(f"科目: {self.account_keyword}")
        self.filterLabel.setText("当前筛选: " + (" | ".join(filter_parts) if filter_parts else "无"))

    def refresh_list(self):
        start_date, end_date = self.get_period_range()
        self.update_labels()
        rows = self.voucherManager.search_vouchers(
            start_date=start_date,
            end_date=end_date,
            summary_keyword=self.summary_keyword or None,
            account_keyword=self.account_keyword or None,
        )
        log_event(
            logger,
            "刷新凭证列表",
            db_path=self.bookset_db_path,
            period=self.period_date.toString("yyyy-MM"),
            summary_keyword=self.summary_keyword,
            account_keyword=self.account_keyword,
            result_count=len(rows),
        )

        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            status_text = "未审核"
            audit_text = ""
            if row["poster"]:
                status_text = "已过账"
                audit_text = f"{row['reviewer'] or ''} / {row['poster']}"
            elif row["reviewer"]:
                status_text = "已审核"
                audit_text = row["reviewer"]

            values = [
                row["voucher_no"],
                row["voucher_date"],
                row["voucher_type"] or "",
                row["first_summary"] or "",
                status_text,
                row["preparer"] or "",
                audit_text.strip(" /"),
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.UserRole, row["voucher_no"])
                self.table.setItem(row_index, column, item)

        if rows:
            self.table.selectRow(0)

    def prompt_summary_filter(self):
        text, ok = QInputDialog.getText(self, "按摘要筛选", "请输入摘要关键字：", text=self.summary_keyword)
        if not ok:
            return
        self.summary_keyword = text.strip()
        self.refresh_list()

    def prompt_subject_filter(self):
        if self.subjectSelector.isVisible():
            self.subjectSelector.raise_()
            self.subjectSelector.activateWindow()
        else:
            self.subjectSelector.show()

        try:
            self.subjectSelector.subFunc.disconnect()
        except Exception:
            pass
        self.subjectSelector.subFunc.connect(self.apply_subject_filter)

    def apply_subject_filter(self, code, name):
        self.account_keyword = f"{code} {name}"
        self.refresh_list()

    def prompt_period(self):
        current_text = self.period_date.toString("yyyy-MM")
        text, ok = QInputDialog.getText(self, "切换会计期间", "请输入会计期间（格式：2026-04）：", text=current_text)
        if not ok:
            return
        value = text.strip()
        if not re.fullmatch(r"\d{4}-\d{2}", value):
            QMessageBox.warning(self, "提示", "请输入正确格式，例如 2026-04")
            return

        year, month = map(int, value.split("-"))
        if month < 1 or month > 12:
            QMessageBox.warning(self, "提示", "月份必须在 01 到 12 之间")
            return

        self.period_date = QDate(year, month, 1)
        self.refresh_list()

    def clear_filters(self):
        self.summary_keyword = ""
        self.account_keyword = ""
        self.refresh_list()

    def open_selected_voucher(self, item):
        voucher_no = item.data(Qt.UserRole)
        if not voucher_no:
            return

        try:
            detail_window = Certification(self.user_info, 2)
            detail_window.load_voucher_by_number(voucher_no)
            detail_window.show()
            self.detail_windows.append(detail_window)
            log_event(logger, "从凭证列表打开凭证详情", voucher_no=voucher_no, db_path=self.bookset_db_path)
        except Exception as exc:
            logger.exception("打开凭证详情失败")
            QMessageBox.critical(self, "错误", f"打开凭证详情失败:\n{exc}")
