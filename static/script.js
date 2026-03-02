// API Base URL
const API_BASE = '/api';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const selectedFiles = document.getElementById('selectedFiles');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const analyzeProgress = document.getElementById('analyzeProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const resultsList = document.getElementById('resultsList');
const singleFile = document.getElementById('singleFile');
const analyzeBtn2 = document.getElementById('analyzeBtn2');
const analysisResult = document.getElementById('analysisResult');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

// Store selected files
let selectedFilesArray = [];
let currentResult = null;
let actualLabel = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkApiStatus();
    loadSystemInfo();
});

// Setup Event Listeners
function setupEventListeners() {
    // Drag and drop
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // File input
    fileInput.addEventListener('change', handleFileSelect);
    
    // Buttons
    analyzeBtn.addEventListener('click', analyzeMultipleFiles);
    clearBtn.addEventListener('click', clearFiles);
    analyzeBtn2.addEventListener('click', analyzeSingleFile);
    
    // Single file input
    singleFile.addEventListener('change', () => {
        if (singleFile.files.length > 0) {
            analyzeBtn2.disabled = false;
        }
    });
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    addFiles(files);
}

// File Selection
function handleFileSelect(e) {
    const files = e.target.files;
    addFiles(files);
}

function addFiles(files) {
    for (let file of files) {
        if (isValidAudioFile(file)) {
            selectedFilesArray.push(file);
        }
    }
    updateFileList();
}

function isValidAudioFile(file) {
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/flac', 'audio/ogg', 'audio/mp3'];
    const validExtensions = ['.wav', '.mp3', '.flac', '.ogg'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    return validTypes.some(type => file.type.includes(type)) || 
           validExtensions.includes(fileExt);
}

function updateFileList() {
    if (selectedFilesArray.length === 0) {
        fileList.style.display = 'none';
        uploadArea.style.display = 'block';
        return;
    }
    
    uploadArea.style.display = 'none';
    fileList.style.display = 'block';
    
    selectedFiles.innerHTML = '';
    selectedFilesArray.forEach((file, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="file-name">📄 ${file.name}</span>
            <span class="file-size">${formatFileSize(file.size)}</span>
            <button class="remove-btn" onclick="removeFile(${index})">✕</button>
        `;
        selectedFiles.appendChild(li);
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function removeFile(index) {
    selectedFilesArray.splice(index, 1);
    updateFileList();
}

function clearFiles() {
    selectedFilesArray = [];
    fileInput.value = '';
    updateFileList();
    resultsSection.style.display = 'none';
}

// Analyze Multiple Files
async function analyzeMultipleFiles() {
    if (selectedFilesArray.length === 0) {
        showError('Please select files to analyze');
        return;
    }
    
    analyzeBtn.disabled = true;
    analyzeProgress.style.display = 'block';
    resultsSection.style.display = 'block';
    resultsList.innerHTML = '';
    
    const formData = new FormData();
    selectedFilesArray.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch('/detect-batch', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Batch detection failed');
        }
        
        const data = await response.json();
        displayBatchResults(data);
        
    } catch (error) {
        showError('Analysis failed: ' + error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeProgress.style.display = 'none';
    }
}

function displayBatchResults(data) {
    const results = data.results || [];
    let deepfakesCount = 0;
    let realCount = 0;
    
    results.forEach((result, index) => {
        const resultData = result.result;
        
        if (resultData) {
            const isDeepfake = resultData.is_deepfake;
            const confidence = (resultData.confidence * 100).toFixed(2);
            
            if (isDeepfake) deepfakesCount++;
            else realCount++;
            
            const resultCard = document.createElement('div');
            resultCard.className = `result-card ${isDeepfake ? 'deepfake' : 'real'}`;
            
            resultCard.innerHTML = `
                <div class="result-status">
                    <span class="result-status-icon">${isDeepfake ? '⚠️' : '✅'}</span>
                    <span>${isDeepfake ? 'DEEPFAKE' : 'REAL'}</span>
                </div>
                <div class="result-confidence">
                    <div class="confidence-bar-small">
                        <div class="confidence-fill-small" style="width: ${confidence}%"></div>
                    </div>
                    <span>${confidence}%</span>
                </div>
                <div class="result-file">${result.file || `File ${index + 1}`}</div>
            `;
            
            resultsList.appendChild(resultCard);
        }
    });
    
    updateSummaryStats(results.length, deepfakesCount, realCount);
}

function updateSummaryStats(total, deepfakes, real) {
    document.getElementById('totalFiles').textContent = total;
    document.getElementById('deepfakesDetected').textContent = deepfakes;
    document.getElementById('realAudio').textContent = real;
}

// Analyze Single File
async function analyzeSingleFile() {
    if (!singleFile.files || singleFile.files.length === 0) {
        showError('Please select a file');
        return;
    }
    
    const file = singleFile.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    analyzeBtn2.disabled = true;
    analyzeBtn2.innerHTML = '<span class="spinner"></span> Analyzing...';
    
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Detection failed');
        }
        
        const data = await response.json();
        displayAnalysisResult(data, file.name);
        
    } catch (error) {
        showError('Analysis failed: ' + error.message);
    } finally {
        analyzeBtn2.disabled = false;
        analyzeBtn2.innerHTML = 'Analyze';
    }
}

function displayAnalysisResult(data, fileName) {
    const isDeepfake = data.is_deepfake;
    const confidence = (data.confidence * 100).toFixed(2);
    const scores = data.scores;
    
    const resultIcon = document.getElementById('resultIcon');
    const confidenceFill = document.getElementById('confidenceFill');
    
    // Update visualization
    resultIcon.textContent = isDeepfake ? '⚠️ DEEPFAKE' : '✅ REAL';
    resultIcon.style.color = isDeepfake ? '#ef4444' : '#10b981';
    
    confidenceFill.style.width = confidence + '%';
    if (isDeepfake) {
        confidenceFill.classList.add('deepfake');
    } else {
        confidenceFill.classList.remove('deepfake');
    }
    
    // Update details
    document.getElementById('classification').textContent = isDeepfake ? 'DEEPFAKE' : 'REAL VOICE';
    document.getElementById('confidence').textContent = confidence + '%';
    document.getElementById('fileName').textContent = fileName;
    document.getElementById('confidenceText').textContent = 
        `Confidence: ${scores.deepfake.toFixed(4)} (Deepfake) vs ${scores.real.toFixed(4)} (Real)`;
    
    // Store current result for verification
    currentResult = {
        fileName: fileName,
        predicted: isDeepfake ? 'deepfake' : 'real',
        confidence: parseFloat(confidence),
        scores: scores
    };
    actualLabel = null;
    
    // Show verification section
    const verificationSection = document.getElementById('verificationSection');
    const feedbackForm = document.getElementById('feedbackForm');
    const feedbackSuccess = document.getElementById('feedbackSuccess');
    verificationSection.style.display = 'block';
    feedbackForm.style.display = 'none';
    feedbackSuccess.style.display = 'none';
    
    analysisResult.style.display = 'block';
    
    // Load verification stats
    loadVerificationStats();
}

// API Status and Info
async function checkApiStatus() {
    try {
        const response = await fetch('/health', { method: 'GET' });
        const data = await response.json();
        
        if (response.ok) {
            statusDot.classList.add('online');
            statusText.textContent = 'System Online';
            statusText.style.color = '#10b981';
            
            document.getElementById('apiStatus').textContent = 
                `✅ ${data.status}`;
            document.getElementById('modelStatus').textContent = 
                data.model_loaded ? '✅ Loaded' : '❌ Not Loaded';
        } else {
            throw new Error('API offline');
        }
    } catch (error) {
        statusDot.classList.remove('online');
        statusText.textContent = 'System Offline';
        statusText.style.color = '#ef4444';
        document.getElementById('apiStatus').textContent = '❌ Offline';
    }
}

async function loadSystemInfo() {
    try {
        const response = await fetch('/info', { method: 'GET' });
        const data = await response.json();
        
        document.getElementById('supportedFormats').textContent = 
            data.supported_formats.join(', ').toUpperCase();
        document.getElementById('maxFileSize').textContent = 
            data.max_file_size_mb + ' MB';
            
    } catch (error) {
        console.error('Error loading system info:', error);
    }
}

// Utility Functions
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = '❌ ' + message;
    
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection.style.display !== 'none') {
        resultsSection.appendChild(errorDiv);
    } else {
        uploadArea.parentElement.appendChild(errorDiv);
    }
    
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = '✅ ' + message;
    
    document.querySelector('.main-content').appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 3000);
}

// Verification Functions
function submitFeedback(isCorrect) {
    const verificationSection = document.getElementById('verificationSection');
    const feedbackForm = document.getElementById('feedbackForm');
    const feedbackSuccess = document.getElementById('feedbackSuccess');
    
    if (isCorrect) {
        // Correct prediction - submit immediately
        saveFeedback(true, null, '');
    } else {
        // Incorrect - show form to get actual label
        feedbackForm.style.display = 'block';
    }
}

function setActualLabel(label) {
    actualLabel = label;
    const actualReal = document.getElementById('actualReal');
    const actualFake = document.getElementById('actualFake');
    
    actualReal.style.opacity = label === 'real' ? '1' : '0.5';
    actualFake.style.opacity = label === 'deepfake' ? '1' : '0.5';
}

function submitFinalFeedback() {
    if (!actualLabel) {
        showError('Please select the actual label');
        return;
    }
    
    const comment = document.getElementById('feedbackComment').value;
    saveFeedback(false, actualLabel, comment);
}

function saveFeedback(isCorrect, actualLabel, comment) {
    if (!currentResult) {
        showError('No result to verify');
        return;
    }
    
    const feedback = {
        file_name: currentResult.fileName,
        predicted_label: currentResult.predicted,
        actual_label: actualLabel || currentResult.predicted,
        confidence: currentResult.confidence,
        is_correct: isCorrect,
        user_comment: comment
    };
    
    fetch('/api/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedback)
    })
    .then(response => {
        if (!response.ok) throw new Error('Feedback submission failed');
        return response.json();
    })
    .then(data => {
        // Show success message
        const feedbackForm = document.getElementById('feedbackForm');
        const feedbackSuccess = document.getElementById('feedbackSuccess');
        feedbackForm.style.display = 'none';
        feedbackSuccess.style.display = 'block';
        
        setTimeout(() => {
            feedbackSuccess.style.display = 'none';
            loadVerificationStats();
        }, 2000);
    })
    .catch(error => {
        showError('Error submitting feedback: ' + error.message);
    });
}

function loadVerificationStats() {
    fetch('/api/feedback/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalFeedback').textContent = data.total_feedback;
            document.getElementById('correctPredictions').textContent = data.correct_predictions;
            document.getElementById('incorrectPredictions').textContent = data.incorrect_predictions;
            document.getElementById('feedbackAccuracy').textContent = data.accuracy + '%';
            
            if (data.total_feedback > 0) {
                document.getElementById('verificationStatsSection').style.display = 'block';
            }
        })
        .catch(error => console.error('Error loading stats:', error));
}

// Auto-refresh status every 30 seconds
setInterval(checkApiStatus, 30000);
