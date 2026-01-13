import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from PySide6.QtCore import Signal, QObject


class VoucherManager(QObject):
    """凭证管理器 - 支持多分录和完整财务信息"""
    
    # 信号定义
    voucher_saved = Signal(str)  # 凭证保存成功信号，传递凭证号
    voucher_error = Signal(str)  # 凭证保存失败信号，传递错误信息
    
    def __init__(self, db_path="./data/finance.db"):
        super().__init__()
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库 - 改进后的表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. 凭证主表 - 存储凭证的总体信息
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_master (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_no VARCHAR(20) UNIQUE NOT NULL,      -- 凭证编号
                voucher_type VARCHAR(20) DEFAULT '记账凭证',  -- 凭证类型：记账凭证、收款凭证、付款凭证、转账凭证
                voucher_date DATE NOT NULL,                  -- 凭证日期（业务日期）
                c INTEGER DEFAULT 0,                         -- 附件张数
                debit_value DECIMAL(28,2) DEFAULT 0,         -- 借方合计金额
                credit_total DECIMAL(28,2) DEFAULT 0,        -- 贷方合计金额
                status VARCHAR(20) DEFAULT '暂存',           -- 状态：过账、预制、暂存
                auditor VARCHAR(50),                         -- 审核人
                auditor_date DATETIME,                       -- 审核日期
                created_by VARCHAR(50) NOT NULL,             -- 制单人
                created_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 制单时间
                remark TEXT                                  -- 备注
            )
        ''')
        
        # 2. 凭证分录表 - 存储具体的会计分录（一个凭证可以有多个分录）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_id INTEGER NOT NULL,                 -- 关联凭证主表ID
                line_no INTEGER NOT NULL,                    -- 行号
                summary VARCHAR(200) NOT NULL,               -- 摘要
                subject_code VARCHAR(20) NOT NULL,           -- 科目编码
                subject_name VARCHAR(100) NOT NULL,          -- 科目名称
                debit_amount DECIMAL(28,2) DEFAULT 0,        -- 借方金额
                credit_amount DECIMAL(28,2) DEFAULT 0,       -- 贷方金额
                auxiliary_type VARCHAR(50),                  -- 辅助核算类型：客户、供应商、部门、项目等
                auxiliary_code VARCHAR(50),                  -- 辅助核算编码
                auxiliary_name VARCHAR(100),                 -- 辅助核算名称
                currency_code VARCHAR(10) DEFAULT 'CNY',     -- 币种
                exchange_rate DECIMAL(18,6) DEFAULT 1,       -- 汇率
                original_amount DECIMAL(28,2),               -- 原币金额（外币业务用）
                quantity DECIMAL(18,4),                      -- 数量（存货科目用）
                unit_price DECIMAL(18,6),                    -- 单价（存货科目用）
                department_code VARCHAR(20),                 -- 部门编码
                person_code VARCHAR(20),                     -- 人员编码
                project_code VARCHAR(20),                    -- 项目编码
                is_cash_flow BOOLEAN DEFAULT 0,              -- 是否现金流量项目
                cash_flow_code VARCHAR(20),                  -- 现金流量项目编码
                FOREIGN KEY (voucher_id) REFERENCES voucher_master(id) ON DELETE CASCADE
            )
        ''')
        
        # 3. 凭证号规则表 - 支持自定义凭证号生成规则
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voucher_number_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_type VARCHAR(20) UNIQUE NOT NULL,    -- 凭证类型
                prefix VARCHAR(10) DEFAULT '',               -- 前缀
                year_format VARCHAR(10) DEFAULT 'YYYY',      -- 年份格式
                month_format VARCHAR(10) DEFAULT 'MM',       -- 月份格式
                separator VARCHAR(5) DEFAULT '-',            -- 分隔符
                sequence_length INTEGER DEFAULT 4,           -- 序号长度
                current_sequence INTEGER DEFAULT 0,          -- 当前序号
                reset_rule VARCHAR(20) DEFAULT 'MONTHLY'     -- 重置规则：NEVER, MONTHLY, YEARLY
            )
        ''')
        
        # 4. 科目表 - 存储会计科目信息
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounting_subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code VARCHAR(20) UNIQUE NOT NULL,    -- 科目编码
                subject_name VARCHAR(100) NOT NULL,          -- 科目名称
                subject_level INTEGER DEFAULT 1,             -- 科目级次：1-一级，2-二级，3-三级
                parent_code VARCHAR(20),                     -- 父级科目编码
                subject_type VARCHAR(20),                    -- 科目类型：资产、负债、权益、成本、损益
                direction VARCHAR(10),                       -- 余额方向：借、贷
                is_leaf BOOLEAN DEFAULT 1,                   -- 是否明细科目
                is_cash BOOLEAN DEFAULT 0,                   -- 是否现金科目
                is_bank BOOLEAN DEFAULT 0,                   -- 是否银行科目
                auxiliary_types TEXT,                        -- 辅助核算类型，JSON格式
                is_enabled BOOLEAN DEFAULT 1,                -- 是否启用
                remark TEXT                                  -- 备注
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_voucher_date ON voucher_master(voucher_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_voucher_period ON voucher_master(accounting_period)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_voucher_status ON voucher_master(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_details_voucher_id ON voucher_details(voucher_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_details_subject ON voucher_details(subject_code)')
        
        # 初始化默认凭证号规则
        self._init_default_number_rules(cursor)
        
        conn.commit()
        conn.close()
    
    def _init_default_number_rules(self, cursor):
        """初始化默认凭证号规则"""
        default_rules = [
            ('记账凭证', 'J', 'YYYY', 'MM', '-', 4, 0, 'MONTHLY'),
            ('收款凭证', 'S', 'YYYY', 'MM', '-', 4, 0, 'MONTHLY'),
            ('付款凭证', 'F', 'YYYY', 'MM', '-', 4, 0, 'MONTHLY'),
            ('转账凭证', 'Z', 'YYYY', 'MM', '-', 4, 0, 'MONTHLY'),
        ]
        
        for rule in default_rules:
            cursor.execute('''
                INSERT OR IGNORE INTO voucher_number_rules 
                (voucher_type, prefix, year_format, month_format, separator, 
                 sequence_length, current_sequence, reset_rule)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', rule)
    
    def get_next_voucher_no(self, voucher_type='记账凭证', voucher_date=None):
        """获取下一个可用的凭证号（根据规则生成）"""
        if voucher_date is None:
            voucher_date = datetime.now()
        
        year = voucher_date.year
        month = voucher_date.month
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取凭证号规则
        cursor.execute('''
            SELECT prefix, year_format, month_format, separator, 
                   sequence_length, current_sequence, reset_rule
            FROM voucher_number_rules
            WHERE voucher_type = ?
        ''', (voucher_type,))
        
        rule = cursor.fetchone()
        
        if not rule:
            # 如果没有找到规则，使用简单递增
            cursor.execute('''
                SELECT voucher_no FROM voucher_master 
                WHERE voucher_type = ?
                ORDER BY voucher_no DESC LIMIT 1
            ''', (voucher_type,))
            
            result = cursor.fetchone()
            if result:
                # 提取序号并递增
                last_no = result[0]
                try:
                    # 尝试提取数字部分
                    import re
                    numbers = re.findall(r'\d+', last_no)
                    if numbers:
                        next_seq = int(numbers[-1]) + 1
                    else:
                        next_seq = 1
                except:
                    next_seq = 1
            else:
                next_seq = 1
            
            # 生成简单凭证号
            next_no = f"{voucher_type}-{next_seq:04d}"
        else:
            # 根据规则生成凭证号
            prefix, year_format, month_format, separator, seq_length, current_seq, reset_rule = rule
            
            # 检查是否需要重置序号
            if reset_rule == 'MONTHLY':
                # 每月重置，检查是否有当月凭证
                month_str = f"{year:04d}{month:02d}"
                cursor.execute('''
                    SELECT MAX(voucher_no) FROM voucher_master 
                    WHERE voucher_type = ? AND voucher_date LIKE ?
                ''', (voucher_type, f"{year:04d}-{month:02d}%"))
                
                last_voucher = cursor.fetchone()[0]
                if last_voucher:
                    # 提取序号
                    import re
                    match = re.search(r'(\d+)$', last_voucher)
                    if match:
                        current_seq = int(match.group(1))
                else:
                    current_seq = 0
            
            # 更新序号
            next_seq = current_seq + 1
            
            # 生成凭证号各部分
            parts = []
            if prefix:
                parts.append(prefix)
            
            if year_format == 'YYYY':
                parts.append(f"{year:04d}")
            elif year_format == 'YY':
                parts.append(f"{year % 100:02d}")
            
            if month_format == 'MM':
                parts.append(f"{month:02d}")
            
            # 添加序号
            seq_format = f"{{:0{seq_length}d}}"
            parts.append(seq_format.format(next_seq))
            
            # 组合成完整凭证号
            next_no = separator.join(parts)
            
            # 更新数据库中的当前序号
            cursor.execute('''
                UPDATE voucher_number_rules 
                SET current_sequence = ? 
                WHERE voucher_type = ?
            ''', (next_seq, voucher_type))
        
        conn.commit()
        conn.close()
        
        return next_no
    
    def save_voucher(self, voucher_data: Dict) -> Tuple[bool, str]:
        """
        保存凭证（支持多分录）
        
        Args:
            voucher_data: 包含凭证主表和分录列表的字典
                {
                    'voucher_type': '记账凭证',
                    'voucher_date': '2023-12-15',
                    'accounting_period': '2023-12',
                    'attachment_count': 2,
                    'remark': '备注信息',
                    'created_by': '张三',
                    'entries': [
                        {
                            'line_no': 1,
                            'summary': '摘要1',
                            'subject_code': '1001',
                            'subject_name': '现金',
                            'debit_amount': 1000.00,
                            'credit_amount': 0.00,
                            'auxiliary_type': '部门',
                            'auxiliary_code': '001',
                            'auxiliary_name': '销售部'
                        },
                        # ... 更多分录
                    ]
                }
        
        Returns:
            (success: bool, message: str or voucher_no: str)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 1. 获取凭证号
            voucher_no = self.get_next_voucher_no(
                voucher_data.get('voucher_type', '记账凭证'),
                datetime.strptime(voucher_data['voucher_date'], '%Y-%m-%d')
            )
            
            # 2. 验证借贷平衡
            total_debit = sum(entry.get('debit_amount', 0) for entry in voucher_data['entries'])
            total_credit = sum(entry.get('credit_amount', 0) for entry in voucher_data['entries'])
            
            if abs(total_debit - total_credit) > 0.01:  # 允许0.01的误差
                return False, f"借贷不平衡！借方合计：{total_debit}，贷方合计：{total_credit}"
            
            # 3. 插入凭证主表
            cursor.execute('''
                INSERT INTO voucher_master 
                (voucher_no, voucher_type, voucher_date, accounting_period, 
                 attachment_count, total_debit_amount, total_credit_amount,
                 status, created_by, remark)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                voucher_no,
                voucher_data.get('voucher_type', '记账凭证'),
                voucher_data['voucher_date'],
                voucher_data.get('accounting_period', 
                               voucher_data['voucher_date'][:7]),  # 从日期提取期间
                voucher_data.get('attachment_count', 0),
                total_debit,
                total_credit,
                '已保存',
                voucher_data['created_by'],
                voucher_data.get('remark', '')
            ))
            
            voucher_id = cursor.lastrowid
            
            # 4. 插入分录明细
            for entry in voucher_data['entries']:
                cursor.execute('''
                    INSERT INTO voucher_details 
                    (voucher_id, line_no, summary, subject_code, subject_name,
                     debit_amount, credit_amount, auxiliary_type, auxiliary_code,
                     auxiliary_name, currency_code, exchange_rate, original_amount,
                     quantity, unit_price, department_code, person_code, project_code,
                     is_cash_flow, cash_flow_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    voucher_id,
                    entry.get('line_no', 1),
                    entry['summary'],
                    entry['subject_code'],
                    entry['subject_name'],
                    entry.get('debit_amount', 0),
                    entry.get('credit_amount', 0),
                    entry.get('auxiliary_type'),
                    entry.get('auxiliary_code'),
                    entry.get('auxiliary_name'),
                    entry.get('currency_code', 'CNY'),
                    entry.get('exchange_rate', 1),
                    entry.get('original_amount'),
                    entry.get('quantity'),
                    entry.get('unit_price'),
                    entry.get('department_code'),
                    entry.get('person_code'),
                    entry.get('project_code'),
                    entry.get('is_cash_flow', 0),
                    entry.get('cash_flow_code')
                ))
            
            conn.commit()
            conn.close()
            
            # 发送保存成功信号
            self.voucher_saved.emit(voucher_no)
            return True, voucher_no
            
        except sqlite3.IntegrityError as e:
            error_msg = f"凭证号重复或数据完整性错误: {str(e)}"
            self.voucher_error.emit(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"保存凭证时发生错误: {str(e)}"
            self.voucher_error.emit(error_msg)
            return False, error_msg
    
    def get_voucher_history(self, limit=20, filters: Dict = None) -> List[Dict]:
        """获取凭证历史（支持过滤）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
            SELECT vm.*, 
                   GROUP_CONCAT(vd.summary, '|') as summaries,
                   COUNT(vd.id) as entry_count
            FROM voucher_master vm
            LEFT JOIN voucher_details vd ON vm.id = vd.voucher_id
        '''
        
        conditions = []
        params = []
        
        if filters:
            if filters.get('voucher_date_from'):
                conditions.append("vm.voucher_date >= ?")
                params.append(filters['voucher_date_from'])
            if filters.get('voucher_date_to'):
                conditions.append("vm.voucher_date <= ?")
                params.append(filters['voucher_date_to'])
            if filters.get('accounting_period'):
                conditions.append("vm.accounting_period = ?")
                params.append(filters['accounting_period'])
            if filters.get('voucher_type'):
                conditions.append("vm.voucher_type = ?")
                params.append(filters['voucher_type'])
            if filters.get('status'):
                conditions.append("vm.status = ?")
                params.append(filters['status'])
            if filters.get('created_by'):
                conditions.append("vm.created_by = ?")
                params.append(filters['created_by'])
            if filters.get('voucher_no'):
                conditions.append("vm.voucher_no LIKE ?")
                params.append(f"%{filters['voucher_no']}%")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += '''
            GROUP BY vm.id
            ORDER BY vm.voucher_date DESC, vm.voucher_no DESC
            LIMIT ?
        '''
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            voucher_dict = dict(row)
            # 将摘要字符串转换回列表
            if voucher_dict['summaries']:
                voucher_dict['summaries'] = voucher_dict['summaries'].split('|')
            else:
                voucher_dict['summaries'] = []
            result.append(voucher_dict)
        
        conn.close()
        return result
    
    def get_voucher_detail(self, voucher_no: str) -> Dict:
        """获取凭证详细信息（包括所有分录）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 获取主表信息
        cursor.execute('SELECT * FROM voucher_master WHERE voucher_no = ?', (voucher_no,))
        master_row = cursor.fetchone()
        
        if not master_row:
            conn.close()
            return None
        
        voucher_data = dict(master_row)
        
        # 获取分录信息
        cursor.execute('''
            SELECT * FROM voucher_details 
            WHERE voucher_id = ? 
            ORDER BY line_no
        ''', (voucher_data['id'],))
        
        entries = []
        for row in cursor.fetchall():
            entries.append(dict(row))
        
        voucher_data['entries'] = entries
        
        conn.close()
        return voucher_data
    
    def update_voucher_status(self, voucher_no: str, status: str, auditor: str = None) -> bool:
        """更新凭证状态（如审核、记账等）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            update_data = {
                'status': status,
                'updated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if auditor and status in ['已审核', '已记账']:
                update_data['auditor'] = auditor
                update_data['auditor_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
            params = list(update_data.values())
            params.append(voucher_no)
            
            cursor.execute(f'''
                UPDATE voucher_master 
                SET {set_clause}
                WHERE voucher_no = ?
            ''', params)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新凭证状态失败: {e}")
            return False
    
    def delete_voucher(self, voucher_no: str) -> bool:
        """删除凭证（级联删除所有分录）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM voucher_master WHERE voucher_no = ?', (voucher_no,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除凭证失败: {e}")
            return False
    
    def get_voucher_statistics(self, start_date: str, end_date: str) -> Dict:
        """获取凭证统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_count,
                SUM(total_debit_amount) as total_debit,
                SUM(total_credit_amount) as total_credit,
                COUNT(DISTINCT created_by) as user_count
            FROM voucher_master
            WHERE voucher_date BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        result = cursor.fetchone()
        
        cursor.execute('''
            SELECT voucher_type, COUNT(*) as count
            FROM voucher_master
            WHERE voucher_date BETWEEN ? AND ?
            GROUP BY voucher_type
        ''', (start_date, end_date))
        
        type_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_count': result[0],
            'total_debit': result[1] or 0,
            'total_credit': result[2] or 0,
            'user_count': result[3] or 0,
            'type_distribution': dict(type_stats)
        }


# 使用示例
if __name__ == "__main__":
    manager = VoucherManager()
    
    # 示例：创建一个凭证
    voucher_data = {
        'voucher_type': '记账凭证',
        'voucher_date': '2023-12-15',
        'accounting_period': '2023-12',
        'attachment_count': 2,
        'remark': '测试凭证',
        'created_by': '张三',
        'entries': [
            {
                'line_no': 1,
                'summary': '提取现金',
                'subject_code': '1001',
                'subject_name': '现金',
                'debit_amount': 1000.00,
                'credit_amount': 0.00,
            },
            {
                'line_no': 2,
                'summary': '提取现金',
                'subject_code': '1002',
                'subject_name': '银行存款',
                'debit_amount': 0.00,
                'credit_amount': 1000.00,
            }
        ]
    }
    
    success, result = manager.save_voucher(voucher_data)
    if success:
        print(f"凭证保存成功！凭证号：{result}")
    else:
        print(f"凭证保存失败：{result}")
    
    # 查询历史凭证
    history = manager.get_voucher_history(limit=10)
    print(f"共查询到 {len(history)} 条凭证记录")