"""Tests for admin user management methods in UserBooksetManager."""
import os
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.bookset import UserBooksetManager


def test_has_any_admin_returns_false_when_no_admin():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        assert mgr.has_any_admin() is False


def test_has_any_admin_returns_true_after_creating_admin():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        mgr.register_user("admin", "pass123")
        with mgr.get_connection() as conn:
            conn.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
        assert mgr.has_any_admin() is True


def test_has_any_admin_ignores_disabled_admin():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        mgr.register_user("admin", "pass123")
        with mgr.get_connection() as conn:
            conn.execute("UPDATE users SET role = 'admin', status = 'disabled' WHERE username = 'admin'")
        assert mgr.has_any_admin() is False


def test_list_all_users_returns_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        mgr.register_user("user1", "pass")
        mgr.register_user("user2", "pass")
        users = mgr.list_all_users()
        assert len(users) == 2
        assert users[0]["username"] in ("user1", "user2")


def test_list_all_users_includes_role_and_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        mgr.register_user("testuser", "pass")
        with mgr.get_connection() as conn:
            conn.execute("UPDATE users SET role = 'admin' WHERE username = 'testuser'")
        users = mgr.list_all_users()
        assert users[0]["role"] == "admin"
        assert users[0]["status"] == "active"


def test_update_user_status_enables_and_disables():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "pass")
        mgr.update_user_status(user_id, "disabled")
        user = mgr.get_user_by_username("testuser")
        assert user["status"] == "disabled"
        mgr.update_user_status(user_id, "active")
        user = mgr.get_user_by_username("testuser")
        assert user["status"] == "active"


def test_update_user_role_upgrades_to_admin():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "pass")
        # Default role is manager, upgrade to admin
        mgr.update_user_role(user_id, "admin")
        user = mgr.get_user_by_username("testuser")
        assert user["role"] == "admin"


def test_update_user_role_refuses_removing_last_admin():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("admin", "pass")
        with mgr.get_connection() as conn:
            conn.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        try:
            mgr.update_user_role(user_id, "manager")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "最后一个系统管理员" in str(e)


def test_update_user_role_allows_demoting_if_another_admin_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        u1 = mgr.register_user("admin1", "pass")
        u2 = mgr.register_user("admin2", "pass")
        with mgr.get_connection() as conn:
            conn.execute("UPDATE users SET role = 'admin' WHERE id = ?", (u1,))
            conn.execute("UPDATE users SET role = 'admin' WHERE id = ?", (u2,))
        mgr.update_user_role(u1, "manager")
        user = mgr.get_user_by_username("admin1")
        assert user["role"] == "manager"


def test_reset_user_password_forces_change_flag():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "oldpass")
        mgr.reset_user_password(user_id, "newpass")
        user = mgr.get_user_by_username("testuser")
        assert user["must_change_password"] is True
        # Verify new password works
        auth_result = mgr.authenticate_user("testuser", "newpass")
        assert auth_result["user_id"] == user_id


def test_change_own_password_succeeds_with_correct_old_password():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "oldpass")
        mgr.change_own_password(user_id, "oldpass", "newpass")
        # Verify old password no longer works
        try:
            mgr.authenticate_user("testuser", "oldpass")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        # Verify new password works
        auth_result = mgr.authenticate_user("testuser", "newpass")
        assert auth_result["user_id"] == user_id
        # Verify must_change_password is cleared
        user = mgr.get_user_by_username("testuser")
        assert user["must_change_password"] is False


def test_change_own_password_rejects_wrong_old_password():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "oldpass")
        try:
            mgr.change_own_password(user_id, "wrongpass", "newpass")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "原密码错误" in str(e)


def test_update_user_status_rejects_invalid_status():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "pass")
        try:
            mgr.update_user_status(user_id, "deleted")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "无效的用户状态" in str(e)


def test_update_user_role_rejects_invalid_role():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        mgr = UserBooksetManager(db_path)
        user_id = mgr.register_user("testuser", "pass")
        try:
            mgr.update_user_role(user_id, "superadmin")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "无效的角色" in str(e)


if __name__ == "__main__":
    import traceback

    tests = [
        test_has_any_admin_returns_false_when_no_admin,
        test_has_any_admin_returns_true_after_creating_admin,
        test_has_any_admin_ignores_disabled_admin,
        test_list_all_users_returns_list,
        test_list_all_users_includes_role_and_status,
        test_update_user_status_enables_and_disables,
        test_update_user_role_upgrades_to_admin,
        test_update_user_role_refuses_removing_last_admin,
        test_update_user_role_allows_demoting_if_another_admin_exists,
        test_reset_user_password_forces_change_flag,
        test_change_own_password_succeeds_with_correct_old_password,
        test_change_own_password_rejects_wrong_old_password,
        test_update_user_status_rejects_invalid_status,
        test_update_user_role_rejects_invalid_role,
    ]

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
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
