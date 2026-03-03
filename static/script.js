// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFileBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadModal = document.getElementById('uploadModal');
const resultsModal = document.getElementById('resultsModal');
const modalClose = document.getElementById('modalClose');
const resultsModalClose = document.getElementById('resultsModalClose');
const uploadWidgetBtn = document.getElementById('uploadWidgetBtn');

// Results Elements
const classificationBadge = document.getElementById('classificationBadge');
const classificationText = document.getElementById('classificationText');
const resultConfidence = document.getElementById('resultConfidence');
const realBar = document.getElementById('realBar');
const deepfakeBar = document.getElementById('deepfakeBar');
const realScore = document.getElementById('realScore');
const deepfakeScore = document.getElementById('deepfakeScore');
const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');
const correctBtn = document.getElementById('correctBtn');
const incorrectBtn = document.getElementById('incorrectBtn');
const feedbackMessage = document.getElementById('feedbackMessage');

// Sidebar
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.sidebar');
const navItems = document.querySelectorAll('.nav-item');

let selectedFile = null;
let chartInstances = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    initCharts();
    loadDashboardData();
    loadCybercrimeReport();
});

// Event Listeners
function setupEventListeners() {
    // Upload Modal
    uploadWidgetBtn.addEventListener('click', () => openUploadModal());
    modalClose.addEventListener('click', () => closeUploadModal());
    resultsModalClose.addEventListener('click', () => closeResultsModal());
    uploadModal.addEventListener('click', (e) => {
        if (e.target === uploadModal) closeUploadModal();
    });
    resultsModal.addEventListener('click', (e) => {
        if (e.target === resultsModal) closeResultsModal();
    });

    // Upload Area
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.backgroundColor = 'rgba(74, 95, 239, 0.15)';
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.backgroundColor = '';
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.backgroundColor = '';
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    // File Input
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Buttons
    removeFileBtn.addEventListener('click', removeFile);
    analyzeBtn.addEventListener('click', analyzeFile);
    analyzeAgainBtn.addEventListener('click', resetUpload);
    correctBtn.addEventListener('click', () => submitFeedback(true));
    incorrectBtn.addEventListener('click', () => submitFeedback(false));

    // Sidebar
    sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('active'));

    // Navigation
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.getAttribute('data-page');
            switchPage(page);
        });
    });
}

// Modal Functions
function openUploadModal() {
    uploadModal.classList.add('active');
}

function closeUploadModal() {
    uploadModal.classList.remove('active');
    resetUpload();
}

function closeResultsModal() {
    resultsModal.classList.remove('active');
}

// File Selection
function handleFileSelect(file) {
    const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/flac', 'audio/ogg', 'audio/x-wav'];
    if (!allowedTypes.some(type => file.type.includes(type)) && !file.name.match(/\.(wav|mp3|flac|ogg)$/i)) {
        alert('Please select a valid audio file (WAV, MP3, FLAC, or OGG)');
        return;
    }

    if (file.size > 50 * 1024 * 1024) {
        alert('File size must be less than 50MB');
        return;
    }

    selectedFile = file;
    displayFileInfo(file);
}

function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
}

function removeFile() {
    selectedFile = null;
    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    fileInput.value = '';
}

function resetUpload() {
    removeFile();
    closeResultsModal();
}

// Analysis
async function analyzeFile() {
    if (!selectedFile) {
        alert('Please select a file');
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span>Analyzing...</span>';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const result = await response.json();
        displayResults(result);
        closeUploadModal();
        resultsModal.classList.add('active');

    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing file: ' + error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-magnifying-glass"></i> Analyze Audio';
    }
}

// Display Results
function displayResults(result) {
    const isReal = result.classification === 'Real';
    const confidence = result.confidence || 0;

    // Classification
    classificationBadge.textContent = isReal ? '✓' : '✕';
    classificationBadge.style.background = isReal 
        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
        : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';

    classificationText.innerHTML = `
        <h2>${result.classification}</h2>
        <p>${isReal ? 'This is a genuine voice' : 'This appears to be a deepfake'}</p>
    `;

    resultConfidence.textContent = `${(confidence * 100).toFixed(1)}%`;

    // Confidence Bars
    const realProb = (result.real_probability || 0) * 100;
    const fakeProb = (result.deepfake_probability || 0) * 100;

    realBar.style.width = realProb + '%';
    deepfakeBar.style.width = fakeProb + '%';

    realScore.textContent = realProb.toFixed(1) + '%';
    deepfakeScore.textContent = fakeProb.toFixed(1) + '%';

    // Metrics
    document.getElementById('duration').textContent = (result.duration || 0).toFixed(2) + 's';
    document.getElementById('sampleRate').textContent = (result.sample_rate || 0) + 'Hz';
    document.getElementById('channels').textContent = result.channels || 1;
    document.getElementById('bitrate').textContent = (result.bitrate || 0) + 'kbps';

    // Reset feedback
    feedbackMessage.textContent = '';
    correctBtn.disabled = false;
    incorrectBtn.disabled = false;
}

// Feedback
async function submitFeedback(isCorrect) {
    if (!selectedFile) return;

    correctBtn.disabled = true;
    incorrectBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('filename', selectedFile.name);
        formData.append('is_correct', isCorrect.toString());

        const response = await fetch('/feedback', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Feedback submission failed');
        }

        feedbackMessage.textContent = 'Thank you for your feedback!';
        feedbackMessage.style.color = '#10b981';
        console.log('Feedback submitted successfully');
        
        // Reload dashboard data after feedback
        loadDashboardData();

    } catch (error) {
        console.error('Error:', error);
        feedbackMessage.textContent = 'Error submitting feedback: ' + error.message;
        feedbackMessage.style.color = '#ef4444';
    } finally {
        correctBtn.disabled = false;
        incorrectBtn.disabled = false;
    }
}

// Charts
function initCharts() {
    if (document.getElementById('detectionPieChart')) {
        createDetectionPieChart();
    }
    if (document.getElementById('confidenceBarChart')) {
        createConfidenceBarChart();
    }
}

function createDetectionPieChart(data = null) {
    // Destroy existing chart if it exists
    if (chartInstances.pie) {
        chartInstances.pie.destroy();
    }

    const canvas = document.getElementById('detectionPieChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const chartData = data || {
        real: 1200,
        deepfake: 847
    };

    chartInstances.pie = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Real Voice', 'Deepfake'],
            datasets: [{
                data: [chartData.real, chartData.deepfake],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',  // Green for Real
                    'rgba(239, 68, 68, 0.8)'   // Red for Deepfake
                ],
                borderColor: [
                    '#10b981',
                    '#ef4444'
                ],
                borderWidth: 2,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 12 },
                        padding: 15
                    }
                }
            }
        }
    });
}

function createConfidenceBarChart(data = null) {
    // Destroy existing chart if it exists
    if (chartInstances.confidence) {
        chartInstances.confidence.destroy();
    }

    const canvas = document.getElementById('confidenceBarChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const chartData = data || {
        labels: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
        values: [45, 120, 234, 387, 861]
    };

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(74, 95, 239, 0.8)');
    gradient.addColorStop(1, 'rgba(74, 95, 239, 0.3)');

    chartInstances.confidence = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Number of Detections',
                data: chartData.values,
                backgroundColor: gradient,
                borderColor: '#4a5fef',
                borderWidth: 2,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#94a3b8',
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
}

// Load Dashboard Data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/stats');
        if (response.ok) {
            const stats = await response.json();
            updateDashboard(stats);
            
            // Update charts with actual data
            if (stats.detection_distribution) {
                if (chartInstances.pie) chartInstances.pie.destroy();
                if (chartInstances.confidence) chartInstances.confidence.destroy();
                
                createDetectionPieChart(stats.detection_distribution);
                createConfidenceBarChart(stats.confidence_distribution);
            }
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load Filtered Data Based on Time Period
async function loadFilteredData(period = 'today') {
    try {
        const response = await fetch(`/api/stats?period=${period}`);
        if (response.ok) {
            const stats = await response.json();
            updateDashboard(stats);
            
            // Update charts with period-specific data
            if (stats.detection_distribution) {
                // Destroy old charts
                if (chartInstances.pie) chartInstances.pie.destroy();
                if (chartInstances.confidence) chartInstances.confidence.destroy();
                
                createDetectionPieChart(stats.detection_distribution);
                createConfidenceBarChart(stats.confidence_distribution);
            }
        }
    } catch (error) {
        console.error('Error loading filtered stats:', error);
    }
}

// Load History Data
async function loadHistoryData() {
    try {
        const response = await fetch('/api/history');
        if (response.ok) {
            const data = await response.json();
            updateHistory(data);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function updateHistory(data) {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    if (data.history && data.history.length > 0) {
        data.history.forEach(item => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid #374151';
            row.innerHTML = `
                <td style="padding: 15px;">${item.filename || 'N/A'}</td>
                <td style="padding: 15px;"><span class="badge ${item.classification === 'Real' ? 'real' : 'deepfake'}">${item.classification || 'N/A'}</span></td>
                <td style="padding: 15px;">${((item.confidence || 0) * 100).toFixed(1)}%</td>
                <td style="padding: 15px;">${item.timestamp ? new Date(item.timestamp).toLocaleString() : 'N/A'}</td>
                <td style="padding: 15px;">${(item.duration || 0).toFixed(2)}s</td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="5" style="padding: 30px; text-align: center; color: #94a3b8;">No detection history found</td></tr>';
    }
}

function updateDashboard(stats) {
    // Update stat cards with real data
    console.log('Dashboard stats loaded:', stats);
    
    const volumeVal = document.getElementById('volumeValue');
    const accuracyVal = document.getElementById('accuracyValue');
    const tpVal = document.getElementById('tpValue');
    const fpVal = document.getElementById('fpValue');
    
    const volumeChange = document.getElementById('volumeChange');
    const accuracyChange = document.getElementById('accuracyChange');
    const tpChange = document.getElementById('tpChange');
    const fpChange = document.getElementById('fpChange');
    
    if (volumeVal) volumeVal.textContent = (stats.detection_volume || 2847).toLocaleString();
    if (accuracyVal) accuracyVal.textContent = ((stats.accuracy || 94.2).toFixed(1)) + '%';
    if (tpVal) tpVal.textContent = (stats.true_positives || 2456).toLocaleString();
    if (fpVal) fpVal.textContent = (stats.false_positives || 178).toLocaleString();
    
    const volumeChangeVal = stats.detection_volume_change || 28.56;
    const accuracyChangeVal = stats.accuracy_change || -18.33;
    const tpChangeVal = stats.true_positives_change || 15.23;
    const fpChangeVal = stats.false_positives_change || -5.12;
    
    if (volumeChange) {
        volumeChange.textContent = (volumeChangeVal > 0 ? '↑' : '↓') + ' ' + Math.abs(volumeChangeVal).toFixed(2) + '%';
        volumeChange.className = (volumeChangeVal > 0 ? 'trend-badge up' : 'trend-badge down');
    }
    if (accuracyChange) {
        accuracyChange.textContent = (accuracyChangeVal > 0 ? '↑' : '↓') + ' ' + Math.abs(accuracyChangeVal).toFixed(2) + '%';
        accuracyChange.className = (accuracyChangeVal > 0 ? 'trend-badge up' : 'trend-badge down');
    }
    if (tpChange) {
        tpChange.textContent = (tpChangeVal > 0 ? '↑' : '↓') + ' ' + Math.abs(tpChangeVal).toFixed(2) + '%';
        tpChange.className = (tpChangeVal > 0 ? 'trend-badge up' : 'trend-badge down');
    }
    if (fpChange) {
        fpChange.textContent = (fpChangeVal > 0 ? '↑' : '↓') + ' ' + Math.abs(fpChangeVal).toFixed(2) + '%';
        fpChange.className = (fpChangeVal > 0 ? 'trend-badge up' : 'trend-badge down');
    }
    
    // Update detector page stats
    const detectorTotal = document.getElementById('detectorTotalAnalyzed');
    const detectorRate = document.getElementById('detectorDetectionRate');
    if (detectorTotal) detectorTotal.textContent = (stats.detection_volume || 2847).toLocaleString();
    if (detectorRate) detectorRate.textContent = ((stats.accuracy || 94.2).toFixed(1)) + '%';
}

// Page Navigation
function switchPage(page) {
    // Hide all pages
    const pages = document.querySelectorAll('.page-content');
    pages.forEach(p => p.style.display = 'none');
    
    // Show selected page
    const selectedPage = document.getElementById(page + '-page');
    if (selectedPage) selectedPage.style.display = 'block';
    
    // Update nav items active state
    navItems.forEach(item => {
        if (item.getAttribute('data-page') === page) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Load data based on page
    if (page === 'dashboard') {
        loadDashboardData();
    } else if (page === 'detector') {
        loadDashboardData();
    } else if (page === 'history') {
        loadHistoryData();
    } else if (page === 'models') {
        // Models page is static  
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeUploadModal();
        closeResultsModal();
        sidebar.classList.remove('active');
    }
});

// Load Cybercrime Report Data
async function loadCybercrimeReport() {
    try {
        const response = await fetch('/api/cybercrime-report');
        if (response.ok) {
            const report = await response.json();
            updateCybercrimeReport(report);
        }
    } catch (error) {
        console.error('Error loading cybercrime report:', error);
    }
}

function updateCybercrimeReport(report) {
    // Update crime category counts
    if (report.crime_categories) {
        document.getElementById('fraudCount').textContent = report.crime_categories.fraud || 0;
        document.getElementById('impersonationCount').textContent = report.crime_categories.impersonation || 0;
        document.getElementById('blackmailCount').textContent = report.crime_categories.blackmail || 0;
        document.getElementById('identityCount').textContent = report.crime_categories.identity_theft || 0;
        document.getElementById('sextortionCount').textContent = report.crime_categories.sextortion || 0;
        document.getElementById('otherCount').textContent = report.crime_categories.other || 0;
    }
    
    // Update risk assessment
    if (report.risk_assessment) {
        const globalRiskEl = document.getElementById('globalRisk');
        const surgRiskEl = document.getElementById('surgRisk');
        
        if (globalRiskEl) {
            globalRiskEl.textContent = report.risk_assessment.global_level || 'CRITICAL';
            globalRiskEl.className = 'risk-badge ' + (report.risk_assessment.global_level || 'critical').toLowerCase();
        }
        
        if (surgRiskEl) {
            surgRiskEl.textContent = report.risk_assessment.surge_level || 'HIGH';
            surgRiskEl.className = 'risk-badge ' + (report.risk_assessment.surge_level || 'high').toLowerCase();
        }
    }
}
