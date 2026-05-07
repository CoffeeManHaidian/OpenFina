import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import bcrypt

from models.voucher import VoucherManager
from utils.logger import get_logger, log_event
from utils.path_helper import (
    build_bookset_db_filename,
    get_bookset_db_path,
    get_subject_json_path,
    get_user_db_path,
)

logger = get_logger()
BOOKSET_SCHEMA_VERSION = "1.0"


class UserBooksetManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or get_user_db_path()
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            logger.exception("用户库事务执行失败")
            raise
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            if self._needs_reset(conn):
                log_event(logger, "检测到旧版用户库结构，重建用户库", db_path=self.db_path)
                conn.execute("DROP TABLE IF EXISTS user_booksets")
                conn.execute("DROP TABLE IF EXISTS booksets")
                conn.execute("DROP TABLE IF EXISTS users")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    role TEXT NOT NULL DEFAULT 'manager',
                    must_change_password INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS booksets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enterprise_name TEXT NOT NULL,
                    enterprise_code TEXT,
                    fiscal_year INTEGER NOT NULL,
                    db_filename TEXT UNIQUE NOT NULL,
                    archived INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_booksets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    bookset_id INTEGER NOT NULL,
                    is_default INTEGER NOT NULL DEFAULT 0,
                    last_used_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, bookset_id)
                )
                """
            )

            # Migrate existing users table — add role column if missing
            user_columns = {
                row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()
            }
            if "role" not in user_columns:
                conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'manager'")
                log_event(logger, "迁移用户表：添加 role 列")
            if "must_change_password" not in user_columns:
                conn.execute("ALTER TABLE users ADD COLUMN must_change_password INTEGER NOT NULL DEFAULT 0")
                log_event(logger, "迁移用户表：添加 must_change_password 列")

    def _needs_reset(self, conn):
        tables = {
            row["name"] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
        if "users" not in tables:
            return False

        user_columns = {
            row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()
        }
        expected_user_columns = {"id", "username", "password_hash", "status", "created_at"}
        if not expected_user_columns.issubset(user_columns):
            return True

        return not {"booksets", "user_booksets"}.issubset(tables)

    def hash_password(self, password):
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password, password_hash):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except Exception:
            return False

    def register_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                raise ValueError("用户名已存在")

            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, self.hash_password(password)),
            )
            user_id = cursor.lastrowid
            log_event(logger, "创建用户成功", user_id=user_id, username=username)
            return user_id

    def authenticate_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password_hash, status, role, must_change_password FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row is None:
                raise ValueError("用户不存在")
            if row["status"] != "active":
                raise ValueError("用户已停用")
            if not self.verify_password(password, row["password_hash"]):
                raise ValueError("用户名或密码错误")
            return {
                "user_id": row["id"],
                "username": row["username"],
                "role": row["role"],
                "must_change_password": bool(row["must_change_password"]),
            }

    def get_user_by_username(self, username):
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT id, username, status, role, must_change_password FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if row is None:
            return None
        return {
            "user_id": row["id"],
            "username": row["username"],
            "status": row["status"],
            "role": row["role"],
            "must_change_password": bool(row["must_change_password"]),
        }

    def create_user_with_bookset(self, username, password, enterprise_name, fiscal_year, enterprise_code=""):
        user_id = self.register_user(username, password)
        bookset = self.create_bookset_for_user(
            user_id,
            enterprise_name=enterprise_name,
            fiscal_year=fiscal_year,
            enterprise_code=enterprise_code,
            is_default=True,
        )
        return user_id, bookset

    def create_bookset_for_user(self, user_id, enterprise_name, fiscal_year, enterprise_code="", is_default=False):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, enterprise_name, enterprise_code, fiscal_year, db_filename
                FROM booksets
                WHERE enterprise_name = ? AND fiscal_year = ? AND archived = 0
                """,
                (enterprise_name, fiscal_year),
            )
            bookset_row = cursor.fetchone()

            if bookset_row is None:
                cursor.execute(
                    """
                    INSERT INTO booksets (enterprise_name, enterprise_code, fiscal_year, db_filename)
                    VALUES (?, ?, ?, ?)
                    """,
                    (enterprise_name, enterprise_code or None, fiscal_year, "__pending__.db"),
                )
                bookset_id = cursor.lastrowid
                db_filename = build_bookset_db_filename(enterprise_name, fiscal_year, bookset_id)
                cursor.execute(
                    "UPDATE booksets SET db_filename = ? WHERE id = ?",
                    (db_filename, bookset_id),
                )
                bookset = {
                    "bookset_id": bookset_id,
                    "enterprise_name": enterprise_name,
                    "enterprise_code": enterprise_code or "",
                    "fiscal_year": fiscal_year,
                    "db_filename": db_filename,
                }
                log_event(logger, "创建账套目录记录", user_id=user_id, bookset_id=bookset_id, db_filename=db_filename)
            else:
                bookset = {
                    "bookset_id": bookset_row["id"],
                    "enterprise_name": bookset_row["enterprise_name"],
                    "enterprise_code": bookset_row["enterprise_code"] or "",
                    "fiscal_year": bookset_row["fiscal_year"],
                    "db_filename": bookset_row["db_filename"],
                }

            cursor.execute(
                "SELECT id FROM user_booksets WHERE user_id = ? AND bookset_id = ?",
                (user_id, bookset["bookset_id"]),
            )
            link_row = cursor.fetchone()
            if link_row is None:
                if is_default:
                    cursor.execute("UPDATE user_booksets SET is_default = 0 WHERE user_id = ?", (user_id,))
                cursor.execute(
                    """
                    INSERT INTO user_booksets (user_id, bookset_id, is_default, last_used_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    (user_id, bookset["bookset_id"], 1 if is_default else 0),
                )
            elif is_default:
                cursor.execute("UPDATE user_booksets SET is_default = 0 WHERE user_id = ?", (user_id,))
                cursor.execute(
                    """
                    UPDATE user_booksets
                    SET is_default = 1, last_used_at = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND bookset_id = ?
                    """,
                    (user_id, bookset["bookset_id"]),
                )

        db_path = get_bookset_db_path(bookset["db_filename"])
        init_bookset_database(
            db_path,
            bookset_id=bookset["bookset_id"],
            enterprise_name=bookset["enterprise_name"],
            enterprise_code=bookset["enterprise_code"],
            fiscal_year=bookset["fiscal_year"],
        )
        bookset["bookset_db_path"] = db_path
        return bookset

    def list_user_booksets(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    b.id AS bookset_id,
                    b.enterprise_name,
                    b.enterprise_code,
                    b.fiscal_year,
                    b.db_filename,
                    ub.is_default,
                    ub.last_used_at
                FROM user_booksets ub
                JOIN booksets b ON b.id = ub.bookset_id
                WHERE ub.user_id = ? AND b.archived = 0
                ORDER BY ub.is_default DESC, ub.last_used_at DESC, b.fiscal_year DESC, b.id DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()

        return [self._row_to_bookset_dict(row) for row in rows]

    def get_preferred_bookset(self, user_id):
        booksets = self.list_user_booksets(user_id)
        return booksets[0] if booksets else None

    def set_default_bookset(self, user_id, bookset_id):
        with self.get_connection() as conn:
            conn.execute("UPDATE user_booksets SET is_default = 0 WHERE user_id = ?", (user_id,))
            conn.execute(
                "UPDATE user_booksets SET is_default = 1 WHERE user_id = ? AND bookset_id = ?",
                (user_id, bookset_id),
            )
        log_event(logger, "更新默认账套", user_id=user_id, bookset_id=bookset_id)

    def mark_bookset_used(self, user_id, bookset_id):
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE user_booksets
                SET last_used_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND bookset_id = ?
                """,
                (user_id, bookset_id),
            )
        log_event(logger, "更新最近使用账套", user_id=user_id, bookset_id=bookset_id)

    def get_user_context(self, user_id, username, bookset_id=None):
        if bookset_id is None:
            bookset = self.get_preferred_bookset(user_id)
        else:
            bookset = next((item for item in self.list_user_booksets(user_id) if item["bookset_id"] == bookset_id), None)
            if bookset is None:
                bookset = self.get_preferred_bookset(user_id)

        if bookset is None:
            raise ValueError("当前用户未绑定任何账套")

        self.mark_bookset_used(user_id, bookset["bookset_id"])

        # Read role from users table
        with self.get_connection() as conn:
            user_row = conn.execute(
                "SELECT role, must_change_password FROM users WHERE id = ?", (user_id,)
            ).fetchone()

        return {
            "username": username,
            "user_id": user_id,
            "role": user_row["role"] if user_row else "manager",
            "must_change_password": bool(user_row["must_change_password"]) if user_row else False,
            "bookset_id": bookset["bookset_id"],
            "enterprise_name": bookset["enterprise_name"],
            "company": bookset["enterprise_name"],
            "fiscal_year": bookset["fiscal_year"],
            "bookset_db_path": bookset["bookset_db_path"],
            "db_filename": bookset["db_filename"],
        }

    def get_user_bookset_count(self, user_id):
        return len(self.list_user_booksets(user_id))

    def has_any_admin(self):
        """Check if any admin user exists."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(1) AS cnt FROM users WHERE role = 'admin' AND status = 'active'"
            ).fetchone()
            return row["cnt"] > 0

    def list_all_users(self):
        """List all users with their roles (admin only)."""
        with self.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT u.id, u.username, u.status, u.role, u.must_change_password, u.created_at,
                       COUNT(ub.id) AS bookset_count
                FROM users u
                LEFT JOIN user_booksets ub ON ub.user_id = u.id
                GROUP BY u.id
                ORDER BY u.role DESC, u.created_at DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def update_user_status(self, user_id, status):
        """Enable or disable a user account."""
        if status not in ("active", "disabled"):
            raise ValueError("无效的用户状态")
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE users SET status = ? WHERE id = ?", (status, user_id)
            )
        log_event(logger, "更新用户状态", user_id=user_id, status=status)

    def update_user_role(self, user_id, role):
        """Change a user's role."""
        if role not in ("admin", "manager"):
            raise ValueError("无效的角色")
        with self.get_connection() as conn:
            if role == "manager":
                admin_count = conn.execute(
                    "SELECT COUNT(1) FROM users WHERE role = 'admin' AND status = 'active' AND id != ?",
                    (user_id,),
                ).fetchone()[0]
                if admin_count == 0:
                    raise ValueError("不能移除最后一个系统管理员")
            conn.execute(
                "UPDATE users SET role = ? WHERE id = ?", (role, user_id)
            )
        log_event(logger, "更新用户角色", user_id=user_id, role=role)

    def reset_user_password(self, user_id, new_password):
        """Reset a user's password and force change on next login."""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ?, must_change_password = 1 WHERE id = ?",
                (self.hash_password(new_password), user_id),
            )
        log_event(logger, "重置用户密码", user_id=user_id)

    def change_own_password(self, user_id, old_password, new_password):
        """Change own password with old password verification."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT password_hash FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row is None:
                raise ValueError("用户不存在")
            if not self.verify_password(old_password, row["password_hash"]):
                raise ValueError("原密码错误")
            conn.execute(
                "UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?",
                (self.hash_password(new_password), user_id),
            )
        log_event(logger, "用户修改密码", user_id=user_id)

    def _row_to_bookset_dict(self, row):
        db_filename = row["db_filename"]
        return {
            "bookset_id": row["bookset_id"],
            "enterprise_name": row["enterprise_name"],
            "enterprise_code": row["enterprise_code"] or "",
            "fiscal_year": row["fiscal_year"],
            "db_filename": db_filename,
            "bookset_db_path": get_bookset_db_path(db_filename),
            "is_default": bool(row["is_default"]),
            "last_used_at": row["last_used_at"],
        }


def init_bookset_database(db_path, bookset_id, enterprise_name, enterprise_code, fiscal_year):
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bookset_info (
                bookset_id INTEGER PRIMARY KEY,
                enterprise_name TEXT NOT NULL,
                enterprise_code TEXT,
                fiscal_year INTEGER NOT NULL,
                schema_version TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
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
            """
        )
        conn.execute(
            """
            INSERT OR REPLACE INTO bookset_info
            (bookset_id, enterprise_name, enterprise_code, fiscal_year, schema_version)
            VALUES (?, ?, ?, ?, ?)
            """,
            (bookset_id, enterprise_name, enterprise_code or None, fiscal_year, BOOKSET_SCHEMA_VERSION),
        )

        subject_count = conn.execute("SELECT COUNT(1) FROM subjects").fetchone()[0]
        if subject_count == 0:
            _import_subject_template(conn, get_subject_json_path())
        conn.commit()
    finally:
        conn.close()

    VoucherManager(db_path)
    log_event(
        logger,
        "初始化账套数据库完成",
        db_path=db_path,
        bookset_id=bookset_id,
        enterprise_name=enterprise_name,
        fiscal_year=fiscal_year,
    )


def _import_subject_template(conn, json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    sort_order = 0
    for category, subjects in data.items():
        for subject in subjects:
            sort_order += 1
            children = subject.get("subjects", [])
            rows.append(
                (
                    category,
                    subject["code"],
                    subject["name"],
                    None,
                    1,
                    "",
                    0 if children else 1,
                    1,
                    sort_order,
                )
            )
            for child in children:
                sort_order += 1
                rows.append(
                    (
                        category,
                        child["code"],
                        child["name"],
                        subject["code"],
                        2,
                        "",
                        1,
                        1,
                        sort_order,
                    )
                )

    conn.executemany(
        """
        INSERT INTO subjects
        (category, subject_code, subject_name, parent_code, level, balance_direction, is_leaf, enabled, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


class SubjectStore:
    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            logger.exception("科目库事务执行失败")
            raise
        finally:
            conn.close()

    def fetch_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT category, subject_code, subject_name, parent_code, level, is_leaf, enabled, sort_order
                FROM subjects
                WHERE enabled = 1
                ORDER BY category, sort_order, subject_code
                """
            )
            return cursor.fetchall()

    def get_name(self, code):
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT subject_name FROM subjects WHERE subject_code = ? AND enabled = 1",
                (code,),
            ).fetchone()
            return row["subject_name"] if row else f"未找到 code: {code}"

    def get_tree_data(self):
        rows = self.fetch_all()
        grouped = {}
        parents = {}
        for row in rows:
            category = row["category"]
            grouped.setdefault(category, [])
            subject = {
                "code": row["subject_code"],
                "name": row["subject_name"],
            }
            if row["parent_code"]:
                parent = parents.get(row["parent_code"])
                if parent is not None:
                    parent.setdefault("subjects", []).append(subject)
            else:
                grouped[category].append(subject)
                parents[row["subject_code"]] = subject
        return grouped

    def add_child_subject(self, parent_code, subject_name):
        with self.get_connection() as conn:
            parent = conn.execute(
                """
                SELECT category, subject_code, level
                FROM subjects
                WHERE subject_code = ? AND enabled = 1
                """,
                (parent_code,),
            ).fetchone()
            if parent is None:
                raise ValueError("父级科目不存在")
            if parent["level"] != 1:
                raise ValueError("只能在一级科目下新增子科目")

            last_child = conn.execute(
                """
                SELECT subject_code
                FROM subjects
                WHERE parent_code = ?
                ORDER BY subject_code DESC
                LIMIT 1
                """,
                (parent_code,),
            ).fetchone()
            next_index = 1
            if last_child:
                suffix = last_child["subject_code"].split(".")[-1]
                next_index = int(suffix) + 1

            new_code = f"{parent_code}.{next_index:02d}"
            sort_row = conn.execute("SELECT COALESCE(MAX(sort_order), 0) AS value FROM subjects").fetchone()
            sort_order = (sort_row["value"] or 0) + 1
            conn.execute(
                """
                INSERT INTO subjects
                (category, subject_code, subject_name, parent_code, level, is_leaf, enabled, sort_order)
                VALUES (?, ?, ?, ?, 2, 1, 1, ?)
                """,
                (parent["category"], new_code, subject_name, parent_code, sort_order),
            )
            conn.execute(
                "UPDATE subjects SET is_leaf = 0 WHERE subject_code = ?",
                (parent_code,),
            )
            log_event(logger, "新增账套科目", db_path=self.db_path, parent_code=parent_code, code=new_code, name=subject_name)
            return new_code

    def delete_subject(self, subject_code):
        with self.get_connection() as conn:
            subject = conn.execute(
                """
                SELECT parent_code, subject_name
                FROM subjects
                WHERE subject_code = ? AND enabled = 1
                """,
                (subject_code,),
            ).fetchone()
            if subject is None:
                raise ValueError("科目不存在")

            child = conn.execute(
                "SELECT 1 FROM subjects WHERE parent_code = ? AND enabled = 1 LIMIT 1",
                (subject_code,),
            ).fetchone()
            if child:
                raise ValueError("该科目下还有子科目，不能删除")

            conn.execute("DELETE FROM subjects WHERE subject_code = ?", (subject_code,))
            if subject["parent_code"]:
                sibling = conn.execute(
                    "SELECT 1 FROM subjects WHERE parent_code = ? AND enabled = 1 LIMIT 1",
                    (subject["parent_code"],),
                ).fetchone()
                if sibling is None:
                    conn.execute(
                        "UPDATE subjects SET is_leaf = 1 WHERE subject_code = ?",
                        (subject["parent_code"],),
                    )
            log_event(logger, "删除账套科目", db_path=self.db_path, code=subject_code, name=subject["subject_name"])
