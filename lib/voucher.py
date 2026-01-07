import sqlite3
from PySide6.QtWidgets import QWidget, QComboBox


class VoucherManager:
    """凭证号管理器"""
    # number_list = Signal(list)
    
    def __init__(self, db_path="./data/vouchers.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # status VARCHAR(10)              -- 状态
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY,
                voucher_no VARCHAR(20) UNIQUE,  -- 凭证号
                voucher_date DATE,              -- 业务日期
                voucher_type VARCHAR(10),       -- 凭证类型
                voucher_subject VARCHAR(50),    -- 会计科目
                debit_amount DECIMAL(28,2),     -- 借方金额
                credit_amount DECIMAL(28,2),    -- 贷方金额
                created_by VARCHAR(50),         -- 创建人
                created_time DATETIME           -- 凭证时间
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_next_voucher_no(self):
        """获取下一个可用的凭证号"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 查询最大的凭证号
        cursor.execute('''
            SELECT voucher_no FROM vouchers 
            ORDER BY voucher_no DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # 提取序号并递增
            last_no = result[0]
            # 假设格式为 
            number = last_no
            next_number = int(number) + 1
            return f"{next_number:03d}"
        else:
            # 第一个凭证
            return f"001"
    
    def get_voucher_history(self, limit=10):
        """获取历史凭证号"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT voucher_no FROM vouchers 
            ORDER BY voucher_no DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        # self.number_list.emit([r[0] for r in results])
        return [r[0] for r in results]
    
    def save_voucher(self, voucher_no):
        """保存凭证"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vouchers (voucher_no,voucher_date,voucher_type,voucher_subject,
                           debit_amount,credit_amount,created_by,created_time)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (voucher_no,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # 凭证号重复
            return False