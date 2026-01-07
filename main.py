from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                                QListWidgetItem)
from ui.Ui_mainwindow import Ui_MainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import Qt, QIcon
from PySide6.QtCore import QSize

from InputWindow import InputWindow
from ui.certificate import Certification

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # 设置窗口无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 使能模拟边框按钮功能
        self.redefine_window_border_btn()
        # 初始化槽函数
        self.init_solt()

    def btn_max_clicked(self):
        """
        最大化窗口
        return:
        """

        if self.isMaximized():
            self.showNormal()
            icon = QIcon()
            icon.addFile(u":/tittle/icons/maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
            self.btn_max.setIcon(icon)
            self.btn_max.setIconSize(QSize(10,10))
            # 改变最大化窗口圆角
            self.widget.setStyleSheet(u"#widget{\n"
"	background-color: rgb(243, 243, 243);\n"
"	border-radius: 10px;\n"
"}")
        else:
            self.showMaximized()  
            # 改变最大化按钮图标
            icon = QIcon()
            icon.addFile(u":/tittle/icons/reduction.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)  
            self.btn_max.setIcon(icon)
            self.btn_max.setIconSize(QSize(10,10))
            # 改变最大化窗口圆角
            self.widget.setStyleSheet(u"#widget{\n"
"	background-color: rgb(243, 243, 243);\n"
"	border-radius: 0px;\n"
"}")

    def double_clicked_border_bar(self, event):
        """
        双击顶部标题条,使其在最大化和还原之间切换
        param event:
        return:
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.resize_maximize()      

    def move_title_bar(self, event):
        """
        拖动顶部标题条
        param event:
        return:
        """
        self.windowHandle().startSystemMove() 

    def redefine_window_border_btn(self):
        """
        使模拟边框的3个按钮生效(关闭、最小化、最大化、双击标题框)
        return:
        """
        self.btn_close.clicked.connect(self.close)  # 关闭按钮
        self.btn_min.clicked.connect(self.showMinimized)  # 最小化按钮
        self.btn_max.clicked.connect(self.btn_max_clicked)  # 最大化按钮
        # 设置可拖动（通过拖动窗口上的横条来达到拖动窗口的效果）
        self.TittleBar.mouseDoubleClickEvent = self.double_clicked_border_bar
        self.TittleBar.mouseMoveEvent = self.move_title_bar
    
    def init_solt(self):
        """
        初始化槽函数
        """
        self.Ladger.clicked.connect(lambda:self.goto_subfunc_page(1))
        self.Report.clicked.connect(lambda:self.goto_subfunc_page(2))

        self.btn_certification.clicked.connect(lambda:self.goto_detailfunc_page(1))
        self.btn_ledger.clicked.connect(lambda:self.goto_detailfunc_page(2))

        self.btn_input.clicked.connect(self.input_button_clicked)

    def goto_subfunc_page(self, number):
        """
        切换子功能窗口页面
        param number:
        return:
        """
        self.wgt_SubFunc.setCurrentIndex(number)

    def goto_detailfunc_page(self, number):
        """
        切换明细功能窗口页面
        param number:
        return:
        """
        self.wgt_DetailFunc.setCurrentIndex(number)

    def input_button_clicked(self):
        """
        打开凭证录入窗口
        """
        # 如果窗口已打开，则置顶并激活
        if hasattr(self, "inputWindow") and self.inputWindow.isVisible():
            self.inputWindow.raise_()
            self.inputWindow.activateWindow()

        self.inputWindow = Certification()
        self.inputWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    mainwindow = MyWindow()

    mainwindow.show()
    app.exec()