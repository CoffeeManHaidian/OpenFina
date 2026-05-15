"""Tests for get_general_ledger() in VoucherManager."""
import os
import sys
import tempfile
import sqlite3

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.voucher import VoucherManager


def _setup_bookset_db(db_path):
    """Create a minimal bookset database with subjects and voucher tables."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subject_code TEXT NOT NULL UNIQUE,
            subject_name TEXT NOT NULL,
            parent_code TEXT,
            level INTEGER NOT NULL DEFAULT 1,
            balance_direction TEXT DEFAULT '',
            is_leaf INTEGER NOT NULL DEFAULT 1,
            enabled INTEGER NOT NULL DEFAULT 1,
            sort_order INTEGER NOT NULL DEFAULT 0
        )
    """)
    # Insert test subjects
    conn.execute("""
        INSERT INTO subjects (category, subject_code, subject_name, level, balance_direction, is_leaf, enabled, sort_order)
        VALUES ('资产', '1001', '库存现金', 1, '借', 1, 1, 1)
    """)
    conn.execute("""
        INSERT INTO subjects (category, subject_code, subject_name, level, balance_direction, is_leaf, enabled, sort_order)
        VALUES ('资产', '1002', '银行存款', 1, '借', 1, 1, 2)
    """)
    conn.execute("""
        INSERT INTO subjects (category, subject_code, subject_name, parent_code, level, balance_direction, is_leaf, enabled, sort_order)
        VALUES ('负债', '2001', '短期借款', NULL, 1, '贷', 1, 1, 3)
    """)
    conn.commit()
    conn.close()

    # VoucherManager.__init__ will create voucher_master + voucher_details
    mgr = VoucherManager(db_path)
    return mgr


def _insert_posted_voucher(mgr, voucher_no, voucher_date, preparer, reviewer, poster, details):
    """Insert a posted voucher with details directly."""
    with mgr.get_connection() as conn:
        conn.execute("""
            INSERT INTO voucher_master (voucher_no, voucher_date, preparer, reviewer, poster)
            VALUES (?, ?, ?, ?, ?)
        """, (voucher_no, voucher_date, preparer, reviewer, poster))
        voucher_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for i, d in enumerate(details):
            conn.execute("""
                INSERT INTO voucher_details (voucher_id, line_no, account_code, account_name,
                    debit_amount, credit_amount, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (voucher_id, i + 1, d["account_code"], d["account_name"],
                  d.get("debit", 0.0), d.get("credit", 0.0), d.get("summary", "")))
    return voucher_id


def test_basic_current_period_amounts():
    """总分类账应正确汇总本期已过账凭证的借贷发生额"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 5000.00},
            {"account_code": "1002", "account_name": "银行存款", "credit": 5000.00},
        ])
        _insert_posted_voucher(mgr, "2026-01-0002", "2026-01-10", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 3000.00},
            {"account_code": "2001", "account_name": "短期借款", "credit": 3000.00},
        ])

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31")

        # Find 1001 (库存现金)
        cash = next(r for r in result if r["account_code"] == "1001")
        assert cash["current_debit"] == 8000.00, f"Expected 8000, got {cash['current_debit']}"
        assert cash["current_credit"] == 0.00, f"Expected 0, got {cash['current_credit']}"

        # Find 1002 (银行存款)
        bank = next(r for r in result if r["account_code"] == "1002")
        assert bank["current_debit"] == 0.00
        assert bank["current_credit"] == 5000.00

        # Find 2001 (短期借款)
        loan = next(r for r in result if r["account_code"] == "2001")
        assert loan["current_debit"] == 0.00
        assert loan["current_credit"] == 3000.00


def test_opening_balance_from_prior_period():
    """期初余额应统计本期开始前所有已过账凭证的累计"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        # 上期凭证 (2025-12)
        _insert_posted_voucher(mgr, "2025-12-0001", "2025-12-15", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 10000.00},
            {"account_code": "2001", "account_name": "短期借款", "credit": 10000.00},
        ])

        # 本期凭证 (2026-01)
        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 5000.00},
            {"account_code": "1002", "account_name": "银行存款", "credit": 5000.00},
        ])

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31")

        cash = next(r for r in result if r["account_code"] == "1001")
        assert cash["begin_debit"] == 10000.00, f"期初借方应为10000, got {cash['begin_debit']}"
        assert cash["begin_credit"] == 0.00
        assert cash["current_debit"] == 5000.00
        # 期末 = 10000 + 5000 = 15000 (借方)
        assert cash["end_debit"] == 15000.00, f"期末借方应为15000, got {cash['end_debit']}"
        assert cash["end_credit"] == 0.00

        loan = next(r for r in result if r["account_code"] == "2001")
        assert loan["begin_credit"] == 10000.00, f"期初贷方应为10000, got {loan['begin_credit']}"
        assert loan["begin_debit"] == 0.00
        assert loan["current_credit"] == 0.00
        assert loan["end_credit"] == 10000.00


def test_excludes_unposted_vouchers():
    """默认应排除未过账凭证"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        # 已过账
        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 1000.00},
            {"account_code": "1002", "account_name": "银行存款", "credit": 1000.00},
        ])

        # 未过账（只有制单人，无审核人/过账人）
        with mgr.get_connection() as conn:
            conn.execute("""
                INSERT INTO voucher_master (voucher_no, voucher_date, preparer)
                VALUES (?, ?, ?)
            """, ("2026-01-0002", "2026-01-10", "张三"))
            voucher_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute("""
                INSERT INTO voucher_details (voucher_id, line_no, account_code, account_name, debit_amount, credit_amount)
                VALUES (?, 1, '1001', '库存现金', 5000.00, 0.0)
            """, (voucher_id,))

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31")

        cash = next(r for r in result if r["account_code"] == "1001")
        assert cash["current_debit"] == 1000.00, f"只应统计已过账凭证, got {cash['current_debit']}"


def test_include_unposted_vouchers():
    """include_unposted=True 时应包含未过账凭证"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 1000.00},
        ])

        with mgr.get_connection() as conn:
            conn.execute("""
                INSERT INTO voucher_master (voucher_no, voucher_date, preparer)
                VALUES (?, ?, ?)
            """, ("2026-01-0002", "2026-01-10", "张三"))
            voucher_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute("""
                INSERT INTO voucher_details (voucher_id, line_no, account_code, account_name, debit_amount, credit_amount)
                VALUES (?, 1, '1001', '库存现金', 5000.00, 0.0)
            """, (voucher_id,))

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31", include_unposted=True)

        cash = next(r for r in result if r["account_code"] == "1001")
        assert cash["current_debit"] == 6000.00, f"应包含未过账凭证, got {cash['current_debit']}"


def test_subject_code_range_filter():
    """科目代码范围筛选"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 1000.00},
            {"account_code": "1002", "account_name": "银行存款", "credit": 500.00},
            {"account_code": "2001", "account_name": "短期借款", "credit": 500.00},
        ])

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31",
                                         subject_code_from="1001", subject_code_to="1002")

        codes = [r["account_code"] for r in result]
        assert "1001" in codes
        assert "1002" in codes
        assert "2001" not in codes


class TestLedgerCalculations:
    """测试总分类账的计算逻辑"""

    def test_totals_sum_correctly(self):
        from ui.general_ledger import compute_totals
        rows = [
            {"begin_debit": 100.0, "begin_credit": 0.0, "current_debit": 50.0, "current_credit": 30.0, "end_debit": 120.0, "end_credit": 0.0},
            {"begin_debit": 0.0, "begin_credit": 200.0, "current_debit": 0.0, "current_credit": 100.0, "end_debit": 0.0, "end_credit": 300.0},
        ]
        totals = compute_totals(rows)
        assert totals["begin_debit"] == 100.0
        assert totals["begin_credit"] == 200.0
        assert totals["current_debit"] == 50.0
        assert totals["current_credit"] == 130.0
        assert totals["end_debit"] == 120.0
        assert totals["end_credit"] == 300.0

    def test_totals_balanced_returns_true(self):
        from ui.general_ledger import compute_totals
        rows = [
            {"begin_debit": 500.0, "begin_credit": 500.0},
            {"current_debit": 300.0, "current_credit": 300.0},
            {"end_debit": 800.0, "end_credit": 800.0},
        ]
        totals = compute_totals(rows)
        assert abs(totals["begin_debit"] - totals["begin_credit"]) < 0.01
        assert abs(totals["current_debit"] - totals["current_credit"]) < 0.01
        assert abs(totals["end_debit"] - totals["end_credit"]) < 0.01

    def test_empty_rows_returns_zero_totals(self):
        from ui.general_ledger import compute_totals
        totals = compute_totals([])
        for v in totals.values():
            assert v == 0.0


def test_closing_balance_net_calculation():
    """期末余额 = 期初借-贷 + 本期借-贷；正数为借方余额，负数为贷方余额"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = _setup_bookset_db(db_path)

        # 上期: 1001 借100
        _insert_posted_voucher(mgr, "2025-12-0001", "2025-12-01", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "debit": 100.00},
        ])
        # 本期: 1001 贷80 (净借方余额20)
        _insert_posted_voucher(mgr, "2026-01-0001", "2026-01-05", "张三", "李四", "王五", [
            {"account_code": "1001", "account_name": "库存现金", "credit": 80.00},
        ])

        result = mgr.get_general_ledger("2026-01-01", "2026-01-31")
        cash = next(r for r in result if r["account_code"] == "1001")
        assert cash["begin_debit"] == 100.00
        assert cash["current_credit"] == 80.00
        assert cash["end_debit"] == 20.00, f"期末借方应为20, got {cash['end_debit']}"
        assert cash["end_credit"] == 0.00


if __name__ == "__main__":
    import traceback

    tests = [
        test_basic_current_period_amounts,
        test_opening_balance_from_prior_period,
        test_excludes_unposted_vouchers,
        test_include_unposted_vouchers,
        test_subject_code_range_filter,
        test_closing_balance_net_calculation,
    ]

    # Add TestLedgerCalculations methods
    calc = TestLedgerCalculations()
    tests.extend([
        calc.test_totals_sum_correctly,
        calc.test_totals_balanced_returns_true,
        calc.test_empty_rows_returns_zero_totals,
    ])

    failed = []
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except AssertionError as e:
            failed.append(test.__name__)
            print(f"FAIL: {test.__name__} — {e}")
        except Exception:
            failed.append(test.__name__)
            print(f"ERROR: {test.__name__}")
            traceback.print_exc()

    print(f"\n{len(tests) - len(failed)}/{len(tests)} passed, {len(failed)} failed")
    if failed:
        sys.exit(1)
