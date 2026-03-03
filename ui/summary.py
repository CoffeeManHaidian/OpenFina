import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QPushButton,
    QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidgetItem,
    QDialog)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from models.voucher import VoucherManager
from utils.subject import SubjectLookup
from ui.filter import FilterWidget


class VoucherSummary(QWidget):
    def __init__(self, user_info):
        super().__init__()
        
        # 参数设置
        self.filterWidget = FilterWidget()
        self.subjectManage = SubjectLookup("source\\subject.json")
        # UI
        self.user_info = user_info
        self.setupUi()
        self.setStyle()
        self.init_slot()

    def setupUi(self):
        self.setWindowTitle("凭证汇总")
        self.resize(1100, 600)

        mainLayout = QVBoxLayout()

        ## 汇总表
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        
        # 设置表头（使用合并单元格实现多级表头）
        self.table.setRowCount(2)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        
        # 第一行：大标题
        headers = [
            ("科目编码", 0, 1), ("科目名称", 1, 1),
            ("期初余额", 2, 2), ("本期发生", 4, 2), 
            ("本年累计", 6, 2), ("期末余额", 8, 2)
        ]
        for text, col, span in headers:
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled)  # 只读
            self.table.setItem(0, col, item)
            if span > 1:
                self.table.setSpan(0, col, 1, span)
            else:
                self.table.setSpan(0, col, 2, span)
        
        # 第二行：子标题
        sub_headers = ["借方", "贷方", "借方", "贷方", "借方", "贷方", "借方", "贷方"]
        for i, text in enumerate(sub_headers):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(1, i+2, item)
        
        # 数据行从索引2开始
        self.table.setRowCount(2 + 100)  # 2行表头 + 数据
        
        # 设置表头行高度
        self.table.setRowHeight(0, 25)
        self.table.setRowHeight(1, 25)

        ## 设置列宽
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnWidth(7, 100)
        self.table.setColumnWidth(8, 100)
        self.table.setColumnWidth(9, 100)
        self.table.setColumnWidth(10, 100)

        # 内容布局
        ## 内容
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)

        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)

    def setStyle(self):
        """设置页面风格"""       
        # 设置无边框
        # self.setStyleSheet("border: none;")

    def init_slot(self):
        """绑定信号与槽"""
        self.filterWidget.filer_info.connect(self.show_info)      

    def show_info(self, info):
        """解析筛选信息并保存为字典
        info: [会计期间开始年，开始月，结束年，结束月，起始编号+科目，结束编号+科目，凭证等级]
        """
        if not info or len(info) < 7:
            return
        
        # 解析筛选信息并保存为字典
        start_year = int(info[0])
        start_month = int(info[1])
        end_year = int(info[2])
        end_month = int(info[3])
        
        # 构建起止日期
        start_date = QDate(start_year, start_month, 1)
        if end_month == 12:
            end_date = QDate(end_year + 1, 1, 1).addDays(-1)
        else:
            end_date = QDate(end_year, end_month + 1, 1).addDays(-1)
        
        self.filter_dict = {
            'start_date': start_date,
            'end_date': end_date,
            'start_subject': info[4].split()[0] if info[4] else "",
            'end_subject': info[5].split()[0] if info[5] else "",
            'voucher_level': info[6],  # 凭证等级
            'company': self.user_info.get('company', '') if hasattr(self, 'user_info') else ''
        }
        
        # 链接数据库
        db_path = f"data\\{self.filter_dict['company']}_{start_year}_vouchers.db"
        if not os.path.exists(db_path):
            return
        
        self.voucherManage = VoucherManager(db_path)

        # 清空旧数据（保留表头行0-1）
        for row in range(2, self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.setItem(row, col, None)
                
        self.beginning_balance()    # 期初余额
        self.current_balance()      # 本期发生
        self.ending_balance()       # 期末余额

    def beginning_balance(self):
        """计算期初余额（上一个月的期末余额）"""
        if not hasattr(self, 'filter_dict'):
            return
        
        # 从字典中获取本期开始日期
        current_start_date = self.filter_dict['start_date']
        start_subject = self.filter_dict['start_subject']
        end_subject = self.filter_dict['end_subject']
        
        # 计算上一个月的日期范围
        current_year = current_start_date.year()
        current_month = current_start_date.month()
        
        if current_month == 1:
            # 如果当前是1月，上个月是上一年的12月
            prev_year = current_year - 1
            prev_month = 12
        else:
            # 否则就是上一月
            prev_year = current_year
            prev_month = current_month - 1
        
        # 构建上一个月的起止日期
        prev_start_date = QDate(prev_year, prev_month, 1)
        if prev_month == 12:
            prev_end_date = QDate(prev_year + 1, 1, 1).addDays(-1)
        else:
            prev_end_date = QDate(prev_year, prev_month + 1, 1).addDays(-1)
        
        # 获取上个月的科目汇总数据（作为期初余额）
        result = self.voucherManage.summary_subject(prev_start_date, prev_end_date)
        
        # 创建期初余额字典，用于快速查找
        beginning_balances = {}
        for info in result:
            subject_code = info['parent_code']
            beginning_balances[subject_code] = {
                'debit': info['total_debit'],
                'credit': info['total_credit']
            }
        
        # 获取本期科目列表（用于确定需要显示哪些科目）
        current_start = self.filter_dict['start_date']
        current_end = self.filter_dict['end_date']
        current_result = self.voucherManage.summary_subject(current_start, current_end)
        
        # 收集所有需要显示的科目代码（本期有的 + 上期有的）
        all_subjects = set(beginning_balances.keys())
        for info in current_result:
            all_subjects.add(info['parent_code'])
        
        # 填充期初余额数据（第2列借方，第3列贷方）
        data_row = 2  # 数据从第2行开始
        for subject_code in sorted(all_subjects):
            # 筛选科目代码范围
            if start_subject and subject_code < start_subject:
                continue
            if end_subject and subject_code > end_subject:
                continue
            
            # 确保表格行数足够
            if data_row >= self.table.rowCount():
                self.table.setRowCount(data_row + 1)
            
            # 获取期初余额
            balance = beginning_balances.get(subject_code, {'debit': 0.0, 'credit': 0.0})
            
            # 期初余额-借方（第2列）
            begin_debit = QTableWidgetItem(f"{balance['debit']:.2f}")
            begin_debit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            begin_debit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 2, begin_debit)
            
            # 期初余额-贷方（第3列）
            begin_credit = QTableWidgetItem(f"{balance['credit']:.2f}")
            begin_credit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            begin_credit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 3, begin_credit)
            
            data_row += 1

    def current_balance(self):
        """计算本期发生"""
        if not hasattr(self, 'filter_dict'):
            return
        
        # 从字典中获取筛选信息
        start_date = self.filter_dict['start_date']
        end_date = self.filter_dict['end_date']
        start_subject = self.filter_dict['start_subject']
        end_subject = self.filter_dict['end_subject']
        
        # 获取科目汇总数据（本期发生）
        result = self.voucherManage.summary_subject(start_date, end_date)
        
        # 遍历结果填充本期发生列（第4列借方，第5列贷方）
        data_row = 2  # 数据从第2行开始
        for info in result:
            # 筛选科目代码范围
            subject_code = info['parent_code']
            if start_subject and subject_code < start_subject:
                continue
            if end_subject and subject_code > end_subject:
                continue
            
            # 确保表格行数足够
            if data_row >= self.table.rowCount():
                self.table.setRowCount(data_row + 1)
            
            # 本期发生-借方（第4列）
            current_debit = QTableWidgetItem(f"{info['total_debit']:.2f}")
            current_debit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            current_debit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 4, current_debit)
            
            # 本期发生-贷方（第5列）
            current_credit = QTableWidgetItem(f"{info['total_credit']:.2f}")
            current_credit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            current_credit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 5, current_credit)
            
            data_row += 1

    # def year_balance(self):

    def ending_balance(self):
        """计算期末余额"""
        if not hasattr(self, 'filter_dict'):
            return
        
        # 从字典中获取筛选信息
        start_date = self.filter_dict['start_date']
        end_date = self.filter_dict['end_date']
        start_subject = self.filter_dict['start_subject']
        end_subject = self.filter_dict['end_subject']
        
        # 获取科目汇总数据
        result = self.voucherManage.summary_subject(start_date, end_date)

        # 填充数据
        data_row = 2  # 数据从第2行开始
        for info in result:
            # 筛选科目代码范围
            subject_code = info['parent_code']
            if start_subject and subject_code < start_subject:
                continue
            if end_subject and subject_code > end_subject:
                continue
            
            # 确保表格行数足够
            if data_row >= self.table.rowCount():
                self.table.setRowCount(data_row + 1)
            
            # 科目代码
            code_item = QTableWidgetItem(subject_code)
            code_item.setTextAlignment(Qt.AlignCenter)
            code_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 0, code_item)
            
            # 科目名称
            name = self.subjectManage.get_name(subject_code)
            name_item = QTableWidgetItem(name if name else "")
            name_item.setTextAlignment(Qt.AlignCenter)
            name_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 1, name_item)
            
            # 期末余额-借方
            debit = QTableWidgetItem(f"{info['total_debit']:.2f}")
            debit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            debit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 8, debit)
            
            # 期末余额-贷方
            credit = QTableWidgetItem(f"{info['total_credit']:.2f}")
            credit.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            credit.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(data_row, 9, credit)
            
            data_row += 1
        
        # 调整表格行数为实际数据行数 + 表头
        self.table.setRowCount(max(data_row, 2))


if __name__ == "__main__":
    app = QApplication([])
    window = VoucherSummary([])

    window.show()
    app.exec()
