const map = L.map('map').setView([20.289594, 85.835212], 12);
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '©OpenStreetMap, ©CartoDB'
}).addTo(map);

let markers = [];

async function updateDashboard() {
    let hardwareData = null;
    let isHardwareConnected = false;

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        const response = await fetch('https://iotwm-api.teamitj.tech/api/bins', {
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        hardwareData = await response.json();
        isHardwareConnected = true;
    } catch (error) {
        console.log('Hardware connection failed:', error.message);
        hardwareData = {
            bin1: {
                fillLevel: Math.floor(Math.random() * 100),
                timestamp: Date.now()
            },
            bin2: {
                fillLevel: Math.floor(Math.random() * 100),
                timestamp: Date.now()
            }
        };
    }

    const bins = [
        {
            id: 1,
            location: {
                lat: 20.289594,
                lng: 85.835212
            },
            fillLevel: hardwareData.bin1.fillLevel,
            status: hardwareData.bin1.fillLevel >= 90 ? 'full' :
                hardwareData.bin1.fillLevel >= 75 ? 'almost-full' : 'normal',
            lastUpdated: new Date(hardwareData.bin1.timestamp).toLocaleTimeString(),
            isHardware: true,
            isConnected: isHardwareConnected
        },
        {
            id: 2,
            location: {
                lat: 20.289694,
                lng: 85.835312
            },
            fillLevel: hardwareData.bin2.fillLevel,
            status: hardwareData.bin2.fillLevel >= 90 ? 'full' :
                hardwareData.bin2.fillLevel >= 75 ? 'almost-full' : 'normal',
            lastUpdated: new Date(hardwareData.bin2.timestamp).toLocaleTimeString(),
            isHardware: true,
            isConnected: isHardwareConnected
        }
    ];

    for (let i = 3; i <= 20; i++) {
        const fillLevel = Math.floor(Math.random() * 100);
        bins.push({
            id: i,
            location: {
                lat: 20.289594 + (Math.random() - 0.5) * 0.1,
                lng: 85.835212 + (Math.random() - 0.5) * 0.1
            },
            fillLevel,
            status: fillLevel >= 90 ? 'full' :
                fillLevel >= 75 ? 'almost-full' : 'normal',
            lastUpdated: new Date().toLocaleTimeString(),
            isHardware: false,
            isConnected: true
        });
    }

    const binsList = document.getElementById('bins-list');
    binsList.innerHTML = '';
    const fragment = document.createDocumentFragment();

    bins.forEach(bin => {
        const binItem = document.createElement('div');
        binItem.classList.add('bin-item');
        binItem.innerHTML = `
    <div class="bin-info">
        <h4>${bin.isHardware ? `${bin.isConnected ? '📡' : '❌'} Smart` : ''} Bin #${bin.id}</h4>
        <p>Fill Level: ${bin.fillLevel}%</p>
        <p style="font-size: 12px; color: var(--text-secondary);">
            Last Updated: ${bin.lastUpdated}
            ${bin.isHardware ?
                `<br>(${bin.isConnected ? 'Hardware Sensor' : 'Hardware Offline - Using Simulated Data'})` :
                ' (Simulated)'}
        </p>
    </div>
    <div style="text-align: right;">
        <span class="status-badge ${bin.status}">
            ${bin.status.replace('-', ' ').toUpperCase()}
        </span>
        ${bin.fillLevel >= 75 ?
                `<br><button class="dispatch-btn" onclick="dispatchTruck(${bin.id})">
                Dispatch
            </button>` : ''}
    </div>
`;
        fragment.appendChild(binItem);
    });

    binsList.appendChild(fragment);
    document.getElementById('total-bins').textContent = bins.length;
    document.getElementById('full-bins').textContent = bins.filter(bin => bin.status === 'full').length;
    document.getElementById('active-trucks').textContent = Math.floor(Math.random() * 5);
    document.getElementById('total-collected').textContent = `${Math.floor(Math.random() * 1000)} kg`;

    markers.forEach(marker => map.removeLayer(marker));
    markers = bins.map(bin => {
        const markerColor = bin.status === 'full' ? 'red' :
            bin.status === 'almost-full' ? 'orange' : 'blue';
        return L.circleMarker([bin.location.lat, bin.location.lng], {
            radius: bin.isHardware ? 10 : 8,
            fillColor: markerColor,
            color: bin.isHardware ? (bin.isConnected ? '#fff' : '#ff4444') : '#ccc',
            weight: bin.isHardware ? 3 : 2,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(`
    <div style="color: black;">
        <strong>${bin.isHardware ? `${bin.isConnected ? '📡' : '❌'} Smart` : ''} Bin #${bin.id}</strong><br>
        Fill Level: ${bin.fillLevel}%<br>
        Status: ${bin.status.replace('-', ' ').toUpperCase()}<br>
        Last Updated: ${bin.lastUpdated}<br>
        ${bin.isHardware ?
                `<strong>(${bin.isConnected ? 'Hardware Sensor' : 'Hardware Offline - Using Simulated Data'})</strong>` :
                '(Simulated)'}
    </div>
`).addTo(map);
    });

    showConnectionStatus(isHardwareConnected);
}

function initCharts() {
    new Chart(document.getElementById('wasteChart'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Total Waste (tons)',
                data: [120, 150, 180, 165, 190, 210],
                borderColor: '#3b82f6',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                }
            },
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#e2e8f0' } },
                x: { grid: { color: '#334155' }, ticks: { color: '#e2e8f0' } }
            }
        }
    });

    new Chart(document.getElementById('fillRateChart'), {
        type: 'bar',
        data: {
            labels: ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%'],
            datasets: [{
                label: 'Number of Bins',
                data: [5, 8, 12, 7, 3],
                backgroundColor: '#60a5fa'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                }
            },
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#e2e8f0' } },
                x: { grid: { color: '#334155' }, ticks: { color: '#e2e8f0' } }
            }
        }
    });

    new Chart(document.getElementById('truckChart'), {
        type: 'line',
        data: {
            labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Active Trucks',
                data: Array.from({ length: 24 }, () => Math.floor(Math.random() * 5) + 1),
                borderColor: '#22c55e',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                }
            },
            scales: {
                y: {
                    grid: { color: '#334155' },
                    ticks: { color: '#e2e8f0' },
                    min: 0,
                    max: 10
                },
                x: {
                    grid: { color: '#334155' }, ticks: { color: '#e2e8f0' },
                    maxTicksLimit: 12
                }
            }
        }
    });

    new Chart(document.getElementById('wasteTypeChart'), {
        type: 'doughnut',
        data: {
            labels: ['Organic', 'Recyclable', 'General', 'Hazardous'],
            datasets: [{
                data: [40, 30, 20, 10],
                backgroundColor: ['#22c55e', '#3b82f6', '#eab308', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#e2e8f0' }
                }
            }
        }
    });
}

function dispatchTruck(binId) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--accent);
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    `;
    toast.textContent = `Dispatching truck to Bin #${binId}`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

updateDashboard();
initCharts();

setInterval(() => {
    updateDashboard();
    initCharts();
}, 5000);

async function loadAIAnalytics() {
    try {
        const response = await fetch('https://hackathon.teamitj.tech/iot-waste-management/data/all_analytics.json');
        const analytics = await response.json();

        updateWasteDistribution(analytics['waste-distribution'].data);
        updateLocationAnalytics(analytics['location-analytics'].data);
        updateCollectionPredictions(analytics['collection-schedule'].data);
        updateEfficiencyMetrics(analytics['efficiency-metrics'].data);

        const currentStatus = analytics['current-status'].data;
        document.getElementById('total-bins').textContent = currentStatus.total_bins;
        document.getElementById('full-bins').textContent = currentStatus.critical_bins;
    } catch (error) {
        console.error('Error loading AI analytics:', error);
    }
}

function updateWasteDistribution(data) {
    const ctx = document.getElementById('aiWasteChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data).map(item => item.percentage),
                backgroundColor: [
                    '#22c55e',
                    '#3b82f6',
                    '#eab308',
                    '#ef4444',
                    '#8b5cf6'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#e2e8f0' }
                }
            }
        }
    });
}

function updateLocationAnalytics(data) {
    const locations = Object.keys(data);
    const fillLevels = locations.map(loc => data[loc].fill_level);

    const ctx = document.getElementById('locationAnalyticsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: locations,
            datasets: [{
                label: 'Average Fill Level',
                data: fillLevels,
                backgroundColor: '#3b82f6'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                }
            },
            scales: {
                y: {
                    grid: { color: '#334155' },
                    ticks: { color: '#e2e8f0' }
                },
                x: {
                    grid: { color: '#334155' },
                    ticks: { color: '#e2e8f0' }
                }
            }
        }
    });
}

function updateCollectionPredictions(predictions) {
    const container = document.getElementById('collection-predictions');
    container.innerHTML = '';

    Object.entries(predictions)
        .sort((a, b) => a[1].hours_until_full - b[1].hours_until_full)
        .forEach(([binId, data]) => {
            const div = document.createElement('div');
            div.className = 'prediction-item';
            div.innerHTML = `
                <div class="bin-title">${binId}</div>
                <div class="bin-location">${data.location}</div>
                <div class="fill-info">
                    <div class="fill-level">
                        Fill Level:
                        <div class="fill-bar">
                            <div class="fill-bar-progress" style="width: ${data.current_fill}%"></div>
                        </div>
                        ${data.current_fill}%
                    </div>
                </div>
                <div class="time-info">
                    <div class="hours-until">
                        ${data.hours_until_full.toFixed(1)} hours until full
                    </div>
                    <div class="priority priority-${data.priority.toLowerCase()}">
                        ${data.priority}
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
}

function updateEfficiencyMetrics(metrics) {
    const container = document.getElementById('efficiency-metrics');
    container.innerHTML = '';

    const { collection_efficiency, overflow_incidents } = metrics;

    const metricsData = [
        {
            icon: '📊',
            title: 'Collections',
            value: collection_efficiency.total_collections,
            subtitle: `Avg ${collection_efficiency.avg_collections_per_bin.toFixed(2)}/bin`,
            warning: false
        },
        {
            icon: '⚠️',
            title: 'Overflows',
            value: overflow_incidents.total_overflows,
            subtitle: `${overflow_incidents.bins_with_overflow} bins affected`,
            warning: true
        }
    ];

    metricsData.forEach(item => {
        const div = document.createElement('div');
        div.className = `metric-item ${item.warning ? 'warning' : ''}`;
        div.innerHTML = `
            <div class="metric-header">
                <span class="metric-icon">${item.icon}</span>
                <span class="metric-title">${item.title}</span>
            </div>
            <div class="metric-value">${item.value}</div>
            <div class="metric-subtitle">${item.subtitle}</div>
        `;
        container.appendChild(div);
    });
}

setInterval(() => {
    updateDashboard();
    loadAIAnalytics();
}, 5000);
loadAIAnalytics();