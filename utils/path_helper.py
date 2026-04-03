"""路径处理工具模块 - 统一开发环境和 PyInstaller 打包环境的路径行为。"""
import os
import sys
import re

from utils.logger import get_logger, log_db_path

# 获取日志记录器
logger = get_logger()


def get_app_dir():
    """获取可写应用目录。开发环境为项目根目录，打包环境为 exe 所在目录。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bundle_dir():
    """获取打包资源所在目录。PyInstaller 打包后优先使用 _MEIPASS。"""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return get_app_dir()


def ensure_dir(path):
    """确保目录存在。"""
    os.makedirs(path, exist_ok=True)
    return path


def get_data_dir():
    """获取 data 目录路径。"""
    return ensure_dir(os.path.join(get_app_dir(), "data"))


def get_booksets_dir():
    """获取账套数据库目录。"""
    return ensure_dir(os.path.join(get_data_dir(), "booksets"))


def get_resource_dir():
    """获取资源目录路径。"""
    return get_bundle_dir()


def get_db_path(db_name):
    """
    获取数据库文件的完整路径
    
    Args:
        db_name: 数据库文件名（如 'users.db'）
    
    Returns:
        数据库文件的绝对路径
    """
    db_path = os.path.join(get_data_dir(), db_name)
    
    # 记录数据库路径信息
    log_db_path(logger, db_name, db_path)
    
    return db_path


def get_user_db_path():
    """获取用户中心数据库路径。"""
    return get_db_path("users.db")


def slugify_name(name):
    """将企业名称转为安全文件名片段。"""
    value = (name or "").strip().lower()
    value = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fa5]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "bookset"


def build_bookset_db_filename(enterprise_name, fiscal_year, bookset_id):
    """生成账套数据库文件名。"""
    slug = slugify_name(enterprise_name)
    return f"{slug}_{fiscal_year}_{bookset_id}.db"


def get_bookset_db_path(db_filename):
    """获取账套数据库完整路径。"""
    db_path = os.path.join(get_booksets_dir(), db_filename)
    log_db_path(logger, db_filename, db_path)
    return db_path


def get_settings_path():
    """
    获取配置文件路径
    
    Returns:
        settings.json 的绝对路径
    """
    return os.path.join(get_data_dir(), "settings.json")


def get_subject_json_path():
    """
    获取会计科目JSON文件路径
    
    Returns:
        source/subject.json 的绝对路径
    """
    return os.path.join(get_bundle_dir(), "source", "subject.json")


def get_icon_path(icon_name):
    """
    获取图标文件路径
    
    Args:
        icon_name: 图标文件名（如 'user.png'）
    
    Returns:
        图标文件的绝对路径
    """
    return os.path.join(get_bundle_dir(), "icons", icon_name)
