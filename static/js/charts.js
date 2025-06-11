let barChart = null;

document.addEventListener('DOMContentLoaded', function() {
    // Atualiza o gráfico inicialmente
    updateChart('weekly');

    // Atualiza o gráfico a cada 5 segundos
    setInterval(() => {
        // Pega o período selecionado no botão ativo
        const activeBtn = document.querySelector('.period-btn.active');
        const period = activeBtn ? activeBtn.dataset.period : 'weekly';

        updateChart(period);
    }, 5000);

    // Controle dos botões para troca de período
    const buttons = document.querySelectorAll('.period-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateChart(btn.dataset.period);
        });
    });
});

function updateChart(period) {
    fetch(`/get_chart_data/${period}`)
        .then(response => {
            if (!response.ok) throw new Error("Erro ao carregar dados");
            return response.json();
        })
        .then(data => {
            renderBarChart(data.labels, data.data, period);
        })
        .catch(error => {
            console.error("Erro ao carregar dados do gráfico:", error);
        });
}

function renderBarChart(labels, data, period) {
    const ctx = document.getElementById('bar-chart').getContext('2d');

    if (barChart) {
        barChart.destroy();
    }

    // Gradiente para as barras
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(230, 57, 70, 0.8)');
    gradient.addColorStop(1, 'rgba(230, 57, 70, 0.2)');

    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Número de Alertas',
                data: data,
                backgroundColor: gradient,
                borderColor: 'rgba(230, 57, 70, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        color: '#333'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#333'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#333',
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}
