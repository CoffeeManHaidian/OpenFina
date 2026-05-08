import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from models.bookset import UserBooksetManager
from utils.logger import get_logger, log_event
from utils.theme import material_dialog_style

logger = get_logger()


class UserManagementDialog(QDialog):
    def __init__(self, user_info, parent=None):
        super().__init__(parent)
        self.user_info = user_info
        self.userManager = UserBooksetManager()
        self.setWindowTitle("用户管理")
        self.resize(700, 500)
        self.setStyleSheet(material_dialog_style())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("用户管理")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #202124;")

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "用户名", "角色", "状态", "账套数", "创建时间"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.createBtn = QPushButton("创建用户")
        self.createBtn.clicked.connect(self.on_create_user)
        self.disableBtn = QPushButton("启用/禁用")
        self.disableBtn.clicked.connect(self.on_toggle_status)
        self.roleBtn = QPushButton("切换角色")
        self.roleBtn.clicked.connect(self.on_toggle_role)
        self.resetPwdBtn = QPushButton("重置密码")
        self.resetPwdBtn.clicked.connect(self.on_reset_password)

        btn_layout.addWidget(self.createBtn)
        btn_layout.addWidget(self.disableBtn)
        btn_layout.addWidget(self.roleBtn)
        btn_layout.addWidget(self.resetPwdBtn)
        btn_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

    def load_users(self):
        try:
            users = self.userManager.list_all_users()
        except Exception as exc:
            logger.exception("加载用户列表失败")
            QMessageBox.critical(self, "错误", f"加载用户列表失败: {exc}")
            return

        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(str(u["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(u["username"]))
            role_text = "系统管理员" if u["role"] == "admin" else "财务主管"
            self.table.setItem(i, 2, QTableWidgetItem(role_text))
            status_text = "正常" if u["status"] == "active" else "已禁用"
            self.table.setItem(i, 3, QTableWidgetItem(status_text))
            self.table.setItem(i, 4, QTableWidgetItem(str(u.get("bookset_count", 0))))
            self.table.setItem(i, 5, QTableWidgetItem(u.get("created_at", "")))

    def _get_selected_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请先选择一个用户")
            return None
        user_id = int(self.table.item(row, 0).text())
        username = self.table.item(row, 1).text()
        role_text = self.table.item(row, 2).text()
        role = "admin" if role_text == "系统管理员" else "manager"
        status_text = self.table.item(row, 3).text()
        status = "active" if status_text == "正常" else "disabled"
        return {"user_id": user_id, "username": username, "role": role, "status": status}

    def on_create_user(self):
        dialog = CreateUserDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        username, password, role = dialog.get_values()
        try:
            user_id = self.userManager.register_user(username, password)
            if role == "admin":
                with self.userManager.get_connection() as conn:
                    conn.execute("UPDATE users SET role = 'admin', must_change_password = 1 WHERE id = ?", (user_id,))
            log_event(logger, "管理员创建用户", created_by=self.user_info["username"], new_user=username, role=role)
            QMessageBox.information(self, "成功", f"用户 {username} 创建成功")
            self.load_users()
        except ValueError as exc:
            QMessageBox.warning(self, "错误", str(exc))

    def on_toggle_status(self):
        user = self._get_selected_user()
        if user is None:
            return
        if user["user_id"] == self.user_info["user_id"]:
            QMessageBox.warning(self, "提示", "不能修改自己的状态")
            return
        new_status = "disabled" if user["status"] == "active" else "active"
        try:
            self.userManager.update_user_status(user["user_id"], new_status)
            QMessageBox.information(self, "成功", f"用户 {user['username']} 已{'禁用' if new_status == 'disabled' else '启用'}")
            self.load_users()
        except Exception as exc:
            QMessageBox.critical(self, "错误", str(exc))

    def on_toggle_role(self):
        user = self._get_selected_user()
        if user is None:
            return
        if user["user_id"] == self.user_info["user_id"]:
            QMessageBox.warning(self, "提示", "不能修改自己的角色")
            return
        new_role = "manager" if user["role"] == "admin" else "admin"
        try:
            self.userManager.update_user_role(user["user_id"], new_role)
            QMessageBox.information(self, "成功",
                f"用户 {user['username']} 角色已切换为 {'系统管理员' if new_role == 'admin' else '财务主管'}")
            self.load_users()
        except ValueError as exc:
            QMessageBox.warning(self, "错误", str(exc))

    def on_reset_password(self):
        user = self._get_selected_user()
        if user is None:
            return
        reply = QMessageBox.question(
            self, "确认", f"确定要重置用户 {user['username']} 的密码为 '123456' 吗？\n用户下次登录时需要修改密码。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        try:
            self.userManager.reset_user_password(user["user_id"], "123456")
            QMessageBox.information(self, "成功", f"用户 {user['username']} 密码已重置为 123456")
        except Exception as exc:
            QMessageBox.critical(self, "错误", str(exc))


class CreateUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("创建用户")
        self.resize(380, 280)
        self.setStyleSheet(material_dialog_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("创建新用户")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #202124;")

        self.usernameEdit = QLineEdit()
        self.usernameEdit.setPlaceholderText("请输入用户名")

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("请输入密码")
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.roleCombo = QComboBox()
        self.roleCombo.addItem("财务主管", "manager")
        self.roleCombo.addItem("系统管理员", "admin")

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(QLabel("用户名"))
        layout.addWidget(self.usernameEdit)
        layout.addWidget(QLabel("密码"))
        layout.addWidget(self.passwordEdit)
        layout.addWidget(QLabel("角色"))
        layout.addWidget(self.roleCombo)
        layout.addWidget(buttons)

    def _on_accept(self):
        if not self.usernameEdit.text().strip():
            QMessageBox.warning(self, "提示", "请输入用户名")
            return
        if not self.passwordEdit.text().strip():
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        self.accept()

    def get_values(self):
        return (
            self.usernameEdit.text().strip(),
            self.passwordEdit.text().strip(),
            self.roleCombo.currentData(),
        )
