import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.bookset import SubjectStore
from utils.logger import get_logger, log_event
from utils.theme import material_widget_style

logger = get_logger()


class SubjectWindow(QWidget):
    subFunc = Signal(str, str)

    def __init__(self, bookset_db_path):
        super().__init__()
        self.bookset_db_path = bookset_db_path
        self.subject_store = SubjectStore(bookset_db_path)
        log_event(logger, "初始化科目窗口", bookset_db_path=self.bookset_db_path)
        self.all_items = []
        self.setupUi()
        self.setStyleSheet(material_widget_style())
        self.load_tree()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("会计科目")
        self.resize(600, 700)
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        mainLayout = QVBoxLayout()
        searchLayout = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("搜索科目名称或编号...")
        self.clearButton = QPushButton("清除")

        self.subjectTree = QTreeWidget()
        self.subjectTree.setHeaderLabels(["科目编号", "会计科目"])
        self.subjectTree.setColumnCount(2)
        header = self.subjectTree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        topLayout = QHBoxLayout()
        topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.OkBtn = QPushButton("确认")
        self.CancelBtn = QPushButton("取消")
        self.addBtn = QPushButton("新增")
        self.modifyBtn = QPushButton("修改")
        self.deleteBtn = QPushButton("删除")
        topLayout.addWidget(self.OkBtn)
        topLayout.addWidget(self.CancelBtn)
        topLayout.addWidget(self.addBtn)
        topLayout.addWidget(self.modifyBtn)
        topLayout.addWidget(self.deleteBtn)
        topLayout.addItem(topSpacer)

        searchLayout.addWidget(QLabel("搜索:"))
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.clearButton)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.subjectTree)
        self.setLayout(mainLayout)

    def init_slot(self):
        self.searchInput.textChanged.connect(self.filter_items)
        self.clearButton.clicked.connect(self.clear_search)
        self.OkBtn.clicked.connect(self.accept)
        self.CancelBtn.clicked.connect(self.close)
        self.addBtn.clicked.connect(self.on_addBtn_clicked)
        self.deleteBtn.clicked.connect(self.on_deleteBtn_clicked)
        self.subjectTree.itemDoubleClicked.connect(self.accept)

    def load_tree(self):
        try:
            data = self.subject_store.get_tree_data()
            log_event(logger, "加载账套科目树", bookset_db_path=self.bookset_db_path)
        except Exception as exc:
            logger.exception("账套科目加载失败")
            QMessageBox.critical(self, "错误", f"账套科目加载失败:\n{exc}")
            return

        self.subjectTree.clear()
        self.all_items.clear()

        for category, subjects in data.items():
            category_item = QTreeWidgetItem(self.subjectTree)
            category_item.setText(0, category)
            font = category_item.font(0)
            font.setBold(True)
            font.setPointSize(11)
            category_item.setFont(0, font)
            category_item.setFont(1, font)
            category_item.setBackground(0, QColor(240, 240, 240))
            category_item.setBackground(1, QColor(240, 240, 240))

            for subject in subjects:
                self._append_subject_item(category_item, category_item, category, subject)

            category_item.setExpanded(False)

        self.subjectTree.resizeColumnToContents(0)
        log_event(logger, "账套科目树加载完成", count=len(self.all_items), bookset_db_path=self.bookset_db_path)

    def _append_subject_item(self, parent_item, category_item, category, subject):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, subject["code"])
        item.setText(1, subject["name"])
        item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            {"category": category, "code": subject["code"], "name": subject["name"]},
        )
        self.all_items.append(
            {"item": item, "text": f"{subject['code']} {subject['name']}", "category_item": category_item}
        )

        for child in subject.get("subjects", []):
            self._append_subject_item(item, category_item, category, child)

    def filter_items(self, search_text):
        search_text = search_text.strip().lower()
        if not search_text:
            for item_info in self.all_items:
                item_info["item"].setHidden(False)
                item_info["category_item"].setHidden(False)
                item_info["category_item"].setExpanded(False)
            return

        def hide_item(item):
            item.setHidden(True)
            for index in range(item.childCount()):
                hide_item(item.child(index))

        for index in range(self.subjectTree.topLevelItemCount()):
            hide_item(self.subjectTree.topLevelItem(index))

        def show_parents(item):
            parent = item.parent()
            if parent is not None:
                parent.setHidden(False)
                parent.setExpanded(True)
                show_parents(parent)

        for item_info in self.all_items:
            if search_text in item_info["text"].lower():
                item_info["item"].setHidden(False)
                show_parents(item_info["item"])

    def clear_search(self):
        self.searchInput.clear()
        for item_info in self.all_items:
            item_info["item"].setHidden(False)
            item_info["category_item"].setHidden(False)
            item_info["category_item"].setExpanded(False)

    def accept(self):
        current_item = self.subjectTree.currentItem()
        if not current_item or current_item.parent() is None:
            QMessageBox.information(self, "提示", "请选择具体科目")
            return

        subject_data = current_item.data(0, Qt.ItemDataRole.UserRole) or {}
        code = subject_data.get("code", current_item.text(0))
        name = subject_data.get("name", current_item.text(1))
        log_event(logger, "选择账套科目", code=code, name=name, bookset_db_path=self.bookset_db_path)
        self.subFunc.emit(code, name)
        self.close()

    def on_addBtn_clicked(self):
        current_item = self.subjectTree.currentItem()
        if current_item is None or current_item.parent() is None or current_item.parent().parent() is not None:
            QMessageBox.information(self, "提示", "请选择一级科目后再新增子科目")
            return

        text, ok = QInputDialog.getText(self, "新增科目", "输入科目名称:")
        if not ok or not text.strip():
            QMessageBox.warning(self, "输入取消", "没有输入或取消了操作")
            return

        try:
            self.subject_store.add_child_subject(current_item.text(0), text.strip())
            self.load_tree()
        except Exception as exc:
            logger.exception("新增账套科目失败")
            QMessageBox.critical(self, "错误", f"新增科目失败:\n{exc}")

    def on_deleteBtn_clicked(self):
        current_item = self.subjectTree.currentItem()
        if current_item is None or current_item.parent() is None:
            QMessageBox.information(self, "提示", "请选择具体科目")
            return

        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确认删除 {current_item.text(1)} 吗？\n此操作不可恢复！！！",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        try:
            self.subject_store.delete_subject(current_item.text(0))
            self.load_tree()
        except Exception as exc:
            logger.exception("删除账套科目失败")
            QMessageBox.critical(self, "错误", f"删除科目失败:\n{exc}")


if __name__ == "__main__":
    app = QApplication([])
    window = SubjectWindow("")
    window.show()
    app.exec()



