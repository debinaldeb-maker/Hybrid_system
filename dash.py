
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import Config
from .employee import EmployeeManagement
from .attendance import AttendanceSystem
from .reports import ReportsDashboard
from .visitor import VisitorManagement
from .performance import PerformanceDashboard
from .security import SecurityDashboard
from .settings import SystemSettings
from .heatmap import HeatmapVisualizer
import datetime

class MainDashboard(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.title(f"نظام بصيرة الهجين - {user_data['name']}")  # تغيير العنوان
        self.geometry("1400x800")
        self.configure(bg=Config.BACKGROUND_COLOR)
        
        self.user_data = user_data
        self.current_tab = None
        self.tabs = {}
        self.alerts = []  # قائمة لتخزين الإنذارات الأمنية
        
        self.create_widgets()
        self.show_tab("attendance")
        
        # محاكاة إنذار أمني للعرض
        self.add_sample_alert()
    
    def create_widgets(self):
        # شريط العنوان المحدث
        title_frame = ttk.Frame(self, style='Header.TFrame')
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # شعار النظام
        logo_label = ttk.Label(title_frame, text="⚡", font=("Arial", 28))
        logo_label.pack(side=tk.LEFT, padx=10)
        
        title = ttk.Label(title_frame, text="نظام بصيرة الهجين لتسجيل الحضور والمراقبة الأمنية", 
                         font=("Arial", 16, "bold"), foreground="white")
        title.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # معلومات المستخدم مع رمز المستخدم
        user_frame = ttk.Frame(title_frame)
        user_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(user_frame, text="👤", font=("Arial", 14)).pack(side=tk.LEFT)
        user_info = ttk.Label(user_frame, 
                             text=f"{self.user_data['name']} | {self.user_data['position']}",
                             font=("Arial", 11))
        user_info.pack(side=tk.RIGHT)
        
        # شريط التنقل المحدث
        nav_frame = ttk.Frame(self, style='Nav.TFrame')
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # أزرار التنقل المحدثة حسب متطلبات التقرير
        nav_buttons = [
            ("📝 تسجيل الحضور", "attendance"),
            ("👥 إدارة الموظفين", "employees"),
            ("👤 إدارة الزوار", "visitors"),
            ("📊 التقارير والإحصائيات", "reports"),
            ("📈 تحليل الأداء", "performance"),
            ("🔒 المراقبة الأمنية", "security"),
            ("🌡️ الخرائط الحرارية", "heatmap"),  # إضافة جديدة
            ("⚠️ الإنذارات الأمنية", "alerts"),   # إضافة جديدة
            ("⚙️ إعدادات النظام", "settings"),
            ("🚪 خروج", "exit")
        ]
        
        for text, tab_id in nav_buttons:
            btn = ttk.Button(nav_frame, text=text, width=18, style='Nav.TButton',
                            command=lambda tid=tab_id: self.show_tab(tid))
            btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        # شريط الحالة مع الإنذارات
        status_frame = ttk.Frame(self, style='Status.TFrame', height=30)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        self.alert_label = ttk.Label(status_frame, text="", style='Alert.TLabel')
        self.alert_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(status_frame, text=f"⏱️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                 style='Time.TLabel').pack(side=tk.RIGHT, padx=10)
        
        # منطقة المحتوى
        self.content_frame = ttk.Frame(self, style='Content.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # تحميل الأنماط
        self.configure_styles()
    
    def configure_styles(self):
        style = ttk.Style()
        
        # أنماط الألوان حسب التقرير
        style.configure('Header.TFrame', background=Config.PRIMARY_COLOR)
        style.configure('Nav.TFrame', background=Config.SECONDARY_COLOR)
        style.configure('Status.TFrame', background='#2c3e50')
        style.configure('Content.TFrame', background=Config.BACKGROUND_COLOR)
        
        style.configure('Nav.TButton', font=(Config.FONT_FAMILY, 12), 
                      foreground='white', background=Config.SECONDARY_COLOR,
                      padding=5)
        style.map('Nav.TButton', background=[('active', '#2980b9')])
        
        style.configure('Alert.TLabel', font=(Config.FONT_FAMILY, 11), 
                      foreground='#ff6b6b', background='#2c3e50')
        style.configure('Time.TLabel', font=(Config.FONT_FAMILY, 11), 
                      foreground='#ecf0f1', background='#2c3e50')
        
        style.configure('TFrame', background=Config.BACKGROUND_COLOR)
        style.configure('TLabel', background=Config.BACKGROUND_COLOR, 
                      foreground=Config.TEXT_COLOR, font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        style.configure('TButton', font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        style.configure('Treeview', font=(Config.FONT_FAMILY, Config.FONT_SIZE))
        style.configure('Treeview.Heading', font=(Config.FONT_FAMILY, Config.FONT_SIZE, "bold"))
    
    def show_tab(self, tab_id):
        if self.current_tab and tab_id != self.current_tab:
            if self.current_tab in self.tabs and hasattr(self.tabs[self.current_tab], 'close'):
                self.tabs[self.current_tab].close()
        
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        
        if tab_id == "exit":
            self.close()
            return
        
        if tab_id not in self.tabs:
            self.tabs[tab_id] = self.create_tab(tab_id)
        
        self.tabs[tab_id].pack(fill=tk.BOTH, expand=True)
        self.current_tab = tab_id
        
        # تحديث الإنذارات عند فتح علامة التبويب
        if tab_id == "alerts":
            self.tabs[tab_id].update_alerts(self.alerts)
    
    def create_tab(self, tab_id):
        if tab_id == "attendance":
            return AttendanceSystem(self.content_frame, self.user_data, self.add_alert)
        elif tab_id == "employees" and self.user_data['position'] == 'مدير':
            return EmployeeManagement(self.content_frame)
        elif tab_id == "visitors":
            return VisitorManagement(self.content_frame, self.add_alert)
        elif tab_id == "reports":
            return ReportsDashboard(self.content_frame, self.user_data)
        elif tab_id == "performance":
            return PerformanceDashboard(self.content_frame, self.user_data)
        elif tab_id == "security":
            return SecurityDashboard(self.content_frame, self.add_alert)
        elif tab_id == "settings":
            return SystemSettings(self.content_frame)
        elif tab_id == "heatmap":
            return HeatmapVisualizer(self.content_frame)  # واجهة جديدة
        elif tab_id == "alerts":
            return AlertsDashboard(self.content_frame)  # واجهة جديدة
        else:
            return ttk.Label(self.content_frame, text=f"واجهة {tab_id} قيد التطوير أو غير مسموحة",
                           font=("Arial", 18))
    
    def add_alert(self, alert_data):
        """إضافة إنذار جديد للنظام"""
        self.alerts.append(alert_data)
        self.update_alert_display()
        
        # إشعار فوري للمستخدم
        if not isinstance(self.tabs.get("alerts"), AlertsDashboard):
            messagebox.showwarning("إنذار أمني", alert_data["message"])
    
    def add_sample_alert(self):
        """إضافة إنذار تجريبي للعرض"""
        sample_alert = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "location": "المدخل الرئيسي",
            "type": "حركة غير معتادة",
            "level": "متوسط",
            "message": "تم رصد حركة غير معتادة في منطقة المدخل الرئيسي"
        }
        self.add_alert(sample_alert)
    
    def update_alert_display(self):
        """تحديث شريط الحالة لعرض الإنذارات الأخيرة"""
        if self.alerts:
            latest_alert = self.alerts[-1]
            alert_text = f"⚠️ إنذار: {latest_alert['type']} في {latest_alert['location']} ({latest_alert['time']})"
            self.alert_label.config(text=alert_text)
    
    def close(self):
        for tab_id, tab in self.tabs.items():
            if hasattr(tab, 'close'):
                tab.close()
        self.destroy()


# ===== الوحدات الجديدة حسب متطلبات التقرير =====

class HeatmapVisualizer(ttk.Frame):
    """واجهة الخرائط الحرارية لتحليل حركة الموظفين"""
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.generate_sample_data()
    
    def create_widgets(self):
        # إطار التحكم
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="الفترة الزمنية:").pack(side=tk.LEFT, padx=5)
        self.time_var = tk.StringVar(value="اليوم")
        time_options = ["اليوم", "أمس", "الأسبوع الحالي", "الشهر الحالي"]
        ttk.Combobox(control_frame, textvariable=self.time_var, values=time_options, 
                    state="readonly", width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="الموقع:").pack(side=tk.LEFT, padx=5)
        self.location_var = tk.StringVar(value="جميع الأقسام")
        loc_options = ["جميع الأقسام", "المدخل الرئيسي", "قسم المبيعات", "قسم الدعم", "المطبخ"]
        ttk.Combobox(control_frame, textvariable=self.location_var, values=loc_options, 
                    state="readonly", width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="تحديث البيانات", command=self.update_heatmap).pack(side=tk.LEFT, padx=10)
        
        # منطقة عرض الخريطة الحرارية
        heatmap_frame = ttk.Frame(self)
        heatmap_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(heatmap_frame, bg="white", bd=1, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # مفتاح الألوان
        legend_frame = ttk.Frame(self)
        legend_frame.pack(fill=tk.X, pady=5)
        
        colors = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
        labels = ["قليل", "متوسط", "كثيف", "مكتظ"]
        
        for color, label in zip(colors, labels):
            color_frame = ttk.Frame(legend_frame, width=20, height=20)
            color_frame.pack_propagate(False)
            color_frame.pack(side=tk.LEFT, padx=5)
            tk.Canvas(color_frame, bg=color, highlightthickness=0).pack(fill=tk.BOTH, expand=True)
            ttk.Label(legend_frame, text=label).pack(side=tk.LEFT, padx=(0, 15))
    
    def generate_sample_data(self):
        """إنشاء بيانات تجريبية للخريطة الحرارية"""
        self.heatmap_data = []
        areas = ["المدخل", "الممر الشرقي", "قسم المبيعات", "قسم الدعم", "المطبخ", "قاعة الاجتماعات"]
        
        for area in areas:
            self.heatmap_data.append({
                "area": area,
                "data": [
                    {"hour": f"{h:02d}:00", "density": (h % 5) + 1}
                    for h in range(8, 18)  # من 8 صباحًا إلى 6 مساءً
                ]
            })
        
        self.update_heatmap()
    
    def update_heatmap(self):
        """تحديث الخريطة الحرارية بناءً على التحديدات"""
        self.canvas.delete("all")
        
        # أبعاد الرسم
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 10 or height < 10:
            self.after(100, self.update_heatmap)
            return
        
        # رسم شبكة الخريطة الحرارية
        cols = 10  # عدد الأعمدة (ساعات)
        rows = len(self.heatmap_data)  # عدد الصفوف (المناطق)
        
        cell_width = (width - 100) / cols
        cell_height = (height - 50) / rows
        
        # رسم تسميات المناطق
        for i, area_data in enumerate(self.heatmap_data):
            y_pos = 30 + i * cell_height + cell_height / 2
            self.canvas.create_text(60, y_pos, text=area_data["area"], anchor=tk.E, font=("Arial", 10))
        
        # رسم تسميات الساعات
        for j in range(cols):
            x_pos = 100 + j * cell_width + cell_width / 2
            self.canvas.create_text(x_pos, 15, text=f"{8+j}:00", font=("Arial", 9))
        
        # رسم الخلايا الحرارية
        colors = ["#ecf0f1", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
        
        for i, area_data in enumerate(self.heatmap_data):
            for j, hour_data in enumerate(area_data["data"]):
                x1 = 100 + j * cell_width
                y1 = 30 + i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                density = hour_data["density"]
                color = colors[density] if density < len(colors) else colors[-1]
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#bdc3c7")
                
                # عرض قيمة الكثافة
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(density), font=("Arial", 10))
        
        self.canvas.create_text(width/2, height-20, 
                              text="خريطة حركة الموظفين حسب المنطقة والوقت",
                              font=("Arial", 12, "bold"))


class AlertsDashboard(ttk.Frame):
    """واجهة إدارة الإنذارات الأمنية"""
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # شريط التحكم
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="تصفية الإنذارات:").pack(side=tk.LEFT, padx=5)
        
        self.level_var = tk.StringVar(value="الكل")
        levels = ["الكل", "منخفض", "متوسط", "مرتفع"]
        ttk.Combobox(control_frame, textvariable=self.level_var, values=levels, 
                    state="readonly", width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="تطبيق التصفية", command=self.update_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="مسح جميع الإنذارات", command=self.clear_alerts).pack(side=tk.LEFT, padx=5)
        
        # جدول الإنذارات
        columns = ("#", "الوقت", "الموقع", "نوع الإنذار", "المستوى", "الإجراء")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        # تعيين عناوين الأعمدة
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # ضبط أبعاد خاصة لبعض الأعمدة
        self.tree.column("#", width=50)
        self.tree.column("الموقع", width=150)
        self.tree.column("الإجراء", width=120)
        
        # إضافة شريط تمرير
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # منطقة تفاصيل الإنذار
        detail_frame = ttk.LabelFrame(self, text="تفاصيل الإنذار")
        detail_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=5, font=("Arial", 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detail_text.config(state=tk.DISABLED)
        
        # أزرار الإجراءات
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="تمييز كمقروء", command=self.mark_as_read).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="تصدير إلى PDF", command=self.export_to_pdf).pack(side=tk.LEFT, padx=5)
        
        # ربط حدث اختيار إنذار
        self.tree.bind("<<TreeviewSelect>>", self.show_alert_details)
    
    def update_alerts(self, alerts):
        """تحديث الجدول بقائمة الإنذارات"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # تطبيق التصفية
        level_filter = self.level_var.get()
        filtered_alerts = [a for a in alerts if level_filter == "الكل" or a.get("level") == level_filter]
        
        # إضافة الإنذارات إلى الجدول
        for i, alert in enumerate(filtered_alerts, 1):
            self.tree.insert("", tk.END, values=(
                i,
                alert.get("time", ""),
                alert.get("location", ""),
                alert.get("type", ""),
                alert.get("level", ""),
                "غير مقروء" if alert.get("unread", True) else "مقروء"
            ), tags=('unread' if alert.get("unread", True) else 'read'))
        
        # تلوين الصفوف
        self.tree.tag_configure('unread', background='#ffeeee')
        self.tree.tag_configure('read', background='#f0f0f0')
    
    def show_alert_details(self, event):
        """عرض تفاصيل الإنذار المحدد"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # في تطبيق حقيقي، سيتم جلب التفاصيل من قاعدة البيانات
        details = f"تفاصيل الإنذار #{values[0]}:\n"
        details += f"الوقت: {values[1]}\n"
        details += f"الموقع: {values[2]}\n"
        details += f"نوع الإنذار: {values[3]}\n"
        details += f"المستوى: {values[4]}\n\n"
        details += "تم رصد حركة غير عادية في المنطقة المحددة. يرجى التحقق من لقطات الكاميرا."
        
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, details)
        self.detail_text.config(state=tk.DISABLED)
    
    def mark_as_read(self):
        """تمييز الإنذار المحدد كمقروء"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("معلومات", "يرجى اختيار إنذار أولاً")
            return
        
        item = self.tree.item(selected[0])
        self.tree.item(selected[0], values=(
            *item['values'][:-1],  # جميع القيم ما عدا الأخيرة
            "مقروء"
        ), tags=('read'))
    
    def clear_alerts(self):
        """مسح جميع الإنذارات"""
        if messagebox.askyesno("تأكيد", "هل تريد حقاً مسح جميع الإنذارات؟"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.config(state=tk.DISABLED)
    
    def export_to_pdf(self):
        """محاكاة تصدير الإنذارات إلى PDF"""
        messagebox.showinfo("تصدير", "تم تصدير الإنذارات إلى ملف PDF بنجاح")


# ===== تعديلات على الوحدات الحالية =====

class AttendanceSystem(ttk.Frame):
    """نظام تسجيل الحضور مع التعرف الحيوي المتعدد"""
    def __init__(self, parent, user_data, alert_callback):
        super().__init__(parent)
        self.user_data = user_data
        self.alert_callback = alert_callback
        self.create_widgets()
    
    def create_widgets(self):
        # إطار للتحكم في طريقة التحقق
        auth_frame = ttk.LabelFrame(self, text="طريقة التحقق الحيوي")
        auth_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auth_var = tk.StringVar(value="وجه")  # القيمة الافتراضية
        
        auth_options = [
            ("التعرف على الوجه فقط", "وجه"),
            ("بصمة الأصابع فقط", "بصمة"),
            ("وجه وبصمة معاً (الأكثر أماناً)", "مزدوج")
        ]
        
        for text, mode in auth_options:
            ttk.Radiobutton(auth_frame, text=text, variable=self.auth_var, 
                           value=mode).pack(anchor=tk.W, padx=5, pady=2)
        
        # إطار عرض الكاميرا والنتائج
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # لوحة الكاميرا
        camera_frame = ttk.LabelFrame(main_frame, text="كاميرا التعرف على الوجه")
        camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.camera_label = ttk.Label(camera_frame, background="black")
        self.camera_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # لوحة بصمة الإصبع
        fingerprint_frame = ttk.LabelFrame(main_frame, text="بصمة الإصبع")
        fingerprint_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        fingerprint_img = tk.PhotoImage(file="fingerprint_placeholder.png") if Config.DEBUG else None
        fingerprint_label = ttk.Label(fingerprint_frame, image=fingerprint_img, background="#f0f0f0")
        fingerprint_label.image = fingerprint_img
        fingerprint_label.pack(padx=20, pady=20)
        
        ttk.Label(fingerprint_frame, text="ضع إصبعك على القارئ", 
                font=("Arial", 10)).pack(pady=5)
        
        # لوحة النتائج
        result_frame = ttk.LabelFrame(main_frame, text="نتائج التسجيل")
        result_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=30, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.insert(tk.END, "في انتظار عملية التحقق...\n")
        self.result_text.config(state=tk.DISABLED)
        
        # شريط الإجراءات
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="بدء التسجيل", 
                  command=self.start_authentication).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="إلغاء", 
                  command=self.cancel_authentication).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="طلب مساعدة", 
                  command=self.request_help).pack(side=tk.RIGHT, padx=5)
    
    def start_authentication(self):
        """بدء عملية التحقق الحيوي"""
        auth_method = self.auth_var.get()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # محاكاة عملية التحقق
        if auth_method == "وجه":
            self.simulate_face_recognition()
        elif auth_method == "بصمة":
            self.simulate_fingerprint_scan()
        else:
            self.simulate_multimodal_auth()
        
        self.result_text.config(state=tk.DISABLED)
    
    def simulate_face_recognition(self):
        """محاكاة التعرف على الوجه"""
        self.result_text.insert(tk.END, "جاري تشغيل كاميرا التعرف...\n")
        self.result_text.insert(tk.END, "تم اكتشاف وجه...\n")
        self.result_text.insert(tk.END, "جاري التحقق من الهوية...\n")
        self.after(2000, lambda: self.finalize_auth(True))
    
    def simulate_fingerprint_scan(self):
        """محاكاة مسح بصمة الإصبع"""
        self.result_text.insert(tk.END, "يرجى وضع الإصبع على القارئ...\n")
        self.result_text.insert(tk.END, "تم اكتشاف بصمة...\n")
        self.result_text.insert(tk.END, "جاري التحقق من المطابقة...\n")
        self.after(2000, lambda: self.finalize_auth(True))
    
    def simulate_multimodal_auth(self):
        """محاكاة التحقق المزدوج"""
        self.result_text.insert(tk.END, "بدء التحقق متعدد الوسائط...\n")
        self.result_text.insert(tk.END, "جاري التحقق من الوجه...\n")
        self.after(1000, lambda: self.result_text.insert(tk.END, "تم التحقق من الوجه بنجاح ✓\n"))
        self.result_text.insert(tk.END, "جاري التحقق من بصمة الإصبع...\n")
        self.after(2000, lambda: self.result_text.insert(tk.END, "تم التحقق من البصمة بنجاح ✓\n"))
        self.after(3000, lambda: self.finalize_auth(True))
    
    def finalize_auth(self, success):
        """إنهاء عملية التحقق وعرض النتيجة"""
        if success:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            self.result_text.insert(tk.END, f"\nتم تسجيل الحضور بنجاح!\nالوقت: {time_str}")
            messagebox.showinfo("نجاح", "تم تسجيل حضورك بنجاح")
        else:
            self.result_text.insert(tk.END, "\nفشل التحقق! يرجى المحاولة مرة أخرى")
            messagebox.showerror("خطأ", "فشل التحقق. يرجى المحاولة مرة أخرى")
            
            # إنشاء إنذار أمني
            alert_data = {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "location": "نقطة تسجيل الحضور",
                "type": "فشل التحقق",
                "level": "متوسط",
                "message": "محاولة فاشلة لتسجيل الحضور"
            }
            self.alert_callback(alert_data)
    
    def cancel_authentication(self):
        """إلغاء عملية التحقق"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "تم إلغاء العملية")
        self.result_text.config(state=tk.DISABLED)
    
    def request_help(self):
        """طلب مساعدة من المسؤول"""
        messagebox.showinfo("مساعدة", "تم إرسال طلب المساعدة إلى المسؤول")
        
        # إنشاء إنذار أمني
        alert_data = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "location": "نقطة تسجيل الحضور",
            "type": "طلب مساعدة",
            "level": "منخفض",
            "message": f"{self.user_data['name']} طلب المساعدة في تسجيل الحضور"
        }
        self.alert_callback(alert_data)


class SecurityDashboard(ttk.Frame):
    """لوحة المراقبة الأمنية مع عرض الكاميرات"""
    def __init__(self, parent, alert_callback):
        super().__init__(parent)
        self.alert_callback = alert_callback
        self.create_widgets()
    
    def create_widgets(self):
        # شاشات الكاميرات
        cameras_frame = ttk.Frame(self)
        cameras_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # شاشات افتراضية (4 كاميرات)
        camera_positions = ["المدخل الرئيسي", "قاعة الاجتماعات", "قسم المبيعات", "الطابق العلوي"]
        
        for i, position in enumerate(camera_positions):
            frame = ttk.LabelFrame(cameras_frame, text=f"كاميرا {i+1}: {position}")
            frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            
            # محاكاة فيديو الكاميرا
            canvas = tk.Canvas(frame, width=320, height=240, bg="black")
            canvas.pack(padx=5, pady=5)
            
            # إضافة حركة افتراضية
            if i == 0:
                canvas.create_text(160, 120, text="بث مباشر - المدخل الرئيسي", 
                                 fill="white", font=("Arial", 12))
        
        # ضبط أوزان الصفوف والأعمدة
        for i in range(2):
            cameras_frame.rowconfigure(i, weight=1)
            cameras_frame.columnconfigure(i, weight=1)
        
        # شريط التحكم
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="تحديث المشاهدات", 
                  command=self.refresh_cameras).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="تشغيل الإنذار التجريبي", 
                  command=self.trigger_test_alert).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="تصدير لقطات الشاشة", 
                  command=self.export_screenshots).pack(side=tk.RIGHT, padx=5)
    
    def refresh_cameras(self):
        """تحديث شاشات الكاميرات (محاكاة)"""
        messagebox.showinfo("تحديث", "تم تحديث مشاهدات الكاميرات")
    
    def trigger_test_alert(self):
        """تشغيل إنذار أمني تجريبي"""
        alert_data = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "location": "نظام المراقبة",
            "type": "إنذار تجريبي",
            "level": "منخفض",
            "message": "هذا إنذار تجريبي لنظام المراقبة الأمنية"
        }
        self.alert_callback(alert_data)
        messagebox.showinfo("إنذار تجريبي", "تم تشغيل الإنذار التجريبي بنجاح")
    
    def export_screenshots(self):
        """محاكاة تصدير لقطات الشاشة"""
        messagebox.showinfo("تصدير", "تم تصدير لقطات الشاشة بنجاح")


class VisitorManagement(ttk.Frame):
    """نظام إدارة الزوار مع مسح الهويات"""
    def __init__(self, parent, alert_callback):
        super().__init__(parent)
        self.alert_callback = alert_callback
        self.create_widgets()
    
    def create_widgets(self):
        # قسم مسح الهوية
        scan_frame = ttk.LabelFrame(self, text="مسح هوية الزائر")
        scan_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(scan_frame, text="نوع الهوية:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.id_type = ttk.Combobox(scan_frame, values=["هوية وطنية", "رخصة قيادة", "جواز سفر"], state="readonly")
        self.id_type.current(0)
        self.id_type.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(scan_frame, text="بدء المسح", command=self.scan_id).grid(row=0, column=2, padx=5, pady=5)
        
        # محاكاة ماسح الهوية
        self.scanner_canvas = tk.Canvas(scan_frame, width=300, height=150, bg="#e0e0e0")
        self.scanner_canvas.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        self.scanner_canvas.create_text(150, 75, text="منطقة مسح الهوية", font=("Arial", 12))
        
        # معلومات الزائر
        info_frame = ttk.LabelFrame(self, text="معلومات الزائر")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        fields = [
            ("الاسم الكامل", "name"),
            ("رقم الهوية", "id_number"),
            ("الجهة", "organization"),
            ("الموظف المزمع زيارته", "employee"),
            ("الغرض من الزيارة", "purpose")
        ]
        
        self.visitor_info = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            entry = ttk.Entry(info_frame)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
            self.visitor_info[field] = entry
        
        # أزرار الإجراءات
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="حفظ بيانات الزائر", command=self.save