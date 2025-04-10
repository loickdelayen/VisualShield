let alertsChart = null;

function renderChart(labels, data, period) {
    const ctx = document.getElementById('alerts-chart').getContext('2d');
    
    // Destrói o gráfico anterior se existir
    if (alertsChart) {
        alertsChart.destroy();
    }
    
    // Configurações do gráfico com o tema vermelho/preto
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(230, 57, 70, 0.8)');
    gradient.addColorStop(1, 'rgba(230, 57, 70, 0.2)');
    
    alertsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Número de Alertas',
                data: data,
                backgroundColor: gradient,
                borderColor: 'rgba(230, 57, 70, 1)',
                borderWidth: 1,
                borderRadius: 4,
                hoverBackgroundColor: 'rgba(230, 57, 70, 0.9)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 26, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#e63946',
                    borderWidth: 1
                }
            }
        }
    });
}

function updateChart(period) {
    fetch(`/get_chart_data/${period}`)
        .then(response => {
            if (!response.ok) throw new Error("Erro ao carregar dados");
            return response.json();
        })
        .then(data => {
            if (data.labels && data.data) {
                renderChart(data.labels, data.data, period);
            } else {
                console.error("Dados do gráfico inválidos:", data);
            }
        })
        .catch(error => {
            console.error("Erro ao carregar dados do gráfico:", error);
            // Mostra dados de exemplo em caso de erro
            renderChart(
                ['Exemplo 1', 'Exemplo 2', 'Exemplo 3'], 
                [12, 19, 8], 
                period
            );
        });
}

// Inicializa o gráfico quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Verifica se o elemento do gráfico existe
    const chartCanvas = document.getElementById('alerts-chart');
    if (chartCanvas) {
        // Carrega o gráfico semanal por padrão
        updateChart('weekly');
    } else {
        console.error("Elemento do gráfico não encontrado");
    }
});