# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(203, 169)
        Form.setWindowOpacity(0.900000000000000)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 40, 54, 16))
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setStyleSheet(u"color: rgb(85, 170, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 80, 54, 16))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username = QLineEdit(Form)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(70, 40, 113, 20))
        self.password = QLineEdit(Form)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(70, 80, 113, 20))
        self.login = QPushButton(Form)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(20, 130, 83, 26))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8d26\u53f7", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801", None))
        self.username.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u8d26\u53f7", None))
        self.password.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
        self.login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
    # retranslateUi

