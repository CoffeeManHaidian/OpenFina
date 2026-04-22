import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent


class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text=""):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标悬停时的手形光标
    
    def mousePressEvent(self, event: QMouseEvent):
        """重写鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 发射点击信号
        super().mousePressEvent(event)