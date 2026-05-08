import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from utils.theme import material_dialog_style


class PasswordChangeDialog(QDialog):
    def __init__(self, user_manager, user_id, is_force_change=False, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.user_id = user_id
        self.is_force_change = is_force_change
        self.setWindowTitle("修改密码")
        self.resize(420, 320)
        self.setStyleSheet(material_dialog_style())

        if is_force_change:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        title = QLabel("首次登录，请修改密码" if is_force_change else "修改密码")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #202124;")

        desc = QLabel("系统检测到你的密码为初始密码，为了账户安全，请设置新密码。"
                      if is_force_change else "请输入原密码和新密码。")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #5f6368; line-height: 1.4;")

        self.oldPasswordEdit = QLineEdit()
        self.oldPasswordEdit.setPlaceholderText("请输入原密码")
        self.oldPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.newPasswordEdit = QLineEdit()
        self.newPasswordEdit.setPlaceholderText("请输入新密码")
        self.newPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirmPasswordEdit = QLineEdit()
        self.confirmPasswordEdit.setPlaceholderText("请确认新密码")
        self.confirmPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(8)
        layout.addWidget(QLabel("原密码"))
        layout.addWidget(self.oldPasswordEdit)
        layout.addWidget(QLabel("新密码"))
        layout.addWidget(self.newPasswordEdit)
        layout.addWidget(QLabel("确认新密码"))
        layout.addWidget(self.confirmPasswordEdit)
        layout.addWidget(buttons)

    def _on_accept(self):
        old_pwd = self.oldPasswordEdit.text().strip()
        new_pwd = self.newPasswordEdit.text().strip()
        confirm_pwd = self.confirmPasswordEdit.text().strip()

        if not old_pwd or not new_pwd or not confirm_pwd:
            QMessageBox.warning(self, "提示", "请填写所有密码字段")
            return
        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "提示", "两次输入的新密码不一致")
            return
        if len(new_pwd) < 4:
            QMessageBox.warning(self, "提示", "新密码长度不能少于4位")
            return

        try:
            self.user_manager.change_own_password(self.user_id, old_pwd, new_pwd)
            QMessageBox.information(self, "成功", "密码修改成功")
            self.accept()
        except ValueError as exc:
            QMessageBox.warning(self, "错误", str(exc))

    def closeEvent(self, event):
        if self.is_force_change:
            event.ignore()
        else:
            super().closeEvent(event)
