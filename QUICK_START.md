# 🚀 Quick Start Guide

Get your deepfake detection system running in minutes!

## Prerequisites

- **Python 3.13+** installed
- **Windows, macOS, or Linux**
- Audio files (WAV, MP3, FLAC, OGG)

## Installation

### 1. Navigate to Project Directory
```bash
cd "f:\deepfake voice detection"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install Flask==3.1.3 Jinja2==3.1.4 librosa==0.11.0 soundfile==0.13.1 scikit-learn==1.8.0 numpy==2.4.2 pandas==3.0.1 joblib==1.4.3
```

## Running the System

### 1. Start the API Server
```bash
python api.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 2. Open Web Interface
Open your browser and go to:
```
http://localhost:5000
```

You'll see the web interface with:
- 📁 File upload area (drag & drop)
- 🎵 Single file detection
- 📦 Batch processing
- ✓ Result verification
- 📊 Statistics tracking

## Using the System

### Analyze a Single File

1. **Upload Audio**
   - Click "Choose File" or drag & drop
   - Supported: WAV, MP3, FLAC, OGG
   - Max size: ~50MB

2. **Wait for Analysis**
   - System extracts audio features
   - Model makes prediction
   - Results display in ~1-2 seconds

3. **Review Results**
   - Classification: "Real Voice" or "Deepfake"
   - Confidence: 0-100%
   - Score breakdown

4. **Verify Prediction** ✅❌
   - Click **✅ Correct** if AI got it right
   - Click **❌ Incorrect** if AI was wrong

5. **If Incorrect** 
   - Select actual label ("Real Voice" or "Deepfake")
   - Add optional comment (why it's wrong)
   - Click **Submit Feedback**

6. **Check Statistics**
   - See real-time accuracy metrics
   - Track total feedback count
   - Monitor correct vs incorrect predictions

### Batch Analysis

1. **Upload Multiple Files**
   - Click "Upload Files" (batch button)
   - Select multiple audio files
   - System processes all files

2. **View Summary**
   - Total files processed
   - Real vs Deepfake count
   - Overall statistics

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Detect Single File
```bash
curl -X POST -F "file=@voice.wav" http://localhost:5000/api/detect
```

### Get Statistics
```bash
curl http://localhost:5000/api/feedback/stats
```

### Submit Feedback
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_name":"voice.wav","predicted_label":"real","actual_label":"deepfake","confidence":0.95,"is_correct":false,"user_comment":"Clearly synthetic"}' \
  http://localhost:5000/api/feedback
```

## Project Structure

```
deepfake voice detection/
├── api.py                    # Flask web server
├── VERIFICATION_GUIDE.md     # Feedback system docs
├── QUICK_START.md            # This file
├── src/
│   ├── detector.py           # Audio analysis & detection
│   ├── audio_processor.py    # Audio loading & preprocessing
│   ├── feature_extractor.py  # MFCC & feature extraction
│   ├── model_builder.py      # Model architecture
│   └── feedback.py           # Feedback management ⭐
├── models/
│   └── deepfake_model.pkl    # Pre-trained model
├── templates/
│   └── index.html            # Web interface
├── static/
│   ├── style.css             # Styling
│   └── script.js             # Frontend logic
└── data/
    ├── feedback.json         # User feedback storage ⭐
    └── feedback_stats.json   # Statistics ⭐
```

## Key Features

✅ **Real-time Detection** - Instant results with confidence scores

✅ **User Verification** - Mark predictions correct or incorrect

✅ **Feedback Collection** - Submit corrections and comments

✅ **Statistics Tracking** - Monitor model accuracy over time

✅ **Data Persistence** - Feedback stored locally in JSON

✅ **Batch Processing** - Analyze multiple files at once

✅ **REST API** - Integrate with other systems

✅ **Modern Web UI** - Dark theme, responsive design

## Troubleshooting

### Issue: Port 5000 already in use
```bash
# Use a different port by editing api.py
# Change: app.run(debug=True, port=5000)
# To: app.run(debug=True, port=5001)
```

### Issue: Module not found error
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CORS errors when calling API
```bash
# API already has CORS enabled for all routes
# Check browser console for actual error
```

### Issue: Files not processing
```bash
# Verify audio format is supported (WAV, MP3, FLAC, OGG)
# Check file is not corrupted
# Try with a different audio file
```

## Next Steps

1. **📊 Analyze more files** - Build up feedback dataset
2. **📝 Review statistics** - Check model accuracy trends
3. **🔄 Improve model** - Use feedback to retrain (future feature)
4. **📤 Export data** - Get feedback data for analysis
5. **🚀 Deploy** - Move to production environment

## Important Files for Users

| File | Purpose | User Access |
|------|---------|------------|
| `data/feedback.json` | Stores all feedback submitted | View/Export |
| `data/feedback_stats.json` | Current accuracy statistics | View only |
| `models/deepfake_model.pkl` | Pre-trained AI model | Not editable |
| `templates/index.html` | Web interface | Not editable |

## Performance Tips

- 🚀 **Best results** with clear audio (no background noise)
- ⏱️ **Faster processing** with shorter audio files
- 📊 **Better accuracy** with 20+ verified feedback samples
- 💾 **File organization** - Keep feedback.json backed up

## Security Notes

- 🔒 All processing happens locally on your computer
- 🚫 No audio is sent to cloud or servers
- ✓ Feedback files are plain JSON (human-readable)
- 📋 No sensitive data is logged

## Getting Help

1. Check **VERIFICATION_GUIDE.md** for detailed feature docs
2. Review **API Endpoints** section above
3. Check browser console for error messages
4. Verify all dependencies are installed

## System Requirements

| Component | Requirement |
|-----------|------------|
| **CPU** | Dual-core or better |
| **RAM** | 4GB minimum, 8GB recommended |
| **Disk** | 1GB free space |
| **Python** | 3.13+ |
| **OS** | Windows 10+, macOS 10.13+, Linux |

## Tips for Best Results

### Audio Quality
- Clear, mono or stereo audio
- 16kHz sample rate or higher
- Minimal background noise
- Duration: 1-30 seconds optimal

### Feedback Submission
- Be honest about predictions
- Add comments for complex cases
- Mark clearly wrong predictions as incorrect
- Help build diverse training dataset

### System Accuracy
- More feedback = better statistics
- Varied samples = better model understanding
- Regular use = continuous improvement

---

**Ready to detect deepfakes?** Upload an audio file and get started! 🎵
