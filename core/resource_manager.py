import cv2
import sqlite3
from contextlib import contextmanager
from config import Config

class ResourceManager:
    _cameras = {}
    _db_connections = {}
    _fingerprint_sensors = {}
    
    @classmethod
    @contextmanager
    def get_camera(cls, camera_id=0):
        if camera_id not in cls._cameras:
            cls._cameras[camera_id] = cv2.VideoCapture(camera_id)
            if not cls._cameras[camera_id].isOpened():
                raise RuntimeError(f"فشل في فتح الكاميرا {camera_id}")
        
        try:
            yield cls._cameras[camera_id]
        finally:
            pass  # لا نغلق الكاميرا هنا، سنغلقها عند الخروج
        
    @classmethod
    @contextmanager
    def get_db_connection(cls, db_name=None):
        db_name = db_name or Config.DATABASE_NAME
        if db_name not in cls._db_connections:
            cls._db_connections[db_name] = sqlite3.connect(db_name)
        
        try:
            yield cls._db_connections[db_name].cursor()
            cls._db_connections[db_name].commit()
        finally:
            pass  # لا نغلق الاتصال هنا
        
    @classmethod
    def close_all_resources(cls):
        # إغلاق جميع الكاميرات
        for cam_id, cam in cls._cameras.items():
            if cam.isOpened():
                cam.release()
        cls._cameras = {}
        
        # إغلاق جميع اتصالات قاعدة البيانات
        for db_name, conn in cls._db_connections.items():
            if conn:
                conn.close()
        cls._db_connections = {}
        
        # إغلاق جميع أجهزة البصمة
        for sensor in cls._fingerprint_sensors.values():
            if sensor:
                sensor.close()
        cls._fingerprint_sensors = {}