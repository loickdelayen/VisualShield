document.addEventListener('DOMContentLoaded', function() {
    // Carrega alertas inicialmente
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
        .then(response => response.json())
        .then(alerts => {
            const tbody = document.getElementById('alerts-body');
            tbody.innerHTML = '';
            
            alerts.forEach(alert => {
                const row = document.createElement('tr');
                
                row.innerHTML = `
                    <td>${alert.time}</td>
                    <td>${alert.type}</td>
                    <td>${Math.round(alert.confidence * 100)}%</td>
                    <td><span class="alert-status ${getStatusClass(alert.status)}">${alert.status}</span></td>
                `;
                
                tbody.appendChild(row);
            });
        });
}

function getStatusClass(status) {
    switch(status.toLowerCase()) {
        case 'novo': return 'status-new';
        case 'revisado': return 'status-reviewed';
        default: return 'status-false';
    }
}