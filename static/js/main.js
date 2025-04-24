document.addEventListener('DOMContentLoaded', function() {
    // Carrega alertas
    loadAlerts();
    
    // Atualiza alertas a cada 5 segundos
    setInterval(loadAlerts, 5000);
    
    // Configura botões de período
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateChart(this.dataset.period);
        });
    });
});

function loadAlerts() {
    fetch('/get_alerts')
        .then(response => {
            if (!response.ok) throw new Error("Erro ao carregar alertas");
            return response.json();
        })
        .then(alerts => {
            const tbody = document.getElementById('alerts-body');
            tbody.innerHTML = '';
            
            alerts.forEach(alert => {
                const row = document.createElement('tr');
                
                row.innerHTML = `
                    <td>${alert.time}</td>
                    <td>${alert.type}</td>
                    <td>${Math.round(alert.confidence * 100)}%</td>
                    <td><span class="status-badge ${getStatusClass(alert.status)}">${alert.status || 'Novo'}</span></td>
                `;
                
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Erro ao carregar alertas:", error);
        });
}

function getStatusClass(status) {
    if (!status) return 'status-new';
    switch(status.toLowerCase()) {
        case 'novo': return 'status-new';
        case 'revisado': return 'status-reviewed';
        case 'falso positivo': return 'status-false';
        default: return 'status-new';
    }
}