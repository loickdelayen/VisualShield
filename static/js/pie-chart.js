let pieChart;

document.addEventListener('DOMContentLoaded', function () {
    renderPieChart('realtime');  // Pode usar um parâmetro fixo 'realtime' para seu backend
    setInterval(() => renderPieChart('realtime'), 5000);
});

function renderPieChart(period) {
    fetch(`/get_chart_data/${period}`)
        .then(response => response.json())
        .then(chartData => {
            const ctx = document.getElementById('pie-chart').getContext('2d');

            const data = {
                labels: chartData.labels,
                datasets: [{
                    data: chartData.data,
                    backgroundColor: generateColors(chartData.labels.length),
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            };

            const options = {
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
                        align: 'start',
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
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            };

            if (pieChart) {
                pieChart.data = data;
                pieChart.options = options;
                pieChart.update();
            } else {
                pieChart = new Chart(ctx, {
                    type: 'pie',
                    data: data,
                    options: options
                });
            }
        });
}

function generateColors(count) {
    // Gera cores básicas ou aleatórias para o gráfico
    const baseColors = [
        'rgba(230, 57, 70, 0.7)',
        'rgba(70, 130, 180, 0.7)',
        'rgba(34, 139, 34, 0.7)',
        'rgba(255, 165, 0, 0.7)',
        'rgba(128, 0, 128, 0.7)',
        'rgba(255, 192, 203, 0.7)'
    ];
    let colors = [];
    for(let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    return colors;
}
