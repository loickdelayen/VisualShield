from flask import Flask, render_template, jsonify, Response
from camera_processor import CameraProcessor
from utils.alert_generator import AlertGenerator
from utils.data_processor import DataProcessor
import threading
import time
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')


# Configuração alternativa caso o acima não funcione
# app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
#            static_folder=os.path.join(os.path.dirname(__file__), '../static'))

# Inicializa os componentes
camera = CameraProcessor()
alert_gen = AlertGenerator()
data_processor = DataProcessor()

print("Current directory:", os.getcwd())
print("Template path:", os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates')))
print("Static path:", os.path.abspath(os.path.join(os.path.dirname(__file__), '../static')))

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
        'status': 'active' if camera.cap.isOpened() else 'inactive',
        'last_update': time.time()
    })

@app.route('/get_alerts')
def get_alerts():
    alerts = alert_gen.get_recent_alerts(10)  # Últimos 10 alertas
    return jsonify(alerts)

@app.route('/get_chart_data/<period>')
def get_chart_data(period):
    data = data_processor.get_data(period)  # weekly, monthly, yearly
    return jsonify(data)

def background_tasks():
    """Simula detecções em segundo plano"""
    while True:
        time.sleep(5)
        alert_gen.generate_random_alert()
        data_processor.update_data()

if __name__ == '__main__':
    # Inicia thread para tarefas em segundo plano
    bg_thread = threading.Thread(target=background_tasks)
    bg_thread.daemon = True
    bg_thread.start()
    
    app.run(host='0.0.0.0', port=5000, threaded=True)