from PySide6.QtWidgets import (QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QApplication)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QColor


class SubjectWindow(QWidget):
    subFunc = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("会计科目")
        self.resize(800, 600)

        mainLayout = QVBoxLayout(self)

        ## 科目
        self.topBox = QWidget()
        topLayout = QHBoxLayout(self.topBox)
        self.btnProperty = QPushButton("资产")
        self.btnLiabity = QPushButton("负债")
        self.btnEquity = QPushButton("权益")
        self.btnCost = QPushButton("成本")
        self.btnProfit = QPushButton("损益")
        topLayout.addWidget(self.btnProperty)
        topLayout.addWidget(self.btnLiabity)
        topLayout.addWidget(self.btnEquity)
        topLayout.addWidget(self.btnCost)
        topLayout.addWidget(self.btnProfit)

        ## 子细目     
        # 资产
        self.propertyWidget = QWidget()
        propertyLayout = QVBoxLayout(self.propertyWidget)

        # 负债
        self.liabityWidget = QWidget()
        liabityLayout = QVBoxLayout(self.liabityWidget)

        # 权益
        self.equityWidget = QWidget()
        equityLayout = QVBoxLayout(self.equityWidget)

        # 成本
        self.costWidget = QWidget()
        costLayout = QVBoxLayout(self.costWidget)

        # 损益
        self.profitWidget = QWidget()
        profitLayout = QVBoxLayout(self.profitWidget)

        self.subStack = QStackedWidget()
        self.subStack.addWidget(self.propertyWidget)
        self.subStack.addWidget(self.liabityWidget)
        self.subStack.addWidget(self.equityWidget)
        self.subStack.addWidget(self.costWidget)
        self.subStack.addWidget(self.profitWidget)
        
        mainLayout.addWidget(self.topBox)
        mainLayout.addWidget(self.subStack)
        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        self.btnProperty.clicked.connect(lambda: self.goto_subFunc_page(0))
        self.btnLiabity.clicked.connect(lambda: self.goto_subFunc_page(1))
        self.btnEquity.clicked.connect(lambda: self.goto_subFunc_page(2))
        self.btnCost.clicked.connect(lambda: self.goto_subFunc_page(3))
        self.btnProfit.clicked.connect(lambda: self.goto_subFunc_page(4))

    def goto_subFunc_page(self, number):
        """切换子功能窗口页面"""
        self.subStack.setCurrentIndex(number)


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow()

    window.show()
    app.exec()