import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import os
import time

class CameraProcessor:
    def __init__(self):
        self.cap = self._init_video_source()

        # Carrega os modelos treinados
        self.model1 = YOLO('C:/Users/switc/Downloads/VisualShield_tcc-layout (1)/VisualShield_tcc-layout/runs/detect/train/weights/best.pt')    # Capacete
        self.model2 = YOLO('C:/Users/switc/Downloads/VisualShield_tcc-layout (1)/VisualShield_tcc-layout/runs/detect/train2/weights/best.pt')   # Luvas
        self.model3 = YOLO('C:/Users/switc/Downloads/VisualShield_tcc-layout (1)/VisualShield_tcc-layout/runs/detect/train3/weights/best.pt')   # Óculos

        # Cores e rótulos
        self.color1 = (0, 0, 255)     # Vermelho - Capacete
        self.color2 = (0, 255, 255)   # Amarelo - Luvas
        self.color3 = (255, 0, 0)     # Azul - Óculos
        self.name1 = "Capacete"
        self.name2 = "Luva"
        self.name3 = "Oculos"

        self.detections_log = []  # Armazena os alertas reais detectados

    def _init_video_source(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not cap.isOpened():
            print("Erro: Não foi possível abrir a câmera")
            return self._create_test_video()
        return cap

    def _create_test_video(self):
        print("Usando vídeo simulado como fallback")
        class TestVideo:
            def read(self):
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Camera Simulation", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                return True, frame
        return TestVideo()

    def generate_frames(self):
        os.makedirs("saved_frames", exist_ok=True)
        last_save_time = time.time()

        while True:
            success, frame = self.cap.read()
            if not success:
                break

            annotated_frame = frame.copy()
            detections = []

            results1 = self.model1.predict(frame, conf=0.7, verbose=False)
            results2 = self.model2.predict(frame, conf=0.7, verbose=False)
            results3 = self.model3.predict(frame, conf=0.7, verbose=False)

            detections += self._draw_boxes(annotated_frame, results1, self.color1, self.name1)
            detections += self._draw_boxes(annotated_frame, results2, self.color2, self.name2)
            detections += self._draw_boxes(annotated_frame, results3, self.color3, self.name3)

            current_time = time.time()
            if current_time - last_save_time >= 15:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"frame_{timestamp}.jpg"
                filepath = os.path.join("saved_frames", filename)
                cv2.imwrite(filepath, annotated_frame)

                if not detections:
                    self.detections_log.append({
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "Nenhum",
                        "image": filename,
                        "status": "Não detectado"
                    })

                last_save_time = current_time

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def _draw_boxes(self, frame, results, color, label_name):
        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            label = f"{label_name} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"frame_{timestamp}.jpg"
            filepath = os.path.join("saved_frames", filename)
            cv2.imwrite(filepath, frame)

            self.detections_log.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": label_name,
                "image": filename,
                "status": "Detectado"
            })

            detections.append(label_name)

            if len(self.detections_log) > 100:
                self.detections_log.pop(0)

        return detections