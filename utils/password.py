import bcrypt
import sqlite3
import hashlib
import secrets


class PasswdManager:
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # 创建用户表
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        """使用bcrypt哈希密码"""
        # 使用brcypt自动生成盐并包含在哈希结果中
        salt = bcrypt.gensalt(rounds=12)    # rounds控制计算强度
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
        
    def verify_password(self, password, hashed_password):
        """验证bcrypt哈希的密码"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except:
            return False