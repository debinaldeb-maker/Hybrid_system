import threading
import time
import random
import csv
from datetime import datetime
from config import Config
import os

class SecurityMonitor:
    def __init__(self):
        self.monitoring = False
        self.threads = []
        self.alerts = []
        self.lock = threading.Lock()
        
        # إنشاء ملف السجل إذا لم يكن موجودًا
     #   os.makedirs(os.path.dirname(Config.INTRUSION_LOG), exist_ok=True)
        #if not os.path.exists(Config.INTRUSION_LOG):
      #      with open(Config.INTRUSION_LOG, 'w', newline='') as f:
       #         writer = csv.writer(f)
       #         writer.writerow(['timestamp', 'sensor_type', 'location', 'severity'])
    
    def start_monitoring(self):
        """بدء مراقبة المستشعرات الأمنية"""
        if self.monitoring:
            return
        
        self.monitoring = True
        
        # بدء مراقبة مستشعرات الحركة
        pir_thread = threading.Thread(target=self._monitor_pir_sensors, daemon=True)
        pir_thread.start()
        self.threads.append(pir_thread)
        
        # بدء مراقبة الكاميرات الحرارية
        thermal_thread = threading.Thread(target=self._monitor_thermal_cameras, daemon=True)
        thermal_thread.start()
        self.threads.append(thermal_thread)
    
    def stop_monitoring(self):
        """إيقاف مراقبة المستشعرات الأمنية"""
        self.monitoring = False
        for thread in self.threads:
            thread.join(timeout=2.0)
        self.threads = []
    
    def _monitor_pir_sensors(self):
        """مراقبة مستشعرات الحركة (PIR)"""
        while self.monitoring:
            # محاكاة اكتشاف الحركة
            if random.random() < 0.05:  # 5% فرصة للكشف
                location = f"Gate-{random.randint(1, 4)}"
                severity = random.randint(1, 5)
                self._log_intrusion("PIR", location, severity)
            
            time.sleep(Config.SENSOR_CHECK_INTERVAL)
    
    def _monitor_thermal_cameras(self):
        """مراقبة الكاميرات الحرارية"""
        while self.monitoring:
            # محاكاة اكتشاف التسلل
            if random.random() < 0.02:  # 2% فرصة للكشف
                location = f"Perimeter-{random.randint(1, 5)}"
                severity = random.randint(3, 6)
                self._log_intrusion("Thermal", location, severity)
            
            time.sleep(Config.SENSOR_CHECK_INTERVAL * 2)
    
    def _log_intrusion(self, sensor_type, location, severity):
        """تسجيل حدث الاختراق"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # تسجيل في ملف CSV
        with open(Config.INTRUSION_LOG, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, sensor_type, location, severity])
        
        # تخزين الإنذار في الذاكرة
        with self.lock:
            self.alerts.insert(0, {
                'timestamp': timestamp,
                'sensor_type': sensor_type,
                'location': location,
                'severity': severity
            })
            
            # الاحتفاظ فقط بـ 50 إنذارًا حديثًا
            if len(self.alerts) > 50:
                self.alerts = self.alerts[:50]
        
        print(f"تم تسجيل اختراق: {sensor_type} في {location} - الشدة: {severity}")
    
    def get_recent_alerts(self, limit=10):
        """الحصول على أحدث الإنذارات"""
        with self.lock:
            return self.alerts[:limit]