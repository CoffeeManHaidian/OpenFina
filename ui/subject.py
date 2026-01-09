import json
from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidgetItem, QTreeWidget, QApplication)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QColor


class SubjectWindow(QWidget):
    subFunc = Signal(str, str)

    def __init__(self, json_path="data\subject.json"):
        super().__init__()
        self.json_path = json_path
        self.setupUi()
        self.load_tree()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("会计科目")
        self.resize(500, 600)
        # 移除最大化按钮标志，只保留最小化和关闭按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        mainLayout = QVBoxLayout()
        
        ## 搜索栏
        # 输入框
        searchLayout = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("搜索科目...")
        self.searchInput.textChanged.connect(self.filter_items)
        # 清除按钮
        self.clearButton = QPushButton()
        self.clearButton.setText("清除")

        ## Tree
        self.subjectTree = QTreeWidget()
        self.subjectTree.setHeaderLabels(["科目"])
        self.subjectTree.setColumnCount(1)

        ## ButtonBox
        buttonLayout = QHBoxLayout()
        self.OkBtn = QPushButton("确认")
        self.CancelBtn = QPushButton("取消")

        ## Layout
        # search
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.clearButton)
        # buttonBox
        buttonLayout.addWidget(self.OkBtn)
        buttonLayout.addWidget(self.CancelBtn)
        # main
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.subjectTree)

        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        # 确认取消
        self.clearButton.clicked.connect(self.clear_search)
        self.OkBtn.clicked.connect(self.accept)
        self.CancelBtn.clicked.connect(self.close)
    
    def load_tree(self):
        """加载树形图"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.subjectTree.clear()
        self.all_items = []
        
        def add_item(parent, key, value, depth=0):
            item = QTreeWidgetItem(parent, [key])
            item.setData(0, Qt.UserRole, depth)  # 存储深度信息
            
            # 添加到搜索列表
            self.all_items.append({
                'item': item,
                'text': key,
                'depth': depth
            })
            
            if value:
                for child_key, child_value in value.items():
                    add_item(item, child_key, child_value, depth + 1)
        
        for category, items in data.items():
            category_item = QTreeWidgetItem(self.subjectTree, [category])
            category_item.setExpanded(True)
            
            # 添加到搜索列表
            self.all_items.append({
                'item': category_item,
                'text': category,
                'depth': 0
            })
            
            for key, value in items.items():
                add_item(category_item, key, value, 1)
    
    def filter_items(self, search_text):
        """根据搜索文本过滤项目"""
        # if not search_text:
        #     # 显示所有项目
        #     for item_info in self.all_items:
        #         item_info['item'].setHidden(False)
        #         # 确保父项目展开以显示子项目
        #         parent = item_info['item'].parent()
        #         if parent:
        #             parent.setExpanded(True)
        #     return
        
        search_text = search_text.lower()
        
        # 首先隐藏所有项目
        for item_info in self.all_items:
            item_info['item'].setHidden(True)
        
        # 显示匹配的项目及其父项目
        for item_info in self.all_items:
            if search_text in item_info['text'].lower():
                item = item_info['item']
                item.setHidden(False)
                
                # 显示所有父项目
                parent = item.parent()
                while parent:
                    parent.setHidden(False)
                    parent.setExpanded(True)
                    parent = parent.parent()

    def clear_search(self):
        """清除搜索"""
        self.search_input.clear()
        for item_info in self.all_items:
            item_info['item'].setHidden(False)

    def accept(self):
        """确认按钮点击事件"""
        item = self.subjectTree.currentItem()
        p = item.parent()
        while p:
            parent = p
            p = parent.parent()
        
        self.subFunc.emit(parent.text(0), item.text(0))
        self.close()
        # print(parent.text(0), item.text(0))


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow()

    window.show()
    app.exec()