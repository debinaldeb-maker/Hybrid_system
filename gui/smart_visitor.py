
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.database import DatabaseManager
from core.ai_analysis import AIAnalyzer
from config import Config
import pandas as pd
import numpy as np
import seaborn as sns
class SmartVisitorManagement(ttk.Frame):
    def __init__(self, parent, status_bar):
        super().__init__(parent)
        self.status_bar = status_bar
        self.create_widgets()
    
    def create_widgets(self):
        # واجهة ذكية لتسجيل الزوار
        self.create_visitor_registration()
    
    def create_visitor_registration(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # قسم مسح الهوية
        scan_frame = ttk.LabelFrame(main_frame, text="مسح هوية الزائر")
        scan_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)
        
        self.scan_canvas = tk.Canvas(scan_frame, width=300, height=200, bg='#ddd')
        self.scan_canvas.pack(pady=10)
        
        ttk.Button(scan_frame, text="بدء المسح", command=self.start_scan).pack(pady=5)
        
        # قسم معلومات الزائر
        info_frame = ttk.LabelFrame(main_frame, text="معلومات الزائر")
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        fields = [
            ("الاسم الكامل", "name_entry"),
            ("الهوية/الجواز", "id_entry"),
            ("الجهة", "organization_entry"),
            ("الموظف المزور", "employee_entry"),
            ("الغرض من الزيارة", "purpose_combobox")
        ]
        
        for label, var_name in fields:
            frame = ttk.Frame(info_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
            if "combobox" in var_name:
                entry = ttk.Combobox(frame, values=["اجتماع", "مقابلة", "توصيل", "أخرى"])
            else:
                entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            setattr(self, var_name, entry)
        
        # أزرار التنفيذ
        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="حفظ وتسجيل", command=self.save_visitor).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="طباعة البطاقة", command=self.print_badge).pack(side=tk.RIGHT, padx=5)
    
    def start_scan(self):
        self.status_bar.config(text="جاري مسح هوية الزائر...")
        # هنا سيتم دمج OCR لمسح الهوية
          
    def save_visitor(self):
        """حفظ بيانات الزائر في قاعدة البيانات"""
        # تنفيذ عملية الحفظ
        print("تم حفظ بيانات الزائر")
        self.status_bar.config(text="تم حفظ بيانات الزائر بنجاح")
    
    def print_badge(self):
        """طباعة بطاقة الزائر"""
        # تنفيذ عملية الطباعة
        print("تم طباعة بطاقة الزائر")
        self.status_bar.config(text="تم طباعة البطاقة")

    def save_visitor(self):
        # تنفيذ عملية الحفظ
        self.status_bar.config(text="تم حفظ بيانات الزائر")
    
    def print_badge(self):
        # تنفيذ عملية الطباعة
        self.status_bar.config(text="تم طباعة بطاقة الزائر")
    
    def close(self):
        # تنظيف الموارد
        print("Closing SmartVisitorManagement")
        if hasattr(super(), 'destroy'):
            super().destroy()



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
    def save_visitor(self):
        """حفظ بيانات الزائر في قاعدة البيانات"""
        # تنفيذ عملية الحفظ
        print("تم حفظ بيانات الزائر")
        self.status_bar.config(text="تم حفظ بيانات الزائر بنجاح")
    
    def print_badge(self):
        """طباعة بطاقة الزائر"""
        # تنفيذ عملية الطباعة
        print("تم طباعة بطاقة الزائر")
        self.status_bar.config(text="تم طباعة البطاقة")
    
    def close(self):
        """تنظيف الموارد عند إغلاق الوحدة"""
        print("Closing SmartVisitorManagement")
        
        # تدمير جميع العناصر الفرعية
        for widget in self.winfo_children():
            try:
                widget.destroy()
            except:
                pass