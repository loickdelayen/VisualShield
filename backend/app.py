from flask import Flask, render_template, jsonify, Response, send_from_directory
from camera_processor import CameraProcessor
from collections import Counter
import threading
import time
import os
from utils import database

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize MySQL database connection and create table on app startup
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '12345678'
MYSQL_DATABASE = 'visionShield'  # Use exact case as requested

# Connect to MySQL without specifying database to create it if not exists
conn = database.create_connection(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=None
)

# Create database if it doesn't exist
database.create_database(conn, MYSQL_DATABASE)
conn.close()

# Connect to the newly created or existing database
conn = database.create_connection(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

# Create required tables
database.create_images_table(conn)
database.create_classes_table(conn)
database.create_log_table(conn)

# Create event scheduler for deleting old images
database.create_delete_old_images_event(conn)

# Inicializa o processador de câmera com YOLO
camera = CameraProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Retorna streaming de vídeo multipart (frames da câmera)
    return Response(camera.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_status')
def camera_status():
    # Verifica se a câmera está ativa
    return jsonify({
        'status': 'active' if hasattr(camera, 'cap') and camera.cap.read()[0] else 'inactive'
    })

@app.route('/get_alerts')
def get_alerts():
    # Retorna os 10 alertas mais recentes (invertido para mostrar os últimos)
    # Now fetches from database instead of in-memory log
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM saved_frames ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        alerts = []
        for row in rows:
            alerts.append({
                "time": f"{row['date']} {row['time']}",
                "type": row['detections'].split(' - ')[0] if row['detections'] else "Unknown",
                "image": row['filename'],
                "status": row['detections'].split(' - ')[1] if row['detections'] else "Unknown"
            })
        return jsonify(alerts)
    except Exception as e:
        print(f"Error fetching alerts from database: {e}")
        return jsonify([])

@app.route('/get_chart_data/<period>')
def get_chart_data(period):
    # Recebe o período (pode usar para filtrar no futuro)
    # Retorna contagem de cada tipo de detecção para o gráfico
    types = [d["type"] for d in camera.detections_log]
    counts = Counter(types)

    return jsonify({
        "labels": list(counts.keys()),
        "data": list(counts.values())
    })

@app.route('/saved_frames/<path:filename>')
def get_saved_frame(filename):
    # Serve as imagens salvas via URL
    return send_from_directory(os.path.abspath("saved_frames"), filename, as_attachment=True)

def background_tasks():
    # Exemplo de tarefa em segundo plano (opcional)
    while True:
        time.sleep(10)
        print("Executando tarefa em segundo plano...")

if __name__ == '__main__':
    bg_thread = threading.Thread(target=background_tasks)
    bg_thread.daemon = True
    bg_thread.start()

    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
