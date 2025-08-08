import tkinter as tk
from gui.login import LoginScreen
from gui.dashboard import MainDashboard
from core.database import DatabaseManager
from core.security import SecurityMonitor
import os
import os
from config import Config

# إنشاء المجلدات المطلوبة

os.makedirs(os.path.dirname(Config.DATABASE_NAME), exist_ok=True)
os.makedirs(Config.DATASET_PATH, exist_ok=True)
os.makedirs(os.path.dirname(Config.TRAINER_FILE), exist_ok=True)
os.makedirs(Config.ATTENDANCE_DIR, exist_ok=True)
os.makedirs(Config.HEATMAP_DIR, exist_ok=True)

def main():
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية مؤقتًا
    
    # تهيئة قاعدة البيانات
    db_manager = DatabaseManager()
    
    # بدء نظام المراقبة الأمنية
    security_monitor = SecurityMonitor()
    security_monitor.start_monitoring()
    
    def on_login_success(user_data):
        """الدالة التي تستدعى عند نجاح تسجيل الدخول"""
        login_screen.destroy()
        dashboard = MainDashboard(user_data)
        dashboard.mainloop()
    
    # عرض شاشة تسجيل الدخول
    login_screen = LoginScreen(root, on_login_success)
    login_screen.mainloop()
    
    # تنظيف الموارد عند الخروج
    db_manager.close()
    security_monitor.stop_monitoring()
    
if __name__ == "__main__":
    # إنشاء المجلدات المطلوبة
    os.makedirs("trainer", exist_ok=True)
    os.makedirs("dataset", exist_ok=True)
    os.makedirs("attendance_records", exist_ok=True)
    os.makedirs("heatmaps", exist_ok=True)
    
    # تشغيل التطبيق
    main()