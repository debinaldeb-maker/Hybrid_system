# gui/employee.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
from PIL import Image, ImageTk
import cv2
from core.database import DatabaseManager
from core.face_recognition import FaceRecognizer
from core.fingerprint import FingerprintManager
from config import Config
import weakref

class EmployeeManagement(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.face_recognizer = FaceRecognizer()
        self.fingerprint_manager = FingerprintManager()
        self.current_employee_id = None
        
        # إنشاء واجهة المستخدم
        self.create_widgets()
        self.load_employees()
    
    def create_widgets(self):
        # إطار رئيسي
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # شريط الأدوات
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=10)
        
        btn_add = ttk.Button(toolbar, text="➕ إضافة موظف جديد", command=self.add_employee)
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_edit = ttk.Button(toolbar, text="✏️ تعديل الموظف", command=self.edit_employee)
        btn_edit.pack(side=tk.LEFT, padx=5)
        
        btn_delete = ttk.Button(toolbar, text="🗑️ حذف الموظف", command=self.delete_employee)
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = ttk.Button(toolbar, text="🔄 تحديث القائمة", command=self.load_employees)
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        # شجرة الموظفين
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("emp_id", "name", "position", "face_registered", "fingerprint_registered")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # عناوين الأعمدة
        headings = {
            "emp_id": "رقم الموظف",
            "name": "الاسم الكامل",
            "position": "الوظيفة",
            "face_registered": "بصمة الوجه",
            "fingerprint_registered": "بصمة الإصبع"
        }
        
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # التخطيط
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط حدث التحديد
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)
    
    def load_employees(self):
        """تحميل قائمة الموظفين من قاعدة البيانات"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب الموظفين من قاعدة البيانات
        conn = self.db_manager.conn
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, position, face_template, fingerprint_template FROM employees")
        employees = cursor.fetchall()
        
        # إضافة الموظفين إلى الشجرة
        for emp in employees:
            emp_id, name, position, face_embeddings, fingerprint_template = emp
            face_registered = "✅" if face_embeddings else "❌"
            fingerprint_registered = "✅" if fingerprint_template else "❌"
            
            self.tree.insert("", tk.END, values=(
                emp_id, name, position, face_registered, fingerprint_registered
            ))
    
    def on_employee_select(self, event):
        """التعامل مع اختيار موظف من القائمة"""
        selected = self.tree.selection()
        if selected:
            self.current_employee_id = self.tree.item(selected[0], "values")[0]

    def check_camera_available(self):
        """التحقق من توفر الكاميرا"""
        try:
            cap = cv2.VideoCapture(0)
            if cap is None or not cap.isOpened():
                return False
            cap.release()
            return True
        except:
            return False
        
    def capture_employee_photo(self, form):
        """التقاط صورة الموظف باستخدام الكاميرا"""
        if not self.check_camera_available():
            messagebox.showerror("خطأ", "الكاميرا غير متوفرة")
            return
            
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("خطأ", "لا يمكن الوصول إلى الكاميرا")
            return
            
        try:
            ret, frame = cap.read()
            if ret:
                # تحويل الإطار إلى صورة
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                
                # تغيير حجم الصورة لتناسب العرض
                img.thumbnail((200, 200))
                
                # حفظ الصورة للاستخدام لاحقاً
                form.photo_img = img
                
                # تحديث الصورة في واجهة المستخدم
                form.photo_tk = ImageTk.PhotoImage(img)
                form.img_label.configure(image=form.photo_tk)
                form.img_label.image = form.photo_tk  # تحديث المرجع
            else:
                messagebox.showerror("خطأ", "فشل في التقاط الصورة")
        finally:
            cap.release()

    def add_employee(self):
        """فتح نموذج إضافة موظف جديد"""
        form = tk.Toplevel(self)
        form.title("إضافة موظف جديد")
        form.geometry("600x500")
        form.grab_set()
        form.resizable(False, False)
        
        # تخزين مراجع الصورة في نافذة النموذج
        form.photo_img = None
        form.photo_tk = None
        
        # إطار الصورة
        img_frame = ttk.LabelFrame(form, text="صورة الموظف")
        img_frame.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky=tk.N)
        
        # إنشاء صورة افتراضية
        default_img = Image.new('RGB', (200, 200), color='#f0f0f0')
        form.photo_tk = ImageTk.PhotoImage(default_img)
        
        # إنشاء الـ Label
        form.img_label = ttk.Label(img_frame, image=form.photo_tk)
        form.img_label.pack(padx=10, pady=10)
        
        # حقول النموذج
        fields_frame = ttk.Frame(form)
        fields_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)
        
        ttk.Label(fields_frame, text="رقم الموظف:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        emp_id_entry = ttk.Entry(fields_frame, width=25)
        emp_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(fields_frame, text="اسم الموظف:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(fields_frame, width=25)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(fields_frame, text="الوظيفة:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        position_entry = ttk.Entry(fields_frame, width=25)
        position_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(fields_frame, text="كلمة المرور:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        password_entry = ttk.Entry(fields_frame, show="*", width=25)
        password_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # أزرار الإجراءات
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        btn_capture_photo = ttk.Button(btn_frame, text="📷 التقاط صورة", 
                                      command=lambda: self.capture_employee_photo(form))
        btn_capture_photo.pack(side=tk.LEFT, padx=5)
        
        btn_capture_face = ttk.Button(btn_frame, text="👤 تسجيل بصمة الوجه", 
                                     command=lambda: self.capture_face(emp_id_entry.get()))
        btn_capture_face.pack(side=tk.LEFT, padx=5)
        
        btn_capture_finger = ttk.Button(btn_frame, text="🖐️ تسجيل بصمة الإصبع", 
                                       command=lambda: self.capture_fingerprint(emp_id_entry.get()))
        btn_capture_finger.pack(side=tk.LEFT, padx=5)
        
        btn_save = ttk.Button(btn_frame, text="💾 حفظ الموظف", 
                             command=lambda: self.save_employee(
                                 form,
                                 emp_id_entry.get(),
                                 name_entry.get(),
                                 position_entry.get(),
                                 password_entry.get()
                             ))
        btn_save.pack(side=tk.RIGHT, padx=5)
    
    def capture_fingerprint(self, emp_id):
        """التقاط بصمة الإصبع"""
        if not emp_id:
            messagebox.showerror("خطأ", "الرجاء إدخال رقم الموظف أولاً")
            return
        
        if not self.fingerprint_manager.is_connected():
            messagebox.showerror("خطأ", "مستشعر البصمة غير متصل")
            return
        
        # التقاط البصمة (في التطبيق الحقيقي سيتم استدعاء الجهاز)
        # template = self.fingerprint_manager.capture_fingerprint()
        template = b"fake_fingerprint_template_data"  # بيانات افتراضية
        
        # حفظ البصمة في قاعدة البيانات
        conn = self.db_manager.conn
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET fingerprint_template = ? WHERE emp_id = ?", 
                      (template, emp_id))
        conn.commit()
        
        messagebox.showinfo("تم", "تم تسجيل بصمة الإصبع بنجاح")
    
    def save_employee(self, form, emp_id, name, position, password):
        """حفظ بيانات الموظف في قاعدة البيانات"""
        if not all([emp_id, name, position, password]):
            messagebox.showerror("خطأ", "الرجاء إدخال جميع البيانات المطلوبة")
            return
        
        # إضافة الموظف إلى قاعدة البيانات
        try:
            self.db_manager.add_employee(emp_id, name, position, password)
            messagebox.showinfo("تم", "تم إضافة الموظف بنجاح")
            form.destroy()
            self.load_employees()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إضافة الموظف: {str(e)}")
    
    def edit_employee(self):
        """تعديل بيانات الموظف المحدد"""
        if not self.current_employee_id:
            messagebox.showerror("خطأ", "الرجاء تحديد موظف")
            return
        
        # جلب بيانات الموظف من قاعدة البيانات
        conn = self.db_manager.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (self.current_employee_id,))
        employee = cursor.fetchone()
        
        if not employee:
            messagebox.showerror("خطأ", "الموظف غير موجود")
            return
        
        # فتح نموذج التعديل (مشابه لنموذج الإضافة)
        form = tk.Toplevel(self)
        form.title("تعديل بيانات الموظف")
        form.geometry("600x500")
        form.grab_set()
        form.resizable(False, False)
        
        # ... (كود مشابه لنموذج الإضافة مع تعبئة الحقول الحالية) ...
    
    def delete_employee(self):
        """حذف الموظف المحدد"""
        if not self.current_employee_id:
            messagebox.showerror("خطأ", "الرجاء تحديد موظف")
            return
        
        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الموظف {self.current_employee_id}؟"):
            try:
                # حذف من قاعدة البيانات
                conn = self.db_manager.conn
                cursor = conn.cursor()
                cursor.execute("DELETE FROM employees WHERE emp_id = ?", (self.current_employee_id,))
                conn.commit()
                
                # حذف البيانات الحيوية
                self.delete_biometric_data(self.current_employee_id)
                
                messagebox.showinfo("تم", "تم حذف الموظف بنجاح")
                self.load_employees()
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في حذف الموظف: {str(e)}")
    
    def delete_biometric_data(self, emp_id):
        """حذف البيانات الحيوية للموظف"""
        # حذف مجلد الموظف
        employee_dir = os.path.join(Config.DATA_DIR, "employees", emp_id)
        if os.path.exists(employee_dir):
            shutil.rmtree(employee_dir)
        
        # تحديث نموذج التعرف على الوجه
        self.face_recognizer.train_model()
    
    def close(self):
        """تنظيف الموارد عند إغلاق الوحدة"""
        # إغلاق اتصال قاعدة البيانات
        if hasattr(self.db_manager, 'conn'):
            self.db_manager.conn.close()
        
        # تدمير جميع العناصر الفرعية
        for widget in self.winfo_children():
            try:
                widget.destroy()
            except:
                pass