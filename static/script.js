// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFileBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');

// Results Elements
const classificationBadge = document.getElementById('classificationBadge');
const classificationText = document.getElementById('classificationText');
const resultConfidence = document.getElementById('resultConfidence');
const realBar = document.getElementById('realBar');
const deepfakeBar = document.getElementById('deepfakeBar');
const realScore = document.getElementById('realScore');
const deepfakeScore = document.getElementById('deepfakeScore');
const deepfakeProb = document.getElementById('deepfakeProb');
const realProb = document.getElementById('realProb');
const detectionResult = document.getElementById('detectionResult');
const timestamp = document.getElementById('timestamp');
const correctBtn = document.getElementById('correctBtn');
const incorrectBtn = document.getElementById('incorrectBtn');
const feedbackMessage = document.getElementById('feedbackMessage');

let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkSystemStatus();
});

// Event Listeners
function setupEventListeners() {
    // Upload Area
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.backgroundColor = 'rgba(99, 102, 241, 0.2)';
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
    analyzeAgainBtn.addEventListener('click', resetUI);
    correctBtn.addEventListener('click', () => submitFeedback(true));
    incorrectBtn.addEventListener('click', () => submitFeedback(false));
}

// File Selection
function handleFileSelect(file) {
    // Validate file
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

// File Analysis
async function analyzeFile() {
    if (!selectedFile) {
        alert('Please select a file first');
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="loading">⏳</span> Analyzing...';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error:', error);
        alert('Analysis failed. Please try again.');
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '🔍 Analyze Audio';
    }
}

// Display Results
function displayResults(result) {
    const isDeepfake = result.is_deepfake;
    const deepfakeConfidence = result.confidence;
    const realConfidence = result.scores.real;

    // Update classification badge
    classificationBadge.textContent = isDeepfake ? '⚠️' : '✓';
    classificationText.textContent = isDeepfake ? 'DEEPFAKE' : 'REAL VOICE';
    classificationText.className = `classification-text ${isDeepfake ? 'deepfake' : 'real'}`;

    // Update confidence display
    resultConfidence.textContent = `${(deepfakeConfidence * 100).toFixed(1)}%`;

    // Update progress bars
    const realPercent = (realConfidence * 100).toFixed(0);
    const deepfakePercent = (deepfakeConfidence * 100).toFixed(0);

    realBar.style.width = `${realPercent}%`;
    deepfakeBar.style.width = `${deepfakePercent}%`;

    realScore.textContent = `${realPercent}%`;
    deepfakeScore.textContent = `${deepfakePercent}%`;

    // Update detailed metrics
    deepfakeProb.textContent = `${(deepfakeConfidence * 100).toFixed(2)}%`;
    realProb.textContent = `${(realConfidence * 100).toFixed(2)}%`;
    detectionResult.textContent = isDeepfake ? 'DEEPFAKE DETECTED' : 'REAL VOICE DETECTED';
    
    const now = new Date();
    timestamp.textContent = now.toLocaleString();

    // Reset feedback message
    feedbackMessage.style.display = 'none';
    correctBtn.disabled = false;
    incorrectBtn.disabled = false;
}

// Feedback
async function submitFeedback(isCorrect) {
    if (!selectedFile) return;

    const button = isCorrect ? correctBtn : incorrectBtn;
    button.disabled = true;

    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: selectedFile.name,
                file_size: selectedFile.size,
                user_feedback: isCorrect
            })
        });

        if (response.ok) {
            // Show success message
            feedbackMessage.style.display = 'block';
            feedbackMessage.textContent = isCorrect 
                ? '✓ Thank you! Your feedback helps improve our system.' 
                : '✓ Thank you! Your feedback helps improve our system.';
            
            correctBtn.disabled = true;
            incorrectBtn.disabled = true;
        } else {
            throw new Error('Failed to submit feedback');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        feedbackMessage.style.display = 'block';
        feedbackMessage.textContent = '❌ Failed to submit feedback. Please try again.';
        feedbackMessage.style.borderLeftColor = '#ef4444';
        feedbackMessage.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
        feedbackMessage.style.color = '#ef4444';
    }
}

// Reset UI
function resetUI() {
    removeFile();
    resultsSection.style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Check System Status
async function checkSystemStatus() {
    try {
        const response = await fetch('/health');
        if (!response.ok) {
            console.warn('System health check failed');
        }
    } catch (error) {
        console.error('Could not reach API:', error);
    }
}

// Keyboard Support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && selectedFile && fileInfo.style.display === 'block') {
        analyzeFile();
    }
});
