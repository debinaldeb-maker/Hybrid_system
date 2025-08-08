import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config import Config

class HeatmapVisualizer(ttk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.data = data or self.generate_sample_data()
        self.create_widgets()
    
    def generate_sample_data(self):
        """إنشاء بيانات نموذجية للعرض"""
        return np.random.rand(10, 10)
    
    def create_widgets(self):
        # إنشاء شكل الخريطة الحرارية
        fig, ax = plt.subplots(figsize=(8, 6))
        heatmap = ax.imshow(self.data, cmap='viridis')
        fig.colorbar(heatmap)
        
        # تضمين الشكل في واجهة Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # أزرار التحكم
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="تحديث", command=self.update_heatmap).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="تصدير", command=self.export_heatmap).pack(side=tk.RIGHT, padx=5)
    
    def update_heatmap(self, new_data=None):
        """تحديث الخريطة الحرارية ببيانات جديدة"""
        if new_data is None:
            new_data = self.generate_sample_data()
        
        # تحديث البيانات وإعادة الرسم
        self.canvas.figure.axes[0].images[0].set_data(new_data)
        self.canvas.figure.axes[0].autoscale()
        self.canvas.draw()
    
    def export_heatmap(self):
        """تصدير الخريطة كصورة"""
        # في التطبيق الحقيقي سيتم حفظ الصورة في ملف
        print("تم تصدير الخريطة الحرارية")

# اختبار الوحدة
if __name__ == "__main__":
    root = tk.Tk()
    app = HeatmapVisualizer(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
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