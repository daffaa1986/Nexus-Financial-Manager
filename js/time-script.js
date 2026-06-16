document.addEventListener('DOMContentLoaded', function() {
    const trendElement = document.getElementById('timeTrendChart');
    if (!trendElement) return;
    const ctx = trendElement.getContext('2d');

    // Gradient untuk area chart
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
            datasets: [{
                label: 'Response Time (ms)',
                data: [450, 520, 380, 1100, 420, 480, 510],
                borderColor: '#3b82f6',
                borderWidth: 3,
                fill: true,
                backgroundColor: gradient,
                tension: 0.4, // Membuat garis melengkung (smooth)
                pointRadius: 4,
                pointBackgroundColor: '#3b82f6'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f0f0f0' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
});