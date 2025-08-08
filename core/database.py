
#core/database.py
import sqlite3
import os
from config import Config
from cryptography.fernet import Fernet
import logging

# إعدادات التسجيل
logging.basicConfig(filename='database.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cipher = Fernet(Config.AES_KEY)
        self._initialize_database()
        
    def _initialize_database(self):
        """تهيئة قاعدة البيانات والجداول"""
        try:
            os.makedirs(os.path.dirname(Config.DATABASE_NAME), exist_ok=True)
            self.conn = sqlite3.connect(Config.DATABASE_NAME)
            self.cursor = self.conn.cursor()
            
            # إنشاء الجداول
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    password TEXT,
                    face_template BLOB,
                    fingerprint_template BLOB,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time_in TEXT NOT NULL,
                    time_out TEXT,
                    productivity_score INTEGER DEFAULT 0,
                    FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS intrusions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sensor_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    severity INTEGER NOT NULL,
                    handled BOOLEAN DEFAULT 0
                )
            """)
            
            self.conn.commit()
        except Exception as e:
            logging.error(f"فشل في تهيئة قاعدة البيانات: {str(e)}")
            raise
    
    # ... بقية الدوال مع إضافة معالجة الأخطاء ...
    def add_employee(self, emp_id, name, position, password):
        conn = self.conn
        cursor = conn.cursor()
        
        # التحقق من عدم وجود موظف بنفس الرقم
        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        if cursor.fetchone():
            raise ValueError("موظف بنفس الرقم موجود بالفعل")
        
        # إضافة الموظف الجديد
        cursor.execute("""
            INSERT INTO employees (emp_id, name, position, password)
            VALUES (?, ?, ?, ?)
        """, (emp_id, name, position, password))
        conn.commit()
    def mark_attendance(self, emp_id, time_in=None, time_out=None, productivity=0):
        """تسجيل حضور الموظف"""
        try:
            from datetime import datetime
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            
            if time_in:
                # تسجيل الدخول
                query = """
                    INSERT INTO attendance (emp_id, date, time_in, productivity_score)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(emp_id, date) DO UPDATE SET time_in = excluded.time_in
                """
                self.cursor.execute(query, (emp_id, date, time_str, productivity))
            elif time_out:
                # تسجيل الخروج
                query = """
                    UPDATE attendance 
                    SET time_out = ?, productivity_score = ?
                    WHERE emp_id = ? AND date = ? AND time_out IS NULL
                """
                self.cursor.execute(query, (time_str, productivity, emp_id, date))
            
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logging.error(f"فشل في تسجيل الحضور: {str(e)}")
            self.conn.rollback()
            return False
    
    # ... بقية الدوال مع إضافة معالجة الأخطاء ...
    
    def close(self):
        """إغلاق اتصال قاعدة البيانات"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logging.error(f"فشل في إغلاق اتصال قاعدة البيانات: {str(e)}")