"""
路径处理工具模块 - 支持开发环境和打包后的exe环境
"""
import sys
import os


def get_app_dir():
    """
    获取应用程序根目录
    
    在开发环境: 返回项目根目录
    在打包环境: 返回exe所在目录
    """
    if getattr(sys, 'frozen', False):
        # 打包后的exe环境 - sys.executable是exe路径
        return os.path.dirname(sys.executable)
    else:
        # 开发环境 - 返回项目根目录（当前文件的上两级）
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_dir():
    """
    获取数据目录路径
    
    返回: data/ 目录的绝对路径
    """
    app_dir = get_app_dir()
    data_dir = os.path.join(app_dir, 'data')
    
    # 确保data目录存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir


def get_resource_dir():
    """
    获取资源目录路径
    
    返回: 资源目录的绝对路径
    """
    app_dir = get_app_dir()
    return app_dir


def get_db_path(db_name):
    """
    获取数据库文件的完整路径
    
    Args:
        db_name: 数据库文件名（如 'users.db'）
    
    Returns:
        数据库文件的绝对路径
    """
    data_dir = get_data_dir()
    return os.path.join(data_dir, db_name)


def get_settings_path():
    """
    获取配置文件路径
    
    Returns:
        settings.json 的绝对路径
    """
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'settings.json')


def get_subject_json_path():
    """
    获取会计科目JSON文件路径
    
    Returns:
        source/subject.json 的绝对路径
    """
    app_dir = get_app_dir()
    return os.path.join(app_dir, 'source', 'subject.json')


def get_icon_path(icon_name):
    """
    获取图标文件路径
    
    Args:
        icon_name: 图标文件名（如 'user.png'）
    
    Returns:
        图标文件的绝对路径
    """
    app_dir = get_app_dir()
    return os.path.join(app_dir, 'icons', icon_name)