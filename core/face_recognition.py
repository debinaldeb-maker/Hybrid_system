import cv2
import os
import numpy as np
import sqlite3
from config import Config
from sklearn.neighbors import KNeighborsClassifier
import joblib

class FaceRecognizer:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(Config.HAAR_CASCADE)
        self.recognizer = self._load_or_create_model()
        self.labels_map = {}
        self._load_labels()
    
    def _load_or_create_model(self):
        """تحميل أو إنشاء نموذج التعرف على الوجوه"""
        if os.path.exists(Config.TRAINER_FILE):
            return joblib.load(Config.TRAINER_FILE)
        return KNeighborsClassifier(n_neighbors=5)
    
    def _load_labels(self):
        """تحميل تسميات الموظفين"""
        if os.path.exists(Config.LABELS_FILE):
            self.labels_map = joblib.load(Config.LABELS_FILE)
    
    def detect_faces(self, frame):
        """الكشف عن الوجوه في إطار الفيديو"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )
        return gray, faces
    
    def recognize_face(self, face_img):
        """التعرف على وجه"""
        # تغيير حجم الصورة وتسطيحها
        resized = cv2.resize(face_img, (100, 100)).flatten()
        prediction = self.recognizer.predict([resized])
        emp_id = prediction[0]
        
        # حساب المسافة إلى أقرب الجيران (كقيمة ثقة)
        distances, indices = self.recognizer.kneighbors([resized])
        confidence = 100 - distances[0][0]
        
        return emp_id, confidence
    
    def capture_training_images(self, emp_id, num_images=50):
        """التقاط صور تدريبية لموظف جديد"""
        # إنشاء مجلد للموظف
        user_dir = os.path.join(Config.DATASET_PATH, f"User_{emp_id}")
        os.makedirs(user_dir, exist_ok=True)
        
        # فتح الكاميرا
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise RuntimeError("فشل في فتح الكاميرا")
        
        count = 0
        while count < num_images:
            ret, frame = cam.read()
            if not ret:
                continue
            
            gray, faces = self.detect_faces(frame)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                face_img = gray[y:y+h, x:x+w]
                
                # حفظ الصورة
                img_path = os.path.join(user_dir, f"{emp_id}_{count}.jpg")
                cv2.imwrite(img_path, face_img)
                count += 1
            
            # عرض التقدم
            cv2.putText(frame, f"التقطت: {count}/{num_images}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('التقاط صور التدريب', frame)
            
            if cv2.waitKey(100) & 0xFF == 27:  # زر ESC للخروج
                break
        
        cam.release()
        cv2.destroyAllWindows()
        self._train_new_model()  # إعادة تدريب النموذج
    
    def _train_new_model(self):
        """تدريب نموذج جديد للتعرف على الوجوه"""
        faces = []
        labels = []
        self.labels_map = {}
        
        # جمع بيانات التدريب
        for root, dirs, files in os.walk(Config.DATASET_PATH):
            for file in files:
                if file.endswith('.jpg'):
                    # استخراج emp_id من اسم المجلد
                    emp_id = int(root.split('_')[-1])
                    
                    # تحميل الصورة
                    img_path = os.path.join(root, file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    
                    if img is not None:
                        # تغيير الحجم والتسطيح
                        resized = cv2.resize(img, (100, 100)).flatten()
                        faces.append(resized)
                        labels.append(emp_id)
                        
                        # تحديث خريطة التسميات
                        self.labels_map[emp_id] = f"User_{emp_id}"
        
        if len(faces) == 0:
            raise ValueError("لا توجد صور للتدريب")
        
        # تدريب النموذج
        self.recognizer.fit(faces, labels)
        
        # حفظ النموذج والتسميات
        os.makedirs(os.path.dirname(Config.TRAINER_FILE), exist_ok=True)
        joblib.dump(self.recognizer, Config.TRAINER_FILE)
        joblib.dump(self.labels_map, Config.LABELS_FILE)
    
    def get_employee_name(self, emp_id):
        """الحصول على اسم الموظف"""
        return self.labels_map.get(emp_id, "غير معروف")