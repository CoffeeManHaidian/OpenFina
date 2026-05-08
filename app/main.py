import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

from ui.mainwindow import Ui_MainWindow
from ui.certificate import Certification
from ui.login import clear_settings
from ui.summary import VoucherSummary
from ui.voucher_list_dialog import VoucherListDialog
from utils.logger import get_logger, log_system_info
from utils.theme import chrome_main_window_style

logger = get_logger()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, user_context):
        super().__init__()
        if isinstance(user_context, dict):
            self.user_info = user_context
        else:
            username, company = user_context
            self.user_info = {
                "username": username,
                "company": company,
            }

        self.setupUi(self)
        self.setObjectName("ChromeStyleMainWindow")
        self.setStyleSheet(chrome_main_window_style())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.update_shell_context()
        self.redefine_window_border_btn()
        self.init_solt()
        self.apply_role_visibility()

    def update_shell_context(self):
        enterprise_name = self.user_info.get("enterprise_name") or self.user_info.get("company", "OpenFina")
        fiscal_year = self.user_info.get("fiscal_year", "")
        username = self.user_info.get("username", "")

        if hasattr(self, "windowTitleLabel"):
            self.windowTitleLabel.setText("OpenFina")
        if hasattr(self, "windowContextLabel"):
            self.windowContextLabel.setText(f"{enterprise_name} / {fiscal_year} / {username}".strip(" /"))

    def on_maxBtn_clicked(self):
        """最大化窗口"""
        if self.isMaximized():
            self.showNormal()
            icon = QIcon()
            icon.addFile(u":/tittle/icons/maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.btn_max.setIcon(icon)
            self.btn_max.setText(u"▢")
            self.btn_max.setIconSize(QSize(10, 10))
            self.widget.setStyleSheet("#widget{background-color:#f8f9fa;border-radius:18px;}")
        else:
            self.showMaximized()
            icon = QIcon()
            icon.addFile(u":/tittle/icons/reduction.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.btn_max.setIcon(icon)
            self.btn_max.setText(u"❐")
            self.btn_max.setIconSize(QSize(10, 10))
            self.widget.setStyleSheet("#widget{background-color:#f8f9fa;border-radius:0px;}")

    def double_clicked_border_bar(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_maxBtn_clicked()

    def move_title_bar(self, event):
        self.windowHandle().startSystemMove()

    def redefine_window_border_btn(self):
        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.on_maxBtn_clicked)
        self.TittleBar.mouseDoubleClickEvent = self.double_clicked_border_bar
        self.TittleBar.mouseMoveEvent = self.move_title_bar

        # 在窗口控制按钮左侧添加切换用户按钮
        self.btn_switch_user = QPushButton("切换用户")
        self.btn_switch_user.setObjectName("btn_switch_user")
        self.btn_switch_user.setFixedHeight(28)
        self.btn_switch_user.clicked.connect(self.on_switch_user_clicked)
        self.controlsLayout.insertWidget(0, self.btn_switch_user)

    def init_solt(self):
        self.Ladger.clicked.connect(lambda: self.goto_subfunc_page(1))
        self.Report.clicked.connect(lambda: self.goto_subfunc_page(2))

        self.btn_certification.clicked.connect(lambda: self.goto_detailfunc_page(1))
        self.btn_ledger.clicked.connect(lambda: self.goto_detailfunc_page(2))

        self.inputBtn.clicked.connect(self.on_inputBtn_clicked)
        self.queryBtn.clicked.connect(self.on_queryBtn_clicked)
        self.postBtn.clicked.connect(self.on_postBtn_clicked)
        self.summaryBtn.clicked.connect(self.on_summaryBtn_clicked)
        self.btn_review.clicked.connect(self.on_reviewBtn_clicked)

    def apply_role_visibility(self):
        role = self.user_info.get("role", "manager")

        if role == "admin":
            # 隐藏业务操作按钮（查询和汇总保留）
            self.inputBtn.hide()
            self.postBtn.hide()
            self.btn_review.hide()
            self.btn_mode.hide()
            self.btn_introduce.hide()
            self.btn_out.hide()

            # 隐藏纯业务导航项（现金管理、期末结账）
            self.btn_cash_shortcut.hide()
            self.btn_settlement.hide()

            # 在左侧导航栏添加用户管理入口（与总账管理同级）
            self.btn_user_mgmt = QPushButton("用户管理")
            self.btn_user_mgmt.setObjectName("btn_user_mgmt")
            self.btn_user_mgmt.setMinimumHeight(42)
            self.btn_user_mgmt.clicked.connect(self.on_user_mgmt_clicked)
            self.leftBarLayout.insertWidget(self.leftBarLayout.count() - 1, self.btn_user_mgmt)

    def on_user_mgmt_clicked(self):
        try:
            from ui.user_management import UserManagementDialog
            dlg = UserManagementDialog(self.user_info, self)
            dlg.exec()
        except Exception as exc:
            logger.exception("打开用户管理窗口失败")
            QMessageBox.critical(self, "错误", f"打开用户管理窗口失败:\n{exc}")

    def goto_subfunc_page(self, number):
        self.wgt_SubFunc.setCurrentIndex(number)

    def goto_detailfunc_page(self, number):
        self.wgt_DetailFunc.setCurrentIndex(number)

    def on_inputBtn_clicked(self):
        if hasattr(self, "inputWindow") and self.inputWindow.isVisible():
            self.inputWindow.raise_()
            self.inputWindow.activateWindow()
            return

        try:
            self.inputWindow = Certification(self.user_info, 1)
            if hasattr(self.inputWindow, "voucherManager"):
                self.inputWindow.voucherManager.set_current_user_role(self.user_info.get("role", "manager"))
            self.inputWindow.show()
        except Exception as exc:
            logger.exception("打开凭证录入窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证录入窗口失败:\n{exc}")

    def on_queryBtn_clicked(self):
        if hasattr(self, "queryListWindow") and self.queryListWindow.isVisible():
            self.queryListWindow.raise_()
            self.queryListWindow.activateWindow()
            return

        try:
            self.queryListWindow = VoucherListDialog(self.user_info, self)
            self.queryListWindow.show()
        except Exception as exc:
            logger.exception("打开凭证查询窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证查询窗口失败:\n{exc}")

    def on_postBtn_clicked(self):
        if hasattr(self, "postWindow") and self.postWindow.isVisible():
            self.postWindow.raise_()
            self.postWindow.activateWindow()
            return

        try:
            self.postWindow = Certification(self.user_info, 3)
            if hasattr(self.postWindow, "voucherManager"):
                self.postWindow.voucherManager.set_current_user_role(self.user_info.get("role", "manager"))
            self.postWindow.show()
        except Exception as exc:
            logger.exception("打开凭证过账窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证过账窗口失败:\n{exc}")

    def on_summaryBtn_clicked(self):
        if hasattr(self, "summaryWindow") and self.summaryWindow.isVisible():
            self.summaryWindow.raise_()
            self.summaryWindow.activateWindow()
            return

        try:
            self.summaryWindow = VoucherSummary(self.user_info)
            self.summaryWindow.show()
            self.summaryWindow.filterWidget.show()
        except Exception as exc:
            logger.exception("打开凭证汇总窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证汇总窗口失败:\n{exc}")

    def on_reviewBtn_clicked(self):
        if hasattr(self, "reviewWindow") and self.reviewWindow.isVisible():
            self.reviewWindow.raise_()
            self.reviewWindow.activateWindow()
            return

        try:
            self.reviewWindow = Certification(self.user_info, 4)
            if hasattr(self.reviewWindow, "voucherManager"):
                self.reviewWindow.voucherManager.set_current_user_role(self.user_info.get("role", "manager"))
            self.reviewWindow.show()
        except Exception as exc:
            logger.exception("打开双敲审核窗口失败")
            QMessageBox.critical(self, "错误", f"打开双敲审核窗口失败:\n{exc}")

    def on_switch_user_clicked(self):
        reply = QMessageBox.question(
            self, "确认", "确定要切换用户吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        clear_settings()
        from ui.login import LoginWidget
        self.loginWidget = LoginWidget()
        self.loginWidget.show()
        self.close()


if __name__ == "__main__":
    log_system_info(logger)

    app = QApplication([])
    mainwindow = MyWindow(
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
    mainwindow.show()
    app.exec()


