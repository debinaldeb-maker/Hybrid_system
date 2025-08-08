import tkinter as tk
from tkinter import ttk, messagebox
from config import Config
import json
import os

class SystemSettings(ttk.Frame):
    def __init__(self, parent):  # تقليل الوسائط
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # واجهة إعدادات النظام الأساسية
        label = ttk.Label(self, text="إعدادات النظام", font=("Arial", 16))
        label.pack(pady=20)
        
    
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.load_settings()
    
    def create_widgets(self):
        # إعدادات النظام
        settings_frame = ttk.LabelFrame(self, text="إعدادات النظام العامة")
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # إعدادات قاعدة البيانات
        ttk.Label(settings_frame, text="اسم قاعدة البيانات:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.db_name_entry = ttk.Entry(settings_frame, width=30)
        self.db_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # إعدادات الكاميرا
        ttk.Label(settings_frame, text="رقم الكاميرا الافتراضية:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.camera_id_entry = ttk.Entry(settings_frame, width=5)
        self.camera_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # إعدادات الألوان
        ttk.Label(settings_frame, text="اللون الأساسي:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.primary_color_entry = ttk.Entry(settings_frame, width=10)
        self.primary_color_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # زر الحفظ
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_save = ttk.Button(btn_frame, text="حفظ الإعدادات", command=self.save_settings)
        btn_save.pack(side=tk.RIGHT)
    
    def load_settings(self):
        """تحميل الإعدادات من ملف"""
        try:
            if os.path.exists("system_settings.json"):
                with open("system_settings.json", "r") as f:
                    settings = json.load(f)
                    self.db_name_entry.insert(0, settings.get("database_name", Config.DATABASE_NAME))
                    self.camera_id_entry.insert(0, settings.get("camera_id", 0))
                    self.primary_color_entry.insert(0, settings.get("primary_color", Config.PRIMARY_COLOR))
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل الإعدادات: {str(e)}")
    
    def save_settings(self):
        """حفظ الإعدادات إلى ملف"""
        try:
            settings = {
                "database_name": self.db_name_entry.get(),
                "camera_id": int(self.camera_id_entry.get() or 0),
                "primary_color": self.primary_color_entry.get()
            }
            
            with open("system_settings.json", "w") as f:
                json.dump(settings, f)
            
            messagebox.showinfo("تم", "تم حفظ الإعدادات بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الإعدادات: {str(e)}")


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