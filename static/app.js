let map;
let heatmapLayer;
let markerGroup;
let clusterGroup;
let allData = [];
let filteredData = [];
let currentView = 'heatmap';
let isLoading = false;

// Initialize map
function initMap() {
    map = L.map('map').setView([38.787919, -77.226064], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    markerGroup = L.featureGroup();
    clusterGroup = L.markerClusterGroup();
    
    loadWiFiScans();
}

// Fetch WiFi scan data from backend API
function loadWiFiScans() {
    if (isLoading) return;
    isLoading = true;
    
    const minSignal = document.getElementById('signalFilter').value;
    const ssidFilter = document.getElementById('ssidFilter').value;
    
    fetch(`/api/wifi-scans?min_signal=${minSignal}&ssid=${encodeURIComponent(ssidFilter)}`)
        .then(response => response.json())
        .then(data => {
            allData = data;
            applyFilters();
            updateStats();
            renderView();
            console.log(`Loaded ${data.length} WiFi scans`);
            isLoading = false;
        })
        .catch(error => {
            console.error('Error loading WiFi scans:', error);
            isLoading = false;
        });
}

// Apply filters to data
function applyFilters() {
    const minSignal = parseInt(document.getElementById('signalFilter').value);
    const ssidFilter = document.getElementById('ssidFilter').value.toLowerCase();
    
    filteredData = allData.filter(scan => {
        const signalMatch = scan.signal_strength >= minSignal;
        const ssidMatch = !ssidFilter || (scan.ssid && scan.ssid.toLowerCase().includes(ssidFilter));
        return signalMatch && ssidMatch;
    });
}

// Render view based on current mode
function renderView() {
    // Clear all layers
    if (heatmapLayer) {
        map.removeLayer(heatmapLayer);
    }
    markerGroup.clearLayers();
    if (map.hasLayer(markerGroup)) map.removeLayer(markerGroup);
    if (map.hasLayer(clusterGroup)) map.removeLayer(clusterGroup);
    clusterGroup.clearLayers();
    
    if (currentView === 'heatmap') {
        renderHeatmap();
    } else if (currentView === 'markers') {
        renderMarkers();
    } else if (currentView === 'clusters') {
        renderClusters();
    }
}

// Render heatmap
function renderHeatmap() {
    if (filteredData.length === 0) return;
    
    const heatmapData = filteredData.map(scan => [
        scan.latitude,
        scan.longitude,
        Math.max(0, Math.min(1, (scan.signal_strength + 100) / 100))
    ]);
    
    heatmapLayer = L.heatLayer(heatmapData, {
        radius: 25,
        blur: 15,
        maxZoom: 17,
        max: 1,
        minOpacity: 0.2,
        gradient: {
            0.0: '#0000FF',
            0.25: '#00FF00',
            0.5: '#FFFF00',
            0.75: '#FF7F00',
            1.0: '#FF0000'
        }
    }).addTo(map);
    
    fitMapToData();
}

// Render markers with color coding
function renderMarkers() {
    if (filteredData.length === 0) return;
    
    filteredData.forEach(scan => {
        let color = 'green';
        if (scan.signal_strength < -80) color = 'red';
        else if (scan.signal_strength < -70) color = 'orange';
        
        const marker = L.circleMarker([scan.latitude, scan.longitude], {
            radius: 6,
            fillColor: color,
            color: '#000',
            weight: 1,
            opacity: 0.8,
            fillOpacity: 0.7
        }).bindPopup(`
            <b>${scan.ssid || 'Hidden'}</b><br>
            Signal: ${scan.signal_strength} dBm<br>
            Channel: ${scan.channel || 'N/A'}
        `);
        markerGroup.addLayer(marker);
    });
    
    map.addLayer(markerGroup);
    fitMapToData();
}

// Render clustered markers
function renderClusters() {
    if (filteredData.length === 0) return;
    
    filteredData.forEach(scan => {
        const marker = L.marker([scan.latitude, scan.longitude])
            .bindPopup(`<b>${scan.ssid || 'Hidden'}</b><br>Signal: ${scan.signal_strength} dBm`);
        clusterGroup.addLayer(marker);
    });
    
    map.addLayer(clusterGroup);
    fitMapToData();
}

// Fit map to data bounds
function fitMapToData() {
    if (filteredData.length === 0) return;
    
    let minLat = filteredData[0].latitude;
    let maxLat = minLat;
    let minLng = filteredData[0].longitude;
    let maxLng = minLng;
    
    for (let i = 1; i < filteredData.length; i++) {
        const scan = filteredData[i];
        if (scan.latitude < minLat) minLat = scan.latitude;
        if (scan.latitude > maxLat) maxLat = scan.latitude;
        if (scan.longitude < minLng) minLng = scan.longitude;
        if (scan.longitude > maxLng) maxLng = scan.longitude;
    }
    
    const bounds = L.latLngBounds([minLat, minLng], [maxLat, maxLng]);
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
}

// Update statistics
function updateStats() {
    if (filteredData.length === 0) {
        document.getElementById('totalNetworks').textContent = '0';
        document.getElementById('avgSignal').textContent = '0';
        document.getElementById('strongestSignal').textContent = '0';
        document.getElementById('topSSID').textContent = '-';
        document.getElementById('dataPoints').textContent = '0';
        return;
    }
    
    const uniqueSSIDs = new Set(filteredData.map(s => s.ssid).filter(Boolean));
    const signals = filteredData.map(s => s.signal_strength);
    const avgSignal = (signals.reduce((a, b) => a + b) / signals.length).toFixed(1);
    const strongestSignal = Math.max(...signals);
    
    // Find top SSID
    const ssidCounts = {};
    filteredData.forEach(scan => {
        const ssid = scan.ssid || 'Hidden';
        ssidCounts[ssid] = (ssidCounts[ssid] || 0) + 1;
    });
    const topSSID = Object.keys(ssidCounts).reduce((a, b) => ssidCounts[a] > ssidCounts[b] ? a : b);
    
    document.getElementById('totalNetworks').textContent = uniqueSSIDs.size;
    document.getElementById('avgSignal').textContent = avgSignal;
    document.getElementById('strongestSignal').textContent = strongestSignal;
    document.getElementById('topSSID').textContent = topSSID || '-';
    document.getElementById('dataPoints').textContent = filteredData.length;
}

// Event listeners
document.getElementById('viewMode').addEventListener('change', (e) => {
    currentView = e.target.value;
    renderView();
});

document.getElementById('signalFilter').addEventListener('change', (e) => {
    document.getElementById('signalLabel').textContent = `${e.target.value} dBm+`;
    applyFilters();
    updateStats();
    renderView();
});

document.getElementById('ssidFilter').addEventListener('input', () => {
    applyFilters();
    updateStats();
    renderView();
});

document.getElementById('refreshBtn').addEventListener('click', loadWiFiScans);

document.getElementById('exportBtn').addEventListener('click', () => {
    const json = JSON.stringify(filteredData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `wardriving_data_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', initMap);
