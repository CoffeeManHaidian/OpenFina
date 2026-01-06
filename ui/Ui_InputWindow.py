# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InputWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_InuputWindow(object):
    def setupUi(self, InuputWindow):
        if not InuputWindow.objectName():
            InuputWindow.setObjectName(u"InuputWindow")
        InuputWindow.resize(667, 406)
        self.horizontalLayout = QHBoxLayout(InuputWindow)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.contentBox = QWidget(InuputWindow)
        self.contentBox.setObjectName(u"contentBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentBox.sizePolicy().hasHeightForWidth())
        self.contentBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.contentBox)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 20))
        self.widget.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_assets = QPushButton(self.widget)
        self.btn_assets.setObjectName(u"btn_assets")

        self.horizontalLayout_2.addWidget(self.btn_assets)

        self.btn_debt = QPushButton(self.widget)
        self.btn_debt.setObjectName(u"btn_debt")

        self.horizontalLayout_2.addWidget(self.btn_debt)

        self.btn_cost = QPushButton(self.widget)
        self.btn_cost.setObjectName(u"btn_cost")

        self.horizontalLayout_2.addWidget(self.btn_cost)

        self.btn_porfitnloss = QPushButton(self.widget)
        self.btn_porfitnloss.setObjectName(u"btn_porfitnloss")

        self.horizontalLayout_2.addWidget(self.btn_porfitnloss)


        self.verticalLayout_2.addWidget(self.widget)

        self.stackedWidget = QStackedWidget(self.contentBox)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.WidgetAsset = QWidget()
        self.WidgetAsset.setObjectName(u"WidgetAsset")
        self.verticalLayout_3 = QVBoxLayout(self.WidgetAsset)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tree_Itemlist = QTreeWidget(self.WidgetAsset)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        __qtreewidgetitem = QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        QTreeWidgetItem(self.tree_Itemlist)
        self.tree_Itemlist.setObjectName(u"tree_Itemlist")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tree_Itemlist.sizePolicy().hasHeightForWidth())
        self.tree_Itemlist.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.tree_Itemlist)

        self.stackedWidget.addWidget(self.WidgetAsset)
        self.WidgetDebt = QWidget()
        self.WidgetDebt.setObjectName(u"WidgetDebt")
        self.verticalLayout_4 = QVBoxLayout(self.WidgetDebt)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.WidgetDebt)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_4.addWidget(self.listWidget)

        self.stackedWidget.addWidget(self.WidgetDebt)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.contentBox)

        self.leftBox = QWidget(InuputWindow)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy2)
        self.leftBox.setMinimumSize(QSize(100, 0))
        self.leftBox.setMaximumSize(QSize(100, 16777215))
        self.leftBox.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QVBoxLayout(self.leftBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_confirm = QPushButton(self.leftBox)
        self.btn_confirm.setObjectName(u"btn_confirm")

        self.verticalLayout.addWidget(self.btn_confirm)

        self.btn_cancel = QPushButton(self.leftBox)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.verticalLayout.addWidget(self.btn_cancel)

        self.verticalSpacer = QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_search = QPushButton(self.leftBox)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setStyleSheet(u"#btn_search{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover{		\n"
"	background-color: rgba(221, 221, 221, 1);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgba(221, 221, 221, 0.8);\n"
"}")

        self.verticalLayout.addWidget(self.btn_search)

        self.btn_new = QPushButton(self.leftBox)
        self.btn_new.setObjectName(u"btn_new")

        self.verticalLayout.addWidget(self.btn_new)

        self.btn_revise = QPushButton(self.leftBox)
        self.btn_revise.setObjectName(u"btn_revise")

        self.verticalLayout.addWidget(self.btn_revise)

        self.btn_delete = QPushButton(self.leftBox)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.btn_copy = QPushButton(self.leftBox)
        self.btn_copy.setObjectName(u"btn_copy")

        self.verticalLayout.addWidget(self.btn_copy)

        self.btn_budget = QPushButton(self.leftBox)
        self.btn_budget.setObjectName(u"btn_budget")

        self.verticalLayout.addWidget(self.btn_budget)

        self.btn_refresh = QPushButton(self.leftBox)
        self.btn_refresh.setObjectName(u"btn_refresh")

        self.verticalLayout.addWidget(self.btn_refresh)


        self.horizontalLayout.addWidget(self.leftBox)


        self.retranslateUi(InuputWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InuputWindow)
    # setupUi

    def retranslateUi(self, InuputWindow):
        InuputWindow.setWindowTitle(QCoreApplication.translate("InuputWindow", u"\u51ed\u8bc1\u5f55\u5165", None))
        self.btn_assets.setText(QCoreApplication.translate("InuputWindow", u"\u8d44\u4ea7", None))
        self.btn_debt.setText(QCoreApplication.translate("InuputWindow", u"\u8d1f\u503a", None))
        self.btn_cost.setText(QCoreApplication.translate("InuputWindow", u"\u6210\u672c", None))
        self.btn_porfitnloss.setText(QCoreApplication.translate("InuputWindow", u"\u635f\u76ca", None))
        ___qtreewidgetitem = self.tree_Itemlist.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("InuputWindow", u"\u8d44\u4ea7", None));

        __sortingEnabled = self.tree_Itemlist.isSortingEnabled()
        self.tree_Itemlist.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_Itemlist.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e93\u5b58\u8d44\u91d1", None));
        ___qtreewidgetitem2 = self.tree_Itemlist.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("InuputWindow", u"\u94f6\u884c\u5b58\u6b3e", None));
        ___qtreewidgetitem3 = self.tree_Itemlist.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u6536\u7968\u636e", None));
        ___qtreewidgetitem4 = self.tree_Itemlist.topLevelItem(3)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u6536\u8d26\u6b3e", None));
        ___qtreewidgetitem5 = self.tree_Itemlist.topLevelItem(4)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("InuputWindow", u"\u574f\u8d26\u51c6\u5907", None));
        ___qtreewidgetitem6 = self.tree_Itemlist.topLevelItem(5)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("InuputWindow", u"\u9884\u4ed8\u8d26\u6b3e", None));
        ___qtreewidgetitem7 = self.tree_Itemlist.topLevelItem(6)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("InuputWindow", u"\u5176\u4ed6\u5e94\u6536\u6b3e", None));
        ___qtreewidgetitem8 = self.tree_Itemlist.topLevelItem(7)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("InuputWindow", u"\u5b58\u8d27", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem8.child(0)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("InuputWindow", u"\u539f\u6750\u6599", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem8.child(1)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("InuputWindow", u"\u4ea7\u6210\u54c1", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem8.child(2)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("InuputWindow", u"\u5305\u88c5\u7269", None));
        ___qtreewidgetitem12 = self.tree_Itemlist.topLevelItem(8)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("InuputWindow", u"\u5f85\u644a\u8d39\u7528", None));
        ___qtreewidgetitem13 = self.tree_Itemlist.topLevelItem(9)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("InuputWindow", u"\u56fa\u5b9a\u8d44\u4ea7", None));
        ___qtreewidgetitem14 = self.tree_Itemlist.topLevelItem(10)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("InuputWindow", u"\u7d2f\u8ba1\u6298\u65e7", None));
        ___qtreewidgetitem15 = self.tree_Itemlist.topLevelItem(11)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("InuputWindow", u"\u77ed\u671f\u501f\u6b3e", None));
        ___qtreewidgetitem16 = self.tree_Itemlist.topLevelItem(12)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u4ed8\u7968\u636e", None));
        ___qtreewidgetitem17 = self.tree_Itemlist.topLevelItem(13)
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u4ed8\u8d26\u6b3e", None));
        ___qtreewidgetitem18 = self.tree_Itemlist.topLevelItem(14)
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("InuputWindow", u"\u9884\u6536\u8d26\u6b3e", None));
        ___qtreewidgetitem19 = self.tree_Itemlist.topLevelItem(15)
        ___qtreewidgetitem19.setText(0, QCoreApplication.translate("InuputWindow", u"\u5176\u4ed6\u5e94\u4ed8\u6b3e", None));
        ___qtreewidgetitem20 = self.tree_Itemlist.topLevelItem(16)
        ___qtreewidgetitem20.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u4ed8\u5de5\u8d44", None));
        ___qtreewidgetitem21 = self.tree_Itemlist.topLevelItem(17)
        ___qtreewidgetitem21.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u4ed8\u798f\u5229\u8d39", None));
        ___qtreewidgetitem22 = self.tree_Itemlist.topLevelItem(18)
        ___qtreewidgetitem22.setText(0, QCoreApplication.translate("InuputWindow", u"\u5e94\u7f34\u7a0e\u91d1", None));
        ___qtreewidgetitem23 = self.tree_Itemlist.topLevelItem(19)
        ___qtreewidgetitem23.setText(0, QCoreApplication.translate("InuputWindow", u"\u9884\u63d0\u8d39\u7528", None));
        ___qtreewidgetitem24 = self.tree_Itemlist.topLevelItem(20)
        ___qtreewidgetitem24.setText(0, QCoreApplication.translate("InuputWindow", u"\u9500\u552e\u6298\u8ba9", None));
        self.tree_Itemlist.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("InuputWindow", u"\u8d1f\u503a", None));
        self.listWidget.setSortingEnabled(__sortingEnabled1)

        self.btn_confirm.setText(QCoreApplication.translate("InuputWindow", u"\u786e\u5b9a", None))
        self.btn_cancel.setText(QCoreApplication.translate("InuputWindow", u"\u53d6\u6d88", None))
        self.btn_search.setText(QCoreApplication.translate("InuputWindow", u"\u67e5\u627e", None))
        self.btn_new.setText(QCoreApplication.translate("InuputWindow", u"\u65b0\u589e", None))
        self.btn_revise.setText(QCoreApplication.translate("InuputWindow", u"\u4fee\u6539", None))
        self.btn_delete.setText(QCoreApplication.translate("InuputWindow", u"\u5220\u9664", None))
        self.btn_copy.setText(QCoreApplication.translate("InuputWindow", u"\u590d\u5236", None))
        self.btn_budget.setText(QCoreApplication.translate("InuputWindow", u"\u9884\u7b97", None))
        self.btn_refresh.setText(QCoreApplication.translate("InuputWindow", u"\u5237\u65b0", None))
    # retranslateUi

