document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById('trafficTrendChart');
    if (!chartCanvas) return;

    let dates = [];
    let conversations = [];
    let messages = [];

    try {
        dates = JSON.parse(chartCanvas.dataset.labels || '[]');
        conversations = JSON.parse(chartCanvas.dataset.conversations || '[]');
        messages = JSON.parse(chartCanvas.dataset.messages || '[]');
    } catch (e) {
        console.error("Failed to parse chart metrics from data attributes", e);
    }

    const ctx = chartCanvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Conversations Started',
                    data: conversations,
                    borderColor: '#198754', 
                    backgroundColor: 'rgba(25, 135, 84, 0.02)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'Messages Exchanged',
                    data: messages,
                    borderColor: '#0d6efd', 
                    backgroundColor: 'rgba(13, 110, 253, 0.02)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { 
                        boxWidth: 12, 
                        usePointStyle: true, 
                        font: { family: 'Plus Jakarta Sans, sans-serif' } 
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.04)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
});
