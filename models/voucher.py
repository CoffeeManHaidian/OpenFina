import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
from typing import List, Optional
from contextlib import contextmanager
from PySide6.QtCore import QDate

from models.data import Voucher, VoucherDetail
from utils.logger import get_logger, log_event

logger = get_logger()

class VoucherManager:
    def __init__(self, db_path="finance.db"):
        self.db_path = db_path
        log_event(logger, "初始化 VoucherManager", db_path=self.db_path)
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
            logger.exception("数据库事务执行失败")
            raise
        finally:
            conn.close()
    
    def _require_role(self, role, operation):
        current_role = getattr(self, "_current_user_role", None)
        if current_role is None:
            return
        if current_role != role:
            raise PermissionError(f"当前用户角色 '{current_role}' 没有权限执行 '{operation}' 操作")

    def set_current_user_role(self, role):
        self._current_user_role = role

    def init_database(self):
        with self.get_connection() as conn:
            log_event(logger, "初始化凭证数据库结构", db_path=self.db_path)
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
                    reviewer_account TEXT,                          -- 审核操作账号
                    poster TEXT,                                    -- 过账人
                    poster_account TEXT,                            -- 过账操作账号
                    attention TEXT,                                 -- 经办人
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- 凭证时间
                    posted_time TIMESTAMP,                          -- 过账时间
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

            columns = {
                row["name"] for row in conn.execute("PRAGMA table_info(voucher_master)").fetchall()
            }
            if "poster" not in columns:
                conn.execute("ALTER TABLE voucher_master ADD COLUMN poster TEXT")
            if "reviewer_account" not in columns:
                conn.execute("ALTER TABLE voucher_master ADD COLUMN reviewer_account TEXT")
            if "poster_account" not in columns:
                conn.execute("ALTER TABLE voucher_master ADD COLUMN poster_account TEXT")
            if "posted_time" not in columns:
                conn.execute("ALTER TABLE voucher_master ADD COLUMN posted_time TIMESTAMP")
    
    def save_voucher(self, voucher: Voucher) -> int:
        """保存凭证（包含事务）"""
        self._require_role("manager", "凭证录入")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(logger, "开始写入凭证", db_path=self.db_path, voucher_no=voucher.voucher_no, detail_count=len(voucher.details))
            
            cursor.execute(
                "SELECT voucher_id FROM voucher_master WHERE voucher_no = ?",
                (voucher.voucher_no,)
                )
            result = cursor.fetchone()

            if result is None:
                # 新增
                log_event(logger, "写入新凭证主表", voucher_no=voucher.voucher_no)
                cursor.execute("""
                    INSERT INTO voucher_master 
                    (
                        voucher_no, voucher_type, voucher_date, attach_count,
                        preparer, reviewer, reviewer_account, poster, poster_account, attention
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    voucher.voucher_no,
                    voucher.voucher_type,
                    voucher.voucher_date,
                    voucher.attach_count,
                    voucher.preparer,
                    voucher.reviewer,
                    voucher.reviewer_account,
                    voucher.poster,
                    voucher.poster_account,
                    voucher.attention
                ))
                voucher_id = cursor.lastrowid
            else:
                # 更新
                voucher_id = voucher.voucher_id
                log_event(logger, "更新已有凭证主表", voucher_no=voucher.voucher_no, voucher_id=voucher_id)
                cursor.execute("""
                    UPDATE voucher_master SET
                    voucher_no = ?, voucher_type = ?, voucher_date = ?, attach_count = ?,
                    preparer = ?, reviewer = ?, reviewer_account = ?,
                    poster = ?, poster_account = ?, attention = ?
                    WHERE voucher_id = ?
                """, (
                    voucher.voucher_no,
                    voucher.voucher_type,
                    voucher.voucher_date,
                    voucher.attach_count,
                    voucher.preparer,
                    voucher.reviewer,
                    voucher.reviewer_account,
                    voucher.poster,
                    voucher.poster_account,
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
            log_event(logger, "凭证写入完成", voucher_id=voucher_id, voucher_no=voucher.voucher_no, detail_count=len(voucher.details))
            
            return voucher_id

    def _normalize_date_value(self, value):
        if value is None:
            return None
        if hasattr(value, "toString"):
            return value.toString("yyyy-MM-dd")
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)
    
    def search_voucher(self, number: int) -> Optional[Voucher]:
        """获取单个凭证"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(logger, "查询单张凭证", db_path=self.db_path, voucher_no=number)
            
            # 获取主表信息
            cursor.execute("SELECT * FROM voucher_master WHERE voucher_no = ?", (number,))
            master_row = cursor.fetchone()
            
            if not master_row:
                log_event(logger, "凭证查询结果为空", level=30, db_path=self.db_path, voucher_no=number)
                return None
            
            # 获取明细
            cursor.execute("""
                SELECT * FROM voucher_details 
                WHERE voucher_id = ? 
                ORDER BY line_no
            """, (master_row['voucher_id'],))
            detail_rows = cursor.fetchall()
            
            # 构建Voucher对象
            voucher = Voucher(
                voucher_id=master_row['voucher_id'],
                voucher_no=master_row['voucher_no'],
                voucher_type=master_row['voucher_type'],
                voucher_date=master_row['voucher_date'],
                attach_count=master_row['attach_count'],
                preparer=master_row['preparer'],
                reviewer=master_row['reviewer'],
                reviewer_account=master_row['reviewer_account'],
                poster=master_row['poster'],
                poster_account=master_row['poster_account'],
                attention=master_row['attention'],
                created_time=master_row['created_time'],
                posted_time=master_row['posted_time']
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
            log_event(logger, "凭证查询成功", voucher_no=number, detail_count=len(voucher.details))
            
            return voucher        

    def review_voucher(self, voucher_no: str, reviewer_name: str, reviewer_account: str):
        """审核凭证"""
        self._require_role("manager", "凭证审核")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(
                logger,
                "开始审核凭证",
                db_path=self.db_path,
                voucher_no=voucher_no,
                reviewer=reviewer_name,
                reviewer_account=reviewer_account,
            )
            cursor.execute(
                """
                SELECT voucher_id, preparer, reviewer
                FROM voucher_master
                WHERE voucher_no = ?
                """,
                (voucher_no,)
            )
            row = cursor.fetchone()

            if row is None:
                raise ValueError("凭证不存在")

            if row["preparer"] == reviewer_name:
                raise ValueError("制单人与审核人不能是同一人")

            if row["reviewer"]:
                raise ValueError(f"凭证已由 {row['reviewer']} 审核")

            cursor.execute(
                "UPDATE voucher_master SET reviewer = ?, reviewer_account = ? WHERE voucher_id = ?",
                (reviewer_name, reviewer_account, row["voucher_id"])
            )
            log_event(
                logger,
                "凭证审核完成",
                db_path=self.db_path,
                voucher_no=voucher_no,
                reviewer=reviewer_name,
                reviewer_account=reviewer_account,
            )

    def cancel_review(self, voucher_no: str, reviewer_account: str):
        """取消审核"""
        self._require_role("manager", "取消审核")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(
                logger,
                "开始取消审核",
                db_path=self.db_path,
                voucher_no=voucher_no,
                reviewer_account=reviewer_account,
            )
            cursor.execute(
                """
                SELECT voucher_id, reviewer, reviewer_account, poster
                FROM voucher_master
                WHERE voucher_no = ?
                """,
                (voucher_no,)
            )
            row = cursor.fetchone()

            if row is None:
                raise ValueError("凭证不存在")

            if not row["reviewer"]:
                raise ValueError("凭证尚未审核")

            if row["poster"]:
                raise ValueError("凭证已过账，不能取消审核")

            if not row["reviewer_account"]:
                raise ValueError("历史数据缺少审核操作账号，不能取消审核")

            if row["reviewer_account"] != reviewer_account:
                raise ValueError(f"该凭证由 {row['reviewer']} 审核，当前用户不能取消")

            cursor.execute(
                "UPDATE voucher_master SET reviewer = NULL, reviewer_account = NULL WHERE voucher_id = ?",
                (row["voucher_id"],)
            )
            log_event(
                logger,
                "取消审核完成",
                db_path=self.db_path,
                voucher_no=voucher_no,
                reviewer_account=reviewer_account,
            )

    def post_voucher(self, voucher_no: str, poster_name: str, poster_account: str):
        """过账凭证"""
        self._require_role("manager", "凭证过账")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(
                logger,
                "开始过账凭证",
                db_path=self.db_path,
                voucher_no=voucher_no,
                poster=poster_name,
                poster_account=poster_account,
            )
            cursor.execute(
                """
                SELECT voucher_id, reviewer, poster
                FROM voucher_master
                WHERE voucher_no = ?
                """,
                (voucher_no,)
            )
            row = cursor.fetchone()

            if row is None:
                raise ValueError("凭证不存在")

            if not row["reviewer"]:
                raise ValueError("凭证尚未审核，不能过账")

            if row["poster"]:
                raise ValueError(f"凭证已由 {row['poster']} 过账")

            cursor.execute(
                """
                UPDATE voucher_master
                SET poster = ?, poster_account = ?, posted_time = CURRENT_TIMESTAMP
                WHERE voucher_id = ?
                """,
                (poster_name, poster_account, row["voucher_id"])
            )
            log_event(
                logger,
                "凭证过账完成",
                db_path=self.db_path,
                voucher_no=voucher_no,
                poster=poster_name,
                poster_account=poster_account,
            )

    def cancel_post(self, voucher_no: str, poster_account: str):
        """取消过账"""
        self._require_role("manager", "取消过账")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(
                logger,
                "开始取消过账",
                db_path=self.db_path,
                voucher_no=voucher_no,
                poster_account=poster_account,
            )
            cursor.execute(
                """
                SELECT voucher_id, poster, poster_account
                FROM voucher_master
                WHERE voucher_no = ?
                """,
                (voucher_no,)
            )
            row = cursor.fetchone()

            if row is None:
                raise ValueError("凭证不存在")

            if not row["poster"]:
                raise ValueError("凭证尚未过账")

            if not row["poster_account"]:
                raise ValueError("历史数据缺少过账操作账号，不能取消过账")

            if row["poster_account"] != poster_account:
                raise ValueError(f"该凭证由 {row['poster']} 过账，当前用户不能取消")

            cursor.execute(
                """
                UPDATE voucher_master
                SET poster = NULL, poster_account = NULL, posted_time = NULL
                WHERE voucher_id = ?
                """,
                (row["voucher_id"],)
            )
            log_event(
                logger,
                "取消过账完成",
                db_path=self.db_path,
                voucher_no=voucher_no,
                poster_account=poster_account,
            )

    def batch_cancel_post(self, start_date, end_date):
        """批量取消过账（仅限管理员）"""
        self._require_role("admin", "批量取消过账")
        with self.get_connection() as conn:
            result = conn.execute(
                """
                UPDATE voucher_master
                SET poster = NULL, poster_account = NULL, posted_time = NULL
                WHERE voucher_date >= ? AND voucher_date <= ? AND poster IS NOT NULL
                """,
                (self._normalize_date_value(start_date), self._normalize_date_value(end_date)),
            )
            count = result.rowcount
        log_event(logger, "批量取消过账完成", count=count, start_date=start_date, end_date=end_date)
        return count

    def batch_cancel_review(self, start_date, end_date):
        """批量取消审核（仅限管理员）"""
        self._require_role("admin", "批量取消审核")
        with self.get_connection() as conn:
            result = conn.execute(
                """
                UPDATE voucher_master
                SET reviewer = NULL, reviewer_account = NULL
                WHERE voucher_date >= ? AND voucher_date <= ?
                  AND reviewer IS NOT NULL AND poster IS NULL
                """,
                (self._normalize_date_value(start_date), self._normalize_date_value(end_date)),
            )
            count = result.rowcount
        log_event(logger, "批量取消审核完成", count=count, start_date=start_date, end_date=end_date)
        return count

    def search_vouchers(self, start_date=None, end_date=None, voucher_no=None, summary_keyword=None, account_keyword=None):
        """查询凭证列表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            log_event(
                logger,
                "查询凭证列表",
                db_path=self.db_path,
                start_date=start_date,
                end_date=end_date,
                voucher_no=voucher_no,
                summary_keyword=summary_keyword,
                account_keyword=account_keyword,
            )

            query = """
                SELECT
                    vm.*,
                    (
                        SELECT vd.summary
                        FROM voucher_details vd
                        WHERE vd.voucher_id = vm.voucher_id
                        ORDER BY vd.line_no
                        LIMIT 1
                    ) AS first_summary
                FROM voucher_master vm
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND vm.voucher_date >= ?"
                params.append(self._normalize_date_value(start_date))
            if end_date:
                query += " AND vm.voucher_date <= ?"
                params.append(self._normalize_date_value(end_date))
            if voucher_no:
                query += " AND vm.voucher_no LIKE ?"
                params.append(f"%{voucher_no}%")
            if summary_keyword:
                query += """
                    AND EXISTS (
                        SELECT 1
                        FROM voucher_details vd
                        WHERE vd.voucher_id = vm.voucher_id
                        AND vd.summary LIKE ?
                    )
                """
                params.append(f"%{summary_keyword}%")
            if account_keyword:
                account_parts = str(account_keyword).split(" ", 1)
                account_code = account_parts[0].strip()
                query += """
                    AND EXISTS (
                        SELECT 1
                        FROM voucher_details vd
                        WHERE vd.voucher_id = vm.voucher_id
                        AND (
                            vd.account_code LIKE ?
                            OR vd.account_name LIKE ?
                        )
                    )
                """
                params.extend((f"%{account_code}%", f"%{account_keyword.strip()}%"))

            query += " ORDER BY vm.voucher_date, vm.voucher_no"
            cursor.execute(query, params)
            
            rows = cursor.fetchall()
            log_event(logger, "凭证列表查询完成", result_count=len(rows))
            return rows
        
    def update_voucher_no(self, date) -> int:
        """获取下一个可用凭证号"""
        # 当月的起止日期
        year = date.year()
        month = date.month()
        first_date = QDate(year, month, 1)
        last_date = QDate(year, month+1, 1).addDays(-1)
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
        next_number = str(number + 1)
        log_event(logger, "生成下一个凭证号", db_path=self.db_path, period=date.toString("yyyy-MM"), next_number=next_number)
        return next_number
            
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
            log_event(logger, "加载凭证号列表", db_path=self.db_path, period=date.toString("yyyy-MM"), count=len(voucher_nos))
            return voucher_nos
    
    def summary_voucher(self, start_date, end_date):
        """按会计时期查找凭证，返回ID"""
        # 按会计时期查找凭证主表
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM voucher_master \
                WHERE voucher_date >= ? AND voucher_date <= ?",
                (start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd"),)
            )
            master_row = cursor.fetchall()

        # 凭证主表id
        voucher_ids = []
        for voucher in master_row:
            voucher_ids.append(int(voucher['voucher_id']))
        log_event(logger, "汇总凭证主表查询完成", db_path=self.db_path, start_date=start_date.toString("yyyy-MM-dd"), end_date=end_date.toString("yyyy-MM-dd"), count=len(voucher_ids))

        return voucher_ids
    
    def summary_subject(self, start_date, end_date):
        """按科目汇总"""
        voucher_ids = self.summary_voucher(start_date, end_date)
        if not voucher_ids:
            log_event(logger, "科目汇总无可用凭证", level=30, db_path=self.db_path, start_date=start_date.toString("yyyy-MM-dd"), end_date=end_date.toString("yyyy-MM-dd"))
            return []
        # 查询指定凭证的数据
        with self.get_connection() as conn:
            cursor = conn.cursor()

            placeholders = ','.join(['?' for _ in voucher_ids])
            result = cursor.execute(f'''
                SELECT 
                    CASE 
                        WHEN INSTR(account_code, '.') > 0 
                        THEN SUBSTR(account_code, 1, INSTR(account_code, '.') - 1)
                        ELSE account_code
                    END AS parent_code,
                    SUM(debit_amount) as total_debit,
                    SUM(credit_amount) as total_credit
                FROM voucher_details 
                WHERE voucher_id IN ({placeholders})
                GROUP BY parent_code
            ''',
            voucher_ids).fetchall()

        log_event(logger, "科目汇总完成", db_path=self.db_path, start_date=start_date.toString("yyyy-MM-dd"), end_date=end_date.toString("yyyy-MM-dd"), result_count=len(result))
        return result
