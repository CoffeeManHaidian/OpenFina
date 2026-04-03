import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.bookset import UserBooksetManager
from models.data import Voucher, VoucherDetail
from models.voucher import VoucherManager
from utils.path_helper import get_user_db_path


SAMPLE_VOUCHERS = [
    {
        "voucher_no": "2026-01-0001",
        "voucher_type": "记账凭证",
        "voucher_date": "2026-01-05",
        "preparer": "alice",
        "reviewer": "审核员乙",
        "summary": "股东投入注册资本",
        "details": [
            ("1002", "银行存款", 500000.00, 0.00, "收到股东投资款"),
            ("4001", "实收资本", 0.00, 500000.00, "确认实收资本"),
        ],
    },
    {
        "voucher_no": "2026-01-0002",
        "voucher_type": "收款凭证",
        "voucher_date": "2026-01-18",
        "preparer": "alice",
        "reviewer": "",
        "summary": "取得短期借款",
        "details": [
            ("1002", "银行存款", 120000.00, 0.00, "收到银行短期借款"),
            ("2001", "短期借款", 0.00, 120000.00, "确认短期借款"),
        ],
    },
    {
        "voucher_no": "2026-02-0001",
        "voucher_type": "转账凭证",
        "voucher_date": "2026-02-03",
        "preparer": "alice",
        "reviewer": "审核员乙",
        "summary": "赊购原材料",
        "details": [
            ("1403", "原材料", 30000.00, 0.00, "采购包装材料入库"),
            ("2202", "应付帐款", 0.00, 30000.00, "形成供应商应付款"),
        ],
    },
    {
        "voucher_no": "2026-02-0002",
        "voucher_type": "支付凭证",
        "voucher_date": "2026-02-15",
        "preparer": "alice",
        "reviewer": "",
        "summary": "支付办公租金",
        "details": [
            ("6602", "管理费用", 8000.00, 0.00, "支付二月办公租金"),
            ("1002", "银行存款", 0.00, 8000.00, "银行转账支付租金"),
        ],
    },
    {
        "voucher_no": "2026-03-0001",
        "voucher_type": "转账凭证",
        "voucher_date": "2026-03-10",
        "preparer": "alice",
        "reviewer": "审核员乙",
        "summary": "计提管理人员工资",
        "details": [
            ("6602", "管理费用", 15000.00, 0.00, "计提三月管理人员工资"),
            ("2211", "应付职工薪酬", 0.00, 15000.00, "确认应付工资"),
        ],
    },
    {
        "voucher_no": "2026-03-0002",
        "voucher_type": "支付凭证",
        "voucher_date": "2026-03-15",
        "preparer": "alice",
        "reviewer": "",
        "summary": "发放管理人员工资",
        "details": [
            ("2211", "应付职工薪酬", 15000.00, 0.00, "冲减应付工资"),
            ("1002", "银行存款", 0.00, 15000.00, "银行代发工资"),
        ],
    },
    {
        "voucher_no": "2026-04-0001",
        "voucher_type": "收款凭证",
        "voucher_date": "2026-04-08",
        "preparer": "alice",
        "reviewer": "审核员乙",
        "summary": "销售商品并收款",
        "details": [
            ("1002", "银行存款", 46800.00, 0.00, "收到客户货款"),
            ("6001", "主营业务收入", 0.00, 45000.00, "确认销售收入"),
            ("2221", "应交税费", 0.00, 1800.00, "确认销项税额"),
        ],
    },
    {
        "voucher_no": "2026-04-0002",
        "voucher_type": "支付凭证",
        "voucher_date": "2026-04-12",
        "preparer": "alice",
        "reviewer": "",
        "summary": "支付市场推广费",
        "details": [
            ("6601", "销售费用", 5200.00, 0.00, "支付线上推广服务费"),
            ("1001", "库存现金", 0.00, 5200.00, "现金支付推广费"),
        ],
    },
    {
        "voucher_no": "2026-04-0003",
        "voucher_type": "支付凭证",
        "voucher_date": "2026-04-18",
        "preparer": "alice",
        "reviewer": "",
        "summary": "采购库存商品并付款",
        "details": [
            ("1406", "库存商品", 12000.00, 0.00, "采购成品一批"),
            ("1002", "银行存款", 0.00, 12000.00, "支付采购货款"),
        ],
    },
]


def build_voucher(sample):
    voucher = Voucher(
        voucher_no=sample["voucher_no"],
        voucher_type=sample["voucher_type"],
        voucher_date=sample["voucher_date"],
        attach_count=0,
        preparer=sample["preparer"],
        reviewer="",
        attention="测试数据",
        created_time=sample["voucher_date"],
    )
    for line_no, detail in enumerate(sample["details"], start=1):
        code, name, debit_amount, credit_amount, summary = detail
        voucher.details.append(
            VoucherDetail(
                line_no=line_no,
                account_code=code,
                account_name=name,
                debit_amount=debit_amount,
                credit_amount=credit_amount,
                summary=summary,
            )
        )
    return voucher


def main():
    parser = argparse.ArgumentParser(description="为 OpenFina 新结构账套生成测试凭证")
    parser.add_argument("--username", default="demo", help="目标用户名")
    parser.add_argument("--password", default="123456", help="若用户不存在，用该密码创建")
    parser.add_argument("--enterprise", default="OpenFina", help="企业名称")
    parser.add_argument("--year", type=int, default=2026, help="会计年度")
    parser.add_argument("--reset", action="store_true", help="先删除现有账套数据库，再重新生成测试数据")
    args = parser.parse_args()

    user_manager = UserBooksetManager(get_user_db_path())
    user = user_manager.get_user_by_username(args.username)
    if user is None:
        user_id, bookset = user_manager.create_user_with_bookset(
            username=args.username,
            password=args.password,
            enterprise_name=args.enterprise,
            fiscal_year=args.year,
        )
    else:
        user_id = user["user_id"]
        bookset = user_manager.create_bookset_for_user(
            user_id,
            enterprise_name=args.enterprise,
            fiscal_year=args.year,
            is_default=True,
        )

    db_path = Path(bookset["bookset_db_path"])
    if args.reset and db_path.exists():
        db_path.unlink()
        bookset = user_manager.create_bookset_for_user(
            user_id,
            enterprise_name=args.enterprise,
            fiscal_year=args.year,
            is_default=True,
        )
        db_path = Path(bookset["bookset_db_path"])

    manager = VoucherManager(str(db_path))
    created = 0
    skipped = 0

    for sample in SAMPLE_VOUCHERS:
        existing = manager.search_voucher(sample["voucher_no"])
        if existing is not None:
            skipped += 1
            continue

        voucher = build_voucher(sample)
        manager.save_voucher(voucher)
        created += 1

        if sample["reviewer"]:
            manager.review_voucher(sample["voucher_no"], sample["reviewer"], "auditor")

    print(f"db_path={db_path}")
    print(f"bookset_id={bookset['bookset_id']}")
    print(f"created={created}")
    print(f"skipped={skipped}")


if __name__ == "__main__":
    main()
