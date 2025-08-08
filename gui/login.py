import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time

# Assuming these are available in core and config directories
from core.face_recognition import FaceRecognizer
from core.fingerprint import FingerprintManager
from core.database import DatabaseManager
from config import Config

class LoginScreen(tk.Toplevel):
    """
    شاشة تسجيل الدخول لنظام بصيرة الهجين.
    تتيح تسجيل الدخول عبر الوجه، بصمة الإصبع، أو كلاهما، بالإضافة إلى دخول المسؤول.
    """

    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.camera_active = False
        self.cap = None
        self.face_recognizer = FaceRecognizer()
        self.fingerprint_manager = FingerprintManager()
        self.db_manager = DatabaseManager()

        self._setup_window()
        self._load_configurations()
        self._create_widgets()
        self._configure_styles()
        self._start_camera_thread()

    def _setup_window(self):
        """إعداد خصائص النافذة الرئيسية."""
        self.title("تسجيل الدخول - نظام بصيرة")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.configure(bg=self.get_config_color("PRIMARY_COLOR", "#2c3e50"))

    def _load_configurations(self):
        """تحميل الألوان من ملف الإعدادات."""
        self.colors = {
            "primary": self.get_config_color("PRIMARY_COLOR", "#2c3e50"),
            "secondary": self.get_config_color("SECONDARY_COLOR", "#3498db"),
            "highlight": self.get_config_color("HIGHLIGHT_COLOR", "#2980b9"),
            "accent": self.get_config_color("ACCENT_COLOR", "#e74c3c"),
            "dark": self.get_config_color("DARK_COLOR", "#34495e"),
            "background": "#f0f0f0"
        }
        self.face_confidence_threshold = getattr(Config, "FACE_CONFIDENCE_THRESHOLD", 0.6)

    def get_config_color(self, color_name, default):
        """الحصول على لون من التكوين أو استخدام قيمة افتراضية."""
        try:
            return getattr(Config, color_name, default)
        except AttributeError:
            return default

    def _create_widgets(self):
        """إنشاء جميع مكونات واجهة المستخدم."""
        self._create_title_frame()
        self._create_content_frame()

    def _create_title_frame(self):
        """إنشاء إطار العنوان والشعار."""
        title_frame = ttk.Frame(self, style="Title.TFrame")
        title_frame.pack(pady=40, fill=tk.X)

        try:
            # Placeholder for a real logo image
            logo_img = Image.new('RGB', (120, 120), color=self.colors["accent"])
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(title_frame, image=self.logo_tk, background=self.colors["primary"])
            logo_label.pack(side=tk.LEFT, padx=20)
        except Exception:
            pass # Handle missing PIL or image file more gracefully if needed

        ttk.Label(title_frame, text="نظام بصيرة الهجين",
                  font=("Arial", 28, "bold"), foreground="white",
                  background=self.colors["primary"]).pack(pady=5)
        ttk.Label(title_frame, text="تسجيل الدخول الآمن",
                  font=("Arial", 16), foreground="#ddd",
                  background=self.colors["primary"]).pack(pady=5)

    def _create_content_frame(self):
        """إنشاء إطار المحتوى الذي يضم الكاميرا وخيارات التحكم."""
        content_frame = ttk.Frame(self, style="Content.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        self._create_camera_panel(content_frame)
        self._create_control_panel(content_frame)

    def _create_camera_panel(self, parent_frame):
        """إنشاء لوحة عرض الكاميرا."""
        camera_container = ttk.Frame(parent_frame)
        camera_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.camera_frame = ttk.LabelFrame(camera_container, text="بصمة الوجه", style="Camera.TLabelframe")
        self.camera_frame.pack(fill=tk.BOTH, expand=True)

        self.camera_label = ttk.Label(self.camera_frame, style="Camera.TLabel")
        self.camera_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def _create_control_panel(self, parent_frame):
        """إنشاء لوحة التحكم التي تحتوي على خيارات تسجيل الدخول ودخول المسؤول."""
        control_frame = ttk.Frame(parent_frame, style="Control.TFrame")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

        self._create_login_options(control_frame)
        self._create_admin_login_section(control_frame)

    def _create_login_options(self, parent_frame):
        """إنشاء أزرار خيارات تسجيل الدخول (وجه، إصبع، هجين)."""
        login_options_frame = ttk.LabelFrame(parent_frame, text="خيارات تسجيل الدخول", style="TLabelframe")
        login_options_frame.pack(fill=tk.X, pady=20)

        ttk.Button(login_options_frame, text="دخول بالوجه",
                   command=self._face_login, width=20).pack(pady=10, padx=20, fill=tk.X)
        ttk.Button(login_options_frame, text="دخول بالإصبع",
                   command=self._fingerprint_login, width=20).pack(pady=10, padx=20, fill=tk.X)
        ttk.Button(login_options_frame, text="دخول هجين (وجه + إصبع)",
                   command=self._hybrid_login, width=20, style="Hybrid.TButton").pack(pady=10, padx=20, fill=tk.X)

    def _create_admin_login_section(self, parent_frame):
        """إنشاء قسم تسجيل دخول المسؤول."""
        admin_frame = ttk.LabelFrame(parent_frame, text="دخول المسؤول", style="Admin.TLabelframe")
        admin_frame.pack(fill=tk.X, pady=20)

        ttk.Label(admin_frame, text="اسم المستخدم:", style="Admin.TLabel").pack(anchor=tk.W, padx=20, pady=(10, 0))
        self.username_entry = ttk.Entry(admin_frame, width=25, style="Admin.TEntry")
        self.username_entry.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(admin_frame, text="كلمة المرور:", style="Admin.TLabel").pack(anchor=tk.W, padx=20)
        self.password_entry = ttk.Entry(admin_frame, show="*", width=25, style="Admin.TEntry")
        self.password_entry.pack(fill=tk.X, padx=20, pady=5)

        ttk.Button(admin_frame, text="دخول",
                   command=self._admin_login, width=20, style="Admin.TButton").pack(pady=20, padx=20, fill=tk.X)

    def _configure_styles(self):
        """تكوين أنماط واجهة المستخدم."""
        style = ttk.Style()

        # General styles
        style.configure("TLabel", background=self.colors["background"], foreground="#333")
        style.configure("TLabelframe", background=self.colors["background"], foreground=self.colors["dark"], font=("Arial", 12, "bold"))
        style.configure("TLabelframe.Label", background=self.colors["background"], foreground=self.colors["dark"])
        style.configure("TEntry", font=("Arial", 10), padding=5)

        # Frame specific styles
        style.configure("Title.TFrame", background=self.colors["primary"])
        style.configure("Content.TFrame", background=self.colors["background"])
        style.configure("Control.TFrame", background=self.colors["background"])

        # Camera specific styles
        style.configure("Camera.TLabelframe", background=self.colors["background"])
        style.configure("Camera.TLabel", background="#333") # Dark background for camera feed

        # Button styles
        style.configure("TButton",
                        font=("Arial", 12, "bold"),
                        foreground="white",
                        background=self.colors["secondary"],
                        padding=10,
                        relief="flat")
        style.map("TButton",
                  background=[("active", self.colors["highlight"])])

        style.configure("Hybrid.TButton",
                        font=("Arial", 12, "bold"),
                        foreground="white",
                        background=self.colors["accent"],
                        padding=10,
                        relief="flat")
        style.map("Hybrid.TButton",
                  background=[("active", self.colors["highlight"])])

        style.configure("Admin.TButton",
                        font=("Arial", 12, "bold"),
                        foreground="white",
                        background=self.colors["dark"],
                        padding=10,
                        relief="flat")
        style.map("Admin.TButton",
                  background=[("active", self.colors["highlight"])])

    def _start_camera_thread(self):
        """بدء تشغيل الكاميرا في خيط منفصل لتجنب تجميد الواجهة."""
        threading.Thread(target=self._initialize_camera, daemon=True).start()

    def _initialize_camera(self):
        """تهيئة الكاميرا."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("خطأ", "لا يمكن الوصول إلى الكاميرا. يرجى التأكد من توصيلها بشكل صحيح.")
                self.camera_active = False
                return
            self.camera_active = True
            self.master.after(10, self._update_camera_feed) # Start updating feed after camera is ready
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في بدء تشغيل الكاميرا: {e}")
            self.camera_active = False

    def _update_camera_feed(self):
        """تحديث إطار الكاميرا بشكل مستمر."""
        if not self.camera_active or not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            try:
                # Face detection (lightweight)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_recognizer.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Convert to Tkinter format
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_tk = ImageTk.PhotoImage(image=img)

                # Update UI
                self.camera_label.configure(image=img_tk)
                self.camera_label.image = img_tk
            except Exception as e:
                print(f"Error updating camera feed: {e}") # Log error, don't show messagebox repeatedly

        if self.camera_active:
            self.master.after(50, self._update_camera_feed)

    def _stop_camera(self):
        """إيقاف تشغيل الكاميرا وتحرير مواردها."""
        self.camera_active = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None

    def _capture_single_frame(self):
        """التقاط إطار واحد من الكاميرا."""
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("خطأ", "الكاميرا غير نشطة أو غير متصلة.")
            return None
        ret, frame = self.cap.read()
        if ret:
            return frame
        messagebox.showerror("خطأ", "فشل في التقاط الصورة من الكاميرا.")
        return None

    def _face_login(self):
        """معالجة تسجيل الدخول باستخدام الوجه."""
        frame = self._capture_single_frame()
        if frame is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_recognizer.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if not faces:
            messagebox.showerror("خطأ", "لم يتم اكتشاف أي وجه.")
            return

        x, y, w, h = faces[0]
        face_img = gray[y:y + h, x:x + w]
        emp_id, confidence = self.face_recognizer.recognize_face(face_img)

        if confidence < self.face_confidence_threshold:
            employee = self.db_manager.get_employee(emp_id)
            if employee:
                messagebox.showinfo("نجاح", f"تم تسجيل الدخول بنجاح للموظف: {employee['name']}")
                self.on_login_success(employee)
                self._on_closing()
                return

        messagebox.showerror("فشل", "لم يتم التعرف على الوجه أو غير مصرح به.")

    def _fingerprint_login(self):
        """معالجة تسجيل الدخول باستخدام بصمة الإصبع."""
        if not self.fingerprint_manager.is_connected():
            messagebox.showerror("خطأ", "مستشعر البصمة غير متصل. يرجى التحقق من الاتصال.")
            return

        messagebox.showinfo("بصمة الإصبع", "يرجى وضع إصبعك على المستشعر...")
        position = self.fingerprint_manager.search_fingerprint()

        if position is None:
            messagebox.showerror("فشل", "بصمة الإصبع غير مسجلة أو لم يتم اكتشافها.")
            return

        employee = self.db_manager.get_employee_by_fingerprint(position)
        if employee:
            messagebox.showinfo("نجاح", f"تم تسجيل الدخول بنجاح للموظف: {employee['name']}")
            self.on_login_success(employee)
            self._on_closing()
        else:
            messagebox.showerror("فشل", "بصمة الإصبع غير مسجلة في النظام.")

    def _hybrid_login(self):
        """معالجة تسجيل الدخول الهجين (وجه + إصبع)."""
        frame = self._capture_single_frame()
        if frame is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_recognizer.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if not faces:
            messagebox.showerror("خطأ", "لم يتم اكتشاف أي وجه.")
            return

        x, y, w, h = faces[0]
        face_img = gray[y:y + h, x:x + w]
        emp_id, confidence = self.face_recognizer.recognize_face(face_img)

        if confidence >= self.face_confidence_threshold: # Changed from < to >= for failure case
            messagebox.showerror("فشل", "لم يتم التعرف على الوجه بشكل كافٍ.")
            return

        employee = self.db_manager.get_employee(emp_id)
        if not employee:
            messagebox.showerror("فشل", "الموظف المرتبط بالوجه غير مسجل.")
            return

        if not self.fingerprint_manager.is_connected():
            messagebox.showerror("خطأ", "مستشعر البصمة غير متصل. لا يمكن إتمام الدخول الهجين.")
            return

        messagebox.showinfo("بصمة الإصبع", "يرجى وضع إصبع الموظف على المستشعر للتحقق...")
        # Assuming verify_fingerprint takes employee's fingerprint template directly
        # This part might need adjustment based on actual FingerprintManager implementation
        if 'fingerprint_template' not in employee or not employee['fingerprint_template']:
            messagebox.showerror("فشل", "لا يوجد قالب بصمة إصبع مسجل لهذا الموظف.")
            return

        # This part assumes verify_fingerprint will capture a new fingerprint and compare
        # If it expects a pre-captured one, the logic needs to change.
        is_verified = self.fingerprint_manager.verify_fingerprint(employee['fingerprint_template'])

        if is_verified:
            messagebox.showinfo("نجاح", f"تم تسجيل الدخول الهجين بنجاح للموظف: {employee['name']}")
            self.on_login_success(employee)
            self._on_closing()
        else:
            messagebox.showerror("فشل", "بصمة الإصبع غير متطابقة أو لم يتم التحقق منها.")

    def _admin_login(self):
        """معالجة تسجيل دخول المسؤول."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("خطأ", "الرجاء إدخال اسم المستخدم وكلمة المرور.")
            return

        # For demonstration: hardcoded admin credentials
        if username == "admin" and password == "admin123":
            admin_data = {
                'emp_id': 'ADMIN001',
                'name': 'مسؤول النظام',
                'position': 'مدير'
            }
            messagebox.showinfo("نجاح", "تم تسجيل دخول المسؤول بنجاح.")
            self.on_login_success(admin_data)
            self._on_closing()
        else:
            messagebox.showerror("فشل", "بيانات الاعتماد غير صحيحة. يرجى التحقق والمحاولة مرة أخرى.")

    def _on_closing(self):
        """إغلاق النافذة وتحرير الموارد عند محاولة الإغلاق."""
        self._stop_camera()
        self.destroy()

    def __del__(self):
        """تحرير الموارد عند حذف الكائن."""
        self._stop_camera()

# Example of how to run the LoginScreen (for testing purposes)
if __name__ == "__main__":
    # Mock classes for demonstration if core modules are not available
    class MockFaceRecognizer:
        def __init__(self):
            class MockCascade:
                def detectMultiScale(self, *args, **kwargs):
                    return [] # No faces detected by default
            self.face_cascade = MockCascade()
        def recognize_face(self, face_img):
            return "unknown", 0.0

    class MockFingerprintManager:
        def is_connected(self):
            return True
        def search_fingerprint(self):
            return None
        def verify_fingerprint(self, template):
            return False

    class MockDatabaseManager:
        def get_employee(self, emp_id):
            if emp_id == "EMP001":
                return {'emp_id': 'EMP001', 'name': 'أحمد', 'fingerprint_template': 'template_ahmed'}
            return None
        def get_employee_by_fingerprint(self, position):
            if position == 1:
                return {'emp_id': 'EMP001', 'name': 'أحمد', 'fingerprint_template': 'template_ahmed'}
            return None

    class MockConfig:
        PRIMARY_COLOR = "#1a2a3a"
        SECONDARY_COLOR = "#4a90e2"
        HIGHLIGHT_COLOR = "#3a7bd5"
        ACCENT_COLOR = "#c0392b"
        DARK_COLOR = "#2c3e50"
        FACE_CONFIDENCE_THRESHOLD = 0.7

    # Override the actual imports with mocks for testing
    import sys
    sys.modules['core.face_recognition'] = type('module', (object,), {'FaceRecognizer': MockFaceRecognizer})
    sys.modules['core.fingerprint'] = type('module', (object,), {'FingerprintManager': MockFingerprintManager})
    sys.modules['core.database'] = type('module', (object,), {'DatabaseManager': MockDatabaseManager})
    sys.modules['config'] = type('module', (object,), {'Config': MockConfig})

    def on_login_success_callback(employee_data):
        print(f"Login successful for: {employee_data['name']}")
        root.destroy()

    root = tk.Tk()
    root.withdraw() # Hide the main Tkinter window
    login_screen = LoginScreen(root, on_login_success_callback)
    root.mainloop()

