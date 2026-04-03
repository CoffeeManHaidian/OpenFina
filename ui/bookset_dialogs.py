import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
)

from utils.theme import material_dialog_style


class CreateBooksetDialog(QDialog):
    def __init__(self, parent=None, title="创建初始账套"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(440, 240)
        self.setStyleSheet(material_dialog_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        titleLabel = QLabel("创建企业年度账套")
        titleLabel.setStyleSheet("font-size: 22px; font-weight: 700; color: #202124;")
        descLabel = QLabel("账套会按企业与会计年度独立建库，后续凭证、科目和报表都将写入该账套。")
        descLabel.setWordWrap(True)
        descLabel.setStyleSheet("color: #5f6368; line-height: 1.4;")

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.enterpriseEdit = QLineEdit()
        self.enterpriseEdit.setPlaceholderText("请输入企业名称")
        self.yearSpin = QSpinBox()
        self.yearSpin.setRange(2000, 2100)
        self.yearSpin.setValue(QDate.currentDate().year())
        self.codeEdit = QLineEdit()
        self.codeEdit.setPlaceholderText("可选，用于企业编码")

        form.addRow("企业名称", self.enterpriseEdit)
        form.addRow("会计年度", self.yearSpin)
        form.addRow("企业编码", self.codeEdit)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(titleLabel)
        layout.addWidget(descLabel)
        layout.addLayout(form)
        layout.addWidget(self.buttonBox)

    def accept(self):
        if not self.enterpriseEdit.text().strip():
            QMessageBox.warning(self, "提示", "请输入企业名称")
            return
        super().accept()

    def get_values(self):
        return {
            "enterprise_name": self.enterpriseEdit.text().strip(),
            "fiscal_year": self.yearSpin.value(),
            "enterprise_code": self.codeEdit.text().strip(),
        }


class BooksetSelectionDialog(QDialog):
    def __init__(self, booksets, parent=None):
        super().__init__(parent)
        self.booksets = booksets
        self.setWindowTitle("选择账套")
        self.resize(480, 220)
        self.setStyleSheet(material_dialog_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        titleLabel = QLabel("选择要进入的账套")
        titleLabel.setStyleSheet("font-size: 22px; font-weight: 700; color: #202124;")
        descLabel = QLabel("一个账号可以绑定多个企业年度账套。请选择本次登录要进入的工作台。")
        descLabel.setWordWrap(True)
        descLabel.setStyleSheet("color: #5f6368; line-height: 1.4;")

        self.combo = QComboBox()
        for bookset in booksets:
            label = f"{bookset['enterprise_name']} - {bookset['fiscal_year']}"
            if bookset.get("is_default"):
                label += " (默认)"
            self.combo.addItem(label, bookset["bookset_id"])

        self.defaultBox = QCheckBox("将本次选择设为默认账套")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(titleLabel)
        layout.addWidget(descLabel)
        layout.addWidget(self.combo)
        layout.addWidget(self.defaultBox)
        layout.addWidget(self.buttonBox)

    def get_selection(self):
        bookset_id = self.combo.currentData()
        selected = next(item for item in self.booksets if item["bookset_id"] == bookset_id)
        return selected, self.defaultBox.isChecked()

