import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.Ui_mainwindow import Ui_MainWindow
from ui.certificate import Certification
from ui.summary import VoucherSummary
from utils.logger import get_logger, log_system_info

logger = get_logger()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username, company):
        super().__init__()
        self.user_info = {
            "username": username,
            "company": company,
        }

        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.redefine_window_border_btn()
        self.init_solt()

    def on_maxBtn_clicked(self):
        """最大化窗口"""
        if self.isMaximized():
            self.showNormal()
            icon = QIcon()
            icon.addFile(u":/tittle/icons/maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.btn_max.setIcon(icon)
            self.btn_max.setIconSize(QSize(10, 10))
            self.widget.setStyleSheet(
                u"#widget{\n"
                "\tbackground-color: rgb(243, 243, 243);\n"
                "\tborder-radius: 10px;\n"
                "}"
            )
        else:
            self.showMaximized()
            icon = QIcon()
            icon.addFile(u":/tittle/icons/reduction.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.btn_max.setIcon(icon)
            self.btn_max.setIconSize(QSize(10, 10))
            self.widget.setStyleSheet(
                u"#widget{\n"
                "\tbackground-color: rgb(243, 243, 243);\n"
                "\tborder-radius: 0px;\n"
                "}"
            )

    def double_clicked_border_bar(self, event):
        """双击顶部标题条,使其在最大化和还原之间切换"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_maxBtn_clicked()

    def move_title_bar(self, event):
        """拖动顶部标题条"""
        self.windowHandle().startSystemMove()

    def redefine_window_border_btn(self):
        """使模拟边框的3个按钮生效(关闭、最小化、最大化、双击标题框)"""
        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.on_maxBtn_clicked)
        self.TittleBar.mouseDoubleClickEvent = self.double_clicked_border_bar
        self.TittleBar.mouseMoveEvent = self.move_title_bar

    def init_solt(self):
        """初始化槽函数"""
        self.Ladger.clicked.connect(lambda: self.goto_subfunc_page(1))
        self.Report.clicked.connect(lambda: self.goto_subfunc_page(2))

        self.btn_certification.clicked.connect(lambda: self.goto_detailfunc_page(1))
        self.btn_ledger.clicked.connect(lambda: self.goto_detailfunc_page(2))

        self.inputBtn.clicked.connect(self.on_inputBtn_clicked)
        self.queryBtn.clicked.connect(self.on_queryBtn_clicked)
        self.summaryBtn.clicked.connect(self.on_summaryBtn_clicked)

    def goto_subfunc_page(self, number):
        """切换子功能窗口页面"""
        self.wgt_SubFunc.setCurrentIndex(number)

    def goto_detailfunc_page(self, number):
        """切换明细功能窗口页面"""
        self.wgt_DetailFunc.setCurrentIndex(number)

    def on_inputBtn_clicked(self):
        """打开凭证录入窗口"""
        if hasattr(self, "inputWindow") and self.inputWindow.isVisible():
            self.inputWindow.raise_()
            self.inputWindow.activateWindow()
            return

        try:
            self.inputWindow = Certification(self.user_info, 1)
            self.inputWindow.show()
        except Exception as exc:
            logger.exception("打开凭证录入窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证录入窗口失败:\n{exc}")

    def on_queryBtn_clicked(self):
        """凭证查询功能"""
        if hasattr(self, "queryWindow") and self.queryWindow.isVisible():
            self.queryWindow.raise_()
            self.queryWindow.activateWindow()
            return

        try:
            self.queryWindow = Certification(self.user_info, 2)
            self.queryWindow.show()
        except Exception as exc:
            logger.exception("打开凭证查询窗口失败")
            QMessageBox.critical(self, "错误", f"打开凭证查询窗口失败:\n{exc}")

    def on_summaryBtn_clicked(self):
        """凭证汇总"""
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


if __name__ == "__main__":
    log_system_info(logger)

    app = QApplication([])
    mainwindow = MyWindow("demo", "OpenFina")
    mainwindow.show()
    app.exec()
