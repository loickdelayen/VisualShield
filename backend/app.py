from flask import Flask, render_template, jsonify, Response, send_from_directory
from camera_processor import CameraProcessor
from collections import Counter
import threading
import time
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Inicializa o processador de câmera com YOLO
camera = CameraProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_status')
def camera_status():
    return jsonify({
        'status': 'active' if hasattr(camera, 'cap') and camera.cap.read()[0] else 'inactive'
    })

@app.route('/get_alerts')
def get_alerts():
    # Retorna os 10 alertas reais mais recentes da câmera
    return jsonify(camera.detections_log[::-1][:10])

@app.route('/get_chart_data/<period>')
def get_chart_data(period):
    # Calcula contagem de cada tipo de detecção
    types = [d["type"] for d in camera.detections_log]
    counts = Counter(types)

    return jsonify({
        "labels": list(counts.keys()),
        "data": list(counts.values())
    })

@app.route('/saved_frames/<path:filename>')
def get_saved_frame(filename):
    return send_from_directory(os.path.abspath("saved_frames"), filename, as_attachment=True)

def background_tasks():
    """Exemplo de tarefa de segundo plano (opcional)"""
    while True:
        time.sleep(10)
        print("Executando tarefa em segundo plano...")

if __name__ == '__main__':
    bg_thread = threading.Thread(target=background_tasks)
    bg_thread.daemon = True
    bg_thread.start()

    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
