import sys
import hashlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame, QCheckBox
)
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from PySide6.QtCore import Qt, QSize


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.init_slot()

    def setupUi(self):
        """初始化用户界面"""
        self.setWindowTitle("用户登录系统")
        self.setFixedSize(400, 500)
        
        # 设置应用程序图标
        # self.setWindowIcon(QIcon(self.create_icon()))
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                border: 2px solid #dcdcdc;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;

            }
            QLineEdit:focus {
                border: 2px solid #4d90fe;
            }
            QPushButton {
                background-color: rgb(255, 255, 255);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(221, 221, 221, 1);
            }
            QPushButton:pressed {
                background-color: rgba(221, 221, 221, 0.8);
            }

            QLabel#titleLabel {
                font-size: 24px;
            }
            QLabel#subtitleLabel {
                font-size: 14px;
            }
        """)
        
        # 模拟用户数据库 (在实际应用中应使用数据库)
        self.users = {
            "admin": self.hash_password("admin123"),  # 用户: admin, 密码: admin123
            "user": self.hash_password("user123"),    # 用户: user, 密码: user123
        }

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("用户登录")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("欢迎回来，请登录您的账户")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 表单框架
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # 用户名输入
        username_layout = QVBoxLayout()
        username_layout.setSpacing(5)
        
        username_label = QLabel("用户名")
        username_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setMinimumHeight(40)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # 密码输入
        password_layout = QVBoxLayout()
        password_layout.setSpacing(5)
        
        password_label = QLabel("密码")
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # 记住密码和忘记密码
        options_layout = QHBoxLayout()
        
        self.remember_checkbox = QCheckBox("记住密码")
        
        self.forgot_password_btn = QPushButton("忘记密码?")
        self.forgot_password_btn.setFlat(True)
        self.forgot_password_btn.setStyleSheet("""
            QPushButton {
                color: #4d90fe;
                border: none;
                font-size: 13px;
                text-align: right;
            }
            QPushButton:hover {
                color: #357ae8;
                text-decoration: underline;
            }
        """)
        
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(self.forgot_password_btn)
        
        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.setMinimumHeight(45)
        
        # 注册提示
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        register_label = QLabel("还没有账户?")
        
        self.register_btn = QPushButton("立即注册")
        self.register_btn.setObjectName("registerBtn")
        self.register_btn.setFixedSize(100, 35)
        
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_btn)
        
        # 添加所有组件到表单布局
        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(options_layout)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.login_btn)
        
        # 添加所有组件到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(form_frame)
        main_layout.addLayout(register_layout)
        main_layout.addStretch()

    def init_slot(self):
        # 记住密码功能
        self.remember_password = False
        self.load_saved_credentials()

        self.remember_checkbox.stateChanged.connect(self.on_remember_changed)
        self.login_btn.clicked.connect(self.on_login)
        self.register_btn.clicked.connect(self.on_register)
        self.forgot_password_btn.clicked.connect(self.on_forgot_password)
        
    
    def hash_password(self, password):
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def on_login(self):
        """处理登录按钮点击事件"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # 验证输入
        if not username:
            self.show_error("请输入用户名")
            self.username_input.setFocus()
            return
        
        if not password:
            self.show_error("请输入密码")
            self.password_input.setFocus()
            return
        
        # 验证用户名和密码
        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username] == hashed_password:
                # 登录成功
                self.save_credentials(username, password)
                self.show_success(f"登录成功！欢迎回来，{username}。")
                
                # 在实际应用中，这里会跳转到主界面
                # 现在只是显示成功消息并关闭窗口
                self.close()
            else:
                self.show_error("密码错误，请重试")
                self.password_input.clear()
                self.password_input.setFocus()
        else:
            self.show_error("用户名不存在")
            self.username_input.setFocus()
    
    def on_register(self):
        """处理注册按钮点击事件"""
        QMessageBox.information(
            self, 
            "注册功能", 
            "注册功能正在开发中，敬请期待！\n\n"
            "当前测试账户：\n"
            "用户名: admin, 密码: admin123\n"
            "用户名: user, 密码: user123"
        )
    
    def on_forgot_password(self):
        """处理忘记密码按钮点击事件"""
        QMessageBox.information(
            self, 
            "找回密码", 
            "密码找回功能正在开发中，敬请期待！\n\n"
            "请联系系统管理员重置密码。"
        )
    
    def on_remember_changed(self, state):
        """处理记住密码复选框状态改变"""
        self.remember_password = (state == Qt.CheckState.Checked.value)
    
    def save_credentials(self, username, password):
        """保存用户凭证"""
        if self.remember_password:
            # 在实际应用中，应该使用安全的方式存储凭证
            # 这里只是简单演示
            with open("credentials.txt", "w") as f:
                f.write(f"{username}\n{password}")
        else:
            # 清除保存的凭证
            try:
                import os
                os.remove("credentials.txt")
            except:
                pass
    
    def load_saved_credentials(self):
        """加载保存的用户凭证"""
        try:
            with open("credentials.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    username = lines[0].strip()
                    password = lines[1].strip()
                    
                    self.username_input.setText(username)
                    self.password_input.setText(password)
                    self.remember_checkbox.setChecked(True)
                    self.remember_password = True
        except:
            # 文件不存在或读取错误
            pass
    
    def show_error(self, message):
        """显示错误消息"""
        QMessageBox.critical(self, "登录失败", message)
    
    def show_success(self, message):
        """显示成功消息"""
        QMessageBox.information(self, "登录成功", message)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        reply = QMessageBox.question(
            self, 
            "确认退出", 
            "确定要退出登录系统吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """主函数"""
    app = QApplication([])
    window = LoginWindow()

    window.show()    
    app.exec()


if __name__ == "__main__":
    main()