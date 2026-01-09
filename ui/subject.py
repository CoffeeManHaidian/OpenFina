import json
import os
from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidgetItem, QTreeWidget, QApplication, QHeaderView)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QColor


class SubjectWindow(QWidget):
    subFunc = Signal(str, str)

    def __init__(self, json_path="data/subject.json"):
        super().__init__()
        # 修正路径分隔符，使用os.path处理
        self.json_path = json_path.replace("\\", os.path.sep)
        self.all_items = []  # 存储所有科目节点用于搜索
        self.setupUi()
        self.load_tree()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("会计科目")
        self.resize(600, 700)  # 增加宽度以显示两列
        
        # 只保留最小化和关闭按钮
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | 
                           Qt.WindowType.WindowCloseButtonHint)

        mainLayout = QVBoxLayout()
        
        ## 搜索栏
        searchLayout = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("搜索科目名称或编号...")
        
        # 清除按钮
        self.clearButton = QPushButton("清除")
        
        ## Tree
        self.subjectTree = QTreeWidget()
        self.subjectTree.setHeaderLabels(["科目编号", "会计科目"])
        self.subjectTree.setColumnCount(2)
        
        # 设置列宽
        header = self.subjectTree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        # 设置交替行颜色
        self.subjectTree.setAlternatingRowColors(True)
        
        ## ButtonBox
        buttonLayout = QHBoxLayout()
        self.OkBtn = QPushButton("确认")
        self.CancelBtn = QPushButton("取消")
        
        # 添加按钮间距
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.OkBtn)
        buttonLayout.addWidget(self.CancelBtn)
        buttonLayout.addStretch()

        ## Layout
        # search
        searchLayout.addWidget(QLabel("搜索:"))
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.clearButton)
        
        # main
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.subjectTree)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        # 搜索和清除
        self.searchInput.textChanged.connect(self.filter_items)
        self.clearButton.clicked.connect(self.clear_search)
        
        # 确认取消
        self.OkBtn.clicked.connect(self.accept)
        self.CancelBtn.clicked.connect(self.close)
        
        # 双击确认
        self.subjectTree.itemDoubleClicked.connect(self.accept)
    
    def load_tree(self):
        """将JSON数据加载到QTreeWidget的通用函数"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.json_path}")
            # 创建示例数据用于测试
            json_data = {
                "资产类": [{"code": "1001", "name": "库存现金"}],
                "负债类": [{"code": "2001", "name": "短期借款"}],
                "共同类": [{"code": "3001", "name": "清算资金往来"}],
                "所有者权益": [{"code": "4001", "name": "实收资本"}],
                "成本类": [{"code": "5001", "name": "生产成本"}],
                "损益类": [{"code": "6001", "name": "主营业务收入"}]
            }
            print("使用示例数据")

        self.subjectTree.clear()
        self.all_items.clear()
        
        if not json_data:
            print("错误: JSON数据为空")
            return
        
        # 按顺序处理六大类
        categories = ["资产类", "负债类", "共同类", "所有者权益", "成本类", "损益类"]
        
        for category in categories:
            if category in json_data:
                # 创建大类节点
                category_item = QTreeWidgetItem(self.subjectTree)
                category_item.setText(0, category)
                category_item.setText(1, "")  # 第二列为空
                
                # 设置大类的字体加粗
                font = category_item.font(0)
                font.setBold(True)
                font.setPointSize(11)
                category_item.setFont(0, font)
                category_item.setFont(1, font)
                
                # 设置大类的背景色
                category_item.setBackground(0, QColor(240, 240, 240))
                category_item.setBackground(1, QColor(240, 240, 240))
                
                # 添加具体的会计科目
                subjects = json_data[category]
                for subject in subjects:
                    if isinstance(subject, dict) and "code" in subject and "name" in subject:
                        subject_item = QTreeWidgetItem(category_item)
                        subject_item.setText(0, subject["code"])
                        subject_item.setText(1, subject["name"])
                        
                        # 存储完整信息，以便搜索和发射信号
                        subject_item.setData(0, Qt.ItemDataRole.UserRole, {
                            "category": category,
                            "code": subject["code"],
                            "name": subject["name"]
                        })
                        
                        # 添加到搜索列表
                        search_text = f"{subject['code']} {subject['name']}"
                        self.all_items.append({
                            'item': subject_item,
                            'text': search_text,
                            'category_item': category_item
                        })
                    else:
                        print(f"警告: {category} 中的科目数据格式不正确: {subject}")
                
                # 添加子节点数量统计
                child_count = category_item.childCount()
                if child_count > 0:
                    category_item.setText(0, f"{category} ({child_count}个科目)")
                
                # 默认展开所有大类
                category_item.setExpanded(True)
            else:
                print(f"警告: 在JSON数据中未找到类别: {category}")
        
        # 调整列宽
        self.subjectTree.resizeColumnToContents(0)
        self.subjectTree.expandAll()
        
        print(f"加载完成，共加载 {len(self.all_items)} 个科目")
    
    def filter_items(self, search_text):
        """根据搜索文本过滤项目"""
        search_text = search_text.strip().lower()
        
        if not search_text:
            # 显示所有项目
            for item_info in self.all_items:
                item_info['item'].setHidden(False)
                item_info['category_item'].setHidden(False)
                item_info['category_item'].setExpanded(True)
            return
        
        # 首先隐藏所有科目节点
        for item_info in self.all_items:
            item_info['item'].setHidden(True)
        
        # 标记哪些类别有可见的子节点
        visible_categories = set()
        
        # 显示匹配的项目
        for item_info in self.all_items:
            if search_text in item_info['text'].lower():
                item = item_info['item']
                item.setHidden(False)
                visible_categories.add(item_info['category_item'])
        
        # 显示或隐藏类别节点
        for i in range(self.subjectTree.topLevelItemCount()):
            category_item = self.subjectTree.topLevelItem(i)
            if category_item in visible_categories:
                category_item.setHidden(False)
                category_item.setExpanded(True)
            else:
                category_item.setHidden(True)
    
    def clear_search(self):
        """清除搜索"""
        self.searchInput.clear()
        for item_info in self.all_items:
            item_info['item'].setHidden(False)
            item_info['category_item'].setHidden(False)
            item_info['category_item'].setExpanded(True)

    def accept(self):
        """确认按钮点击事件或双击事件"""
        current_item = self.subjectTree.currentItem()
        
        if not current_item:
            # 如果没有选中任何项，尝试获取第一个叶子节点
            for i in range(self.subjectTree.topLevelItemCount()):
                category_item = self.subjectTree.topLevelItem(i)
                if category_item.childCount() > 0:
                    current_item = category_item.child(0)
                    break
        
        if not current_item:
            print("错误: 未选中任何科目")
            return
        
        # 如果选中的是大类节点，不处理
        if current_item.parent() is None:
            print("提示: 请选择一个具体的科目，而不是大类")
            return
        
        # 获取选中的科目信息
        category_item = current_item.parent()
        category = category_item.text(0)
        code = current_item.text(0)
        name = current_item.text(1)
        
        # 获取存储的数据
        subject_data = current_item.data(0, Qt.ItemDataRole.UserRole)
        if subject_data:
            category = subject_data.get("category", category)
            code = subject_data.get("code", code)
            name = subject_data.get("name", name)
        
        # 清理类别名称中的计数信息（如果有）
        if "(" in category:
            category = category.split("(")[0].strip()
        
        print(f"选中的科目: {category} - {code} - {name}")
        
        # 发射信号：第一个参数为科目编号，第二个参数为科目名称
        # 如果需要其他格式，可以调整这里
        self.subFunc.emit(code, name)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow()
    
    # 连接信号到打印函数用于测试
    def print_selected(code, name):
        print(f"发射信号: 编号={code}, 名称={name}")
    
    window.subFunc.connect(print_selected)
    
    window.show()
    app.exec()