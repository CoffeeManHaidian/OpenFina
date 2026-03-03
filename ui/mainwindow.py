# -*- coding: utf-8 -*-

"""
Chrome 风格的主窗口界面
包含标签页、地址栏、导航按钮等现代浏览器元素

使用方法：
    from ui.mainwindow import Ui_MainWindow
    
    class MyWindow(QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
"""

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget,
    QTabWidget, QToolButton, QMenu, QTextEdit, QSplitter)


class Ui_MainWindow(object):
    """
    Chrome 风格的 UI 设置类
    与原有代码兼容，可与 QMainWindow 多重继承使用
    """
    
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QSize(900, 600))
        
        # 中央部件
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#centralwidget{\n"
"	border-radius: 20px;\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # 主垂直布局
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # ===== 主容器 widget（与原有代码兼容） =====
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"#widget{\n"
"	background-color: rgb(243, 243, 243);\n"
"	border-radius: 15px;\n"
"}")
        
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        
        # ===== 顶部标题栏（仿 Chrome 标签栏区域） =====
        self.setup_title_bar()
        
        # ===== 导航工具栏（仿 Chrome 地址栏） =====
        self.setup_nav_toolbar()
        
        # ===== 主内容区域 =====
        self.setup_content_area()
        
        self.verticalLayout_2.addWidget(self.contentContainer, 1)
        self.verticalLayout.addWidget(self.widget)
        
        # 设置窗口标题
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        
        self.retranslateUi(MainWindow)
        
        self.wgt_SubFunc.setCurrentIndex(0)
        self.wgt_DetailFunc.setCurrentIndex(0)
        
        QMetaObject.connectSlotsByName(MainWindow)
        
    def setup_title_bar(self):
        """设置标题栏（Chrome 标签栏风格）"""
        self.titleBar = QWidget(self.centralwidget)
        self.titleBar.setObjectName(u"titleBar")
        self.titleBar.setMinimumSize(QSize(0, 40))
        self.titleBar.setMaximumSize(QSize(16777215, 40))
        
        self.titleBarLayout = QHBoxLayout(self.titleBar)
        self.titleBarLayout.setSpacing(0)
        self.titleBarLayout.setContentsMargins(8, 0, 0, 0)
        self.titleBarLayout.setObjectName(u"titleBarLayout")
        
        # 窗口控制按钮（左侧，macOS 风格）
        self.windowControls = QWidget(self.titleBar)
        self.windowControls.setObjectName(u"windowControls")
        self.windowControls.setFixedWidth(80)
        
        self.controlsLayout = QHBoxLayout(self.windowControls)
        self.controlsLayout.setSpacing(8)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)
        
        # 关闭按钮（红色）
        self.btn_close = QPushButton(self.windowControls)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setFixedSize(12, 12)
        self.btn_close.setToolTip(u"关闭")
        self.controlsLayout.addWidget(self.btn_close)
        
        # 最小化按钮（黄色）
        self.btn_min = QPushButton(self.windowControls)
        self.btn_min.setObjectName(u"btn_min")
        self.btn_min.setFixedSize(12, 12)
        self.btn_min.setToolTip(u"最小化")
        self.controlsLayout.addWidget(self.btn_min)
        
        # 最大化按钮（绿色）
        self.btn_max = QPushButton(self.windowControls)
        self.btn_max.setObjectName(u"btn_max")
        self.btn_max.setFixedSize(12, 12)
        self.btn_max.setToolTip(u"最大化")
        self.btn_max.setCheckable(True)
        self.controlsLayout.addWidget(self.btn_max)
        
        self.titleBarLayout.addWidget(self.windowControls)
        
        # 标签页区域（仿 Chrome 标签）
        self.tabWidget = QTabWidget(self.titleBar)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setDocumentMode(True)
        
        # 添加默认标签页
        self.add_new_tab(u"总账管理")
        
        self.titleBarLayout.addWidget(self.tabWidget, 1)
        
        # 新建标签页按钮
        self.btn_new_tab = QToolButton(self.titleBar)
        self.btn_new_tab.setObjectName(u"btn_new_tab")
        self.btn_new_tab.setText(u"+")
        self.btn_new_tab.setToolTip(u"新建标签页")
        self.btn_new_tab.setFixedSize(28, 28)
        self.titleBarLayout.addWidget(self.btn_new_tab)
        
        # 右侧菜单按钮
        self.btn_menu = QToolButton(self.titleBar)
        self.btn_menu.setObjectName(u"btn_menu")
        self.btn_menu.setText(u"⋮")
        self.btn_menu.setToolTip(u"菜单")
        self.btn_menu.setFixedSize(36, 36)
        self.titleBarLayout.addWidget(self.btn_menu)
        
        self.verticalLayout_2.addWidget(self.titleBar)
        
        # 添加 TittleBar 别名（与原有代码兼容）
        self.TittleBar = self.titleBar
        
    def setup_nav_toolbar(self):
        """设置导航工具栏（Chrome 地址栏风格）"""
        self.navToolbar = QWidget(self.centralwidget)
        self.navToolbar.setObjectName(u"navToolbar")
        self.navToolbar.setMinimumSize(QSize(0, 44))
        self.navToolbar.setMaximumSize(QSize(16777215, 44))
        
        self.navLayout = QHBoxLayout(self.navToolbar)
        self.navLayout.setSpacing(8)
        self.navLayout.setContentsMargins(12, 4, 12, 4)
        self.navLayout.setObjectName(u"navLayout")
        
        # 导航按钮组
        self.navButtons = QWidget(self.navToolbar)
        self.navButtons.setObjectName(u"navButtons")
        self.navButtonsLayout = QHBoxLayout(self.navButtons)
        self.navButtonsLayout.setSpacing(4)
        self.navButtonsLayout.setContentsMargins(0, 0, 0, 0)
        
        # 后退按钮
        self.btn_back = QToolButton(self.navButtons)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setText(u"◀")
        self.btn_back.setToolTip(u"后退")
        self.btn_back.setFixedSize(32, 32)
        self.btn_back.setEnabled(False)
        self.navButtonsLayout.addWidget(self.btn_back)
        
        # 前进按钮
        self.btn_forward = QToolButton(self.navButtons)
        self.btn_forward.setObjectName(u"btn_forward")
        self.btn_forward.setText(u"▶")
        self.btn_forward.setToolTip(u"前进")
        self.btn_forward.setFixedSize(32, 32)
        self.btn_forward.setEnabled(False)
        self.navButtonsLayout.addWidget(self.btn_forward)
        
        # 刷新按钮
        self.btn_refresh = QToolButton(self.navButtons)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setText(u"↻")
        self.btn_refresh.setToolTip(u"刷新")
        self.btn_refresh.setFixedSize(32, 32)
        self.navButtonsLayout.addWidget(self.btn_refresh)
        
        self.navLayout.addWidget(self.navButtons)
        
        # 地址/搜索栏（Chrome Omnibox 风格）
        self.addressBar = QLineEdit(self.navToolbar)
        self.addressBar.setObjectName(u"addressBar")
        self.addressBar.setPlaceholderText(u"搜索功能或输入代码...")
        self.navLayout.addWidget(self.addressBar, 1)
        
        # 扩展功能按钮组
        self.extButtons = QWidget(self.navToolbar)
        self.extButtons.setObjectName(u"extButtons")
        self.extLayout = QHBoxLayout(self.extButtons)
        self.extLayout.setSpacing(4)
        self.extLayout.setContentsMargins(0, 0, 0, 0)
        
        # 书签按钮
        self.btn_bookmark = QToolButton(self.extButtons)
        self.btn_bookmark.setObjectName(u"btn_bookmark")
        self.btn_bookmark.setText(u"☆")
        self.btn_bookmark.setToolTip(u"添加书签")
        self.btn_bookmark.setFixedSize(32, 32)
        self.btn_bookmark.setCheckable(True)
        self.extLayout.addWidget(self.btn_bookmark)
        
        # 用户头像按钮
        self.btn_user = QToolButton(self.extButtons)
        self.btn_user.setObjectName(u"btn_user")
        self.btn_user.setText(u"👤")
        self.btn_user.setToolTip(u"用户菜单")
        self.btn_user.setFixedSize(32, 32)
        self.extLayout.addWidget(self.btn_user)
        
        self.navLayout.addWidget(self.extButtons)
        
        self.verticalLayout_2.addWidget(self.navToolbar)
        
    def setup_content_area(self):
        """设置主内容区域"""
        self.contentContainer = QWidget(self.centralwidget)
        self.contentContainer.setObjectName(u"contentContainer")
        
        self.contentLayout = QHBoxLayout(self.contentContainer)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setObjectName(u"contentLayout")
        
        # 左侧边栏（书签栏/快捷导航）
        self.leftBar = QWidget(self.contentContainer)
        self.leftBar.setObjectName(u"leftBar")
        self.leftBar.setMinimumSize(QSize(200, 0))
        self.leftBar.setMaximumSize(QSize(300, 16777215))
        
        self.leftBarLayout = QVBoxLayout(self.leftBar)
        self.leftBarLayout.setSpacing(4)
        self.leftBarLayout.setContentsMargins(8, 8, 8, 8)
        self.leftBarLayout.setObjectName(u"leftBarLayout")
        
        # 书签栏标题
        self.bookmarksTitle = QLabel(self.leftBar)
        self.bookmarksTitle.setObjectName(u"bookmarksTitle")
        self.bookmarksTitle.setText(u"快捷功能")
        self.leftBarLayout.addWidget(self.bookmarksTitle)
        
        # 书签/快捷功能列表
        # 使用原有的按钮名称保持兼容
        self.Ladger = QPushButton(self.leftBar)
        self.Ladger.setObjectName(u"Ladger")
        self.Ladger.setText(u"📊 总账")
        self.Ladger.setMinimumHeight(36)
        self.Ladger.setFlat(True)
        self.leftBarLayout.addWidget(self.Ladger)
        
        self.Report = QPushButton(self.leftBar)
        self.Report.setObjectName(u"Report")
        self.Report.setText(u"📈 报表")
        self.Report.setMinimumHeight(36)
        self.Report.setFlat(True)
        self.leftBarLayout.addWidget(self.Report)
        
        self.Funds = QPushButton(self.leftBar)
        self.Funds.setObjectName(u"Funds")
        self.Funds.setText(u"💰 资金")
        self.Funds.setMinimumHeight(36)
        self.Funds.setFlat(True)
        self.leftBarLayout.addWidget(self.Funds)
        
        # 更多功能按钮
        btn_voucher = QPushButton(self.leftBar)
        btn_voucher.setObjectName(u"btn_voucher")
        btn_voucher.setText(u"📝 凭证")
        btn_voucher.setMinimumHeight(36)
        btn_voucher.setFlat(True)
        self.leftBarLayout.addWidget(btn_voucher)
        
        btn_cash = QPushButton(self.leftBar)
        btn_cash.setObjectName(u"btn_cash")
        btn_cash.setText(u"💵 现金")
        btn_cash.setMinimumHeight(36)
        btn_cash.setFlat(True)
        self.leftBarLayout.addWidget(btn_cash)
        
        btn_settlement = QPushButton(self.leftBar)
        btn_settlement.setObjectName(u"btn_settlement")
        btn_settlement.setText(u"📋 结账")
        btn_settlement.setMinimumHeight(36)
        btn_settlement.setFlat(True)
        self.leftBarLayout.addWidget(btn_settlement)
        
        self.leftBarLayout.addStretch(1)
        
        # 折叠侧边栏按钮
        self.btn_toggle_sidebar = QToolButton(self.leftBar)
        self.btn_toggle_sidebar.setObjectName(u"btn_toggle_sidebar")
        self.btn_toggle_sidebar.setText(u"◀")
        self.btn_toggle_sidebar.setToolTip(u"隐藏侧边栏")
        self.btn_toggle_sidebar.setFixedSize(24, 48)
        self.btn_toggle_sidebar.move(0, 200)
        
        self.contentLayout.addWidget(self.leftBar)
        
        # 主内容分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal, self.contentContainer)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setHandleWidth(1)
        
        # 主内容区
        self.MainWidget = QWidget()
        self.MainWidget.setObjectName(u"MainWidget")
        self.mainWidgetLayout = QVBoxLayout(self.MainWidget)
        self.mainWidgetLayout.setSpacing(0)
        self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)
        
        # 子功能标签
        self.lb_Sub = QLabel(self.MainWidget)
        self.lb_Sub.setObjectName(u"lb_Sub")
        self.lb_Sub.setMinimumSize(QSize(0, 20))
        self.lb_Sub.setMaximumSize(QSize(16777215, 20))
        self.lb_Sub.setText(u"子功能")
        self.mainWidgetLayout.addWidget(self.lb_Sub)
        
        # 内容堆叠窗口 - 使用原有名称 wgt_SubFunc 保持兼容
        self.wgt_SubFunc = QStackedWidget(self.MainWidget)
        self.wgt_SubFunc.setObjectName(u"wgt_SubFunc")
        self.wgt_SubFunc.setMinimumSize(QSize(400, 0))
        
        # 添加默认页面 - 首页
        self.subHome = QWidget()
        self.subHome.setObjectName(u"subHome")
        self.subHomeLayout = QVBoxLayout(self.subHome)
        self.subHomeLayout.setContentsMargins(20, 20, 20, 20)
        
        self.welcomeLabel = QLabel(self.subHome)
        self.welcomeLabel.setObjectName(u"welcomeLabel")
        self.welcomeLabel.setText(u"欢迎使用 OpenFina 财务管理系统")
        self.welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subHomeLayout.addWidget(self.welcomeLabel)
        
        # 快捷操作区域
        self.quickActions = QWidget(self.subHome)
        self.quickActions.setObjectName(u"quickActions")
        self.quickLayout = QHBoxLayout(self.quickActions)
        self.quickLayout.setSpacing(16)
        self.quickLayout.setContentsMargins(0, 40, 0, 0)
        
        actions = [
            (u"📝 新建凭证", u"new_voucher"),
            (u"🔍 查询凭证", u"query_voucher"),
            (u"📊 生成报表", u"generate_report"),
            (u"⚙️ 系统设置", u"settings"),
        ]
        
        for text, name in actions:
            btn = QPushButton(self.quickActions)
            btn.setObjectName(name)
            btn.setText(text)
            btn.setMinimumSize(120, 80)
            btn.setProperty(u"action", name)
            self.quickLayout.addWidget(btn)
            
        self.quickLayout.addStretch(1)
        self.subHomeLayout.addWidget(self.quickActions)
        self.subHomeLayout.addStretch(1)
        
        self.wgt_SubFunc.addWidget(self.subHome)
        
        # 子功能页面 - 总账（使用原有名称 ladgerWidget 保持兼容）
        self.ladgerWidget = QWidget()
        self.ladgerWidget.setObjectName(u"ladgerWidget")
        self.ladgerLayout = QVBoxLayout(self.ladgerWidget)
        self.ladgerLayout.setSpacing(0)
        self.ladgerLayout.setContentsMargins(0, 0, 0, 0)
        
        # 凭证处理按钮 - 使用原有名称 btn_certification
        self.btn_certification = QPushButton(self.ladgerWidget)
        self.btn_certification.setObjectName(u"btn_certification")
        self.btn_certification.setMinimumSize(QSize(0, 40))
        self.btn_certification.setMaximumSize(QSize(16777215, 40))
        self.btn_certification.setText(u"01001 凭证录入")
        self.btn_certification.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_certification)
        
        # 总账按钮 - 使用原有名称 btn_ledger
        self.btn_ledger = QPushButton(self.ladgerWidget)
        self.btn_ledger.setObjectName(u"btn_ledger")
        self.btn_ledger.setMinimumSize(QSize(0, 40))
        self.btn_ledger.setMaximumSize(QSize(16777215, 40))
        self.btn_ledger.setText(u"01002 凭证查询")
        self.btn_ledger.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_ledger)
        
        # 报表按钮 - 使用原有名称 btn_report
        self.btn_report = QPushButton(self.ladgerWidget)
        self.btn_report.setObjectName(u"btn_report")
        self.btn_report.setMinimumSize(QSize(0, 40))
        self.btn_report.setMaximumSize(QSize(16777215, 40))
        self.btn_report.setText(u"01003 凭证过账")
        self.btn_report.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_report)
        
        # 现金按钮
        self.btn_cash = QPushButton(self.ladgerWidget)
        self.btn_cash.setObjectName(u"btn_cash_func")
        self.btn_cash.setMinimumSize(QSize(0, 40))
        self.btn_cash.setMaximumSize(QSize(16777215, 40))
        self.btn_cash.setText(u"01004 现金流量")
        self.btn_cash.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_cash)
        
        # 结账按钮 - 使用原有名称 btn_bill
        self.btn_bill = QPushButton(self.ladgerWidget)
        self.btn_bill.setObjectName(u"btn_bill")
        self.btn_bill.setMinimumSize(QSize(0, 40))
        self.btn_bill.setMaximumSize(QSize(16777215, 40))
        self.btn_bill.setText(u"01005 结账")
        self.btn_bill.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_bill)
        
        # 往来按钮 - 使用原有名称 btn_transaction
        self.btn_transaction = QPushButton(self.ladgerWidget)
        self.btn_transaction.setObjectName(u"btn_transaction")
        self.btn_transaction.setMinimumSize(QSize(0, 40))
        self.btn_transaction.setMaximumSize(QSize(16777215, 40))
        self.btn_transaction.setText(u"01006 往来管理")
        self.btn_transaction.setIconSize(QSize(16, 16))
        self.ladgerLayout.addWidget(self.btn_transaction)
        
        self.wgt_SubFunc.addWidget(self.ladgerWidget)
        
        # 报表页面 - 使用原有名称 reportWidget
        self.reportWidget = QWidget()
        self.reportWidget.setObjectName(u"reportWidget")
        self.reportLayout = QVBoxLayout(self.reportWidget)
        
        self.lineEdit_2 = QLineEdit(self.reportWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(200, 100))
        self.lineEdit_2.setText(u"这是报表")
        self.reportLayout.addWidget(self.lineEdit_2)
        
        self.wgt_SubFunc.addWidget(self.reportWidget)
        
        self.mainWidgetLayout.addWidget(self.wgt_SubFunc)
        self.splitter.addWidget(self.MainWidget)
        
        # 右侧详情面板 - 使用原有名称 RightBar 保持兼容
        self.RightBar = QWidget()
        self.RightBar.setObjectName(u"RightBar")
        self.RightBar.setMinimumSize(QSize(250, 0))
        self.RightBar.setMaximumSize(QSize(400, 16777215))
        
        self.rightBarLayout = QVBoxLayout(self.RightBar)
        self.rightBarLayout.setSpacing(8)
        self.rightBarLayout.setContentsMargins(12, 12, 12, 12)
        
        self.lb_Detail = QLabel(self.RightBar)
        self.lb_Detail.setObjectName(u"lb_Detail")
        self.lb_Detail.setMinimumSize(QSize(0, 20))
        self.lb_Detail.setMaximumSize(QSize(16777215, 20))
        self.lb_Detail.setText(u"明细功能")
        self.rightBarLayout.addWidget(self.lb_Detail)
        
        # 详情功能堆叠窗口 - 使用原有名称 wgt_DetailFunc
        self.wgt_DetailFunc = QStackedWidget(self.RightBar)
        self.wgt_DetailFunc.setObjectName(u"wgt_DetailFunc")
        
        # 详情首页
        self.detailHome = QWidget()
        self.detailHome.setObjectName(u"detailHome")
        self.wgt_DetailFunc.addWidget(self.detailHome)
        
        # 凭证详情 - 使用原有名称 detCertificate
        self.detCertificate = QWidget()
        self.detCertificate.setObjectName(u"detCertificate")
        self.detCertificate.setMinimumSize(QSize(0, 240))
        self.detCertLayout = QVBoxLayout(self.detCertificate)
        self.detCertLayout.setSpacing(0)
        self.detCertLayout.setContentsMargins(0, 0, 0, 0)
        
        # 录入按钮 - 使用原有名称 inputBtn
        self.inputBtn = QPushButton(self.detCertificate)
        self.inputBtn.setObjectName(u"inputBtn")
        self.inputBtn.setMinimumSize(QSize(0, 40))
        self.inputBtn.setMaximumSize(QSize(16777215, 40))
        self.inputBtn.setText(u"01001 凭证录入")
        self.detCertLayout.addWidget(self.inputBtn)
        
        # 查询按钮 - 使用原有名称 queryBtn
        self.queryBtn = QPushButton(self.detCertificate)
        self.queryBtn.setObjectName(u"queryBtn")
        self.queryBtn.setMinimumSize(QSize(0, 40))
        self.queryBtn.setMaximumSize(QSize(16777215, 40))
        self.queryBtn.setText(u"01002 凭证查询")
        self.detCertLayout.addWidget(self.queryBtn)
        
        # 过账按钮
        self.postBtn = QPushButton(self.detCertificate)
        self.postBtn.setObjectName(u"postBtn")
        self.postBtn.setMinimumSize(QSize(0, 40))
        self.postBtn.setMaximumSize(QSize(16777215, 40))
        self.postBtn.setText(u"01003 凭证过账")
        self.detCertLayout.addWidget(self.postBtn)
        
        # 汇总按钮 - 使用原有名称 summaryBtn
        self.summaryBtn = QPushButton(self.detCertificate)
        self.summaryBtn.setObjectName(u"summaryBtn")
        self.summaryBtn.setMinimumSize(QSize(0, 40))
        self.summaryBtn.setMaximumSize(QSize(16777215, 40))
        self.summaryBtn.setText(u"01004 凭证汇总")
        self.detCertLayout.addWidget(self.summaryBtn)
        
        # 模式凭证按钮
        self.btn_mode = QPushButton(self.detCertificate)
        self.btn_mode.setObjectName(u"btn_mode")
        self.btn_mode.setMinimumSize(QSize(0, 40))
        self.btn_mode.setMaximumSize(QSize(16777215, 40))
        self.btn_mode.setText(u"01005 模式凭证")
        self.detCertLayout.addWidget(self.btn_mode)
        
        # 审核按钮
        self.btn_review = QPushButton(self.detCertificate)
        self.btn_review.setObjectName(u"btn_review")
        self.btn_review.setMinimumSize(QSize(0, 40))
        self.btn_review.setMaximumSize(QSize(16777215, 40))
        self.btn_review.setText(u"01006 双敲审核")
        self.detCertLayout.addWidget(self.btn_review)
        
        # 引入按钮
        self.btn_introduce = QPushButton(self.detCertificate)
        self.btn_introduce.setObjectName(u"btn_introduce")
        self.btn_introduce.setMinimumSize(QSize(0, 40))
        self.btn_introduce.setMaximumSize(QSize(16777215, 40))
        self.btn_introduce.setText(u"01007 标准凭证引入")
        self.detCertLayout.addWidget(self.btn_introduce)
        
        # 引出按钮
        self.btn_out = QPushButton(self.detCertificate)
        self.btn_out.setObjectName(u"btn_out")
        self.btn_out.setMinimumSize(QSize(0, 40))
        self.btn_out.setMaximumSize(QSize(16777215, 40))
        self.btn_out.setText(u"01008 标准凭证引出")
        self.detCertLayout.addWidget(self.btn_out)
        
        self.wgt_DetailFunc.addWidget(self.detCertificate)
        
        # 总账详情 - 使用原有名称 detLadger
        self.detLadger = QWidget()
        self.detLadger.setObjectName(u"detLadger")
        self.detLadger.setMinimumSize(QSize(0, 40))
        self.detLadgerLayout = QVBoxLayout(self.detLadger)
        self.detLadgerLayout.setSpacing(0)
        self.detLadgerLayout.setContentsMargins(0, 0, 0, 0)
        
        self.pushButton = QPushButton(self.detLadger)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setMaximumSize(QSize(16777215, 40))
        self.pushButton.setText(u"PushButton")
        self.detLadgerLayout.addWidget(self.pushButton)
        
        self.wgt_DetailFunc.addWidget(self.detLadger)
        
        self.rightBarLayout.addWidget(self.wgt_DetailFunc)
        self.splitter.addWidget(self.RightBar)
        
        # 设置分割器比例
        self.splitter.setSizes([200, 600, 250])
        
        self.contentLayout.addWidget(self.splitter, 1)
        # contentContainer 将在 setupUi 中添加至 verticalLayout_2
        
    def add_new_tab(self, title=u"新标签页"):
        """添加新标签页"""
        new_page = QWidget()
        new_page.setObjectName(u"tabPage_{}".format(self.tabWidget.count()))
        
        layout = QVBoxLayout(new_page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        label = QLabel(new_page)
        label.setText(u"这是 {} 的内容区域".format(title))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        index = self.tabWidget.addTab(new_page, title)
        self.tabWidget.setCurrentIndex(index)
        
    def retranslateUi(self, MainWindow):
        """翻译UI文本"""
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OpenFina - 财务管理系统", None))
        
    def apply_chrome_styles(self, MainWindow):
        """应用 Chrome 风格样式（可选调用）"""
        MainWindow.setStyleSheet(u"""
            /* 窗口背景 */
            #ChromeStyleMainWindow {
                background-color: #f5f5f5;
            }
            
            /* 标题栏 */
            #titleBar {
                background-color: #dee1e6;
                border-bottom: 1px solid #c6cacf;
            }
            
            /* 窗口控制按钮 */
            #btn_close {
                background-color: #ff5f56;
                border: 1px solid #e0443e;
                border-radius: 6px;
            }
            #btn_min {
                background-color: #ffbd2e;
                border: 1px solid #dea123;
                border-radius: 6px;
            }
            #btn_max {
                background-color: #27c93f;
                border: 1px solid #1aab29;
                border-radius: 6px;
            }
            
            /* 标签页样式 */
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #dee1e6;
                border: none;
                border-radius: 8px 8px 0 0;
                padding: 8px 16px;
                margin-right: 2px;
                min-width: 120px;
                color: #5f6368;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #202124;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e8eaed;
            }
            
            /* 导航工具栏 */
            #navToolbar {
                background-color: #ffffff;
                border-bottom: 1px solid #dadce0;
            }
            
            /* 导航按钮 */
            #btn_back, #btn_forward, #btn_refresh {
                background-color: transparent;
                border: none;
                color: #5f6368;
                font-size: 14px;
            }
            #btn_back:hover:enabled, #btn_forward:hover:enabled, #btn_refresh:hover {
                background-color: #e8eaed;
                border-radius: 16px;
            }
            #btn_back:disabled, #btn_forward:disabled {
                color: #dadce0;
            }
            
            /* 地址栏 */
            #addressBar {
                background-color: #f1f3f4;
                border: 1px solid transparent;
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 14px;
                color: #202124;
            }
            #addressBar:focus {
                background-color: #ffffff;
                border-color: #4285f4;
            }
            
            /* 左侧边栏 */
            #leftBar {
                background-color: #ffffff;
                border-right: 1px solid #dadce0;
            }
            #leftBar QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                color: #3c4043;
                font-size: 13px;
                padding: 8px 12px;
                text-align: left;
            }
            #leftBar QPushButton:hover {
                background-color: #e8eaed;
            }
            
            /* 主内容区 */
            #MainWidget {
                background-color: #ffffff;
            }
            
            /* 子功能按钮 */
            #ladgerWidget QPushButton, #detCertificate QPushButton {
                background-color: rgb(255, 255, 255);
                border: none;
                text-align: left;
                padding-left: 12px;
            }
            #ladgerWidget QPushButton:hover, #detCertificate QPushButton:hover {
                background-color: rgb(241, 241, 241);
            }
            #ladgerWidget QPushButton:pressed, #detCertificate QPushButton:pressed {
                background-color: rgb(230, 230, 230);
            }
            
            /* 右侧详情面板 */
            #RightBar {
                background-color: #f8f9fa;
                border-left: 1px solid #dadce0;
            }
            
            /* 分割器 */
            QSplitter::handle {
                background-color: #dadce0;
            }
            QSplitter::handle:hover {
                background-color: #4285f4;
            }
        """)


# 兼容性别名
ChromeStyleMainWindow = Ui_MainWindow


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 测试：使用多重继承方式
    class TestWindow(QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.apply_chrome_styles(self)
            
    window = TestWindow()
    window.show()
    sys.exit(app.exec())