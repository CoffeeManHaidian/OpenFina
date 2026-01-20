# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(903, 600)
        MainWindow.setMinimumSize(QSize(900, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#centralwidget{\n"
"	border-radius: 20px;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.TittleBar = QWidget(self.widget)
        self.TittleBar.setObjectName(u"TittleBar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TittleBar.sizePolicy().hasHeightForWidth())
        self.TittleBar.setSizePolicy(sizePolicy)
        self.TittleBar.setMinimumSize(QSize(0, 40))
        self.TittleBar.setMaximumSize(QSize(16777215, 40))
        self.TittleBar.setStyleSheet(u"#TopBar{\n"
"	background-color: rgb(243, 243, 243);\n"
"	border-top-left-radius: 15px;\n"
"	border-top-right-radius: 15px;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.TittleBar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.TittleBar)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(70, 0))
        self.label.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(680, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame = QFrame(self.TittleBar)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(150, 0))
        self.frame.setMaximumSize(QSize(100, 16777215))
        self.frame.setStyleSheet(u"QFrame{\n"
"	border: none;\n"
"}")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_min = QPushButton(self.frame)
        self.btn_min.setObjectName(u"btn_min")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.btn_min.sizePolicy().hasHeightForWidth())
        self.btn_min.setSizePolicy(sizePolicy1)
        self.btn_min.setMinimumSize(QSize(16, 16))
        self.btn_min.setStyleSheet(u"#btn_min{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton{\n"
"	border: none;\n"
"}\n"
"QPushButton:hover{		\n"
"	background-color: rgba(221, 221, 221, 1);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgba(221, 221, 221, 0.8);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/tittle/icons/minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_min.setIcon(icon)
        self.btn_min.setIconSize(QSize(10, 10))

        self.horizontalLayout_2.addWidget(self.btn_min)

        self.btn_max = QPushButton(self.frame)
        self.btn_max.setObjectName(u"btn_max")
        sizePolicy1.setHeightForWidth(self.btn_max.sizePolicy().hasHeightForWidth())
        self.btn_max.setSizePolicy(sizePolicy1)
        self.btn_max.setMinimumSize(QSize(16, 16))
        self.btn_max.setStyleSheet(u"#btn_max{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton{\n"
"	border: none;\n"
"}\n"
"QPushButton:hover{		\n"
"	background-color: rgba(221, 221, 221, 1);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgba(221, 221, 221, 0.8);\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	qproperty-icon: url(:/tittle/icons/reduction.png);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/tittle/icons/maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_max.setIcon(icon1)
        self.btn_max.setIconSize(QSize(10, 10))

        self.horizontalLayout_2.addWidget(self.btn_max)

        self.btn_close = QPushButton(self.frame)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QSize(16, 16))
        self.btn_close.setStyleSheet(u"#btn_close{\n"
"	color: rgb(0, 0, 0);\n"
"	border-top-right-radius: 10px;\n"
"}\n"
"QPushButton{\n"
"	border: none;\n"
"}\n"
"QPushButton:hover{		\n"
"	background-color: rgb(232, 17, 35);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgba(232, 17, 35, 0.8);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/tittle/icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_close.setIcon(icon2)
        self.btn_close.setIconSize(QSize(10, 10))

        self.horizontalLayout_2.addWidget(self.btn_close)


        self.horizontalLayout.addWidget(self.frame)


        self.verticalLayout_2.addWidget(self.TittleBar)

        self.MainWidget = QWidget(self.widget)
        self.MainWidget.setObjectName(u"MainWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(19)
        sizePolicy2.setHeightForWidth(self.MainWidget.sizePolicy().hasHeightForWidth())
        self.MainWidget.setSizePolicy(sizePolicy2)
        self.MainWidget.setStyleSheet(u"#MainWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-bottom-left-radius: 15px;\n"
"	border-bottom-right-radius: 15px;\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.MainWidget)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.leftBar = QWidget(self.MainWidget)
        self.leftBar.setObjectName(u"leftBar")
        sizePolicy.setHeightForWidth(self.leftBar.sizePolicy().hasHeightForWidth())
        self.leftBar.setSizePolicy(sizePolicy)
        self.leftBar.setMaximumSize(QSize(100, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.leftBar)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.Ladger = QPushButton(self.leftBar)
        self.Ladger.setObjectName(u"Ladger")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.Ladger.sizePolicy().hasHeightForWidth())
        self.Ladger.setSizePolicy(sizePolicy3)
        self.Ladger.setMinimumSize(QSize(0, 0))
        self.Ladger.setStyleSheet(u"#Ladger{\n"
"	color: rgb(0, 0, 0);\n"
"	\n"
"	font: 9pt \"Microsoft YaHei UI\";\n"
"}\n"
"/*QPushButton{\n"
"	border: none;\n"
"}*/\n"
"QPushButton:pressed{\n"
"	padding-bottom: 5px;\n"
"}")

        self.verticalLayout_3.addWidget(self.Ladger)

        self.Report = QPushButton(self.leftBar)
        self.Report.setObjectName(u"Report")
        sizePolicy3.setHeightForWidth(self.Report.sizePolicy().hasHeightForWidth())
        self.Report.setSizePolicy(sizePolicy3)
        self.Report.setStyleSheet(u"#Report{\n"
"	color: rgb(0, 0, 0);\n"
"	\n"
"	font: 9pt \"Microsoft YaHei UI\";\n"
"}\n"
"/*QPushButton{\n"
"	border: none;\n"
"}*/\n"
"QPushButton:pressed{\n"
"	padding-bottom: 5px;\n"
"}")

        self.verticalLayout_3.addWidget(self.Report)

        self.Funds = QPushButton(self.leftBar)
        self.Funds.setObjectName(u"Funds")
        sizePolicy3.setHeightForWidth(self.Funds.sizePolicy().hasHeightForWidth())
        self.Funds.setSizePolicy(sizePolicy3)
        self.Funds.setStyleSheet(u"#Funds{\n"
"	color: rgb(0, 0, 0);\n"
"	\n"
"	font: 9pt \"Microsoft YaHei UI\";\n"
"}\n"
"/*QPushButton{\n"
"	border: none;\n"
"}*/\n"
"QPushButton:pressed{\n"
"	padding-bottom: 5px;\n"
"}")

        self.verticalLayout_3.addWidget(self.Funds)


        self.horizontalLayout_3.addWidget(self.leftBar)

        self.contentBox = QWidget(self.MainWidget)
        self.contentBox.setObjectName(u"contentBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.contentBox.sizePolicy().hasHeightForWidth())
        self.contentBox.setSizePolicy(sizePolicy4)
        self.contentBox.setMinimumSize(QSize(400, 0))
        self.verticalLayout_6 = QVBoxLayout(self.contentBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lb_Sub = QLabel(self.contentBox)
        self.lb_Sub.setObjectName(u"lb_Sub")
        self.lb_Sub.setMinimumSize(QSize(0, 20))
        self.lb_Sub.setMaximumSize(QSize(16777215, 20))
        self.lb_Sub.setStyleSheet(u"font: 7pt \"Microsoft YaHei UI\";")

        self.verticalLayout_6.addWidget(self.lb_Sub)

        self.wgt_SubFunc = QStackedWidget(self.contentBox)
        self.wgt_SubFunc.setObjectName(u"wgt_SubFunc")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(2)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.wgt_SubFunc.sizePolicy().hasHeightForWidth())
        self.wgt_SubFunc.setSizePolicy(sizePolicy5)
        self.wgt_SubFunc.setMinimumSize(QSize(400, 0))
        self.wgt_SubFunc.setMaximumSize(QSize(16777215, 16777215))
        self.wgt_SubFunc.setStyleSheet(u"#subHome{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.subHome = QWidget()
        self.subHome.setObjectName(u"subHome")
        self.subHome.setMaximumSize(QSize(16777215, 500))
        self.subHome.setStyleSheet(u"#homeWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.wgt_SubFunc.addWidget(self.subHome)
        self.ladgerWidget = QWidget()
        self.ladgerWidget.setObjectName(u"ladgerWidget")
        self.ladgerWidget.setMaximumSize(QSize(16777215, 260))
        self.ladgerWidget.setStyleSheet(u"#ladgerWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.ladgerWidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_certification = QPushButton(self.ladgerWidget)
        self.btn_certification.setObjectName(u"btn_certification")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btn_certification.sizePolicy().hasHeightForWidth())
        self.btn_certification.setSizePolicy(sizePolicy6)
        self.btn_certification.setMinimumSize(QSize(0, 40))
        self.btn_certification.setMaximumSize(QSize(16777215, 40))
        self.btn_certification.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/tittle/icons/folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_certification.setIcon(icon3)
        self.btn_certification.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.btn_certification)

        self.btn_ledger = QPushButton(self.ladgerWidget)
        self.btn_ledger.setObjectName(u"btn_ledger")
        sizePolicy6.setHeightForWidth(self.btn_ledger.sizePolicy().hasHeightForWidth())
        self.btn_ledger.setSizePolicy(sizePolicy6)
        self.btn_ledger.setMinimumSize(QSize(0, 40))
        self.btn_ledger.setMaximumSize(QSize(16777215, 40))
        self.btn_ledger.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_ledger.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.btn_ledger)

        self.btn_report = QPushButton(self.ladgerWidget)
        self.btn_report.setObjectName(u"btn_report")
        sizePolicy6.setHeightForWidth(self.btn_report.sizePolicy().hasHeightForWidth())
        self.btn_report.setSizePolicy(sizePolicy6)
        self.btn_report.setMinimumSize(QSize(0, 40))
        self.btn_report.setMaximumSize(QSize(16777215, 40))
        self.btn_report.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_report.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.btn_report)

        self.btn_cash = QPushButton(self.ladgerWidget)
        self.btn_cash.setObjectName(u"btn_cash")
        sizePolicy6.setHeightForWidth(self.btn_cash.sizePolicy().hasHeightForWidth())
        self.btn_cash.setSizePolicy(sizePolicy6)
        self.btn_cash.setMinimumSize(QSize(0, 40))
        self.btn_cash.setMaximumSize(QSize(16777215, 40))
        self.btn_cash.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_cash.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.btn_cash)

        self.btn_bill = QPushButton(self.ladgerWidget)
        self.btn_bill.setObjectName(u"btn_bill")
        sizePolicy6.setHeightForWidth(self.btn_bill.sizePolicy().hasHeightForWidth())
        self.btn_bill.setSizePolicy(sizePolicy6)
        self.btn_bill.setMinimumSize(QSize(0, 40))
        self.btn_bill.setMaximumSize(QSize(16777215, 40))
        self.btn_bill.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_bill.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.btn_bill)

        self.btn_transaction = QPushButton(self.ladgerWidget)
        self.btn_transaction.setObjectName(u"btn_transaction")
        sizePolicy6.setHeightForWidth(self.btn_transaction.sizePolicy().hasHeightForWidth())
        self.btn_transaction.setSizePolicy(sizePolicy6)
        self.btn_transaction.setMinimumSize(QSize(0, 40))
        self.btn_transaction.setMaximumSize(QSize(16777215, 40))
        self.btn_transaction.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_transaction.setIcon(icon3)

        self.verticalLayout_4.addWidget(self.btn_transaction)

        self.wgt_SubFunc.addWidget(self.ladgerWidget)
        self.reportWidget = QWidget()
        self.reportWidget.setObjectName(u"reportWidget")
        self.lineEdit_2 = QLineEdit(self.reportWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(160, 230, 200, 100))
        self.lineEdit_2.setMinimumSize(QSize(200, 100))
        self.lineEdit_2.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")
        self.wgt_SubFunc.addWidget(self.reportWidget)

        self.verticalLayout_6.addWidget(self.wgt_SubFunc)


        self.horizontalLayout_3.addWidget(self.contentBox)

        self.RightBar = QWidget(self.MainWidget)
        self.RightBar.setObjectName(u"RightBar")
        sizePolicy4.setHeightForWidth(self.RightBar.sizePolicy().hasHeightForWidth())
        self.RightBar.setSizePolicy(sizePolicy4)
        self.RightBar.setMinimumSize(QSize(400, 0))
        self.RightBar.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.RightBar)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lb_Detail = QLabel(self.RightBar)
        self.lb_Detail.setObjectName(u"lb_Detail")
        self.lb_Detail.setMinimumSize(QSize(0, 20))
        self.lb_Detail.setMaximumSize(QSize(16777215, 20))
        self.lb_Detail.setStyleSheet(u"font: 7pt \"Microsoft YaHei UI\";")

        self.verticalLayout_5.addWidget(self.lb_Detail)

        self.wgt_DetailFunc = QStackedWidget(self.RightBar)
        self.wgt_DetailFunc.setObjectName(u"wgt_DetailFunc")
        self.wgt_DetailFunc.setStyleSheet(u"#detailHome{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.detailHome = QWidget()
        self.detailHome.setObjectName(u"detailHome")
        self.widget_2 = QWidget(self.detailHome)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(90, 140, 120, 80))
        self.wgt_DetailFunc.addWidget(self.detailHome)
        self.detCertificate = QWidget()
        self.detCertificate.setObjectName(u"detCertificate")
        self.detCertificate.setMinimumSize(QSize(0, 240))
        self.detCertificate.setMaximumSize(QSize(16777215, 320))
        self.verticalLayout_7 = QVBoxLayout(self.detCertificate)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.inputBtn = QPushButton(self.detCertificate)
        self.inputBtn.setObjectName(u"inputBtn")
        self.inputBtn.setMinimumSize(QSize(0, 40))
        self.inputBtn.setMaximumSize(QSize(16777215, 40))
        self.inputBtn.setStyleSheet(u"#btn_input{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/tittle/icons/excel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.inputBtn.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.inputBtn)

        self.queryBtn = QPushButton(self.detCertificate)
        self.queryBtn.setObjectName(u"queryBtn")
        self.queryBtn.setMinimumSize(QSize(0, 40))
        self.queryBtn.setMaximumSize(QSize(16777215, 40))
        self.queryBtn.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.queryBtn.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.queryBtn)

        self.postBtn = QPushButton(self.detCertificate)
        self.postBtn.setObjectName(u"postBtn")
        self.postBtn.setMinimumSize(QSize(0, 40))
        self.postBtn.setMaximumSize(QSize(16777215, 40))
        self.postBtn.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.postBtn.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.postBtn)

        self.summaryBtn = QPushButton(self.detCertificate)
        self.summaryBtn.setObjectName(u"summaryBtn")
        self.summaryBtn.setMinimumSize(QSize(0, 40))
        self.summaryBtn.setMaximumSize(QSize(16777215, 40))
        self.summaryBtn.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.summaryBtn.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.summaryBtn)

        self.btn_mode = QPushButton(self.detCertificate)
        self.btn_mode.setObjectName(u"btn_mode")
        self.btn_mode.setMinimumSize(QSize(0, 40))
        self.btn_mode.setMaximumSize(QSize(16777215, 40))
        self.btn_mode.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_mode.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.btn_mode)

        self.btn_review = QPushButton(self.detCertificate)
        self.btn_review.setObjectName(u"btn_review")
        self.btn_review.setMinimumSize(QSize(0, 40))
        self.btn_review.setMaximumSize(QSize(16777215, 40))
        self.btn_review.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_review.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.btn_review)

        self.btn_introduce = QPushButton(self.detCertificate)
        self.btn_introduce.setObjectName(u"btn_introduce")
        self.btn_introduce.setMinimumSize(QSize(0, 40))
        self.btn_introduce.setMaximumSize(QSize(16777215, 40))
        self.btn_introduce.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_introduce.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.btn_introduce)

        self.btn_out = QPushButton(self.detCertificate)
        self.btn_out.setObjectName(u"btn_out")
        self.btn_out.setMinimumSize(QSize(0, 40))
        self.btn_out.setMaximumSize(QSize(16777215, 40))
        self.btn_out.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")
        self.btn_out.setIcon(icon4)

        self.verticalLayout_7.addWidget(self.btn_out)

        self.wgt_DetailFunc.addWidget(self.detCertificate)
        self.detLadger = QWidget()
        self.detLadger.setObjectName(u"detLadger")
        self.detLadger.setMinimumSize(QSize(0, 40))
        self.detLadger.setMaximumSize(QSize(16777215, 40))
        self.verticalLayout_8 = QVBoxLayout(self.detLadger)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.detLadger)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setMaximumSize(QSize(16777215, 40))
        self.pushButton.setStyleSheet(u"QPushButton{	\n"
"	background-color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:pressed{	\n"
"	background-color: rgb(241, 241, 241);\n"
"}")

        self.verticalLayout_8.addWidget(self.pushButton)

        self.wgt_DetailFunc.addWidget(self.detLadger)

        self.verticalLayout_5.addWidget(self.wgt_DetailFunc)


        self.horizontalLayout_3.addWidget(self.RightBar)


        self.verticalLayout_2.addWidget(self.MainWidget)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.wgt_SubFunc.setCurrentIndex(0)
        self.wgt_DetailFunc.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u63a7\u5236\u53f0", None))
        self.btn_min.setText("")
        self.btn_max.setText("")
        self.btn_close.setText("")
        self.Ladger.setText(QCoreApplication.translate("MainWindow", u"\u603b\u8d26", None))
        self.Report.setText(QCoreApplication.translate("MainWindow", u"\u62a5\u8868", None))
        self.Funds.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u91d1\u7ba1\u7406", None))
        self.lb_Sub.setText(QCoreApplication.translate("MainWindow", u"\u5b50\u529f\u80fd", None))
        self.btn_certification.setText(QCoreApplication.translate("MainWindow", u" \u51ed\u8bc1\u5904\u7406", None))
        self.btn_ledger.setText(QCoreApplication.translate("MainWindow", u" \u8d26\u7c3f", None))
        self.btn_report.setText(QCoreApplication.translate("MainWindow", u" \u8d22\u52a1\u62a5\u8868", None))
        self.btn_cash.setText(QCoreApplication.translate("MainWindow", u" \u73b0\u91d1\u6d41\u91cf", None))
        self.btn_bill.setText(QCoreApplication.translate("MainWindow", u" \u7ed3\u8d26", None))
        self.btn_transaction.setText(QCoreApplication.translate("MainWindow", u" \u5f80\u6765", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"\u8fd9\u662f\u62a5\u8868", None))
        self.lb_Detail.setText(QCoreApplication.translate("MainWindow", u"\u660e\u7ec6\u529f\u80fd", None))
        self.inputBtn.setText(QCoreApplication.translate("MainWindow", u"01001 \u51ed\u8bc1\u5f55\u5165", None))
        self.queryBtn.setText(QCoreApplication.translate("MainWindow", u"01002 \u51ed\u8bc1\u67e5\u8be2", None))
        self.postBtn.setText(QCoreApplication.translate("MainWindow", u"01003 \u51ed\u8bc1\u8fc7\u8d26", None))
        self.summaryBtn.setText(QCoreApplication.translate("MainWindow", u"01004 \u51ed\u8bc1\u6c47\u603b", None))
        self.btn_mode.setText(QCoreApplication.translate("MainWindow", u"01005 \u6a21\u5f0f\u51ed\u8bc1", None))
        self.btn_review.setText(QCoreApplication.translate("MainWindow", u"01006 \u53cc\u6572\u5ba1\u6838", None))
        self.btn_introduce.setText(QCoreApplication.translate("MainWindow", u"01007 \u6807\u51c6\u51ed\u8bc1\u5f15\u5165", None))
        self.btn_out.setText(QCoreApplication.translate("MainWindow", u"01008 \u6807\u51c6\u51ed\u8bc1\u5f15\u51fa", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

