# core/visitor.py

import os
import cv2
import sqlite3
from .face_recognition import FaceRecognizer
import numpy as np
from datetime import datetime
from config import Config
from cryptography.fernet import Fernet
from .utils import ReportGenerator

class VisitorSystem:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DATABASE_NAME)
        self.cursor = self.conn.cursor()
        self._init_db()
        self.cipher = Fernet(Config.AES_KEY)
      
    
    def _init_db(self):
        """تهيئة قاعدة بيانات الزوار"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_id TEXT UNIQUE NOT NULL,
                name TEXT,
                organization TEXT,
                person_to_meet TEXT,
                purpose TEXT,
                face_encoding BLOB,
                fingerprint_template BLOB,
                access_level INTEGER DEFAULT 1,
                checkin_time DATETIME,
                checkout_time DATETIME,
                is_unknown BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def register_visitor(self, name, organization, person_to_meet, purpose, face_image):
        """تسجيل زائر جديد"""
        visitor_id = generate_unique_id("VIS")
        
        # استخراج ملامح الوجه
        face_encoding = self._extract_face_encoding(face_image)
        
        if face_encoding is None:
            return None
        
        # تشفير البيانات الحساسة
        encrypted_face = self.cipher.encrypt(face_encoding.tobytes())
        
        # تحديد مستوى الوصول
        access_level = self._determine_access_level(purpose)
        
        # إضافة الزائر إلى قاعدة البيانات
        self.cursor.execute("""
            INSERT INTO visitors (visitor_id, name, organization, person_to_meet, purpose, 
                                 face_encoding, access_level, checkin_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (visitor_id, name, organization, person_to_meet, purpose, 
              encrypted_face, access_level))
        
        self.conn.commit()
        return visitor_id
    
    def register_unknown_visitor(self, face_image):
        """تسجيل زائر غير معروف"""
        visitor_id = generae_unique_id("UNK")
        face_encoding = self._extract_face_encoding(face_image)
        
        if face_encoding is None:
            return None
        
        # حفظ صورة الزائر غير المعروف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(Config.UNKNOWN_VISITOR_DIR, f"{visitor_id}_{timestamp}.jpg")
        cv2.imwrite(img_path, face_image)
        
        # إضافة إلى قاعدة البيانات
        self.cursor.execute("""
            INSERT INTO visitors (visitor_id, is_unknown, face_encoding, checkin_time)
            VALUES (?, 1, ?, datetime('now'))
        """, (visitor_id, self.cipher.encrypt(face_encoding.tobytes())))
        
        self.conn.commit()
        return visitor_id
    
    def check_visitor(self, face_image):
        """التحقق من هوية الزائر"""
        # استخراج ملامح الوجه
        current_encoding = self._extract_face_encoding(face_image)
        
        if current_encoding is None:
            return None
        
        # البحث في قاعدة البيانات
        self.cursor.execute("SELECT visitor_id, face_encoding FROM visitors")
        visitors = self.cursor.fetchall()
        
        for visitor in visitors:
            stored_encoding = np.frombuffer(self.cipher.decrypt(visitor[1]), dtype=np.float64)
            
            # مقارنة الوجوه
            match =FaceRecognizer.compare_faces([stored_encoding], current_encoding)
            
            if match[0]:
                return visitor[0]
        
        return None
    
    def checkout_visitor(self, visitor_id):
        """تسجيل خروج الزائر"""
        self.cursor.execute("""
            UPDATE visitors 
            SET checkout_time = datetime('now')
            WHERE visitor_id = ? AND checkout_time IS NULL
        """, (visitor_id,))
        
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_visitor_info(self, visitor_id):
        """الحصول على معلومات الزائر"""
        self.cursor.execute("""
            SELECT visitor_id, name, organization, person_to_meet, purpose, 
                   access_level, checkin_time, checkout_time, is_unknown
            FROM visitors
            WHERE visitor_id = ?
        """, (visitor_id,))
        
        visitor = self.cursor.fetchone()
        
        if visitor:
            return {
                "id": visitor[0],
                "name": visitor[1],
                "organization": visitor[2],
                "person_to_meet": visitor[3],
                "purpose": visitor[4],
                "access_level": visitor[5],
                "checkin_time": visitor[6],
                "checkout_time": visitor[7],
                "is_unknown": visitor[8]
            }
        
        return None
    
    def get_today_visitors(self):
        """الحصول على زوار اليوم"""
        self.cursor.execute("""
            SELECT visitor_id, name, organization, person_to_meet, purpose, 
                   access_level, checkin_time, checkout_time, is_unknown
            FROM visitors
            WHERE date(checkin_time) = date('now')
            ORDER BY checkin_time DESC
        """)
        
        return self.cursor.fetchall()
    
    def _extract_face_encoding(self, image):
        """استخراج ملامح الوجه"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            return None
        
        # استخدام أول وجه مكتشف
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        return face_encodings[0] if len(face_encodings) > 0 else None
    
    def _determine_access_level(self, purpose):
        """تحديد مستوى الوصول بناءً على الغرض من الزيارة"""
        purpose = purpose.lower()
        
        if "اجتماع" in purpose or "مدير" in purpose:
            return 3
        elif "مقابلة" in purpose or "توظيف" in purpose:
            return 2
        elif "تسليم" in purpose or "استلام" in purpose:
            return 1
        else:
            return 1