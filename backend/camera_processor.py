import cv2
import numpy as np
import random

class CameraProcessor:
    def __init__(self):
        self.cap = self._init_video_source()
        
    def _init_video_source(self):
        # Tenta abrir a câmera padrão (0)
        cap = cv2.VideoCapture(0)
        
        # Configura a resolução (ajuste conforme necessário)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not cap.isOpened():
            print("Erro: Não foi possível abrir a câmera")
            # Cria um vídeo de teste como fallback
            return self._create_test_video()
        return cap
    
    def _create_test_video(self):
        print("Usando vídeo simulado como fallback")
        class TestVideo:
            def read(self):
                # Cria um frame preto com texto
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Vision Shield - Camera Simulation", 
                          (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 
                          0.8, (0, 255, 255), 2)
                return True, frame
        return TestVideo()
    
    def generate_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
                
            # Simula detecções (remova quando implementar detecção real)
            if random.random() > 0.95:
                x, y = random.randint(50, frame.shape[1]-50), random.randint(50, frame.shape[0]-50)
                cv2.rectangle(frame, (x, y), (x+100, y+100), (0, 255, 0), 2)
                cv2.putText(frame, "OBJETO", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Converte para JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')