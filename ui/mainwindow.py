# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSplitter,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 760)
        MainWindow.setMinimumSize(QSize(1180, 720))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.setup_title_bar()
        self.setup_content_area()

        self.verticalLayout.addWidget(self.widget)
        self.retranslateUi(MainWindow)

        self.wgt_SubFunc.setCurrentIndex(0)
        self.wgt_DetailFunc.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def setup_title_bar(self):
        self.titleBar = QWidget(self.widget)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setMinimumHeight(56)
        self.titleBar.setMaximumHeight(56)

        self.titleBarLayout = QHBoxLayout(self.titleBar)
        self.titleBarLayout.setSpacing(12)
        self.titleBarLayout.setContentsMargins(18, 10, 12, 10)
        self.titleBarLayout.setObjectName(u"titleBarLayout")

        self.titleInfoWidget = QWidget(self.titleBar)
        self.titleInfoWidget.setObjectName(u"titleInfoWidget")
        self.titleInfoLayout = QVBoxLayout(self.titleInfoWidget)
        self.titleInfoLayout.setSpacing(2)
        self.titleInfoLayout.setContentsMargins(0, 0, 0, 0)

        self.windowTitleLabel = QLabel(self.titleInfoWidget)
        self.windowTitleLabel.setObjectName(u"windowTitleLabel")
        self.windowTitleLabel.setText(u"OpenFina")
        self.titleInfoLayout.addWidget(self.windowTitleLabel)

        self.windowContextLabel = QLabel(self.titleInfoWidget)
        self.windowContextLabel.setObjectName(u"windowContextLabel")
        self.windowContextLabel.setText(u"企业账套工作台")
        self.titleInfoLayout.addWidget(self.windowContextLabel)

        self.titleBarLayout.addWidget(self.titleInfoWidget)
        self.titleBarLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.windowControls = QWidget(self.titleBar)
        self.windowControls.setObjectName(u"windowControls")
        self.controlsLayout = QHBoxLayout(self.windowControls)
        self.controlsLayout.setSpacing(6)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)

        self.btn_min = QToolButton(self.windowControls)
        self.btn_min.setObjectName(u"btn_min")
        self.btn_min.setToolTip(u"最小化")
        self.btn_min.setText(u"━")
        self.btn_min.setFixedSize(36, 28)
        self.controlsLayout.addWidget(self.btn_min)

        self.btn_max = QToolButton(self.windowControls)
        self.btn_max.setObjectName(u"btn_max")
        self.btn_max.setToolTip(u"最大化")
        self.btn_max.setText(u"▢")
        self.btn_max.setCheckable(True)
        self.btn_max.setFixedSize(36, 28)
        self.controlsLayout.addWidget(self.btn_max)

        self.btn_close = QToolButton(self.windowControls)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setToolTip(u"关闭")
        self.btn_close.setText(u"✕")
        self.btn_close.setFixedSize(36, 28)
        self.controlsLayout.addWidget(self.btn_close)

        self.titleBarLayout.addWidget(self.windowControls)
        self.verticalLayout_2.addWidget(self.titleBar)

        self.TittleBar = self.titleBar

    def setup_content_area(self):
        self.contentContainer = QWidget(self.widget)
        self.contentContainer.setObjectName(u"contentContainer")
        self.contentLayout = QHBoxLayout(self.contentContainer)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setObjectName(u"contentLayout")

        self.leftBar = QWidget(self.contentContainer)
        self.leftBar.setObjectName(u"leftBar")
        self.leftBar.setMinimumWidth(260)
        self.leftBar.setMaximumWidth(320)
        self.leftBarLayout = QVBoxLayout(self.leftBar)
        self.leftBarLayout.setSpacing(8)
        self.leftBarLayout.setContentsMargins(14, 18, 14, 18)
        self.leftBarLayout.setObjectName(u"leftBarLayout")
        self.leftBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.bookmarksTitle = QLabel(self.leftBar)
        self.bookmarksTitle.setObjectName(u"bookmarksTitle")
        self.bookmarksTitle.setText(u"快捷功能")
        self.leftBarLayout.addWidget(self.bookmarksTitle)

        self.Ladger = QPushButton(self.leftBar)
        self.Ladger.setObjectName(u"Ladger")
        self.Ladger.setText(u"总账管理")
        self.Ladger.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.Ladger)

        self.Report = QPushButton(self.leftBar)
        self.Report.setObjectName(u"Report")
        self.Report.setText(u"报表中心")
        self.Report.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.Report)

        self.Funds = QPushButton(self.leftBar)
        self.Funds.setObjectName(u"Funds")
        self.Funds.setText(u"资金管理")
        self.Funds.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.Funds)

        self.btn_voucher = QPushButton(self.leftBar)
        self.btn_voucher.setObjectName(u"btn_voucher")
        self.btn_voucher.setText(u"凭证处理")
        self.btn_voucher.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.btn_voucher)

        self.btn_cash_shortcut = QPushButton(self.leftBar)
        self.btn_cash_shortcut.setObjectName(u"btn_cash")
        self.btn_cash_shortcut.setText(u"现金管理")
        self.btn_cash_shortcut.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.btn_cash_shortcut)

        self.btn_settlement = QPushButton(self.leftBar)
        self.btn_settlement.setObjectName(u"btn_settlement")
        self.btn_settlement.setText(u"期末结账")
        self.btn_settlement.setMinimumHeight(42)
        self.leftBarLayout.addWidget(self.btn_settlement)

        self.leftBarLayout.addStretch(1)
        self.contentLayout.addWidget(self.leftBar)

        self.splitter = QSplitter(Qt.Orientation.Horizontal, self.contentContainer)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setHandleWidth(1)

        self.MainWidget = QWidget()
        self.MainWidget.setObjectName(u"MainWidget")
        self.mainWidgetLayout = QVBoxLayout(self.MainWidget)
        self.mainWidgetLayout.setSpacing(10)
        self.mainWidgetLayout.setContentsMargins(20, 18, 20, 18)
        self.mainWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lb_Sub = QLabel(self.MainWidget)
        self.lb_Sub.setObjectName(u"lb_Sub")
        self.lb_Sub.setText(u"子功能")
        self.mainWidgetLayout.addWidget(self.lb_Sub)

        self.wgt_SubFunc = QStackedWidget(self.MainWidget)
        self.wgt_SubFunc.setObjectName(u"wgt_SubFunc")
        self.wgt_SubFunc.setMinimumWidth(420)

        self.subHome = QWidget()
        self.subHome.setObjectName(u"subHome")
        self.subHomeLayout = QVBoxLayout(self.subHome)
        self.subHomeLayout.setContentsMargins(20, 20, 20, 20)
        self.subHomeLayout.setSpacing(18)
        self.subHomeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.welcomeLabel = QLabel(self.subHome)
        self.welcomeLabel.setObjectName(u"welcomeLabel")
        self.welcomeLabel.setText(u"OpenFina")
        self.welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.subHomeLayout.addWidget(self.welcomeLabel)

        self.subDescription = QLabel(self.subHome)
        self.subDescription.setObjectName(u"subDescription")
        self.subDescription.setText(u"新的数据库架构已经就绪，请从左侧选择业务模块开始处理。")
        self.subDescription.setWordWrap(True)
        self.subHomeLayout.addWidget(self.subDescription)

        self.quickActions = QWidget(self.subHome)
        self.quickActions.setObjectName(u"quickActions")
        self.quickLayout = QVBoxLayout(self.quickActions)
        self.quickLayout.setSpacing(12)
        self.quickLayout.setContentsMargins(0, 8, 0, 0)
        self.quickLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for text, name in [
            (u"新建凭证", u"new_voucher"),
            (u"查询凭证", u"query_voucher"),
            (u"生成报表", u"generate_report"),
            (u"系统设置", u"settings"),
        ]:
            btn = QPushButton(self.quickActions)
            btn.setObjectName(name)
            btn.setText(text)
            btn.setMinimumHeight(56)
            self.quickLayout.addWidget(btn)

        self.subHomeLayout.addWidget(self.quickActions)
        self.subHomeLayout.addStretch(1)
        self.wgt_SubFunc.addWidget(self.subHome)

        self.ladgerWidget = QWidget()
        self.ladgerWidget.setObjectName(u"ladgerWidget")
        self.ladgerLayout = QVBoxLayout(self.ladgerWidget)
        self.ladgerLayout.setSpacing(10)
        self.ladgerLayout.setContentsMargins(0, 0, 0, 0)
        self.ladgerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for attr_name, text in [
            ("btn_certification", u"01001 凭证管理"),
            ("btn_ledger", u"01002 期末处理"),
            ("btn_report", u"01003 账表查询"),
        ]:
            btn = QPushButton(self.ladgerWidget)
            btn.setObjectName(attr_name if attr_name != "btn_cash" else u"btn_cash_func")
            btn.setText(text)
            btn.setMinimumHeight(46)
            setattr(self, attr_name, btn)
            self.ladgerLayout.addWidget(btn)

        self.ladgerLayout.addStretch(1)
        self.wgt_SubFunc.addWidget(self.ladgerWidget)

        self.reportWidget = QWidget()
        self.reportWidget.setObjectName(u"reportWidget")
        self.reportLayout = QVBoxLayout(self.reportWidget)
        self.reportLayout.setContentsMargins(0, 0, 0, 0)
        self.reportLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lineEdit_2 = QLineEdit(self.reportWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumHeight(56)
        self.lineEdit_2.setText(u"这是报表")
        self.reportLayout.addWidget(self.lineEdit_2)
        self.reportLayout.addStretch(1)
        self.wgt_SubFunc.addWidget(self.reportWidget)

        self.mainWidgetLayout.addWidget(self.wgt_SubFunc)
        self.splitter.addWidget(self.MainWidget)

        self.RightBar = QWidget()
        self.RightBar.setObjectName(u"RightBar")
        self.RightBar.setMinimumWidth(360)
        self.RightBar.setMaximumWidth(460)
        self.rightBarLayout = QVBoxLayout(self.RightBar)
        self.rightBarLayout.setSpacing(10)
        self.rightBarLayout.setContentsMargins(18, 18, 18, 18)
        self.rightBarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lb_Detail = QLabel(self.RightBar)
        self.lb_Detail.setObjectName(u"lb_Detail")
        self.lb_Detail.setText(u"明细功能")
        self.rightBarLayout.addWidget(self.lb_Detail)

        self.wgt_DetailFunc = QStackedWidget(self.RightBar)
        self.wgt_DetailFunc.setObjectName(u"wgt_DetailFunc")
        self.wgt_DetailFunc.setMinimumWidth(320)

        self.detailHome = QWidget()
        self.detailHome.setObjectName(u"detailHome")
        self.detailHomeLayout = QVBoxLayout(self.detailHome)
        self.detailHomeLayout.setContentsMargins(0, 0, 0, 0)
        self.detailHomeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.detailHomeLabel = QLabel(self.detailHome)
        self.detailHomeLabel.setObjectName(u"detailHomeLabel")
        self.detailHomeLabel.setText(u"选择子功能后，这里会显示对应的明细入口。")
        self.detailHomeLabel.setWordWrap(True)
        self.detailHomeLayout.addWidget(self.detailHomeLabel)
        self.detailHomeLayout.addStretch(1)
        self.wgt_DetailFunc.addWidget(self.detailHome)

        self.detCertificate = QWidget()
        self.detCertificate.setObjectName(u"detCertificate")
        self.detCertLayout = QVBoxLayout(self.detCertificate)
        self.detCertLayout.setSpacing(10)
        self.detCertLayout.setContentsMargins(0, 0, 0, 0)
        self.detCertLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for attr_name, text in [
            ("inputBtn", u"01001 凭证录入"),
            ("queryBtn", u"01002 凭证查询"),
            ("postBtn", u"01003 凭证过账"),
            ("summaryBtn", u"01004 凭证汇总"),
            ("btn_mode", u"01005 模式凭证"),
            ("btn_review", u"01006 双敲审核"),
            ("btn_introduce", u"01007 标准凭证引入"),
            ("btn_out", u"01008 标准凭证引出"),
        ]:
            btn = QPushButton(self.detCertificate)
            btn.setObjectName(attr_name)
            btn.setText(text)
            btn.setMinimumHeight(46)
            setattr(self, attr_name, btn)
            self.detCertLayout.addWidget(btn)

        self.detCertLayout.addStretch(1)
        self.wgt_DetailFunc.addWidget(self.detCertificate)

        self.detLadger = QWidget()
        self.detLadger.setObjectName(u"detLadger")
        self.detLadgerLayout = QVBoxLayout(self.detLadger)
        self.detLadgerLayout.setSpacing(10)
        self.detLadgerLayout.setContentsMargins(0, 0, 0, 0)
        self.detLadgerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.pushButton = QPushButton(self.detLadger)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumHeight(46)
        self.pushButton.setText(u"总账功能预留")
        self.detLadgerLayout.addWidget(self.pushButton)
        self.detLadgerLayout.addStretch(1)
        self.wgt_DetailFunc.addWidget(self.detLadger)

        self.rightBarLayout.addWidget(self.wgt_DetailFunc)
        self.splitter.addWidget(self.RightBar)
        self.splitter.setSizes([650, 410])

        self.contentLayout.addWidget(self.splitter, 1)
        self.verticalLayout_2.addWidget(self.contentContainer, 1)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OpenFina - 财务管理系统", None))

    def apply_chrome_styles(self, MainWindow):
        pass


ChromeStyleMainWindow = Ui_MainWindow


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    class TestWindow(QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

    window = TestWindow()
    window.show()
    sys.exit(app.exec())
