from ui.Ui_InputWindow import Ui_InuputWindow
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QLineEdit
from PySide6.QtCore import Qt


class InputWindow(QWidget, Ui_InuputWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 绑定信号与槽
        self.init_solt()

    def init_solt(self):
        """
        初始化槽函数
        
        """
        self.btn_assets.clicked.connect(lambda:self.goto_subfunc_page(0))
        self.btn_debt.clicked.connect(lambda:self.goto_subfunc_page(1))

        self.tree_Itemlist.currentItemChanged.connect(self.listchange)
        self.btn_search.clicked.connect(self.search_button_clicked)

    def listchange(self, item):
        print(item.text(0), item.text(0))

    def search_button_clicked(self):
        """
        搜索列表项目       
        """
        search_dialog = QInputDialog()
        item = search_dialog.getText(self, "搜索", "请输入搜索内容:", QLineEdit.EchoMode.Normal)
        search_dialog.setOkButtonText("搜索")
        search_dialog.setCancelButtonText("取消")
        # print(item)
        if item[1]:
            text = item[0]
            list_items = self.tree_Itemlist.findItems(text, Qt.MatchFlag.MatchContains)
            for item in list_items:
                print(item.text(0))

            self.tree_Itemlist.scrollToItem(list_items[0])
    
    def goto_subfunc_page(self, number):
        """
        切换子功能窗口页面
        param number:
        return:
        """
        self.stackedWidget.setCurrentIndex(number)


if __name__ == "__main__":
    app = QApplication([])
    windows = InputWindow()
    windows.show()
    app.exec()