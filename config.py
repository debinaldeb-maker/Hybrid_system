import os
import cv2
from datetime import datetime
import platform  
class Config:
    # الألوان
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#34495e"
    ACCENT_COLOR = "#3498db"
    BACKGROUND_COLOR = "#ecf0f1"
    TEXT_COLOR = "#2c3e50"
    WARNING_COLOR = "#e74c3c"
    SUCCESS_COLOR = "#2ecc71"
    OS = platform.system()
    
    # الألوان
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#34495e"
    ACCENT_COLOR = "#3498db"
    BACKGROUND_COLOR = "#ecf0f1"
    TEXT_COLOR = "#2c3e50"
    WARNING_COLOR = "#e74c3c"
    SUCCESS_COLOR = "#2ecc71"
    
    # الخطوط
    FONT_FAMILY = "Tahoma" if OS == "Windows" else "KacstBook"
    FONT_SIZE = 12
    
    # إعدادات النظام
    BIOMETRIC_THRESHOLD = 0.95
    CAMERA_RESOLUTION = (1280, 720)
    HEATMAP_INTERVAL = 15  # دقائق بين تحديثات الخرائط الحرارية
    
    # إعدادات أخرى
    DATABASE_PATH = "database/baseera_db.sqlite"
    LOG_DIR = "logs/system.log"   
    # الخطوط
    FONT_FAMILY = "Tahoma" if OS == "Windows" else "KacstBook"
    FONT_SIZE = 12
    
    # إعدادات النظام
    BIOMETRIC_THRESHOLD = 0.95
    CAMERA_RESOLUTION = (1280, 720)
    HEATMAP_INTERVAL = 15  # دقائق بين تحديثات الخرائط الحرارية
    # إعدادات النظام الأساسية
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # إعدادات قاعدة البيانات
    DATABASE_NAME = os.path.join(BASE_DIR, "employee_attendance.db")
    
    # إعدادات التعرف على الوجه
    HAAR_CASCADE = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    TRAINER_FILE = os.path.join(BASE_DIR, "trainer", "model.pkl")
    LABELS_FILE = os.path.join(BASE_DIR, "trainer", "labels.pkl")  # ملف جديد للتسميات
    DATASET_PATH = os.path.join(BASE_DIR, "dataset")
    
    # إعدادات بصمة الإصبع
    FINGERPRINT_PORT = "/dev/ttyUSB0"  # أو "COM3" في ويندوز
    FINGERPRINT_BAUDRATE = 57600
    
    # إعدادات الواجهة
    THEME = "clam"  # أو "alt", "default", "classic"
    PRIMARY_COLOR = "#1a2b3c"
    SECONDARY_COLOR = "#2c3e50"
    ACCENT_COLOR = "#3498db"
    
    # إعدادات الأمان
    AES_KEY = b'L5Mh1PHzidUvgH2U24tqxC9TJjd0YmJTYOYDuyRwdGA=' # يجب تغييره في الإنتاج
    
    # مسارات الملفات
    ATTENDANCE_DIR = "attendance_records"
    HEATMAP_DIR = "heatmaps"
    INTRUSION_LOG = "intrusion_alerts.csv"
    THERMAL_LOG = "thermal_logs.csv"
    
    # إعدادات الأداء
    FACE_CONFIDENCE_THRESHOLD = 60
    FINGERPRINT_THRESHOLD = 0.65
    SENSOR_CHECK_INTERVAL = 5  # ثواني
    # إعدادات الزوار
    VISITOR_DB = "visitors.db"
    UNKNOWN_VISITOR_DIR = "unknown_visitors"
    VISITOR_ACCESS_LEVELS = {
        1: "محدود",
        2: "عام",
        3: "مميز"
    }
    
    # إعدادات الذكاء الاصطناعي
    AI_BEHAVIOR_MODEL = "behavior_analysis.h5"
    AI_PERFORMANCE_MODEL = "performance_model.h5"
    AI_FACE_QUALITY_THRESHOLD = 0.8
    
    # إعدادات واجهة المستخدم الجديدة
    THEME = "sun-valley"  # ثيمات حديثة
    PRIMARY_COLOR = "#2c3e50"
    SECONDARY_COLOR = "#34495e"
    ACCENT_COLOR = "#3498db"
    DANGER_COLOR = "#e74c3c"
    SUCCESS_COLOR = "#2ecc71"
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 11
    
    # ألوان إضافية للواجهات
    BACKGROUND_COLOR = "#3f80e1"
    CARD_COLOR = "#93d891"
    TEXT_COLOR = "#333333"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EMPLOYEE_DIR = os.path.join(DATA_DIR, "employees")
    # config.py


    # ... الإعدادات الأخرى الموجودة مسبقاً ...
    
    # الألوان الجديدة
    PRIMARY_COLOR = "#2c3e50"      # اللون الأساسي (أزرق داكن)
    SECONDARY_COLOR = "#3498db"    # اللون الثانوي (أزرق)
    HIGHLIGHT_COLOR = "#2980b9"    # اللون عند التفعيل (أزرق داكن)
    ACCENT_COLOR = "#e74c3c"       # لون التمييز (أحمر)
    DARK_COLOR = "#34495e"         # لون داكن (أزرق رمادي)