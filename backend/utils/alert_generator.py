import random
from datetime import datetime, timedelta

class AlertGenerator:
    def __init__(self):
        self.alert_types = ["Movimento", "Objeto", "Pessoa", "Veículo", "Face"]
        self.alerts = []
        self._generate_initial_alerts(50)
        
    def _generate_initial_alerts(self, count):
        now = datetime.now()
        for i in range(count):
            alert_time = now - timedelta(minutes=random.randint(0, 60*24*7))
            self.alerts.append({
                "id": i+1,
                "time": alert_time.strftime("%Y-%m-%d %H:%M:%S"),
                "type": random.choice(self.alert_types),
                "confidence": round(random.uniform(0.5, 0.99), 2),
                "camera": f"Camera {random.randint(1, 3)}",
                "status": random.choice(["Novo", "Revisado", "Falso positivo"])
            })
        self.alerts.sort(key=lambda x: x['time'], reverse=True)
    
    def generate_random_alert(self):
        """Gera um novo alerta aleatório"""
        new_alert = {
            "id": len(self.alerts) + 1,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": random.choice(self.alert_types),
            "confidence": round(random.uniform(0.7, 0.99), 2),
            "camera": f"Camera {random.randint(1, 3)}",
            "status": "Novo"
        }
        self.alerts.insert(0, new_alert)
        return new_alert
    
    def get_recent_alerts(self, count):
        return self.alerts[:count]