# core/utils.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from config import Config
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_attendance_report(attendance_data):
        """إنشاء تقرير الحضور"""
        df = pd.DataFrame(attendance_data, columns=[
            'emp_id', 'name', 'date', 'time_in', 'time_out', 'productivity'
        ])
        
        # تحويل الأعمدة الزمنية
        df['time_in'] = pd.to_datetime(df['date'] + ' ' + df['time_in'])
        df['time_out'] = pd.to_datetime(df['date'] + ' ' + df['time_out'])
        
        # حساب ساعات العمل
        df['work_hours'] = (df['time_out'] - df['time_in']).dt.total_seconds() / 3600
        df['work_hours'] = df['work_hours'].fillna(0)
        
        # إنشاء تقرير ملخص
        summary = df.groupby(['emp_id', 'name']).agg({
            'date': 'count',
            'work_hours': 'sum',
            'productivity': 'mean'
        }).reset_index()
        summary.columns = ['emp_id', 'name', 'days_present', 'total_hours', 'avg_productivity']
        
        return summary
    
    @staticmethod
    def generate_heatmap(attendance_data):
        """إنشاء خريطة حرارية لأداء الموظفين"""
        df = pd.DataFrame(attendance_data, columns=[
            'emp_id', 'name', 'date', 'time_in', 'time_out', 'productivity'
        ])
        
        # تحويل البيانات إلى مصفوفة خريطة حرارية
        pivot = df.pivot_table(
            index='name',
            columns='date',
            values='productivity',
            fill_value=0,
            aggfunc='mean'
        )
        
        # إنشاء الخريطة الحرارية
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, cmap="YlGnBu", linewidths=.5)
        plt.title("الخرائط الحرارية لأداء الموظفين")
        plt.ylabel("الموظف")
        plt.xlabel("التاريخ")
        plt.tight_layout()
        
        # حفظ الخريطة
        os.makedirs(Config.HEATMAP_DIR, exist_ok=True)
        heatmap_path = os.path.join(Config.HEATMAP_DIR, f"heatmap_{datetime.now().strftime('%Y%m%d')}.png")
        plt.savefig(heatmap_path)
        plt.close()
        
        return heatmap_path
    
    @staticmethod
    def export_to_csv(data, filename):
        """تصدير البيانات إلى ملف CSV"""
        os.makedirs(Config.ATTENDANCE_DIR, exist_ok=True)
        filepath = os.path.join(Config.ATTENDANCE_DIR, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        return filepath