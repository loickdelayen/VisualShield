from datetime import datetime, timedelta
import random

class DataProcessor:
    def __init__(self):
        self.data = {
            "weekly": self._generate_weekly_data(),
            "monthly": self._generate_monthly_data(),
            "yearly": self._generate_yearly_data()
        }
    
    def _generate_weekly_data(self):
        now = datetime.now()
        days = [(now - timedelta(days=i)).strftime("%a") for i in range(7)][::-1]
        return {
            "labels": days,
            "data": [random.randint(5, 30) for _ in range(7)]
        }
    
    def _generate_monthly_data(self):
        weeks = [f"Semana {i}" for i in range(1, 5)]
        return {
            "labels": weeks,
            "data": [random.randint(30, 120) for _ in range(4)]
        }
    
    def _generate_yearly_data(self):
        months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"]
        return {
            "labels": months,
            "data": [random.randint(150, 500) for _ in range(12)]
        }
    
    def get_data(self, period):
        # Garante que o período solicitado existe
        return self.data.get(period, self._generate_empty_data(period))
    
    def _generate_empty_data(self, period):
        # Retorna dados vazios se o período não existir
        return {
            "labels": [],
            "data": []
        }
    
    def update_data(self):
        """Atualiza dados periodicamente com base nos alertas"""
        # Atualiza dados semanais
        self.data["weekly"]["data"] = [max(0, x + random.randint(-3, 3)) 
                                      for x in self.data["weekly"]["data"]]
        
        # Atualiza dados mensais
        self.data["monthly"]["data"] = [max(0, x + random.randint(-10, 10)) 
                                       for x in self.data["monthly"]["data"]]
        
        # Atualiza dados anuais
        self.data["yearly"]["data"] = [max(0, x + random.randint(-20, 20)) 
                                       for x in self.data["yearly"]["data"]]