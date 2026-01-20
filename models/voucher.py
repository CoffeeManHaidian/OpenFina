# database.py
import sqlite3
import os
# from datetime import date, timedelta
from typing import List, Optional
from contextlib import contextmanager
from PySide6.QtCore import QDate

from models.data import Voucher, VoucherDetail

class VoucherManager:
    def __init__(self, db_path="finance.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """上下文管理器管理连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 使查询返回字典式对象
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_database(self):
        with self.get_connection() as conn:
            # 创建凭证主表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voucher_master (
                    voucher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    voucher_no TEXT NOT NULL,                       -- 凭证号
                    voucher_type TEXT,                              -- 凭证类型
                    voucher_date DATE NOT NULL,                     -- 业务日期
                    attach_count INTEGER DEFAULT 0,                 -- 附件张数
                    preparer TEXT,                                  -- 制单人
                    reviewer TEXT,                                  -- 审核人
                    attention TEXT,                                 -- 经办人
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 凭证时间
                    UNIQUE(voucher_id, voucher_no)
                )
            """)
            
            # 创建凭证明细表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voucher_details (
                    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    voucher_id INTEGER NOT NULL,
                    line_no INTEGER NOT NULL,                       -- 行号
                    account_code TEXT NOT NULL,                     -- 科目编号
                    account_name TEXT NOT NULL,                     -- 科目名称
                    debit_amount DECIMAL(15,2) DEFAULT 0,           -- 借方金额
                    credit_amount DECIMAL(15,2) DEFAULT 0,          -- 贷方金额
                    summary TEXT,                                   -- 摘要
                    auxiliary TEXT,                                 -- 辅助核算
                    UNIQUE(voucher_id, line_no)
                )
            """)
            
            # 创建索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_voucher_date ON voucher_master(voucher_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_voucher_details ON voucher_details(voucher_id)")
    
    def save_voucher(self, voucher: Voucher) -> int:
        """保存凭证（包含事务）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT voucher_id FROM voucher_master WHERE voucher_no = ?",
                (voucher.voucher_no,)
                )
            result = cursor.fetchone()

            if result is None:
                # 新增
                cursor.execute("""
                    INSERT INTO voucher_master 
                    (voucher_no, voucher_type, voucher_date, attach_count, preparer, reviewer, attention)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    voucher.voucher_no,
                    voucher.voucher_type,
                    voucher.voucher_date,
                    voucher.attach_count,
                    voucher.preparer,
                    voucher.reviewer,
                    voucher.attention
                ))
                voucher_id = cursor.lastrowid
            else:
                # 更新
                voucher_id = voucher.voucher_id
                cursor.execute("""
                    UPDATE voucher_master SET
                    voucher_no = ?, voucher_type = ?, voucher_date = ?, attach_count = ?,
                    preparer = ?, reviewer = ?, attention = ?
                    WHERE voucher_id = ?
                """, (
                    voucher.voucher_no,
                    voucher.voucher_type,
                    voucher.voucher_date,
                    voucher.attach_count,
                    voucher.preparer,
                    voucher.reviewer,
                    voucher.attention,
                    voucher_id
                ))
                # 删除旧的明细
                # cursor.execute("DELETE FROM voucher_details WHERE voucher_id = ?", (voucher_id,))
            
            # 插入明细
            for i, detail in enumerate(voucher.details):
                cursor.execute("""
                    INSERT INTO voucher_details 
                    (voucher_id, line_no, account_code, account_name, 
                     debit_amount, credit_amount, summary, auxiliary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    voucher_id,
                    i + 1,  # 分录号从1开始
                    detail.account_code,
                    detail.account_name,
                    detail.debit_amount,
                    detail.credit_amount,
                    detail.summary,
                    detail.auxiliary
                ))
            
            return voucher_id
    
    def search_voucher(self, voucher_id: int) -> Optional[Voucher]:
        """获取单个凭证"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取主表信息
            cursor.execute("SELECT * FROM voucher_master WHERE voucher_id = ?", (voucher_id,))
            master_row = cursor.fetchone()
            
            if not master_row:
                return None
            
            # 获取明细
            cursor.execute("""
                SELECT * FROM voucher_details 
                WHERE voucher_id = ? 
                ORDER BY line_no
            """, (voucher_id,))
            detail_rows = cursor.fetchall()
            
            # 构建Voucher对象
            voucher = Voucher(
                voucher_id=master_row['voucher_id'],
                voucher_no=master_row['voucher_no'],
                voucher_date=master_row['voucher_date'],
                attach_count=master_row['attach_count'],
                preparer=master_row['preparer'],
                reviewer=master_row['reviewer'],
                attention=master_row['attention']
            )
            
            # 添加明细
            for row in detail_rows:
                voucher.details.append(VoucherDetail(
                    detail_id=row['detail_id'],
                    voucher_id=row['voucher_id'],
                    line_no=row['line_no'],
                    account_code=row['account_code'],
                    account_name=row['account_name'],
                    debit_amount=row['debit_amount'],
                    credit_amount=row['credit_amount'],
                    summary=row['summary'],
                    auxiliary=row['auxiliary']
                ))
            
            return voucher        
    
    def search_vouchers(self, start_date=None, end_date=None, voucher_no=None):
        """查询凭证列表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM voucher_master WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND voucher_date >= ?"
                params.append(start_date.isoformat())
            if end_date:
                query += " AND voucher_date <= ?"
                params.append(end_date.isoformat())
            if voucher_no:
                query += " AND voucher_no LIKE ?"
                params.append(f"%{voucher_no}%")
            
            query += " ORDER BY voucher_date, voucher_no"
            cursor.execute(query, params)
            
            return cursor.fetchall()
        
    def update_voucher_no(self, date) -> int:
        """获取下一个可用凭证号"""
        # 当月的起止日期
        year = date.year()
        month = date.month()
        first_date = QDate(year, month, 1)
        last_date = QDate(year, month+1, 1).addDays(-1)
        print(first_date, last_date)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(voucher_no) as max_no FROM voucher_master \
                WHERE voucher_date >= ? AND voucher_date <= ?",
                (first_date.toString("yyyy-MM-dd"), last_date.toString("yyyy-MM-dd"),)
                )
            result = cursor.fetchone()

            # 最大编号
            if result and result['max_no']:
                max_id = result['max_no'] 
            else:
                max_id = date.toString("yyyy-MM") + "-0000"

            number = int(max_id.split("-")[2])

        return str(number + 1)
            
    def load_voucher_no(self, date) -> List[str]:
        """获取全部凭证号"""
        # 当月的起止日期
        year = date.year()
        month = date.month()
        first_date = QDate(year, month, 1)
        last_date = QDate(year, month+1, 1).addDays(-1)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            # DISTINCT: 消除重复记录
            # ORDER BY: 按升序或降序排列 默认 ASC 升序, DESC 降序
            # cursor.execute("SELECT DISTINCT voucher_no FROM voucher_master ORDER BY voucher_no")
            cursor.execute(
                "SELECT DISTINCT voucher_no FROM voucher_master \
                WHERE voucher_date >= ? AND voucher_date <= ? \
                ORDER BY voucher_no ASC",
                (first_date.toString("yyyy-MM-dd"), last_date.toString("yyyy-MM-dd"),)
                )
            result = cursor.fetchall()

            # 提取凭证号列表
            voucher_nos = [str(row['voucher_no'].split("-")[2]) for row in result]
            return voucher_nos
