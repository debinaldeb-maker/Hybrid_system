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

class PerformanceHeatmap(ttk.Frame):
    def __init__(self, parent, user_data, status_bar):
        super().__init__(parent)
        self.status_bar = status_bar
        self.create_widgets()
    
    def create_widgets(self):
        self.status_bar.config(text="جاري تحميل خرائط الأداء الحرارية...")
        
        # واجهة تحليل الأداء المكاني-الزماني
        self.create_spatiotemporal_analysis()
    
    def create_spatiotemporal_analysis(self):
        # عرض الخرائط الحرارية مع تحليلات الأداء
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # قسم الخريطة
        map_frame = ttk.LabelFrame(main_frame, text="خريطة حركة الموظفين")
        map_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.map_canvas = tk.Canvas(map_frame, bg='#f0f0f0')
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        
        # قسم التحليلات
        analytics_frame = ttk.LabelFrame(main_frame, text="مؤشرات الأداء", width=300)
        analytics_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # مؤشرات الأداء الرئيسية
        metrics = [
            ("الكثافة القصوى", "قاعة الاجتماعات A", "12:30 PM"),
            ("أطول مكوث", "المكتب 204", "ساعتان 45 دقيقة"),
            ("أعلى إنتاجية", "المنطقة الهادئة", "92%")
        ]
        
        for metric in metrics:
            metric_frame = ttk.Frame(analytics_frame)
            metric_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(metric_frame, text=metric[0], font=("Arial", 10, "bold")).pack(anchor=tk.W)
            ttk.Label(metric_frame, text=metric[1]).pack(anchor=tk.W)
            ttk.Label(metric_frame, text=metric[2], foreground="#3498db").pack(anchor=tk.W)

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