import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QComboBox, QDateTimeEdit,
    QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QLineEdit)
from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QColor

from ui.subject import SubjectWindow


class FilterWidget(QWidget):
    filer_info = Signal(list)

    def __init__(self):
        super().__init__()

        self.subjectSelector = SubjectWindow() 

        self.setupUi()
        self.init_slot()

    def setupUi(self):
        """界面设计"""
        self.setWindowTitle("筛选条件")
        self.resize(400, 400)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        # mainLayout.setContentsMargins(0,0,0,0)

        current_date = QDateTime.currentDateTime()
        # 标题
        title = QLabel("条件")
        
        # 筛选条件
        self.conditionWidget = QWidget()
        conditionLayout = QVBoxLayout(self.conditionWidget)
        ## 会计期间
        periodSLayout = QHBoxLayout()
        startLb = QLabel("会计期间: ")
        self.yearSSpin = QDateTimeEdit()
        self.yearSSpin.setDisplayFormat("yyyy")
        self.yearSSpin.setDateTime(current_date)
        # self.yearSSpin.setReadOnly(True)
        self.monthSSpin = QDateTimeEdit()
        self.monthSSpin.setDisplayFormat("MM")
        self.monthSSpin.setDateTime(current_date)
        # self.monthSSpin.setReadOnly(True)
        ## 至
        periodELayout = QHBoxLayout()
        endLb = QLabel("至: ")
        self.yearESpin = QDateTimeEdit()
        self.yearESpin.setDisplayFormat("yyyy")
        self.yearESpin.setDateTime(current_date)
        # self.yearESpin.setReadOnly(True)
        self.monthESpin = QDateTimeEdit()
        self.monthESpin.setDisplayFormat("MM")
        self.monthESpin.setDateTime(current_date)
        # self.monthESpin.setReadOnly(True)

        # 科目代码
        self.subjectWidget = QWidget()
        subjectLayout = QVBoxLayout(self.subjectWidget)
        ## 科目代码
        subline1Layout = QHBoxLayout()
        subjectLb = QLabel("科目代码: ")
        self.subjectLine = QLineEdit()
        self.subjectBtn = QPushButton()
        ## 至
        subline2Layout = QHBoxLayout()
        untilLb = QLabel("至: ")
        self.untilLine = QLineEdit()
        self.untilBtn = QPushButton()
        ## 科目级别
        subline3Layout = QHBoxLayout()
        levelLb = QLabel("科目级别: ")
        self.levelCombo = QComboBox()
        self.levelCombo.addItems(str(i+1) for i in range(2))

        # 控件
        self.buttomWidget = QWidget()
        buttomLayout = QHBoxLayout(self.buttomWidget)
        self.confirmBtn = QPushButton("确认")
        self.cancelBtn = QPushButton("取消")
        
        # 布局
        ## 筛选条件布局
        ### 会计期间开始
        periodSLayout.addWidget(startLb)
        periodSLayout.addWidget(self.yearSSpin)
        periodSLayout.addWidget(self.monthSSpin)
        ### 会计期间结束
        periodELayout.addWidget(endLb)
        periodELayout.addWidget(self.yearESpin)
        periodELayout.addWidget(self.monthESpin)
        ### 会计期间
        conditionLayout.addLayout(periodSLayout)
        conditionLayout.addLayout(periodELayout)
        ## 科目布局
        ### 科目代码布局
        subline1Layout.addWidget(subjectLb)
        subline1Layout.addWidget(self.subjectLine)
        subline1Layout.addWidget(self.subjectBtn)
        ### 至布局
        subline2Layout.addWidget(untilLb)
        subline2Layout.addWidget(self.untilLine)
        subline2Layout.addWidget(self.untilBtn)
        ### 科目级别布局
        subline3Layout.addWidget(levelLb)
        subline3Layout.addWidget(self.levelCombo)

        subjectLayout.addLayout(subline1Layout)
        subjectLayout.addLayout(subline2Layout)
        subjectLayout.addLayout(subline3Layout)
        ## 控件布局
        buttomLayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        buttomLayout.addWidget(self.confirmBtn)
        buttomLayout.addWidget(self.cancelBtn)
        ## 主布局
        mainLayout.addWidget(title)
        mainLayout.addWidget(self.conditionWidget)
        mainLayout.addWidget(self.subjectWidget)
        mainLayout.addSpacerItem(QSpacerItem(100, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        mainLayout.addWidget(self.buttomWidget)
        self.setLayout(mainLayout)

    def setStyle(self):
        """界面设置"""

    def init_slot(self):
        """绑定信号与槽"""
        self.cancelBtn.clicked.connect(self.close)
        self.confirmBtn.clicked.connect(self.on_confirmBtn_clicked)

        self.subjectBtn.clicked.connect(self.on_subjectBtn_clicked)
        self.untilBtn.clicked.connect(self.on_untilBtn_clicked)

    def on_confirmBtn_clicked(self):
        """发送筛选信息"""
        info = []
        # 会计期间开始（年份和月份）
        start_year = self.yearSSpin.dateTime().toString("yyyy")
        start_month = self.monthSSpin.dateTime().toString("MM")
        # 会计期间结束（年份和月份）
        end_year = self.yearESpin.dateTime().toString("yyyy")
        end_month = self.monthESpin.dateTime().toString("MM")
        # 科目代码
        subject_code = self.subjectLine.text()
        until_code = self.untilLine.text()
        # 科目级别
        level = self.levelCombo.currentText()

        info = [
            start_year,      # 0: 开始年份
            start_month,     # 1: 开始月份
            end_year,        # 2: 结束年份
            end_month,       # 3: 结束月份
            subject_code,    # 4: 科目代码开始
            until_code,      # 5: 科目代码结束
            level            # 6: 科目级别
        ]
        self.filer_info.emit(info)
        self.close()

    def on_subjectBtn_clicked(self):
        """弹出科目开始代码选择窗口"""
        self.show_subject_selector(self.subjectLine)

    def on_untilBtn_clicked(self):
        """弹出科目结束代码选择窗口"""
        self.show_subject_selector(self.untilLine)

    def show_subject_selector(self, target_line):
        """显示科目选择窗口"""
        # 如果窗口已打开，则置顶并激活
        if self.subjectSelector.isVisible():
            self.subjectSelector.raise_()
            self.subjectSelector.activateWindow()
        else:
            self.subjectSelector.show()
        
        # 断开之前可能存在的连接，避免重复连接
        try:
            self.subjectSelector.subFunc.disconnect()
        except:
            pass
        
        # 连接信号到目标输入框
        self.subjectSelector.subFunc.connect(
            lambda code, name, line=target_line: self.set_subject_line(code, name, line)
        )

    def set_subject_line(self, code, name, target_line):
        """设置科目代码到指定的输入框"""
        subject_info = f"{code} {name}"
        target_line.setText(subject_info)


if __name__ == "__main__":
    app = QApplication([])
    window = FilterWidget()

    window.show()
    app.exec()
