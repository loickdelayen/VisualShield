# Código base sugerido para o dashboard

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import random
import pandas as pd

class VisionDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Computer Vision Dashboard")
        self.root.geometry("1200x800")
        
        # Dados fictícios para alertas
        self.alert_types = ["Movimento", "Objeto", "Pessoa", "Veículo", "Face"]
        self.alert_data = self.generate_fake_alerts(50)
        
        # Configuração da câmera (simulada ou real)
        self.cap = cv2.VideoCapture(0)  # Ou usar vídeo de teste
        self.setup_ui()
        
    def generate_fake_alerts(self, count):
        """Gera dados fictícios para o histórico de alertas"""
        alerts = []
        now = datetime.datetime.now()
        for i in range(count):
            alert_time = now - datetime.timedelta(minutes=random.randint(0, 60*24*7))
            alerts.append({
                "id": i+1,
                "time": alert_time.strftime("%Y-%m-%d %H:%M:%S"),
                "type": random.choice(self.alert_types),
                "confidence": round(random.uniform(0.5, 0.99), 2),
                "camera": f"Camera {random.randint(1, 3)}",
                "status": random.choice(["Novo", "Revisado", "Falso positivo"])
            })
        return sorted(alerts, key=lambda x: x['time'], reverse=True)
    
    def generate_chart_data(self):
        """Gera dados fictícios para os gráficos"""
        now = datetime.datetime.now()
        
        # Dados semanais
        weekly = {
            "days": [(now - datetime.timedelta(days=i)).strftime("%a") for i in range(7)][::-1],
            "counts": [random.randint(5, 30) for _ in range(7)]
        }
        
        # Dados mensais
        monthly = {
            "weeks": [f"Semana {i}" for i in range(1, 5)],
            "counts": [random.randint(30, 120) for _ in range(4)]
        }
        
        # Dados anuais
        yearly = {
            "months": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"],
            "counts": [random.randint(150, 500) for _ in range(12)]
        }
        
        return weekly, monthly, yearly
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Seção superior - Câmera e alertas recentes
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Visualização da câmera
        self.camera_frame = ttk.LabelFrame(top_frame, text="Live Camera Feed")
        self.camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack()
        
        # Alertas recentes
        alerts_frame = ttk.LabelFrame(top_frame, text="Recent Alerts")
        alerts_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=("time", "type", "confidence", "status"), show="headings")
        self.alerts_tree.heading("time", text="Time")
        self.alerts_tree.heading("type", text="Type")
        self.alerts_tree.heading("confidence", text="Confidence")
        self.alerts_tree.heading("status", text="Status")
        
        for alert in self.alert_data[:10]:  # Mostrar apenas 10 alertas recentes
            self.alerts_tree.insert("", "end", values=(
                alert["time"], 
                alert["type"], 
                alert["confidence"], 
                alert["status"]
            ))
        
        scrollbar = ttk.Scrollbar(alerts_frame, orient="vertical", command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=scrollbar.set)
        self.alerts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Seção inferior - Gráficos
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles do gráfico
        controls_frame = ttk.Frame(bottom_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(controls_frame, text="Time Period:").pack(side=tk.LEFT)
        
        self.chart_var = tk.StringVar(value="weekly")
        ttk.Radiobutton(controls_frame, text="Weekly", variable=self.chart_var, value="weekly", 
                        command=self.update_chart).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Monthly", variable=self.chart_var, value="monthly", 
                        command=self.update_chart).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Yearly", variable=self.chart_var, value="yearly", 
                        command=self.update_chart).pack(side=tk.LEFT, padx=5)
        
        # Gráfico
        self.chart_frame = ttk.LabelFrame(bottom_frame, text="Alert Statistics")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.figure, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Atualizar gráfico inicial
        self.update_chart()
        
        # Atualizar feed da câmera
        self.update_camera()
    
    def update_chart(self):
        """Atualiza o gráfico com base na seleção do usuário"""
        weekly, monthly, yearly = self.generate_chart_data()
        period = self.chart_var.get()
        
        self.ax.clear()
        
        if period == "weekly":
            self.ax.bar(weekly["days"], weekly["counts"], color='skyblue')
            self.ax.set_title("Alertas por Dia (Semana Atual)")
        elif period == "monthly":
            self.ax.bar(monthly["weeks"], monthly["counts"], color='lightgreen')
            self.ax.set_title("Alertas por Semana (Mês Atual)")
        else:  # yearly
            self.ax.bar(yearly["months"], yearly["counts"], color='salmon')
            self.ax.set_title("Alertas por Mês (Ano Atual)")
        
        self.ax.set_ylabel("Número de Alertas")
        self.canvas.draw()
    
    def update_camera(self):
        """Atualiza o feed da câmera"""
        ret, frame = self.cap.read()
        if ret:
            # Simular detecção (para demonstração)
            if random.random() > 0.9:  # 10% de chance de "detectar" algo
                x, y = random.randint(50, frame.shape[1]-50), random.randint(50, frame.shape[0]-50)
                cv2.rectangle(frame, (x, y), (x+50, y+50), (0, 255, 0), 2)
                cv2.putText(frame, "Objeto", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        
        self.root.after(30, self.update_camera)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisionDashboard(root)
    app.run()