import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, 
    QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPixmap
import json

from utils.password import PasswdManager
from utils.path_helper import get_db_path, get_settings_path, get_icon_path
from utils.logger import get_logger, log_event, install_global_exception_logger
from app.main import MyWindow

# 获取日志记录器
logger = get_logger()
# from ui.auto_login import AutoWidget
DEFAULT_COMPANY = "OpenFina"


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.passwdManage = PasswdManager(get_db_path("users.db"))
        log_event(logger, "初始化登录窗口", db_path=self.passwdManage.db_path)
        self.setupUi()
        self.setStyle()
        self.init_slot()
        
    def setupUi(self):
        self.setWindowTitle("OpenFina")
        self.resize(900, 600)
        # 主布局
        mainLayout = QHBoxLayout()

        ## 左侧边
        self.leftWidget = QWidget()
        self.leftWidget.setObjectName("leftWidget")
        self.leftWidget.setMinimumSize(450, 600)
        self.leftWidget.setMaximumSize(450, 600)
        leftLayout = QVBoxLayout(self.leftWidget)

        ## 登录主界面
        self.rightWidget = QWidget()
        self.rightWidget.setMinimumSize(450, 600)
        self.rightWidget.setMaximumSize(450, 600)
        rightLayout = QVBoxLayout(self.rightWidget)

        # 标题
        self.titleWidget = QWidget()
        self.titleWidget.setMinimumSize(450, 200)
        self.titleWidget.setMaximumSize(450, 200)
        self.titleWidget.setObjectName("titleWidget")
        titleLayout = QVBoxLayout(self.titleWidget)
        self.titleLb = QLabel("用户登录")
        self.titleLb.setObjectName("titleLb")
        self.subtitleLb = QLabel("请登录您的账户")
        self.subtitleLb.setObjectName("subtitleLb")

        # 用户信息
        self.inputWidget = QWidget()
        inputLayout = QVBoxLayout(self.inputWidget)
        ## 用户名
        usernameLb = QLabel("用户名")
        self.usernameLine = QLineEdit()
        ## 密码
        passwdLayout = QHBoxLayout()
        passwordLb = QLabel("密码")
        self.passwordLine = QLineEdit()
        self.passwordLine.setEchoMode(QLineEdit.Password)

        ## 显示/隐藏密码
        self.switchBtn = QPushButton()
        ### 初始使用文本
        self.switchBtn.setText("显示")
        self.switchBtn.setObjectName("switchBtn")

        # 记住/忘记密码
        passBtnLayout = QHBoxLayout()
        self.keepBox = QCheckBox("记住密码")
        self.keepBox.setObjectName("keepBox")
        self.forgetBtn = QPushButton("忘记密码")
        self.forgetBtn.setObjectName("forgetBtn")

        # 登录
        self.loginBtn = QPushButton("登录")

        # 注册
        registerLayout = QHBoxLayout()
        registerLb = QLabel("还没有账户?")
        self.registerBtn = QPushButton("立即注册")
        self.registerBtn.setObjectName("registerBtn")
        
        # 密码可见性状态（不使用checkable）
        self.password_visible = False

        # 布局
        ## 标题栏布局
        titleLayout.addSpacerItem(QSpacerItem(10000, 200, QSizePolicy.Expanding))
        titleLayout.addWidget(self.titleLb)
        titleLayout.addWidget(self.subtitleLb)
        titleLayout.addSpacerItem(QSpacerItem(10000, 200, QSizePolicy.Expanding))
        titleLayout.setSpacing(0)
        ## 密码
        passwdLayout.addWidget(self.passwordLine)
        passwdLayout.addWidget(self.switchBtn)
        ## 记住/忘记密码
        passBtnLayout.addWidget(self.keepBox)
        passBtnLayout.addSpacerItem(QSpacerItem(600, 0, QSizePolicy.Expanding))
        passBtnLayout.addWidget(self.forgetBtn)
        ## 注册
        registerLayout.addSpacerItem(QSpacerItem(200, 0, QSizePolicy.Expanding))
        registerLayout.addWidget(registerLb)
        registerLayout.addWidget(self.registerBtn)
        registerLayout.addSpacerItem(QSpacerItem(200, 0, QSizePolicy.Expanding))
        ## 输入区布局
        # inputLayout.addSpacerItem(QSpacerItem(10000, 10, QSizePolicy.Expanding))
        inputLayout.addWidget(usernameLb)
        inputLayout.addWidget(self.usernameLine)
        inputLayout.addSpacerItem(QSpacerItem(10000, 20, QSizePolicy.Expanding))
        inputLayout.addWidget(passwordLb)
        inputLayout.addLayout(passwdLayout)
        inputLayout.addLayout(passBtnLayout)
        inputLayout.addSpacerItem(QSpacerItem(10000, 20, QSizePolicy.Expanding))
        inputLayout.addWidget(self.loginBtn)
        inputLayout.addLayout(registerLayout)
        inputLayout.addSpacerItem(QSpacerItem(10000, 100, QSizePolicy.Expanding))
        # 右侧布局
        rightLayout.addWidget(self.titleWidget)
        rightLayout.addWidget(self.inputWidget)
        # 主布局
        mainLayout.addWidget(self.leftWidget)
        mainLayout.addWidget(self.rightWidget)
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)

        self.setLayout(mainLayout)

    def setStyle(self):
        """样式设置"""
        self.setStyleSheet("""
            /* 主窗口边框弧度 */
            LoginWidget {
                border-radius: 10px;
                background-color: white;
            }
            
            /* 左侧面板 */
            #leftWidget {
                background-color: rgb(243, 243, 243);
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }
            
            /* 标题标签居中 */
            #titleLb {
                font-size: 28px;
                font-weight: bold;
                color: #333333;
                qproperty-alignment: 'AlignCenter';
            }
            
            /* 副标题标签居中 */
            #subtitleLb {
                font-size: 16px;
                color: #666666;
                qproperty-alignment: 'AlignCenter';
                margin-top: 10px;
            }
            
            /* 标题容器 */
            #titleWidget {
                background-color: transparent;
            }
            
            /* 输入框样式 */
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            
            /* 按钮样式 */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
                           
            /* 记住密码 */
            QCheckBox#keepBox {
                background-color: transparent;
                border: none;
                font-size: 12px;
                color: #666666;
                spacing: 5px;
            }
            
            QCheckBox#keepBox::indicator {
                width: 12px;
                height: 12px;
            }
            
            QCheckBox#keepBox::indicator:unchecked {
                border: 1px solid #cccccc;
                border-radius: 2px;
                background-color: white;
            }
            
            QCheckBox#keepBox::indicator:checked {
                border: 1px solid #007bff;
                border-radius: 2px;
                background-color: #007bff;
            }
            
            /* 忘记密码 */
            QPushButton#forgetBtn {
                background-color: transparent;
                border: none;
                font-size: 12px;
                color: #666666;
                text-decoration: underline;
                padding: 0px;
                margin: 0px;
            }
            
            QPushButton#forgetBtn:hover {
                color: #007bff;
                text-decoration: underline;
            }
            
            QPushButton#forgetBtn:pressed {
                color: #0056b3;
                text-decoration: underline;
            }
                           
            /* 注册密码 */
            QPushButton#registerBtn {
                background-color: transparent;
                border: none;
                font-size: 12px;
                color: #666666;
                text-decoration: underline;
                padding: 0px;
                margin: 0px;           
            }
                           
            QPushButton#registerBtn:hover {
                color: #007bff;
                text-decoration: underline;
            }
            
            QPushButton#registerBtn:pressed {
                color: #0056b3;
                text-decoration: underline;
            }

            /* 显示he隐藏 */              
            QPushButton#switchBtn {
                background-color: transparent;
                border: none;
                padding: 5px;
                min-width: 30px;
                min-height: 30px;
            }
                           
            QPushButton#switchBtn:hover {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
            }
                           
            QPushButton#switchBtn:pressed {
                background-color: rgba(0, 0, 0, 0.15);
            }
"""
        )
        
    def init_slot(self):
        """绑定信号与槽"""
        self.registerBtn.clicked.connect(self.on_registerBtn_clicked)
        self.loginBtn.clicked.connect(self.on_loginBtn_clicked)
        self.switchBtn.clicked.connect(self.switch_password_visibility)
        
        # 初始状态
        self.update_password_visibility()

    def on_registerBtn_clicked(self):
        """注册"""
        # 获取用户名和密码
        self.company = DEFAULT_COMPANY
        self.username = self.usernameLine.text().strip()
        self.password = self.passwordLine.text().strip()
        log_event(logger, "开始注册用户", username=self.username, company=self.company)

        if not self.username or not self.password:
            log_event(logger, "注册失败：用户名或密码为空", level=40, username=self.username)
            QMessageBox.warning(self, "错误", "用户名和密码不能为空")
            return
        
        self.passwdManage.cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (self.username,)
        )
        result = self.passwdManage.cursor.fetchone()
        if result:
            log_event(logger, "注册失败：用户名已存在", level=30, username=self.username)
            QMessageBox(self, "错误", "用户名已存在")
            return
        
        try:
            password_hash = self.passwdManage.hash_password(self.password)
            
            # 存储到数据库
            self.passwdManage.cursor.execute(
                "INSERT INTO users (company, username, password) VALUES (?, ?, ?)",
                (self.company, self.username, password_hash)
            )
            self.passwdManage.conn.commit()
            log_event(logger, "注册成功", username=self.username, company=self.company)
            
            QMessageBox.information(self, "成功", "用户注册成功！")
            
        except Exception as e:
            logger.exception("注册失败")
            QMessageBox.critical(self, "错误", f"注册失败: {str(e)}")

    def update_password_visibility(self):
        """更新密码可见性状态"""
        if self.password_visible:
            self.passwordLine.setEchoMode(QLineEdit.Normal)
            self.switchBtn.setText("隐藏")
        else:
            self.passwordLine.setEchoMode(QLineEdit.Password)
            self.switchBtn.setText("显示")
    
    def switch_password_visibility(self):
        """切换密码可见性"""
        # 切换状态
        self.password_visible = not self.password_visible
        self.update_password_visibility()

    def on_loginBtn_clicked(self):
        """登录"""
        # 获取用户名和密码
        self.username = self.usernameLine.text().strip()
        self.password = self.passwordLine.text().strip()
        log_event(logger, "开始登录", username=self.username)

        if not self.username or not self.password:
            log_event(logger, "登录失败：用户名或密码为空", level=40, username=self.username)
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return
        
        self.passwdManage.cursor.execute(
            "SELECT password, company FROM users WHERE username = ?",
            (self.username,)
        )
        result = self.passwdManage.cursor.fetchone()

        if not result:
            log_event(logger, "登录失败：用户不存在", level=30, username=self.username)
            QMessageBox.warning(self, "错误", "用户不存在")
            return
        
        hash = result
        is_valid = self.passwdManage.verify_password(self.password, hash[0])

        if is_valid:
            self.company = result[1] or DEFAULT_COMPANY
            log_event(logger, "登录成功", username=self.username, company=self.company, remember=self.keepBox.isChecked())
            # QMessageBox.information(self, "成功", "登录成功!")
            self.save_settings()
            self.switch_2_main()
        else:
            log_event(logger, "登录失败：密码错误", level=30, username=self.username)
            QMessageBox.warning(self, "错误", "用户名或密码错误")

    def switch_2_main(self):
        """跳转到主界面"""
        log_event(logger, "进入主界面", username=self.username, company=self.company)
        self.mainWindow = MyWindow(self.username, self.company)
        self.mainWindow.show()

        self.close()

    def save_settings(self):
        if self.keepBox.isChecked():
            settings = {
                "remember_state": True,
                "username": self.username,
                "duration": 7
            }
        else:
            settings = {
                "remember_state": False
            }        
        with open(get_settings_path(), 'w', encoding='utf-8') as f:
            json.dump(settings, f)
        log_event(logger, "保存登录设置", settings_path=get_settings_path(), remember=settings.get("remember_state", False), username=self.username)


class AutoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.passwdManage = PasswdManager(get_db_path("users.db"))
        self.user_info()
        log_event(logger, "初始化自动登录窗口", username=self.username, company=self.company)
        self.setupUi()
        self.setStyle()
        self.init_slot()

    def setupUi(self):
        """设置界面信息"""
        self.setWindowTitle("自动登录")
        self.resize(900, 600)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)

        # 左侧
        self.leftWidget = QWidget()
        self.leftWidget.setMinimumSize(300, 600)
        self.leftWidget.setMaximumSize(16777215, 600)
        leftLayout = QVBoxLayout(self.leftWidget)

        # 中间
        self.middleWidget = QWidget()
        self.middleWidget.setMinimumSize(300, 600)
        self.middleWidget.setMaximumSize(300, 600)
        middleLayout = QVBoxLayout(self.middleWidget)
        middleLayout.setContentsMargins(0,20,0,50)
        self.userLb = QLabel()
        # self.userLb.setObjectName("userLb")
        self.userLb.setPixmap(QPixmap(get_icon_path("user.png")))
        self.usernameLb = QLabel(self.username)
        self.usernameLb.setObjectName("usernameLb")
        self.companyLb = QLabel(DEFAULT_COMPANY)
        self.companyLb.setObjectName("companyLb")
        self.confirmBtn = QPushButton("确认登录")
        self.cancelBtn = QPushButton("取消登录")

        # 右侧
        self.rightWidget = QWidget()
        self.rightWidget.setMinimumSize(300, 600)
        self.rightWidget.setMaximumSize(16777215, 600)
        rightLayout = QVBoxLayout(self.rightWidget)

        ## 布局
        middleLayout.addWidget(self.userLb)
        middleLayout.addWidget(self.usernameLb)
        middleLayout.addWidget(self.companyLb)
        middleLayout.addSpacerItem(QSpacerItem(300, 100, QSizePolicy.Expanding))
        middleLayout.addWidget(self.confirmBtn)
        middleLayout.addWidget(self.cancelBtn)
        # 主布局
        mainLayout.addWidget(self.leftWidget)
        mainLayout.addWidget(self.middleWidget)
        mainLayout.addWidget(self.rightWidget)

        self.setLayout(mainLayout)
    
    def setStyle(self):
        """设置页面风格"""
        self.setStyleSheet("""
            /* 用户名标签居中 */
            #usernameLb {
            font-size: 28px;
            font-weight: bold;
            color: #333333;
            qproperty-alignment: 'AlignCenter';
            }
                           
            #companyLb {
            font-size: 20px;
            font-weight: norm;
            color: #333333;
            qproperty-alignment: 'AlignCenter';
            }
                           
            /* 按钮样式 */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
                           
            #userLb {
                background-image: url(:/image/a.png);
            }
            
        """)

    def init_slot(self):
        """绑定信号和槽"""
        self.confirmBtn.clicked.connect(self.on_confirmBtn_clicked)
        self.cancelBtn.clicked.connect(self.on_cancelBtn_clicked)

    def on_confirmBtn_clicked(self):
        """确认登录"""
        log_event(logger, "确认自动登录", username=self.username, company=self.company)
        self.mainWindow = MyWindow(self.username, self.company)
        self.mainWindow.show()

        self.close()

    def on_cancelBtn_clicked(self):
        """取消登录"""
        log_event(logger, "取消自动登录，返回普通登录", username=self.username)
        self.logingWidget = LoginWidget()
        self.logingWidget.show()
        self.close()

    def user_info(self):
        """获取用户信息"""
        settings_path = get_settings_path()
        log_event(logger, "加载自动登录设置", settings_path=settings_path)
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        self.username = settings['username']

        self.passwdManage.cursor.execute(
            "SELECT company FROM users WHERE username = ?",
            (self.username,)
            )
        result = self.passwdManage.cursor.fetchone()

        if result:
            self.company = result[0] or DEFAULT_COMPANY
            log_event(logger, "自动登录用户信息加载成功", username=self.username, company=self.company)
        else:
            self.company = DEFAULT_COMPANY
            log_event(logger, "自动登录用户缺少公司信息，使用默认公司", level=30, username=self.username, company=self.company)
        

def load_settings():        
    """加载软件配置"""
    settings_path = get_settings_path()
    log_event(logger, "检查登录设置文件", settings_path=settings_path)
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        log_event(logger, "加载登录设置成功", settings_path=settings_path, remember=settings.get('remember_state', False), username=settings.get('username', ''))
    
        if settings['remember_state']:
            return True
        else:
            return False
    
    else:
        log_event(logger, "登录设置文件不存在，使用普通登录", level=30, settings_path=settings_path)
        return False


if __name__ == "__main__":
    # 记录系统启动信息
    from utils.logger import log_system_info
    log_system_info(logger)
    install_global_exception_logger(logger)
    
    is_remember = load_settings()

    app = QApplication([])
    if is_remember:
        # 是否自动登录
        window = AutoWidget()
    else:
        window = LoginWidget()

    window.show()
    app.exec()

