import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.bookset import UserBooksetManager
from models.data import Voucher, VoucherDetail
from models.voucher import VoucherManager
from utils.path_helper import get_user_db_path


TEST_PASSWORD = "123456"


SCENARIOS = [
    {
        "username": "v2multi",
        "enterprise_name": "星河零售",
        "fiscal_year": 2026,
        "is_default": True,
        "vouchers": [
            {
                "voucher_no": "2026-01-0001",
                "voucher_type": "记账凭证",
                "voucher_date": "2026-01-03",
                "preparer": "李会计",
                "summary": "投资人投入启动资金",
                "status": "posted",
                "details": [
                    ("1002", "银行存款", 300000.00, 0.00, "收到投资款"),
                    ("4001", "实收资本", 0.00, 300000.00, "确认实收资本"),
                ],
            },
            {
                "voucher_no": "2026-01-0002",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-01-15",
                "preparer": "李会计",
                "summary": "赊购一批库存商品",
                "status": "reviewed",
                "details": [
                    ("1406", "库存商品", 48000.00, 0.00, "采购春季商品"),
                    ("2202", "应付帐款", 0.00, 48000.00, "形成供应商应付款"),
                ],
            },
            {
                "voucher_no": "2026-02-0001",
                "voucher_type": "收款凭证",
                "voucher_date": "2026-02-08",
                "preparer": "李会计",
                "summary": "门店销售并收款",
                "status": "posted",
                "details": [
                    ("1002", "银行存款", 93600.00, 0.00, "收到门店销售货款"),
                    ("6001", "主营业务收入", 0.00, 90000.00, "确认销售收入"),
                    ("2221", "应交税费", 0.00, 3600.00, "确认销项税额"),
                ],
            },
            {
                "voucher_no": "2026-02-0002",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-02-28",
                "preparer": "李会计",
                "summary": "结转本月销售成本",
                "status": "reviewed",
                "details": [
                    ("5401", "主营业务成本", 32000.00, 0.00, "结转已售商品成本"),
                    ("1406", "库存商品", 0.00, 32000.00, "冲减库存商品"),
                ],
            },
            {
                "voucher_no": "2026-03-0001",
                "voucher_type": "支付凭证",
                "voucher_date": "2026-03-05",
                "preparer": "李会计",
                "summary": "支付商场租金和物业费",
                "status": "draft",
                "details": [
                    ("6601", "销售费用", 12000.00, 0.00, "支付商场租金"),
                    ("6602", "管理费用", 3000.00, 0.00, "支付物业管理费"),
                    ("1002", "银行存款", 0.00, 15000.00, "银行转账支付"),
                ],
            },
            {
                "voucher_no": "2026-04-0001",
                "voucher_type": "支付凭证",
                "voucher_date": "2026-04-18",
                "preparer": "李会计",
                "summary": "支付导购工资",
                "status": "draft",
                "details": [
                    ("6601", "销售费用", 18000.00, 0.00, "支付导购工资"),
                    ("1002", "银行存款", 0.00, 18000.00, "银行代发工资"),
                ],
            },
        ],
    },
    {
        "username": "v2multi",
        "enterprise_name": "远航服务",
        "fiscal_year": 2025,
        "is_default": False,
        "vouchers": [
            {
                "voucher_no": "2025-06-0001",
                "voucher_type": "收款凭证",
                "voucher_date": "2025-06-02",
                "preparer": "王会计",
                "summary": "收到项目实施首付款",
                "status": "posted",
                "details": [
                    ("1002", "银行存款", 159000.00, 0.00, "收到客户项目首付款"),
                    ("6001", "主营业务收入", 0.00, 150000.00, "确认服务收入"),
                    ("2221", "应交税费", 0.00, 9000.00, "确认销项税额"),
                ],
            },
            {
                "voucher_no": "2025-06-0002",
                "voucher_type": "支付凭证",
                "voucher_date": "2025-06-06",
                "preparer": "王会计",
                "summary": "支付办公场地租金",
                "status": "posted",
                "details": [
                    ("6602", "管理费用", 20000.00, 0.00, "支付办公租金"),
                    ("1002", "银行存款", 0.00, 20000.00, "银行付款"),
                ],
            },
            {
                "voucher_no": "2025-07-0001",
                "voucher_type": "转账凭证",
                "voucher_date": "2025-07-01",
                "preparer": "王会计",
                "summary": "计提顾问团队工资",
                "status": "reviewed",
                "details": [
                    ("6602", "管理费用", 36000.00, 0.00, "计提项目团队工资"),
                    ("2211", "应付职工薪酬", 0.00, 36000.00, "确认应付工资"),
                ],
            },
            {
                "voucher_no": "2025-07-0002",
                "voucher_type": "支付凭证",
                "voucher_date": "2025-07-05",
                "preparer": "王会计",
                "summary": "发放顾问团队工资",
                "status": "draft",
                "details": [
                    ("2211", "应付职工薪酬", 36000.00, 0.00, "冲减应付工资"),
                    ("1002", "银行存款", 0.00, 36000.00, "发放工资"),
                ],
            },
            {
                "voucher_no": "2025-08-0001",
                "voucher_type": "支付凭证",
                "voucher_date": "2025-08-20",
                "preparer": "王会计",
                "summary": "报销差旅及交通费用",
                "status": "draft",
                "details": [
                    ("6602", "管理费用", 6800.00, 0.00, "差旅报销"),
                    ("1001", "库存现金", 0.00, 6800.00, "现金支付报销款"),
                ],
            },
        ],
    },
    {
        "username": "v2multi",
        "enterprise_name": "山川制造",
        "fiscal_year": 2026,
        "is_default": False,
        "vouchers": [
            {
                "voucher_no": "2026-03-0001",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-03-04",
                "preparer": "赵会计",
                "summary": "采购原材料入库",
                "status": "posted",
                "details": [
                    ("1403", "原材料", 85000.00, 0.00, "采购钢材入库"),
                    ("2202", "应付帐款", 0.00, 85000.00, "形成应付货款"),
                ],
            },
            {
                "voucher_no": "2026-03-0002",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-03-18",
                "preparer": "赵会计",
                "summary": "领用原材料投入生产",
                "status": "reviewed",
                "details": [
                    ("5001", "生产成本", 42000.00, 0.00, "投入产品生产"),
                    ("1403", "原材料", 0.00, 42000.00, "领用原材料"),
                ],
            },
            {
                "voucher_no": "2026-03-0003",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-03-28",
                "preparer": "赵会计",
                "summary": "结转完工产品入库",
                "status": "draft",
                "details": [
                    ("1406", "库存商品", 61000.00, 0.00, "完工产品入库"),
                    ("5001", "生产成本", 0.00, 61000.00, "结转生产成本"),
                ],
            },
            {
                "voucher_no": "2026-04-0001",
                "voucher_type": "收款凭证",
                "voucher_date": "2026-04-12",
                "preparer": "赵会计",
                "summary": "销售设备并收到货款",
                "status": "posted",
                "details": [
                    ("1002", "银行存款", 234000.00, 0.00, "收到销售回款"),
                    ("6001", "主营业务收入", 0.00, 220000.00, "确认设备销售收入"),
                    ("2221", "应交税费", 0.00, 14000.00, "确认销项税额"),
                ],
            },
            {
                "voucher_no": "2026-04-0002",
                "voucher_type": "转账凭证",
                "voucher_date": "2026-04-13",
                "preparer": "赵会计",
                "summary": "结转已售设备成本",
                "status": "reviewed",
                "details": [
                    ("5401", "主营业务成本", 92000.00, 0.00, "结转销售成本"),
                    ("1406", "库存商品", 0.00, 92000.00, "冲减库存商品"),
                ],
            },
        ],
    },
    {
        "username": "v2single",
        "enterprise_name": "启明科技",
        "fiscal_year": 2026,
        "is_default": True,
        "vouchers": [
            {
                "voucher_no": "2026-02-0001",
                "voucher_type": "记账凭证",
                "voucher_date": "2026-02-01",
                "preparer": "陈会计",
                "summary": "创始团队投入资金",
                "status": "posted",
                "details": [
                    ("1002", "银行存款", 600000.00, 0.00, "收到创业启动资金"),
                    ("4001", "实收资本", 0.00, 600000.00, "确认实收资本"),
                ],
            },
            {
                "voucher_no": "2026-02-0002",
                "voucher_type": "支付凭证",
                "voucher_date": "2026-02-10",
                "preparer": "陈会计",
                "summary": "购买研发设备",
                "status": "reviewed",
                "details": [
                    ("1406", "库存商品", 68000.00, 0.00, "购买测试设备"),
                    ("1002", "银行存款", 0.00, 68000.00, "支付设备款"),
                ],
            },
            {
                "voucher_no": "2026-03-0001",
                "voucher_type": "收款凭证",
                "voucher_date": "2026-03-16",
                "preparer": "陈会计",
                "summary": "收到软件开发项目款",
                "status": "draft",
                "details": [
                    ("1002", "银行存款", 53000.00, 0.00, "收到项目回款"),
                    ("6001", "主营业务收入", 0.00, 50000.00, "确认软件收入"),
                    ("2221", "应交税费", 0.00, 3000.00, "确认销项税额"),
                ],
            },
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
        reviewer_account="",
        poster="",
        poster_account="",
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


def ensure_user(user_manager, username):
    user = user_manager.get_user_by_username(username)
    if user is not None:
        return user["user_id"]
    return user_manager.register_user(username, TEST_PASSWORD)


def main():
    user_manager = UserBooksetManager(get_user_db_path())
    created_users = set()
    created_booksets = []
    created_vouchers = 0
    skipped_vouchers = 0

    for scenario in SCENARIOS:
        user_id = ensure_user(user_manager, scenario["username"])
        created_users.add(scenario["username"])

        bookset = user_manager.create_bookset_for_user(
            user_id=user_id,
            enterprise_name=scenario["enterprise_name"],
            fiscal_year=scenario["fiscal_year"],
            is_default=scenario["is_default"],
        )
        created_booksets.append(
            f"{scenario['username']} -> {bookset['enterprise_name']} {bookset['fiscal_year']} ({bookset['bookset_db_path']})"
        )

        manager = VoucherManager(bookset["bookset_db_path"])

        for sample in scenario["vouchers"]:
            existing = manager.search_voucher(sample["voucher_no"])
            if existing is not None:
                skipped_vouchers += 1
                continue

            voucher = build_voucher(sample)
            manager.save_voucher(voucher)
            created_vouchers += 1

            if sample["status"] in {"reviewed", "posted"}:
                manager.review_voucher(sample["voucher_no"], "审核员周", "auditor")
            if sample["status"] == "posted":
                manager.post_voucher(sample["voucher_no"], "过账员吴", "poster")

    print("users=" + ", ".join(sorted(created_users)))
    print("default_password=" + TEST_PASSWORD)
    print("booksets:")
    for item in created_booksets:
        print("  - " + item)
    print(f"created_vouchers={created_vouchers}")
    print(f"skipped_vouchers={skipped_vouchers}")


if __name__ == "__main__":
    main()
