import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from app.main import MyWindow
from models.bookset import UserBooksetManager
from ui.bookset_dialogs import BooksetSelectionDialog, CreateBooksetDialog
from utils.logger import get_logger, log_event
from utils.path_helper import get_icon_path, get_settings_path, get_user_db_path
from utils.theme import login_widget_style

logger = get_logger()


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.userManager = UserBooksetManager(get_user_db_path())
        log_event(logger, "初始化登录窗口", db_path=self.userManager.db_path)
        self.setupUi()
        self.setStyle()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("OpenFina")
        self.resize(980, 640)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(28, 28, 28, 28)
        mainLayout.setSpacing(0)

        self.leftWidget = QWidget()
        self.leftWidget.setObjectName("leftWidget")
        self.leftWidget.setMinimumWidth(430)
        leftLayout = QVBoxLayout(self.leftWidget)
        leftLayout.setContentsMargins(40, 48, 40, 48)
        leftLayout.setSpacing(18)

        self.brandTitle = QLabel("OpenFina")
        self.brandTitle.setObjectName("brandTitle")
        self.brandSubtitle = QLabel("新的账套数据库架构已经就位。\n登录后直接进入当前企业年度的专属工作台。")
        self.brandSubtitle.setObjectName("brandSubtitle")
        self.brandSubtitle.setWordWrap(True)
        self.heroMeta = QLabel("Google 风格界面\n企业与年度隔离\n更清晰的业务入口")
        self.heroMeta.setObjectName("brandSubtitle")
        self.heroMeta.setWordWrap(True)

        leftLayout.addWidget(self.brandTitle)
        leftLayout.addWidget(self.brandSubtitle)
        leftLayout.addWidget(self.heroMeta)
        leftLayout.addStretch(1)

        self.rightWidget = QWidget()
        self.rightWidget.setObjectName("rightWidget")
        rightLayout = QVBoxLayout(self.rightWidget)
        rightLayout.setContentsMargins(56, 56, 56, 56)
        rightLayout.setSpacing(0)

        self.formCard = QWidget()
        self.formCard.setObjectName("formCard")
        cardLayout = QVBoxLayout(self.formCard)
        cardLayout.setContentsMargins(36, 36, 36, 36)
        cardLayout.setSpacing(14)

        self.titleLb = QLabel("登录到账套")
        self.titleLb.setObjectName("titleLb")
        self.subtitleLb = QLabel("使用你的账号进入 OpenFina")
        self.subtitleLb.setObjectName("subtitleLb")

        usernameLb = QLabel("用户名")
        usernameLb.setObjectName("fieldLabel")
        self.usernameLine = QLineEdit()
        self.usernameLine.setPlaceholderText("请输入用户名")

        passwordLb = QLabel("密码")
        passwordLb.setObjectName("fieldLabel")
        self.passwordLine = QLineEdit()
        self.passwordLine.setPlaceholderText("请输入密码")
        self.passwordLine.setEchoMode(QLineEdit.Password)

        passwdLayout = QHBoxLayout()
        passwdLayout.setSpacing(8)
        self.switchBtn = QPushButton("显示")
        self.switchBtn.setObjectName("switchBtn")

        passBtnLayout = QHBoxLayout()
        passBtnLayout.setSpacing(8)
        self.keepBox = QCheckBox("记住登录")
        self.keepBox.setObjectName("keepBox")
        self.forgetBtn = QPushButton("忘记密码")
        self.forgetBtn.setObjectName("forgetBtn")

        self.loginBtn = QPushButton("登录")
        self.loginBtn.setObjectName("loginBtn")
        self.registerBtn = QPushButton("立即注册")
        self.registerBtn.setObjectName("registerBtn")
        self.password_visible = False

        registerLayout = QHBoxLayout()
        registerLayout.setSpacing(8)
        registerLb = QLabel("还没有账户？")
        registerLb.setObjectName("fieldLabel")

        passwdLayout.addWidget(self.passwordLine)
        passwdLayout.addWidget(self.switchBtn)

        passBtnLayout.addWidget(self.keepBox)
        passBtnLayout.addStretch(1)
        passBtnLayout.addWidget(self.forgetBtn)

        registerLayout.addStretch(1)
        registerLayout.addWidget(registerLb)
        registerLayout.addWidget(self.registerBtn)
        registerLayout.addStretch(1)

        cardLayout.addWidget(self.titleLb)
        cardLayout.addWidget(self.subtitleLb)
        cardLayout.addSpacing(12)
        cardLayout.addWidget(usernameLb)
        cardLayout.addWidget(self.usernameLine)
        cardLayout.addWidget(passwordLb)
        cardLayout.addLayout(passwdLayout)
        cardLayout.addLayout(passBtnLayout)
        cardLayout.addSpacing(6)
        cardLayout.addWidget(self.loginBtn)
        cardLayout.addLayout(registerLayout)

        rightLayout.addStretch(1)
        rightLayout.addWidget(self.formCard)
        rightLayout.addStretch(1)

        mainLayout.addWidget(self.leftWidget, 5)
        mainLayout.addWidget(self.rightWidget, 6)
        self.setLayout(mainLayout)

    def setStyle(self):
        self.setStyleSheet(login_widget_style())

    def init_slot(self):
        self.registerBtn.clicked.connect(self.on_registerBtn_clicked)
        self.loginBtn.clicked.connect(self.on_loginBtn_clicked)
        self.switchBtn.clicked.connect(self.switch_password_visibility)
        self.update_password_visibility()

    def update_password_visibility(self):
        if self.password_visible:
            self.passwordLine.setEchoMode(QLineEdit.Normal)
            self.switchBtn.setText("隐藏")
        else:
            self.passwordLine.setEchoMode(QLineEdit.Password)
            self.switchBtn.setText("显示")

    def switch_password_visibility(self):
        self.password_visible = not self.password_visible
        self.update_password_visibility()

    def on_registerBtn_clicked(self):
        username = self.usernameLine.text().strip()
        password = self.passwordLine.text().strip()
        log_event(logger, "开始注册用户", username=username)

        if not username or not password:
            QMessageBox.warning(self, "错误", "用户名和密码不能为空")
            return

        dialog = CreateBooksetDialog(self, "创建初始账套")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        values = dialog.get_values()
        try:
            user_id, bookset = self.userManager.create_user_with_bookset(
                username=username,
                password=password,
                enterprise_name=values["enterprise_name"],
                fiscal_year=values["fiscal_year"],
                enterprise_code=values["enterprise_code"],
            )
            log_event(
                logger,
                "注册成功",
                user_id=user_id,
                username=username,
                enterprise_name=bookset["enterprise_name"],
                fiscal_year=bookset["fiscal_year"],
            )
            QMessageBox.information(self, "成功", "用户注册成功，并已创建初始账套。")
        except ValueError as exc:
            log_event(logger, "注册失败", level=30, username=username, reason=str(exc))
            QMessageBox.warning(self, "错误", str(exc))
        except Exception as exc:
            logger.exception("注册失败")
            QMessageBox.critical(self, "错误", f"注册失败: {exc}")

    def on_loginBtn_clicked(self):
        username = self.usernameLine.text().strip()
        password = self.passwordLine.text().strip()
        log_event(logger, "开始登录", username=username)

        if not username or not password:
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return

        try:
            user = self.userManager.authenticate_user(username, password)
            if user.get("must_change_password"):
                from ui.password_change_dialog import PasswordChangeDialog
                dlg = PasswordChangeDialog(self.userManager, user["user_id"], is_force_change=True, parent=self)
                if dlg.exec() != QDialog.DialogCode.Accepted:
                    return
            user_context = self.build_user_context(user["user_id"], user["username"])
            self.save_settings(user_context)
            self.switch_2_main(user_context)
        except ValueError as exc:
            log_event(logger, "登录失败", level=30, username=username, reason=str(exc))
            QMessageBox.warning(self, "错误", str(exc))
        except Exception as exc:
            logger.exception("登录失败")
            QMessageBox.critical(self, "错误", f"登录失败: {exc}")

    def build_user_context(self, user_id, username, preferred_bookset_id=None):
        booksets = self.userManager.list_user_booksets(user_id)
        if not booksets:
            dialog = CreateBooksetDialog(self, "创建账套")
            if dialog.exec() != QDialog.DialogCode.Accepted:
                raise ValueError("当前用户未绑定账套")
            values = dialog.get_values()
            bookset = self.userManager.create_bookset_for_user(
                user_id,
                enterprise_name=values["enterprise_name"],
                fiscal_year=values["fiscal_year"],
                enterprise_code=values["enterprise_code"],
                is_default=True,
            )
            return self.userManager.get_user_context(user_id, username, bookset["bookset_id"])

        if preferred_bookset_id is not None:
            matched = next((item for item in booksets if item["bookset_id"] == preferred_bookset_id), None)
            if matched is not None:
                return self.userManager.get_user_context(user_id, username, matched["bookset_id"])

        if len(booksets) == 1:
            return self.userManager.get_user_context(user_id, username, booksets[0]["bookset_id"])

        dialog = BooksetSelectionDialog(booksets, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            raise ValueError("已取消选择账套")
        selected, set_default = dialog.get_selection()
        if set_default:
            self.userManager.set_default_bookset(user_id, selected["bookset_id"])
        return self.userManager.get_user_context(user_id, username, selected["bookset_id"])

    def switch_2_main(self, user_context):
        log_event(
            logger,
            "进入主界面",
            username=user_context["username"],
            enterprise_name=user_context["enterprise_name"],
            bookset_id=user_context["bookset_id"],
        )
        self.mainWindow = MyWindow(user_context)
        self.mainWindow.show()
        self.close()

    def save_settings(self, user_context):
        if self.keepBox.isChecked():
            settings = {
                "remember_state": True,
                "username": user_context["username"],
                "bookset_id": user_context["bookset_id"],
                "duration": 7,
            }
        else:
            settings = {"remember_state": False}
        with open(get_settings_path(), "w", encoding="utf-8") as f:
            json.dump(settings, f)
        log_event(
            logger,
            "保存登录设置",
            settings_path=get_settings_path(),
            remember=settings.get("remember_state", False),
            username=settings.get("username", ""),
            bookset_id=settings.get("bookset_id", ""),
        )


class AutoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.userManager = UserBooksetManager(get_user_db_path())
        self.user_context = self.load_user_context()
        log_event(
            logger,
            "初始化自动登录窗口",
            username=self.user_context["username"],
            enterprise_name=self.user_context["enterprise_name"],
            bookset_id=self.user_context["bookset_id"],
        )
        self.setupUi()
        self.setStyle()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("OpenFina")
        self.resize(980, 640)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(28, 28, 28, 28)
        mainLayout.setSpacing(0)

        self.leftWidget = QWidget()
        self.leftWidget.setObjectName("leftWidget")
        self.leftWidget.setMinimumWidth(430)
        leftLayout = QVBoxLayout(self.leftWidget)
        leftLayout.setContentsMargins(40, 48, 40, 48)
        leftLayout.setSpacing(16)

        self.versionBadge = QLabel("自动登录")
        self.versionBadge.setObjectName("versionBadge")
        self.brandTitle = QLabel("OpenFina")
        self.brandTitle.setObjectName("brandTitle")
        self.brandSubtitle = QLabel("已识别上次使用的账套。\n确认后将直接进入工作台。")
        self.brandSubtitle.setObjectName("brandSubtitle")
        self.brandSubtitle.setWordWrap(True)
        leftLayout.addWidget(self.versionBadge, 0, Qt.AlignmentFlag.AlignLeft)
        leftLayout.addSpacing(24)
        leftLayout.addWidget(self.brandTitle)
        leftLayout.addWidget(self.brandSubtitle)
        leftLayout.addStretch(1)

        self.rightWidget = QWidget()
        self.rightWidget.setObjectName("rightWidget")
        rightLayout = QVBoxLayout(self.rightWidget)
        rightLayout.setContentsMargins(56, 56, 56, 56)

        self.formCard = QWidget()
        self.formCard.setObjectName("formCard")
        cardLayout = QVBoxLayout(self.formCard)
        cardLayout.setContentsMargins(36, 36, 36, 36)
        cardLayout.setSpacing(14)

        self.titleLb = QLabel("继续进入当前账套")
        self.titleLb.setObjectName("titleLb")
        self.subtitleLb = QLabel("确认身份后直接进入主界面")
        self.subtitleLb.setObjectName("subtitleLb")

        self.userLb = QLabel()
        self.userLb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userLb.setPixmap(QPixmap(get_icon_path("user.png")).scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.usernameLb = QLabel(self.user_context["username"])
        self.usernameLb.setObjectName("titleLb")
        self.companyLb = QLabel(f"{self.user_context['enterprise_name']} / {self.user_context['fiscal_year']}")
        self.companyLb.setObjectName("subtitleLb")

        self.confirmBtn = QPushButton("确认登录")
        self.confirmBtn.setObjectName("confirmBtn")
        self.cancelBtn = QPushButton("取消登录")
        self.cancelBtn.setObjectName("cancelBtn")

        cardLayout.addWidget(self.titleLb)
        cardLayout.addWidget(self.subtitleLb)
        cardLayout.addSpacing(8)
        cardLayout.addWidget(self.userLb)
        cardLayout.addWidget(self.usernameLb)
        cardLayout.addWidget(self.companyLb)
        cardLayout.addSpacing(10)
        cardLayout.addWidget(self.confirmBtn)
        cardLayout.addWidget(self.cancelBtn)

        rightLayout.addStretch(1)
        rightLayout.addWidget(self.formCard)
        rightLayout.addStretch(1)

        mainLayout.addWidget(self.leftWidget, 5)
        mainLayout.addWidget(self.rightWidget, 6)
        self.setLayout(mainLayout)

    def setStyle(self):
        self.setStyleSheet(login_widget_style())

    def init_slot(self):
        self.confirmBtn.clicked.connect(self.on_confirmBtn_clicked)
        self.cancelBtn.clicked.connect(self.on_cancelBtn_clicked)

    def on_confirmBtn_clicked(self):
        if self.user_context.get("must_change_password"):
            from ui.password_change_dialog import PasswordChangeDialog
            dlg = PasswordChangeDialog(self.userManager, self.user_context["user_id"], is_force_change=True, parent=self)
            if dlg.exec() != QDialog.DialogCode.Accepted:
                self.on_cancelBtn_clicked()
                return
        log_event(
            logger,
            "确认自动登录",
            username=self.user_context["username"],
            bookset_id=self.user_context["bookset_id"],
        )
        self.mainWindow = MyWindow(self.user_context)
        self.mainWindow.show()
        self.close()

    def on_cancelBtn_clicked(self):
        log_event(logger, "取消自动登录，返回普通登录", username=self.user_context["username"])
        self.logingWidget = LoginWidget()
        self.logingWidget.show()
        self.close()

    def load_user_context(self):
        settings_path = get_settings_path()
        log_event(logger, "加载自动登录设置", settings_path=settings_path)
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        username = settings["username"]
        bookset_id = settings.get("bookset_id")
        user = self.userManager.get_user_by_username(username)
        if user is None:
            raise ValueError("自动登录用户不存在")
        return self.userManager.get_user_context(user["user_id"], user["username"], bookset_id)


def load_settings():
    settings_path = get_settings_path()
    log_event(logger, "检查登录设置文件", settings_path=settings_path)
    if not os.path.exists(settings_path):
        log_event(logger, "登录设置文件不存在，使用普通登录", level=30, settings_path=settings_path)
        return False

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as exc:
        log_event(logger, "登录设置文件读取失败，使用普通登录", level=30, settings_path=settings_path, reason=str(exc))
        return False

    log_event(
        logger,
        "加载登录设置成功",
        settings_path=settings_path,
        remember=settings.get("remember_state", False),
        username=settings.get("username", ""),
        bookset_id=settings.get("bookset_id", ""),
    )
    return settings.get("remember_state", False)


def clear_settings():
    settings_path = get_settings_path()
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump({"remember_state": False}, f)
    log_event(logger, "清理失效登录设置", settings_path=settings_path)


if __name__ == "__main__":
    from app.bootstrap import main

    main()
