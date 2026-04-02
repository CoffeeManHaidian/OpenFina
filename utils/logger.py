"""
日志工具模块 - 支持文件和控制台输出
"""
import logging
import os
import sys
import traceback
from datetime import datetime

# 日志级别映射
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}


def get_log_dir():
    """
    获取日志目录路径
    
    返回: logs/ 目录的绝对路径
    """
    if getattr(sys, 'frozen', False):
        # 打包后的exe环境
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    log_dir = os.path.join(app_dir, 'data', 'logs')
    
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return log_dir


def setup_logger(name='OpenFina', level=logging.INFO):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
    
    Returns:
        logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器 - 按日期命名
    log_dir = get_log_dir()
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8-sig')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def _format_kv(**kwargs):
    """将上下文键值对格式化为稳定的日志片段。"""
    parts = []
    for key, value in kwargs.items():
        if value is None:
            value = ""
        parts.append(f"{key}={value}")
    return " | ".join(parts)


def log_event(logger, message, level=logging.INFO, **kwargs):
    """记录结构化事件日志。"""
    payload = _format_kv(**kwargs)
    if payload:
        logger.log(level, f"{message} | {payload}")
    else:
        logger.log(level, message)


def log_system_info(logger):
    """
    记录系统启动信息
    
    Args:
        logger: 日志记录器
    """
    logger.info("=" * 50)
    logger.info("应用启动")
    logger.info("=" * 50)
    
    # 记录环境信息
    is_frozen = getattr(sys, 'frozen', False)
    logger.info(f"运行环境: {'打包环境 (frozen)' if is_frozen else '开发环境'}")
    logger.info(f"Python版本: {sys.version}")
    logger.info(f"可执行文件: {sys.executable}")
    
    # 记录路径信息
    if is_frozen:
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    logger.info(f"应用根目录: {app_dir}")
    logger.info(f"当前工作目录: {os.getcwd()}")
    
    # 记录数据库相关路径
    data_dir = os.path.join(app_dir, 'data')
    logger.info(f"数据目录: {data_dir}")
    logger.info(f"日志目录: {os.path.join(data_dir, 'logs')}")
    
    # 检查目录是否存在
    if os.path.exists(data_dir):
        logger.info(f"数据目录状态: 存在")
        # 列出data目录下的文件
        try:
            files = os.listdir(data_dir)
            db_files = [f for f in files if f.endswith('.db')]
            if db_files:
                logger.info(f"现有数据库文件: {', '.join(db_files)}")
            else:
                logger.info("现有数据库文件: 无")
        except Exception as e:
            logger.warning(f"无法读取数据目录内容: {e}")
    else:
        logger.warning(f"数据目录状态: 不存在，将自动创建")
    
    logger.info("=" * 50)


def log_db_path(logger, db_name, db_path):
    """
    记录数据库路径信息
    
    Args:
        logger: 日志记录器
        db_name: 数据库名称
        db_path: 数据库完整路径
    """
    logger.info(f"数据库 [{db_name}] 路径: {db_path}")
    
    # 检查文件是否存在
    if os.path.exists(db_path):
        file_size = os.path.getsize(db_path)
        logger.info(f"  状态: 存在 (大小: {file_size} bytes)")
    else:
        logger.info(f"  状态: 不存在（将自动创建）")


def install_global_exception_logger(logger):
    """安装全局未捕获异常日志。"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("未捕获异常:\n%s", "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

    sys.excepthook = handle_exception


# 全局日志实例
_logger = None


def get_logger():
    """
    获取全局日志记录器（单例模式）
    
    Returns:
        logger: 日志记录器
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger
