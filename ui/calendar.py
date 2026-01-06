import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QCalendarWidget,
                                QLabel, QDialogButtonBox)
from PySide6.QtCore import Qt, Signal, QDate


class DatePickerDialog(QDialog):
    """日期选择对话框"""
    date_selected = Signal(QDate)  # 日期选择信号
    
    def __init__(self, current_date=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择日期")
        self.resize(350, 300)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 创建日历控件
        self.calendar = QCalendarWidget()
        
        # 设置初始日期
        if current_date:
            self.calendar.setSelectedDate(current_date)
        else:
            self.calendar.setSelectedDate(QDate.currentDate())
        
        # 设置日历样式（可选）
        # self.calendar.setGridVisible(True)
        
        # # 设置日历颜色（可选）
        # palette = self.calendar.palette()
        # palette.setColor(QPalette.Highlight, Qt.blue)  # 选中日期的颜色
        # self.calendar.setPalette(palette)
        
        layout.addWidget(self.calendar)
        
        # 创建按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def accept(self):
        """确认按钮点击事件"""
        selected_date = self.calendar.selectedDate()
        self.date_selected.emit(selected_date)
        
        super().accept()


if __name__ == "__main__":
    app = QApplication([])
    window = DatePickerDialog()

    window.show()
    app.exec()