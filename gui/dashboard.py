import tkinter as tk
from tkinter import ttk
from config import Config
from .employee import EmployeeManagement
from .hybrid_attendance import HybridAttendanceSystem  # تم التعديل
from .advanced_reports import AdvancedReportsDashboard  # تم التعديل
from .smart_visitor import SmartVisitorManagement  # تم التعديل
from .performance_heatmap import PerformanceHeatmap  # تم التعديل
from .security_monitoring import SecurityMonitoring  # تم التعديل
from .settings import SystemSettings

import sys


class MainDashboard(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.title(f"نظام بصيرة الهجين - {user_data['name']}")
        self.geometry("1600x900")
        self.configure(bg=Config.BACKGROUND_COLOR)
        
        self.user_data = user_data
        self.current_tab = None
        self.tabs = {}
        self.active_tab_frame = None
        
        # إعداد الخط العربي
        self.arabic_font = ("Tahoma", 12) if Config.OS == "Windows" else ("KacstBook", 12)
        
        # إنشاء واجهة المستخدم
        self.create_widgets()
        
        # ربط حدث الإغلاق
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # عرض علامة التبويب الافتراضية
        self.show_tab("attendance")
    
    def create_widgets(self):
        # شريط العنوان
        title_frame = ttk.Frame(self, style="Title.TFrame")
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = ttk.Label(title_frame, 
                         text="نظام بصيرة الهجين لتسجيل الحضور والمراقبة الأمنية",
                         font=("Arial", 18, "bold"),
                         foreground="white", 
                         background=Config.PRIMARY_COLOR)
        title.pack(side=tk.LEFT, padx=10)
        
        # معلومات المستخدم
        user_frame = ttk.Frame(title_frame)
        user_frame.pack(side=tk.RIGHT)
        
        self.user_icon = tk.Label(user_frame, text="👤", font=("Arial", 14))
        self.user_icon.pack(side=tk.LEFT, padx=5)
        
        user_info = ttk.Label(user_frame, 
                             text=f"{self.user_data['name']} | {self.user_data['position']}", 
                             font=self.arabic_font,
                             foreground="#f0f0f0")
        user_info.pack(side=tk.RIGHT)
        
        # شريط التنقل
        nav_frame = ttk.Frame(self, style="Nav.TFrame")
        nav_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # أزرار التنقل
        nav_buttons = [
            ("📋 تسجيل الحضور", "attendance"),
            ("👥 إدارة الموظفين", "employees"),
            ("👤 إدارة الزوار", "visitors"),
            ("📊 التقارير والتحليلات", "reports"),
            ("📈 خرائط الأداء الحرارية", "performance"),
            ("🔒 المراقبة الأمنية الذكية", "security"),
            ("⚙️ إعدادات النظام", "settings"),
            ("🚪 خروج", "exit")
        ]
        
        for text, tab_id in nav_buttons:
            btn = ttk.Button(nav_frame, 
                            text=text, 
                            width=20,
                            style="Nav.TButton",
                            command=lambda tid=tab_id: self.show_tab(tid))
            btn.pack(side=tk.LEFT, padx=5, ipady=5)
        
        # منطقة المحتوى
        self.content_frame = ttk.Frame(self, style="Content.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # شريط الحالة
        self.status_bar = ttk.Label(self, 
                                  text="الحالة: جاهز | نظام بصيرة الهجين v1.0",
                                  relief=tk.SUNKEN, 
                                  anchor=tk.W,
                                  font=self.arabic_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # تهيئة الأنماط
        self.configure_styles()
    
    def show_tab(self, tab_id):
        """إظهار علامة التبويب المحددة"""
        if tab_id == "exit":
            self.on_close()
            return
        
        # إخفاء الإطار النشط السابق
        if self.active_tab_frame:
            self.active_tab_frame.pack_forget()
        
        # إنشاء علامة التبويب إذا لم تكن موجودة
        if tab_id not in self.tabs:
            self.tabs[tab_id] = self.create_tab(tab_id)
        
        # تعيين الإطار النشط الحالي
        self.active_tab_frame = self.tabs[tab_id]
        self.active_tab_frame.pack(fill=tk.BOTH, expand=True)
        self.current_tab = tab_id
        self.update_idletasks()
    
    def create_tab(self, tab_id):
        """إنشاء علامة التبويب المطلوبة"""
        # إنشاء إطار للتبويب
        tab_frame = ttk.Frame(self.content_frame)
        
        # إنشاء الوحدة الفرعية داخل هذا الإطار
        if tab_id == "attendance":
            HybridAttendanceSystem(tab_frame, self.user_data, self.status_bar).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "employees" and self.user_data['position'] == 'مدير':
            EmployeeManagement(tab_frame).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "visitors":
            SmartVisitorManagement(tab_frame, self.status_bar).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "reports":
            AdvancedReportsDashboard(tab_frame, self.user_data, self.status_bar).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "performance":
            PerformanceHeatmap(tab_frame, self.user_data, self.status_bar).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "security":
            SecurityMonitoring(tab_frame, self.status_bar).pack(fill=tk.BOTH, expand=True)
        elif tab_id == "settings":
            SystemSettings(tab_frame).pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(tab_frame, text="الوصول غير مسموح أو الوحدة قيد التطوير", font=("Arial", 18)).pack(fill=tk.BOTH, expand=True)
        
        return tab_frame
    
    def on_close(self):
        """إغلاق جميع الموارد والنافذة"""
        try:
            # إغلاق جميع علامات التبويب
            for tab_id, tab_frame in self.tabs.items():
                # إغلاق الوحدة الفرعية إذا كانت تحتوي على دالة close
                for child in tab_frame.winfo_children():
                    if hasattr(child, 'close'):
                        try:
                            child.close()
                        except Exception as e:
                            print(f"Error closing {tab_id}: {e}")
                # تدمير إطار التبويب
                tab_frame.destroy()
            
            # إغلاق النافذة الرئيسية
            self.destroy()
            sys.exit(0)  # إغلاق التطبيق بشكل نظيف
        except Exception as e:
            print(f"Error during close: {e}")
            self.destroy()
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # ... بقية تهيئة الأنماط ...