# core/fingerprint.py

try:
    from pyfingerprint import PyFingerprint
except ImportError:
    PyFingerprint = None

import sqlite3
import hashlib
from config import Config
from cryptography.fernet import Fernet

class FingerprintManager:
    def __init__(self):
        self.sensor = None
        self._initialize_sensor()
        self.cipher = Fernet(Config.AES_KEY)
    
    def _initialize_sensor(self):
        """تهيئة مستشعر بصمة الإصبع"""
        if PyFingerprint is None:
            return
            
        try:
            self.sensor = PyFingerprint(
                Config.FINGERPRINT_PORT,
                Config.FINGERPRINT_BAUDRATE,
                0xFFFFFFFF,
                0x00000000
            )
            
            if not self.sensor.verifyPassword():
                raise RuntimeError("كلمة مرور المستشعر غير صحيحة")
        except Exception as e:
            print(f"تحذير: تعذر تهيئة مستشعر البصمة: {str(e)}")
            self.sensor = None
    
    def is_connected(self):
        """التحقق من اتصال المستشعر"""
        return self.sensor is not None
    
    def capture_fingerprint(self):
        """التقاط بصمة إصبع جديدة"""
        if not self.is_connected():
            return None
        
        try:
            # انتظار وضع الإصبع
            print("ضع إصبعك على المستشعر...")
            while not self.sensor.readImage():
                pass
            
            # تحويل الصورة إلى قالب
            self.sensor.convertImage(0x01)
            
            # إنشاء القالب
            result = self.sensor.createTemplate()
            if result < 0:
                raise RuntimeError("فشل في إنشاء القالب")
            
            # تنزيل القالب
            template = self.sensor.downloadCharacteristics(0x01)
            
            # تشفير القالب
            encrypted_template = self.cipher.encrypt(bytes(template))
            return encrypted_template
        except Exception as e:
            print(f"خطأ في التقاط البصمة: {str(e)}")
            return None
    
    def verify_fingerprint(self, stored_template):
        """المصادقة باستخدام بصمة الإصبع"""
        if not self.is_connected() or stored_template is None:
            return False
        
        try:
            # فك تشفير القالب المخزن
            template = self.cipher.decrypt(stored_template)
            
            # تحميل القالب إلى المستشعر
            self.sensor.uploadCharacteristics(0x01, list(template))
            
            # انتظار وضع الإصبع للمصادقة
            print("ضع إصبعك للمصادقة...")
            while not self.sensor.readImage():
                pass
            
            # تحويل الصورة إلى قالب
            self.sensor.convertImage(0x02)
            
            # المقارنة بين القوالب
            result = self.sensor.compareCharacteristics()
            return result > Config.FINGERPRINT_THRESHOLD
        except Exception as e:
            print(f"خطأ في المصادقة: {str(e)}")
            return False
    
    def search_fingerprint(self):
        """البحث عن بصمة في قاعدة البيانات"""
        if not self.is_connected():
            return None
        
        try:
            # التقاط البصمة
            print("ضع إصبعك للبحث...")
            while not self.sensor.readImage():
                pass
            
            # تحويل الصورة إلى قالب
            self.sensor.convertImage(0x01)
            
            # البحث في المستشعر
            result = self.sensor.searchTemplate()
            position = result[0]
            accuracy = result[1]
            
            if position == -1:
                return None
                
            return position, accuracy
        except Exception as e:
            print(f"خطأ في البحث: {str(e)}")
            return None