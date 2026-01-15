# models.py
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class VoucherDetail:
    """凭证分录"""
    detail_id: Optional[int] = None
    voucher_id: int = None
    line_no: int = 0  # 行号
    account_code: str = ""  # 科目编码
    account_name: str = ""  # 科目名称
    debit_amount: float = 0.0  # 借方金额
    credit_amount: float = 0.0  # 贷方金额
    summary: str = ""  # 摘要
    auxiliary: Optional[str] = None  # 辅助核算

@dataclass
class Voucher:
    """凭证主表"""
    voucher_id: Optional[int] = None
    voucher_no: str = ""  # 凭证号
    voucher_type: str = ""  # 凭证类型
    voucher_date: date = None  # 凭证时间
    attach_count: int = 0  # 附件张数
    preparer: str = ""  # 制单人
    reviewer: str = ""  # 审核人
    attention: str = ""  # 经办人
    created_time: date = None  # 创建\修改时间
    details: List[VoucherDetail] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = []

