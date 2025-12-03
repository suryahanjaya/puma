// ===== CONFIGURATION =====
const CONFIG = {
    API_URL: 'http://localhost:5000/api',
    REFRESH_INTERVAL: 1500, // 1.5 seconds
    DEFAULT_HISTORY_LIMIT: 150,
    DB_PATH: 'data/uav_telemetry.db'
};

// ===== GLOBAL STATE =====
let anomalyChart = null;
let metricsChart = null;
let historyLimit = CONFIG.DEFAULT_HISTORY_LIMIT;
let isRunning = true;

// ===== INITIALIZE CHARTS =====
function initCharts() {
    // Anomaly Score Chart
    const anomalyCtx = document.getElementById('anomaly-chart').getContext('2d');
    anomalyChart = new Chart(anomalyCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Anomaly Score',
                data: [],
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 6
            }, {
                label: 'Anomaly Detected',
                data: [],
                borderColor: '#ef4444',
                backgroundColor: '#ef4444',
                borderWidth: 0,
                pointRadius: 6,
                pointStyle: 'cross',
                showLine: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#94a3b8',
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#1a1f3a',
                    titleColor: '#ffffff',
                    bodyColor: '#94a3b8',
                    borderColor: '#2d3548',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: { color: '#2d3548' },
                    ticks: { color: '#64748b', maxTicksLimit: 10 }
                },
                y: {
                    display: true,
                    grid: { color: '#2d3548' },
                    ticks: { color: '#64748b' },
                    title: {
                        display: true,
                        text: 'Score',
                        color: '#94a3b8'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });

    // Flight Metrics Chart
    const metricsCtx = document.getElementById('metrics-chart').getContext('2d');
    metricsChart = new Chart(metricsCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Altitude (m)',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                yAxisID: 'y',
                pointRadius: 0
            }, {
                label: 'Battery (%)',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                yAxisID: 'y1',
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#1a1f3a',
                    titleColor: '#ffffff',
                    bodyColor: '#94a3b8',
                    borderColor: '#2d3548',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: { color: '#2d3548' },
                    ticks: { color: '#64748b', maxTicksLimit: 10 }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    grid: { color: '#2d3548' },
                    ticks: { color: '#3b82f6' },
                    title: {
                        display: true,
                        text: 'Altitude (m)',
                        color: '#3b82f6'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#10b981' },
                    title: {
                        display: true,
                        text: 'Battery (%)',
                        color: '#10b981'
                    }
                }
            }
        }
    });
}

// ===== FETCH DATA FROM BACKEND =====
async function fetchData() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/telemetry?limit=${historyLimit}`);
        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('db-status').textContent = '● Disconnected';
        document.getElementById('db-status').style.color = '#ef4444';
        return null;
    }
}

// ===== UPDATE DASHBOARD =====
async function updateDashboard() {
    const data = await fetchData();
    if (!data || data.length === 0) return;

    // Update connection status
    document.getElementById('db-status').textContent = '● Connected';
    document.getElementById('db-status').style.color = '#10b981';

    // Get latest data point
    const latest = data[0];

    // Update status cards
    updateStatusCards(latest);

    // Update charts
    updateCharts(data);

    // Update table
    updateTable(data.slice(0, 15));

    // Update last update time
    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
}

// ===== UPDATE STATUS CARDS =====
function updateStatusCards(latest) {
    // System Status
    const systemStatusCard = document.getElementById('system-status-card');
    const systemStatus = document.getElementById('system-status');

    if (latest.is_anomaly === 1) {
        systemStatusCard.className = 'status-card anomaly';
        systemStatusCard.querySelector('.card-icon').textContent = '🔴';
        systemStatus.textContent = 'ANOMALY';
        systemStatus.style.color = '#ef4444';
    } else {
        systemStatusCard.className = 'status-card normal';
        systemStatusCard.querySelector('.card-icon').textContent = '🟢';
        systemStatus.textContent = 'NORMAL';
        systemStatus.style.color = '#10b981';
    }

    // Timestamp
    const timestamp = latest.dt.split(' ')[1];
    document.getElementById('timestamp-value').textContent = timestamp;

    // Altitude
    document.getElementById('altitude-value').textContent = `${latest.altitude.toFixed(1)} m`;

    // Battery
    const batteryValue = latest.battery_level.toFixed(1);
    document.getElementById('battery-value').textContent = `${batteryValue} %`;

    const batteryLabel = document.getElementById('battery-label');
    if (latest.battery_level > 80) {
        batteryLabel.textContent = 'Fully Charged';
        batteryLabel.style.color = '#10b981';
    } else if (latest.battery_level > 30) {
        batteryLabel.textContent = 'Good';
        batteryLabel.style.color = '#3b82f6';
    } else if (latest.battery_level > 15) {
        batteryLabel.textContent = 'Low Battery';
        batteryLabel.style.color = '#f59e0b';
    } else {
        batteryLabel.textContent = 'Critical';
        batteryLabel.style.color = '#ef4444';
    }

    // Flight Mode
    document.getElementById('mode-value').textContent = latest.mode;
}

// ===== UPDATE CHARTS =====
function updateCharts(data) {
    // Reverse data for chronological order
    const reversedData = [...data].reverse();

    // Extract labels and values
    const labels = reversedData.map(d => d.dt.split(' ')[1]);
    const anomalyScores = reversedData.map(d => d.anomaly_score);
    const altitudes = reversedData.map(d => d.altitude);
    const batteries = reversedData.map(d => d.battery_level);

    // Find anomaly points
    const anomalyPoints = reversedData.map((d, idx) =>
        d.is_anomaly === 1 ? d.anomaly_score : null
    );

    // Update Anomaly Chart
    anomalyChart.data.labels = labels;
    anomalyChart.data.datasets[0].data = anomalyScores;
    anomalyChart.data.datasets[1].data = anomalyPoints;
    anomalyChart.update('none'); // No animation for smoother updates

    // Update Metrics Chart
    metricsChart.data.labels = labels;
    metricsChart.data.datasets[0].data = altitudes;
    metricsChart.data.datasets[1].data = batteries;
    metricsChart.update('none');
}

// ===== UPDATE TABLE =====
function updateTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    let anomalyCount = 0;

    data.forEach(row => {
        if (row.is_anomaly === 1) anomalyCount++;

        const tr = document.createElement('tr');

        // Status badge
        const statusBadge = row.is_anomaly === 1
            ? '<span class="badge badge-anomaly">⚠️ Anomaly</span>'
            : '<span class="badge badge-normal">✓ Normal</span>';

        // System status badge
        let systemBadge = '';
        if (row.system_status === 'Error') {
            systemBadge = '<span class="badge badge-anomaly">Error</span>';
        } else if (row.system_status === 'Warning') {
            systemBadge = '<span class="badge badge-warning">Warning</span>';
        } else {
            systemBadge = '<span class="badge badge-normal">Normal</span>';
        }

        tr.innerHTML = `
            <td>${row.dt}</td>
            <td>${statusBadge}</td>
            <td>${row.anomaly_score.toFixed(3)}</td>
            <td>${row.altitude.toFixed(1)}</td>
            <td>${row.battery_level.toFixed(1)}</td>
            <td>${row.mode}</td>
            <td>${systemBadge}</td>
            <td>${row.event || '-'}</td>
        `;

        tbody.appendChild(tr);
    });

    // Update stats
    document.getElementById('anomaly-count').textContent = `Anomalies: ${anomalyCount}`;
    document.getElementById('total-records').textContent = `Total: ${data.length} records`;
}

// ===== EVENT LISTENERS =====
document.getElementById('history-limit').addEventListener('change', (e) => {
    historyLimit = parseInt(e.target.value);
    updateDashboard();
});

// ===== INITIALIZE DASHBOARD =====
async function init() {
    console.log('🚀 Initializing PUMA Dashboard...');

    // Initialize charts
    initCharts();

    // First update
    await updateDashboard();

    // Start auto-refresh
    setInterval(() => {
        if (isRunning) {
            updateDashboard();
        }
    }, CONFIG.REFRESH_INTERVAL);

    console.log('✅ Dashboard initialized successfully!');
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
