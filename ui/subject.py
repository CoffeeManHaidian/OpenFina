from PySide6.QtWidgets import (QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QApplication)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor


class SubjectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("会计科目")
        self.resize(800, 600)

        mainLayout = QVBoxLayout(self)

        ## 科目
        self.topBox = QWidget()
        topLayout = QHBoxLayout(self.topBox)
        self.btnProperty = QPushButton("资产")
        self.btnProperty = QPushButton("负债")
        self.btnProperty = QPushButton("权益")
        self.btnProperty = QPushButton("成本")
        self.btnProperty = QPushButton("损益")


        ## 子细目
        self.subStack = QStackedWidget()


        self.subStack.addWidget()
        
        mainLayout.addWidget(self.topBox)
        mainLayout.addWidget(self.subStack)
        self.setLayout(mainLayout)


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow()

    window.show()
    app.exec()