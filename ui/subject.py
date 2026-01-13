import json
import os
from PySide6.QtWidgets import (QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidgetItem, QTreeWidget, QApplication, QHeaderView,
    QSpacerItem, QSizePolicy, QInputDialog, QMessageBox)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QColor


class SubjectWindow(QWidget):
    subFunc = Signal(str, str)

    def __init__(self, json_path=r"ui\subject.json"):
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
        # self.subjectTree.setAlternatingRowColors(True)
        
        ## ButtonBox
        topLayout = QHBoxLayout()
        topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.OkBtn = QPushButton("确认")
        self.CancelBtn = QPushButton("取消")
        self.addBtn = QPushButton("新增")
        self.modifyBtn = QPushButton("修改")
        self.deleteBtn = QPushButton("删除")
        
        # 添加按钮间距
        topLayout.addWidget(self.OkBtn)
        topLayout.addWidget(self.CancelBtn)
        topLayout.addWidget(self.addBtn)
        topLayout.addWidget(self.modifyBtn)
        topLayout.addWidget(self.deleteBtn)
        topLayout.addItem(topSpacer)

        ## Layout
        # search
        searchLayout.addWidget(QLabel("搜索:"))
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.clearButton)
        
        # main
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.subjectTree)

        self.setLayout(mainLayout)

    def init_slot(self):
        """绑定信号与槽"""
        # 搜索和清除
        self.searchInput.textChanged.connect(self.filter_items)
        self.clearButton.clicked.connect(self.clear_search)
        
        # 确认取消
        self.OkBtn.clicked.connect(self.accept)
        self.CancelBtn.clicked.connect(self.close)

        # 新增项
        self.addBtn.clicked.connect(self.on_addBtn_clicked)
        # 删除项
        self.deleteBtn.clicked.connect(self.on_deleteBtn_clicked)
        
        # 双击确认
        self.subjectTree.itemDoubleClicked.connect(self.accept)
   
    def load_tree(self):
        """将JSON数据加载到QTreeWidget的通用函数"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            QMessageBox.setText(f"找不到{self.json_path}文件")

        self.subjectTree.clear()
        self.all_items.clear()
        
        if not json_data:
            print("错误: JSON数据为空")
            return
        
        def read_subjects(json_data, parent):
            """递归读取科目数据"""
            # 如果 data 是字典，表示当前是科目对象
            if isinstance(json_data, dict):     
                subjectItem = QTreeWidgetItem(parent)
                subjectItem.setText(0, json_data["code"])
                subjectItem.setText(1, json_data["name"])

                # 存储完整信息，以便搜索和发射信号
                subjectItem.setData(0, Qt.ItemDataRole.UserRole, {
                    "category": category,
                    "code": json_data["code"],
                    "name": json_data["name"]
                })

                # 添加到搜索列表
                search_text = f"{json_data['code']} {json_data['name']}"
                self.all_items.append({
                    'item': subjectItem,
                    'text': search_text,
                    'category_item': categoryItem
                })
                    
                # 如果存在子科目，递归读取
                if 'subjects' in json_data and json_data['subjects']:
                    read_subjects(json_data['subjects'], subjectItem)
            
            # 如果 data 是列表，表示当前是科目列表
            elif isinstance(json_data, list):
                for item in json_data:
                    read_subjects(item, parent)
        
        for category, subjects in json_data.items():
            # 创建大类节点
            categoryItem = QTreeWidgetItem(self.subjectTree)
            categoryItem.setText(0, category)
            
            # 设置大类的字体加粗
            font = categoryItem.font(0)
            font.setBold(True)
            font.setPointSize(11)
            categoryItem.setFont(0, font)
            categoryItem.setFont(1, font)
            
            # 设置大类的背景色
            categoryItem.setBackground(0, QColor(240, 240, 240))
            categoryItem.setBackground(1, QColor(240, 240, 240))

            # 添加具体的会计科目
            read_subjects(subjects, categoryItem)            
                
            # 默认展开所有大类
            categoryItem.setExpanded(False)
        
        # 调整列宽
        self.subjectTree.resizeColumnToContents(0)
        # self.subjectTree.expandAll()
        
        print(f"加载完成，共加载 {len(self.all_items)} 个科目")
    
    def filter_items(self, search_text):
        """根据搜索文本过滤项目"""
        search_text = search_text.strip().lower()

        if not search_text:
            for item_info in self.all_items:
                item_info['item'].setHidden(False)
                item_info['category_item'].setHidden(False)
                item_info['category_item'].setExpanded(False)
            return
        
        # 首先隐藏所有科目节点
        def hideAllItem(item):
            if item:
                item.setHidden(True)
                for i in range(item.childCount()):
                    hideAllItem(item.child(i).setHidden(True))

        for i in range(self.subjectTree.topLevelItemCount()):
            hideAllItem(self.subjectTree.topLevelItem(i))

        # 标记哪些类别有可见的子节点
        visible_categories = set()

        def add_visible(item, visible_categories):
            if item.parent():
                print(item.parent().text(0))
                item.parent().setHidden(False)
                item.parent().setExpanded(True)
                visible_categories.add(item.parent())
                add_visible(item.parent(), visible_categories)

        # 显示匹配的项目
        for item_info in self.all_items:
            if search_text in item_info['text'].lower():
                item = item_info['item']
                item.setHidden(False)
                add_visible(item, visible_categories)
    
    def clear_search(self):
        """清除搜索"""
        self.searchInput.clear()
        for item_info in self.all_items:
            item_info['item'].setHidden(False)
            item_info['category_item'].setHidden(False)
            item_info['category_item'].setExpanded(False)

    def accept(self):
        """确认按钮点击事件或双击事件"""
        current_item = self.subjectTree.currentItem()
        
        if not current_item:
            # 如果没有选中任何项，尝试获取第一个叶子节点
            for i in range(self.subjectTree.topLevelItemCount()):
                categoryItem = self.subjectTree.topLevelItem(i)
                if categoryItem.childCount() > 0:
                    current_item = categoryItem.child(0)
                    break
        
        if not current_item:
            print("错误: 未选中任何科目")
            return
        
        # 如果选中的是大类节点，不处理
        if current_item.parent() is None:
            print("提示: 请选择一个具体的科目，而不是大类")
            return
        
        # 获取选中的科目信息
        categoryItem = current_item.parent()
        category = categoryItem.text(0)
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

    def on_addBtn_clicked(self):
        parent = self.subjectTree.currentItem()
        # 判断子节点深度
        current = parent
        depth = 0
        while current.parent():
            depth += 1
            current = current.parent()
        if depth > 1:
            return
        
        text, ok = QInputDialog.getText(self, "新增科目", "输入科目名称:")
        if ok and text:
            print(text)
        else:
            QMessageBox.warning(self, "输入取消", "没有输入或取消了操作")

        code = f"{parent.text(0)}.{parent.childCount()+1:02d}"
        newItem = QTreeWidgetItem(parent)
        newItem.setText(0, code)
        newItem.setText(1, text)
        parent.setExpanded(True)

        # 存储完整信息，以便搜索和发射信号
        newItem.setData(0, Qt.ItemDataRole.UserRole, {
            "category": parent.parent().text(0),
            "code": newItem.text(0),
            "name": newItem.text(1)
        })
        
        # 添加到搜索列表
        search_text = f"{newItem.text(0)} {newItem.text(1)}"
        print(search_text)
        self.all_items.append({
            'item': newItem,
            'text': search_text,
            'category_item': parent.parent()
        })
        
        def save_subject_to_json(parent_code, sub_code, sub_name):
            json_file_path = self.json_path
            # print(parent_code, sub_code, sub_name)
            # 将新增的科目信息追加写入 JSON 文件（按类别
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
            
            # 遍历所有分类
            for category in data.values():
                for subject in category:
                    if subject["code"] == parent_code:
                        # 如果父科目已有"subjects"字段，则添加；否则创建
                        if "subjects" in subject:
                            subject["subjects"].append({"code": sub_code, "name": sub_name})
                        else:
                            subject["subjects"] = [{"code": sub_code, "name": sub_name}]
                        print(f"成功在科目 {parent_code} 下添加子目录 {sub_code}")
                        
                        # 保存回文件
                        with open(json_file_path, 'w', encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=2)
                        return True

        save_subject_to_json(parent.text(0), newItem.text(0), newItem.text(1))

    def on_deleteBtn_clicked(self):
        """删除子细目"""
        current_item = self.subjectTree.currentItem()

        reply = QMessageBox.question(
            self, 
            "确认删除",
            f"确认删除 {current_item.text(1)} 吗？\n此操作不可恢复！！！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.delete_subject(current_item)

    def delete_subject(self, current_item):
        # print(current_item.childCount())
        if not current_item.childCount() == 0:
            return
        
        parent = current_item.parent()
        if parent:
            parent.removeChild(current_item)

        # 从json文件中删除      
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        target_code = current_item.text(0)
        def delete_subject_from_json(data, target_code, target_item):
            category = target_item.data(0, Qt.UserRole)
            items = data[category['category']]
            for item in items:
                # print(item['code'])
                if "subjects" in item:
                    for i, subitem in enumerate(item['subjects']):
                        if subitem['code'] == target_code:
                            print(subitem)
                            item['subjects'].pop(i)
            return data
        
        upload_data = delete_subject_from_json(data, target_code, current_item)
        # 写入到json
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow()
    
    # 连接信号到打印函数用于测试
    def print_selected(code, name):
        print(f"编号={code}, 名称={name}")
    
    window.subFunc.connect(print_selected)
    
    window.show()
    app.exec()