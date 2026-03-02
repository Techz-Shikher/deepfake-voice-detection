# 🔧 Development & Troubleshooting Reference

Technical reference for developers maintaining or extending the deepfake detection system.

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Module Reference](#module-reference)
4. [Common Development Tasks](#common-development-tasks)
5. [Debugging Guide](#debugging-guide)
6. [Testing Guide](#testing-guide)
7. [Performance Profiling](#performance-profiling)
8. [Known Issues](#known-issues)
9. [Deployment Checklist](#deployment-checklist)

---

## Development Environment Setup

### Prerequisites
- Python 3.13+
- Git (for version control)
- pip (Python package manager)
- Virtual environment support

### Setting Up Dev Environment

```bash
# 1. Clone or navigate to project
cd "f:\deepfake voice detection"

# 2. Create virtual environment
python -m venv venv-dev

# 3. Activate environment
# Windows:
venv-dev\Scripts\activate
# Mac/Linux:
source venv-dev/bin/activate

# 4. Install dependencies with dev tools
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy  # Dev tools

# 5. Verify installation
python -c "import flask, librosa; print('✓ All imports working')"
```

### IDE Setup (VS Code)

1. Install Python extension (Microsoft)
2. Select interpreter: Python 3.13 (venv-dev)
3. Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true
    }
}
```

---

## Project Structure

### Directory Tree
```
deepfake voice detection/
├── api.py                      # Main Flask app (main endpoint)
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── setup.sh / setup.bat        # OS-specific setup scripts
│
├── src/                        # Core modules
│   ├── __init__.py
│   ├── detector.py             # DeepfakeDetector class
│   ├── audio_processor.py      # AudioProcessor class
│   ├── feature_extractor.py    # FeatureExtractor class
│   ├── model_builder.py        # ModelBuilder class
│   └── feedback.py             # FeedbackManager class
│
├── models/                     # Pre-trained models
│   └── deepfake_model.pkl      # Serialized model
│
├── data/                       # Data storage
│   ├── raw/                    # Training audio
│   │   ├── real/               # Real voice samples
│   │   └── fake/               # Deepfake samples
│   ├── feedback.json           # User feedback entries
│   └── feedback_stats.json     # Aggregated stats
│
├── templates/                  # Web interface
│   └── index.html              # Single page app
│
├── static/                     # Client assets
│   ├── style.css               # CSS styling
│   └── script.js               # JavaScript
│
├── tests/                      # Test files
│   ├── test_detector.py
│   ├── test_api.py
│   └── test_feedback.py
│
└── docs/                       # Documentation
    ├── README.md
    ├── QUICK_START.md
    ├── API_REFERENCE.md
    ├── ARCHITECTURE.md
    ├── VERIFICATION_GUIDE.md
    └── USER_MANUAL.md
```

### File Purposes

| File | Purpose | Maintainer |
|------|---------|-----------|
| `api.py` | Flask server & routes | Backend dev |
| `src/detector.py` | Main detection logic | ML engineer |
| `src/audio_processor.py` | Audio loading | Audio engineer |
| `src/feature_extractor.py` | Feature engineering | ML engineer |
| `src/model_builder.py` | Model architecture | ML engineer |
| `src/feedback.py` | Feedback system | Backend dev |
| `templates/index.html` | Web interface | Frontend dev |
| `static/style.css` | Styling | Frontend dev |
| `static/script.js` | Client logic | Frontend dev |

---

## Module Reference

### src/detector.py

**Main class for detection pipeline.**

```python
from src.detector import DeepfakeDetector

# Initialize
detector = DeepfakeDetector('models/deepfake_model.pkl')

# Analyze audio
result = detector.detect('path/to/audio.wav')
# Returns: {
#     'file_name': 'audio.wav',
#     'classification': 'real',
#     'confidence': 0.95,
#     'scores': {'real': 0.95, 'deepfake': 0.05},
#     'processing_time': 1.23
# }
```

**Key Methods:**
- `__init__(model_path)` - Load model
- `detect(audio_path)` - Main pipeline
- `_load_audio(audio_path)` - Load various formats
- `_extract_features(audio)` - Get features
- `_predict(features)` - Get prediction

### src/audio_processor.py

**Audio loading and preprocessing.**

```python
from src.audio_processor import AudioProcessor

# Load audio
audio, sr = AudioProcessor.load_audio('file.wav')
# Returns: (numpy array, sample rate 22050)

# Supported formats: WAV, MP3, FLAC, OGG
```

### src/feature_extractor.py

**Feature engineering: MFCC, statistics, ZCR, energy.**

```python
from src.feature_extractor import FeatureExtractor

# Extract features
features = FeatureExtractor.extract_features(audio)
# Returns: 163-dimensional numpy array
```

**Feature components:**
- MFCC: 40 coefficients
- MFCC Stats: 160 features (4 stats × 40 coefficients)
- ZCR: 1 feature
- Energy: 1 feature
- **Total: 163 features**

### src/model_builder.py

**Model training and architecture.**

```python
from src.model_builder import ModelBuilder

# Build model
model = ModelBuilder.build()
# Returns: GradientBoostingClassifier

# Train model (not used in current system)
# model.fit(X_train, y_train)

# Save model
ModelBuilder.save_model(model, 'models/deepfake_model.pkl')
```

### src/feedback.py

**User feedback and statistics management.**

```python
from src.feedback import FeedbackManager

# Ensure files exist
FeedbackManager.ensure_files_exist()

# Save feedback
FeedbackManager.save_feedback(
    file_name='audio.wav',
    predicted_label='real',
    actual_label='deepfake',
    confidence=0.95,
    is_correct=False,
    user_comment='Optional comment'
)

# Get statistics
stats = FeedbackManager.get_stats()
# Returns: {
#     'total_feedback': 42,
#     'correct_predictions': 38,
#     'incorrect_predictions': 4,
#     'accuracy': 90.48,
#     'last_updated': 'ISO-timestamp'
# }

# Get feedback history
feedback = FeedbackManager.get_feedback(limit=50)

# Get data for retraining
data = FeedbackManager.get_feedback_for_retraining()
```

---

## Common Development Tasks

### Task 1: Add New API Endpoint

**Example: Add /api/test-model endpoint**

```python
# In api.py

@app.route('/api/test-model', methods=['POST'])
def test_model():
    """Test endpoint for model verification."""
    try:
        # Get test data
        test_audio_path = 'data/test_audio.wav'
        
        # Run detection
        result = detector.detect(test_audio_path)
        
        return jsonify({
            'status': 'success',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Task 2: Modify Feature Extraction

**Example: Add new spectral feature**

```python
# In src/feature_extractor.py

@staticmethod
def extract_features(audio):
    """Extract 163-dimensional feature vector."""
    
    # Extract MFCC and stats
    mfcc = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=40)
    mfcc_mean = mfcc.mean(axis=1)  # (40,)
    mfcc_std = mfcc.std(axis=1)    # (40,)
    mfcc_min = mfcc.min(axis=1)    # (40,)
    mfcc_max = mfcc.max(axis=1)    # (40,)
    
    # Zero-crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio)[0].mean()
    
    # Energy
    energy = np.mean(audio ** 2)
    
    # (NEW) Add spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=audio)[0].mean()
    
    # Concatenate all features
    features = np.concatenate([
        mfcc_mean, mfcc_std, mfcc_min, mfcc_max,
        [zcr], [energy], [spectral_centroid]  # Added
    ])
    
    return features  # Now 164 dimensions instead of 163
```

**Important:** If you change feature dimensions, update:
1. Training data format
2. Model input expectations
3. Documentation
4. All clients using the model

### Task 3: Improve Model Accuracy

**Using feedback data for retraining:**

```python
# New script: retrain_model.py

from src.feedback import FeedbackManager
from src.feature_extractor import FeatureExtractor
from src.audio_processor import AudioProcessor
from src.model_builder import ModelBuilder
import numpy as np

# Get feedback data
data = FeedbackManager.get_feedback_for_retraining()

# Prepare training samples
X_train = []
y_train = []

# Add original training data
# (Include real/ and fake/ samples from data/raw/)

# Add misclassified samples from feedback
for sample in data.get('misclassified', []):
    audio, sr = AudioProcessor.load_audio(sample['file_path'])
    features = FeatureExtractor.extract_features(audio)
    
    label = 1 if sample['actual'] == 'deepfake' else 0
    
    X_train.append(features)
    y_train.append(label)

# Retrain model
X_train = np.array(X_train)
y_train = np.array(y_train)

model = ModelBuilder.build()
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_train, y_train)
print(f"New Accuracy: {accuracy:.2%}")

# Save improved model
ModelBuilder.save_model(model, 'models/deepfake_model_v2.pkl')
```

---

## Debugging Guide

### Enable Debug Logging

**In api.py:**
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In routes:
@app.route('/api/detect', methods=['POST'])
def detect():
    logger.debug(f"Received file: {file.filename}")
    # ... rest of code
```

### Debug Detection Pipeline

```python
# Create debug_detector.py

from src.detector import DeepfakeDetector
from src.audio_processor import AudioProcessor
from src.feature_extractor import FeatureExtractor
import numpy as np

# Step 1: Load audio
audio_path = 'test_audio.wav'
audio, sr = AudioProcessor.load_audio(audio_path)
print(f"✓ Loaded audio: shape={audio.shape}, sr={sr}")

# Step 2: Extract features
features = FeatureExtractor.extract_features(audio)
print(f"✓ Extracted features: shape={features.shape}, dtype={features.dtype}")
print(f"  Min: {features.min():.4f}, Max: {features.max():.4f}")
print(f"  Mean: {features.mean():.4f}, Std: {features.std():.4f}")

# Step 3: Full detection
detector = DeepfakeDetector('models/deepfake_model.pkl')
result = detector.detect(audio_path)
print(f"✓ Detection result: {result}")
```

### Debug API Issues

```python
# Test API with curl
curl -X POST -F "file=@test.wav" http://localhost:5000/api/detect -v

# Test with Python
import requests
with open('test.wav', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/detect',
        files={'file': f}
    )
    print(response.status_code)
    print(response.json())
```

### Common Error Messages and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `FileNotFoundError: models/deepfake_model.pkl` | Model missing | Ensure model file exists in correct location |
| `OSError: cannot open shared library` | System library missing (librosa) | Reinstall librosa: `pip install --upgrade librosa` |
| `json.JSONDecodeError: ...` | Invalid JSON response | Check API response format |
| `httpx.ConnectError: ...` | API not running | Verify server is running: `python api.py` |

---

## Testing Guide

### Unit Test Example

```python
# tests/test_detector.py

import pytest
import numpy as np
from src.detector import DeepfakeDetector
from src.audio_processor import AudioProcessor
from src.feature_extractor import FeatureExtractor

def test_audio_loading():
    """Test audio loading from various formats."""
    audio, sr = AudioProcessor.load_audio('data/raw/real/sample1.wav')
    
    assert audio is not None
    assert isinstance(audio, np.ndarray)
    assert sr == 22050
    assert len(audio) > 0

def test_feature_extraction():
    """Test feature extraction produces correct shape."""
    audio = np.random.randn(22050)  # 1 second of audio
    features = FeatureExtractor.extract_features(audio)
    
    assert features.shape == (163,)
    assert not np.any(np.isnan(features))  # No NaN values

def test_detection():
    """Test full detection pipeline."""
    detector = DeepfakeDetector('models/deepfake_model.pkl')
    result = detector.detect('data/raw/real/sample1.wav')
    
    assert 'classification' in result
    assert 'confidence' in result
    assert result['classification'] in ['real', 'deepfake']
    assert 0 <= result['confidence'] <= 1

def test_api_health():
    """Test API health endpoint."""
    from api import app
    
    client = app.test_client()
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/

# Run specific test
pytest tests/test_detector.py::test_audio_loading

# Run with verbose output
pytest -v
```

---

## Performance Profiling

### Profile Detection Speed

```python
# profile_detector.py

import cProfile
import pstats
from src.detector import DeepfakeDetector

def profile_detection():
    detector = DeepfakeDetector('models/deepfake_model.pkl')
    detector.detect('test_audio.wav')

# Run profiler
profiler = cProfile.Profile()
profiler.enable()

for _ in range(10):
    profile_detection()

profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Run with memory profiling
python -m memory_profiler profile_detector.py
```

### Bottleneck Analysis

| Operation | Timing | Optimization |
|-----------|--------|--------------|
| Audio loading | ~300ms | Cache in memory |
| MFCC extraction | ~600ms | Use librosa.stft cache |
| Statistics calc | ~100ms | Vectorize operations |
| Model prediction | ~50ms | Use GPU if available |
| JSON write | ~20ms | Batch writes |

---

## Known Issues

### Issue 1: TensorFlow/Keras Compatibility
**Status:** RESOLVED  
**Details:** Python 3.13 has incompatibility with TensorFlow versions < 2.16  
**Solution:** Using scikit-learn (GradientBoost) instead

### Issue 2: Large File Processing
**Status:** KNOWN  
**Details:** Files > 50MB may fail or timeout  
**Workaround:** Split large files into segments, increase timeout in api.py

### Issue 3: MP3 Decoding on Linux
**Status:** KNOWN  
**Details:** MP3 requires additional system libraries on Linux  
**Solution:** 
```bash
# Ubuntu/Debian
sudo apt-get install libmpg123-0

# Or use different format (WAV, FLAC)
```

### Issue 4: Model Accuracy on Real Deepfakes
**Status:** ACKNOWLEDGED  
**Details:** Model trained on synthetic data, may not work well on real deepfakes  
**Solution:** Provide feedback on misclassified samples for improvement

---

## Deployment Checklist

### Pre-Deployment Verification

```bash
# ✓ Run tests
pytest --cov=src/

# ✓ Check code quality
flake8 src/ api.py
black --check src/ api.py

# ✓ Type checking
mypy src/ api.py

# ✓ Verify all endpoints
curl http://localhost:5000/health
curl http://localhost:5000/info
curl -X POST -F "file=@test.wav" http://localhost:5000/api/detect

# ✓ Check permissions
ls -la data/
# Should have write permissions

# ✓ Verify model exists
ls -la models/deepfake_model.pkl
```

### Deployment Steps

1. **Prepare environment**
   ```bash
   python -m venv venv-prod
   source venv-prod/bin/activate
   pip install -r requirements.txt
   ```

2. **Collect static files**
   ```bash
   mkdir -p static
   # Ensure index.html, style.css, script.js exist
   ```

3. **Start server (development)**
   ```bash
   python api.py
   ```

4. **Start server (production - with Gunicorn)**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

5. **Verify health**
   ```bash
   curl http://localhost:5000/health
   ```

### Production Considerations

- [ ] Use HTTPS (nginx + SSL)
- [ ] Set up logging
- [ ] Configure database (not JSON)
- [ ] Set up monitoring/alerts
- [ ] Regular backups of feedback data
- [ ] Load testing
- [ ] Security audit

---

## Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
# (On GitHub/GitLab)

# After review, merge to main
git checkout main
git merge feature/new-feature
```

### Version Numbering

**Format:** `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

**Current Version:** 1.0.0

---

## Maintenance Tasks

### Daily
- Monitor API health
- Check error logs
- Verify data storage status

### Weekly  
- Review feedback submissions
- Check system performance
- Backup feedback data

### Monthly
- Update dependencies
- Review and merge PRs
- Analyze user feedback patterns
- Update documentation

### Quarterly
- Performance benchmarking
- Security audit
- Model retraining
- Major feature planning

---

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Librosa Documentation](https://librosa.org/)
- [Scikit-Learn Documentation](https://scikit-learn.org/)

### Tools
- VS Code Python Extension
- Postman (API testing)
- Docker (containerization)
- GitHub (version control)

### Community
- Stack Overflow (for debugging)
- GitHub Issues (bug reports)
- ML communities (for research)

---

**Last Updated:** 2026-03-01  
**Maintainer:** Development Team  
**Contact:** [Your contact info]
