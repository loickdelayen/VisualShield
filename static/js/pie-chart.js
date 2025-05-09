document.addEventListener('DOMContentLoaded', function () {
    renderPieChart();
});

function renderPieChart() {
    const ctx = document.getElementById('pie-chart').getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Capacete', 'Oculos', 'Luva'],
            datasets: [{
                data: [35, 25, 20],
                backgroundColor: [
                    'rgba(230, 57, 70, 0.7)',
                    'rgba(70, 130, 180, 0.7)',
                    'rgba(34, 139, 34, 0.7)'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 40,
                    right: 20,
                    top: 10,
                    bottom: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Distribuição por Tipo de Alerta:',
                    align: 'start', // centraliza o título
                    color: '#333',
                    padding: { bottom: 20 },
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'left',
                    labels: {
                        color: '#333',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        boxWidth: 20,
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ${value}%`;
                        }
                    }
                }
            }
        }
    });
}
