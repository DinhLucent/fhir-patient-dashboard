let allPatients = [];
let currentPatient = null;
let chart = null;

async function loadInitialData() {
    try {
        const response = await fetch('/api/patients');
        allPatients = await response.json();

        // Auto-select first patient if none selected
        if (allPatients.length > 0 && !currentPatient) {
            selectPatient(allPatients[0].id);
        }
    } catch (err) {
        console.error("Failed to load clinical data:", err);
    }
}

function selectPatient(id) {
    currentPatient = allPatients.find(p => p.id === id);
    if (!currentPatient) return;

    // UI Update: Active Card
    document.querySelectorAll('.patient-card').forEach(c => {
        c.classList.remove('active');
        if (c.dataset.id === id || c.getAttribute('onclick')?.includes(id)) {
            c.classList.add('active');
        }
    });

    updateChart();
    updateTable();
}

function updateChart() {
    if (!currentPatient) return;

    const metric = document.getElementById('metric-select').value;
    const data = currentPatient.observations.filter(o => o.display === metric);

    const ctx = document.getElementById('vitalsChart').getContext('2d');

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(o => new Date(o.time).toLocaleTimeString()),
            datasets: [{
                label: `${metric} (${data[0]?.unit || ''})`,
                data: data.map(o => o.value),
                borderColor: '#4cc9f0',
                backgroundColor: 'rgba(76, 201, 240, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 6,
                pointBackgroundColor: '#4cc9f0'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: 'rgba(255, 255, 255, 0.8)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: 'rgba(255, 255, 255, 0.8)' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: { family: 'Outfit' },
                    bodyFont: { family: 'Outfit' }
                }
            }
        }
    });
}

function updateTable() {
    if (!currentPatient) return;

    const tbody = document.getElementById('obs-body');
    tbody.innerHTML = '';

    currentPatient.observations.forEach(o => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${o.display}</td>
            <td style="font-weight:600">${o.value}</td>
            <td>${o.unit}</td>
            <td style="opacity:0.7">${new Date(o.time).toLocaleString()}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Initial Load
window.onload = () => {
    loadInitialData();
};
