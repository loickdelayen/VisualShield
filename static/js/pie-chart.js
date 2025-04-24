document.addEventListener('DOMContentLoaded', function() {
    renderPieChart();
});

function renderPieChart() {
    const ctx = document.getElementById('pie-chart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Pessoa', 'Veículo', 'Objeto', 'Face', 'Movimento'],
            datasets: [{
                data: [35, 25, 20, 15, 5],
                backgroundColor: [
                    'rgba(230, 57, 70, 0.7)',
                    'rgba(70, 130, 180, 0.7)',
                    'rgba(34, 139, 34, 0.7)',
                    'rgba(255, 165, 0, 0.7)',
                    'rgba(147, 112, 219, 0.7)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#333',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Distribuição por Tipo de Alerta',
                    color: '#333',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}