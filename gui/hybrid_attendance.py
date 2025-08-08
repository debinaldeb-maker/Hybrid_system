import tkinter as tk
from tkinter import ttk, messagebox
from core.resource_manager import ResourceManager
from core.face_recognition import FaceRecognizer
from core.database import DatabaseManager
from config import Config
import time


class HybridAttendanceSystem(ttk.Frame):
    def __init__(self, parent, user_data, status_bar):
        super().__init__(parent)
        self.status_bar = status_bar
        self.status_bar.config(text="جاري تهيئة نظام الحضور الهجين...")
        
        # واجهة متعددة الوسائط (وجه + بصمة)
        self.create_dual_verification_ui()
        
        # تكامل مع كاميرات المراقبة
        self.camera_feed = self.create_camera_feed()
        
    def create_dual_verification_ui(self):
        # قسم التعرف على الوجه
        face_frame = ttk.LabelFrame(self, text="التعرف بالوجه")
        face_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.face_canvas = tk.Canvas(face_frame, width=400, height=300, bg='#ddd')
        self.face_canvas.pack(pady=5)
        
        # قسم بصمة الإصبع
        fingerprint_frame = ttk.LabelFrame(self, text="بصمة الإصبع")
        fingerprint_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.fingerprint_img = tk.Label(fingerprint_frame, text="⬤⬤⬤⬤⬤", font=("Arial", 48))
        self.fingerprint_img.pack(pady=20)
        
    def create_camera_feed(self):
        # تكامل مع كاميرات المراقبة الحالية
        feed_frame = ttk.Frame(self)
        feed_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        camera_label = ttk.Label(feed_frame, text="بث مباشر من كاميرات المراقبة")
        camera_label.pack()
        
        # سيمول دفق الكاميرا الحقيقي
        self.camera_canvas = tk.Canvas(feed_frame, width=800, height=450, bg='#333')
        self.camera_canvas.pack()
        
        # زر لبدء/إيقاف المراقبة
        monitor_btn = ttk.Button(feed_frame, text="بدء المراقبة الذكية", command=self.start_ai_monitoring)
        monitor_btn.pack(pady=10)
        
    def start_ai_monitoring(self):
        self.status_bar.config(text="جاري تشغيل المراقبة الذكية...")
        # هنا سيتم دمج تحليل السلوك والكشف عن التهديدات
class ModuleName(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets(*args, **kwargs)
    
    def create_widgets(self, *args, **kwargs):
        # إنشاء واجهة الوحدة هنا
        pass
        
    def close(self):
        """تنظيف الموارد عند إغلاق الوحدة"""
        # إغلاق أي موارد مفتوحة (كاميرات، خيوط، إلخ)
        print(f"Closing {self.__class__.__name__}")
        
        # تدمير جميع العناصر الفرعية
        for widget in self.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        
        # إزالة المرجع للوالد
        self.parent = None