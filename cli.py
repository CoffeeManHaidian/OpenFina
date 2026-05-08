"""
OpenFina 命令行调试工具
========================

用法：
    python cli.py [--db PATH] [--json] <命令组> <子命令> [参数]

命令组：
    user         用户管理
    bookset      账套管理
    voucher      凭证管理
    subject      科目管理

示例：
    python cli.py user list
    python cli.py user create alice pass123 --role admin
    python cli.py user list --json
    python cli.py voucher list --start 2026-01-01 --end 2026-01-31
    python cli.py subject tree data/booksets/xxx.db
"""

import argparse
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------------------------
# 输出辅助
# ---------------------------------------------------------------------------

def _print_table(rows, columns):
    """打印对齐的文本表格。columns: {name: min_width}"""
    if not rows:
        print("(无数据)")
        return

    col_names = list(columns.keys())
    col_widths = []
    for name in col_names:
        max_w = max(len(str(row.get(name, ""))) for row in rows)
        col_widths.append(max(columns[name], max_w, len(name)))

    header = "  ".join(name.ljust(col_widths[i]) for i, name in enumerate(col_names))
    print(header)
    print("-" * len(header))

    for row in rows:
        line = "  ".join(
            str(row.get(name, "")).ljust(col_widths[i]) for i, name in enumerate(col_names)
        )
        print(line)

    print(f"\n共 {len(rows)} 条")


def _print_json(data):
    """以 JSON 格式输出。"""
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _output(rows, columns, use_json):
    if use_json:
        _print_json(rows)
    else:
        _print_table(rows, columns)


# ---------------------------------------------------------------------------
# 用户管理
# ---------------------------------------------------------------------------

def _add_user_commands(subparsers):
    user_parser = subparsers.add_parser("user", help="用户管理")
    user_parser.add_argument("--json", action="store_true", help="JSON 输出")
    user_sub = user_parser.add_subparsers(dest="user_cmd")

    # list
    p = user_sub.add_parser("list", help="列出所有用户")
    p.set_defaults(func=_cmd_user_list)

    # info
    p = user_sub.add_parser("info", help="查看用户详情")
    p.add_argument("username", help="用户名")
    p.set_defaults(func=_cmd_user_info)

    # create
    p = user_sub.add_parser("create", help="创建用户")
    p.add_argument("username", help="用户名")
    p.add_argument("password", help="密码")
    p.add_argument("--role", choices=["admin", "manager"], default="manager", help="角色 (默认 manager)")
    p.set_defaults(func=_cmd_user_create)

    # status
    p = user_sub.add_parser("status", help="启用/禁用用户")
    p.add_argument("user_id", type=int, help="用户ID")
    p.add_argument("status", choices=["active", "disabled"], help="目标状态")
    p.set_defaults(func=_cmd_user_status)

    # role
    p = user_sub.add_parser("role", help="切换用户角色")
    p.add_argument("user_id", type=int, help="用户ID")
    p.add_argument("role", choices=["admin", "manager"], help="目标角色")
    p.set_defaults(func=_cmd_user_role)

    # reset-pwd
    p = user_sub.add_parser("reset-pwd", help="重置用户密码")
    p.add_argument("user_id", type=int, help="用户ID")
    p.add_argument("--new-password", default="123456", help="新密码 (默认 123456)")
    p.set_defaults(func=_cmd_user_reset_pwd)

    # check-admin
    p = user_sub.add_parser("check-admin", help="检查是否存在管理员")
    p.set_defaults(func=_cmd_user_check_admin)


def _cmd_user_list(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    rows = mgr.list_all_users()
    for r in rows:
        r["role"] = "系统管理员" if r["role"] == "admin" else "财务主管"
        r["status"] = "正常" if r["status"] == "active" else "已禁用"
    _output(rows, {"id": 4, "username": 12, "role": 10, "status": 6, "bookset_count": 6, "created_at": 19}, args.json)


def _cmd_user_info(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    user = mgr.get_user_by_username(args.username)
    if user is None:
        print(f"用户 '{args.username}' 不存在", file=sys.stderr)
        sys.exit(1)
    _output([user], {"user_id": 8, "username": 12, "status": 8, "role": 8, "must_change_password": 6}, args.json)


def _cmd_user_create(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    try:
        user_id = mgr.register_user(args.username, args.password)
        if args.role == "admin":
            with mgr.get_connection() as conn:
                conn.execute(
                    "UPDATE users SET role = 'admin', must_change_password = 1 WHERE id = ?", (user_id,)
                )
        print(f"用户 '{args.username}' 创建成功 (ID={user_id}, 角色={args.role})")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def _cmd_user_status(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    try:
        mgr.update_user_status(args.user_id, args.status)
        label = "启用" if args.status == "active" else "禁用"
        print(f"用户 {args.user_id} 已{label}")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def _cmd_user_role(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    try:
        mgr.update_user_role(args.user_id, args.role)
        label = "系统管理员" if args.role == "admin" else "财务主管"
        print(f"用户 {args.user_id} 角色已切换为 {label}")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def _cmd_user_reset_pwd(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    mgr.reset_user_password(args.user_id, args.new_password)
    print(f"用户 {args.user_id} 密码已重置")


def _cmd_user_check_admin(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    if mgr.has_any_admin():
        print("存在系统管理员")
    else:
        print("无系统管理员")


# ---------------------------------------------------------------------------
# 账套管理
# ---------------------------------------------------------------------------

def _add_bookset_commands(subparsers):
    bs_parser = subparsers.add_parser("bookset", help="账套管理")
    bs_parser.add_argument("--json", action="store_true", help="JSON 输出")
    bs_sub = bs_parser.add_subparsers(dest="bookset_cmd")

    # list
    p = bs_sub.add_parser("list", help="列出用户绑定的账套")
    p.add_argument("user_id", type=int, help="用户ID")
    p.set_defaults(func=_cmd_bookset_list)

    # create
    p = bs_sub.add_parser("create", help="为用户创建账套")
    p.add_argument("user_id", type=int, help="用户ID")
    p.add_argument("enterprise_name", help="企业名称")
    p.add_argument("fiscal_year", type=int, help="会计年度")
    p.add_argument("--code", default="", help="企业编码")
    p.set_defaults(func=_cmd_bookset_create)

    # set-default
    p = bs_sub.add_parser("set-default", help="设置用户默认账套")
    p.add_argument("user_id", type=int, help="用户ID")
    p.add_argument("bookset_id", type=int, help="账套ID")
    p.set_defaults(func=_cmd_bookset_set_default)


def _cmd_bookset_list(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    rows = mgr.list_user_booksets(args.user_id)
    _output(rows, {"bookset_id": 10, "enterprise_name": 16, "fiscal_year": 8, "is_default": 6, "db_filename": 24}, args.json)


def _cmd_bookset_create(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    try:
        bookset = mgr.create_bookset_for_user(
            args.user_id, args.enterprise_name, args.fiscal_year, args.code
        )
        print(f"账套创建成功 (ID={bookset['bookset_id']}, 企业={args.enterprise_name}, 年度={args.fiscal_year})")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def _cmd_bookset_set_default(args):
    from models.bookset import UserBooksetManager
    mgr = UserBooksetManager(args.db)
    mgr.set_default_bookset(args.user_id, args.bookset_id)
    print(f"已将用户 {args.user_id} 的默认账套设为 {args.bookset_id}")


# ---------------------------------------------------------------------------
# 凭证管理
# ---------------------------------------------------------------------------

def _add_voucher_commands(subparsers):
    v_parser = subparsers.add_parser("voucher", help="凭证管理")
    v_parser.add_argument("--json", action="store_true", help="JSON 输出")
    v_sub = v_parser.add_subparsers(dest="voucher_cmd")

    # list
    p = v_sub.add_parser("list", help="查询凭证列表")
    p.add_argument("--db", dest="bookset_db", required=True, help="账套数据库路径")
    p.add_argument("--start", help="开始日期 (YYYY-MM-DD)")
    p.add_argument("--end", help="结束日期 (YYYY-MM-DD)")
    p.add_argument("--no", dest="voucher_no", help="凭证号模糊搜索")
    p.add_argument("--summary", dest="summary_keyword", help="摘要关键词")
    p.add_argument("--account", dest="account_keyword", help="科目关键词")
    p.set_defaults(func=_cmd_voucher_list)

    # get
    p = v_sub.add_parser("get", help="查看单张凭证")
    p.add_argument("--db", dest="bookset_db", required=True, help="账套数据库路径")
    p.add_argument("voucher_no", type=int, help="凭证号")
    p.set_defaults(func=_cmd_voucher_get)

    # summary
    p = v_sub.add_parser("summary", help="按科目汇总凭证")
    p.add_argument("--db", dest="bookset_db", required=True, help="账套数据库路径")
    p.add_argument("start_date", help="开始日期 (YYYY-MM-DD)")
    p.add_argument("end_date", help="结束日期 (YYYY-MM-DD)")
    p.set_defaults(func=_cmd_voucher_summary)

    # batch-cancel-post
    p = v_sub.add_parser("batch-cancel-post", help="批量取消过账（管理员）")
    p.add_argument("--db", dest="bookset_db", required=True, help="账套数据库路径")
    p.add_argument("start_date", help="开始日期 (YYYY-MM-DD)")
    p.add_argument("end_date", help="结束日期 (YYYY-MM-DD)")
    p.set_defaults(func=_cmd_voucher_batch_cancel_post)

    # batch-cancel-review
    p = v_sub.add_parser("batch-cancel-review", help="批量取消审核（管理员）")
    p.add_argument("--db", dest="bookset_db", required=True, help="账套数据库路径")
    p.add_argument("start_date", help="开始日期 (YYYY-MM-DD)")
    p.add_argument("end_date", help="结束日期 (YYYY-MM-DD)")
    p.set_defaults(func=_cmd_voucher_batch_cancel_review)


def _get_voucher_manager(bookset_db):
    from models.voucher import VoucherManager
    mgr = VoucherManager(bookset_db)
    mgr.set_current_user_role("admin")
    return mgr


def _cmd_voucher_list(args):
    mgr = _get_voucher_manager(args.bookset_db)
    rows = mgr.search_vouchers(
        start_date=args.start,
        end_date=args.end,
        voucher_no=args.voucher_no,
        summary_keyword=args.summary_keyword,
        account_keyword=args.account_keyword,
    )
    result = []
    for r in rows:
        d = dict(r)
        d.pop("voucher_id", None)
        result.append(d)
    _output(result, {
        "voucher_no": 14, "voucher_type": 8, "voucher_date": 10,
        "preparer": 8, "reviewer": 8, "poster": 8, "attention": 8,
        "attach_count": 4, "first_summary": 24,
    }, args.json)


def _cmd_voucher_get(args):
    mgr = _get_voucher_manager(args.bookset_db)
    voucher = mgr.search_voucher(args.voucher_no)
    if voucher is None:
        print(f"凭证号 {args.voucher_no} 不存在", file=sys.stderr)
        sys.exit(1)

    if args.json:
        _print_json({
            "header": {
                "voucher_no": voucher.voucher_no,
                "voucher_type": voucher.voucher_type,
                "voucher_date": voucher.voucher_date,
                "preparer": voucher.preparer,
                "reviewer": voucher.reviewer,
                "poster": voucher.poster,
                "attention": voucher.attention,
                "attach_count": voucher.attach_count,
            },
            "details": [
                {
                    "line_no": d.line_no,
                    "account_code": d.account_code,
                    "account_name": d.account_name,
                    "debit": d.debit_amount,
                    "credit": d.credit_amount,
                    "summary": d.summary,
                }
                for d in voucher.details
            ],
        })
        return

    print(f"凭证号: {voucher.voucher_no}    类型: {voucher.voucher_type or '-'}    日期: {voucher.voucher_date}")
    print(f"制单人: {voucher.preparer or '-'}    审核人: {voucher.reviewer or '-'}    过账人: {voucher.poster or '-'}")
    print(f"附件: {voucher.attach_count}    经办人: {voucher.attention or '-'}")
    print()
    print(f"{'行号':<4}  {'科目编码':<16}  {'科目名称':<20}  {'借方金额':>12}  {'贷方金额':>12}  {'摘要'}")
    print("-" * 90)
    for d in voucher.details:
        print(f"{d.line_no:<4}  {d.account_code:<16}  {d.account_name:<20}  {d.debit_amount:>12.2f}  {d.credit_amount:>12.2f}  {d.summary or ''}")


def _cmd_voucher_summary(args):
    mgr = _get_voucher_manager(args.bookset_db)
    rows = mgr.summary_subject(args.start_date, args.end_date)
    if not rows:
        print("(无数据)")
        return
    result = [{"parent_code": r["parent_code"], "total_debit": float(r["total_debit"]), "total_credit": float(r["total_credit"])} for r in rows]
    _output(result, {"parent_code": 12, "total_debit": 14, "total_credit": 14}, args.json)


def _cmd_voucher_batch_cancel_post(args):
    mgr = _get_voucher_manager(args.bookset_db)
    count = mgr.batch_cancel_post(args.start_date, args.end_date)
    print(f"已取消过账 {count} 条凭证 ({args.start_date} ~ {args.end_date})")


def _cmd_voucher_batch_cancel_review(args):
    mgr = _get_voucher_manager(args.bookset_db)
    count = mgr.batch_cancel_review(args.start_date, args.end_date)
    print(f"已取消审核 {count} 条凭证 ({args.start_date} ~ {args.end_date})")


# ---------------------------------------------------------------------------
# 科目管理
# ---------------------------------------------------------------------------

def _add_subject_commands(subparsers):
    s_parser = subparsers.add_parser("subject", help="科目管理")
    s_parser.add_argument("--json", action="store_true", help="JSON 输出")
    s_sub = s_parser.add_subparsers(dest="subject_cmd")

    # list
    p = s_sub.add_parser("list", help="列出所有科目")
    p.add_argument("db_path", help="账套数据库路径")
    p.set_defaults(func=_cmd_subject_list)

    # tree
    p = s_sub.add_parser("tree", help="按树形展示科目")
    p.add_argument("db_path", help="账套数据库路径")
    p.set_defaults(func=_cmd_subject_tree)

    # add
    p = s_sub.add_parser("add", help="添加下级科目")
    p.add_argument("db_path", help="账套数据库路径")
    p.add_argument("parent_code", help="父级科目编码")
    p.add_argument("name", help="科目名称")
    p.set_defaults(func=_cmd_subject_add)

    # delete
    p = s_sub.add_parser("delete", help="删除科目")
    p.add_argument("db_path", help="账套数据库路径")
    p.add_argument("code", help="科目编码")
    p.set_defaults(func=_cmd_subject_delete)


def _cmd_subject_list(args):
    from models.bookset import SubjectStore
    store = SubjectStore(args.db_path)
    rows = store.fetch_all()
    _output(rows, {"subject_code": 12, "subject_name": 20, "subject_level": 4, "balance_direction": 6}, args.json)


def _cmd_subject_tree(args):
    from models.bookset import SubjectStore
    store = SubjectStore(args.db_path)
    rows = store.get_tree_data()
    if args.json:
        _print_json(rows)
        return
    _print_subject_tree(rows)


def _print_subject_tree(nodes, indent=0):
    for node in nodes:
        code = node.get("subject_code", "")
        name = node.get("subject_name", "")
        print(f"{'  ' * indent}{code}  {name}")
        children = node.get("children", [])
        if children:
            _print_subject_tree(children, indent + 1)


def _cmd_subject_add(args):
    from models.bookset import SubjectStore
    store = SubjectStore(args.db_path)
    try:
        new_code = store.add_child_subject(args.parent_code, args.name)
        print(f"科目 '{args.name}' 添加成功，编码: {new_code}")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def _cmd_subject_delete(args):
    from models.bookset import SubjectStore
    store = SubjectStore(args.db_path)
    try:
        store.delete_subject(args.code)
        print(f"科目 {args.code} 已删除")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    from utils.path_helper import get_user_db_path

    parser = argparse.ArgumentParser(
        description="OpenFina 命令行调试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例: python cli.py user list   |   python cli.py voucher list --db data/booksets/xxx.db --start 2026-01-01",
    )
    parser.add_argument("--db", default=get_user_db_path(), help=f"用户数据库路径 (默认 {get_user_db_path()})")

    subparsers = parser.add_subparsers(dest="group", help="命令组")
    _add_user_commands(subparsers)
    _add_bookset_commands(subparsers)
    _add_voucher_commands(subparsers)
    _add_subject_commands(subparsers)

    args = parser.parse_args()

    if args.group is None:
        parser.print_help()
        sys.exit(1)

    handler = getattr(args, "func", None)
    if handler is None:
        # 子命令组未指定具体子命令
        for group_name in ["user", "bookset", "voucher", "subject"]:
            if getattr(args, f"{group_name}_cmd", None) is None and args.group == group_name:
                # Find the subparser and print help
                parser.print_help()
                sys.exit(1)
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
