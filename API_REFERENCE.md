# 📡 API Reference

Complete documentation of all REST API endpoints for the deepfake detection system.

## Base URL
```
http://localhost:5000
```

## Authentication
✅ No authentication required (local system)

---

## Core Endpoints

### GET / - Root Endpoint
Serve the web interface.

**Request:**
```bash
GET /
```

**Response:**
```
200 OK - HTML page (web interface)
```

**Example:**
```bash
curl http://localhost:5000/
```

---

### GET /health - Health Check
Check if the API is running and model is loaded.

**Request:**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "api_version": "1.0"
}
```

**Status Codes:**
- `200 OK` - API is running, model loaded
- `503 Service Unavailable` - Model failed to load

**Example:**
```bash
curl http://localhost:5000/health
```

---

### GET /info - System Information
Get information about the detection system, supported formats, and model details.

**Request:**
```bash
GET /info
```

**Response:**
```json
{
  "system": "Deepfake Voice Detection",
  "version": "1.0",
  "model": {
    "name": "GradientBoostingClassifier",
    "classes": ["real", "deepfake"],
    "features": 163,
    "feature_extraction": "MFCC + Statistics"
  },
  "supported_formats": ["wav", "mp3", "flac", "ogg"],
  "sample_rate": 22050,
  "feature_details": {
    "mfcc_coefficients": 40,
    "statistics": ["mean", "std", "min", "max"],
    "zero_crossing_rate": true,
    "energy": true
  }
}
```

**Example:**
```bash
curl http://localhost:5000/info
```

---

## Detection Endpoints

### POST /api/detect - Analyze Single File
Analyze a single audio file for deepfake detection.

**Request:**
```bash
POST /api/detect
Content-Type: multipart/form-data

file=@path/to/audio.wav
```

**Response:**
```json
{
  "file_name": "audio.wav",
  "classification": "real",
  "confidence": 0.95,
  "scores": {
    "real": 0.95,
    "deepfake": 0.05
  },
  "processing_time": 1.23
}
```

| Field | Type | Description |
|-------|------|-------------|
| `file_name` | string | Name of uploaded file |
| `classification` | string | "real" or "deepfake" |
| `confidence` | float | 0.0-1.0 confidence score |
| `scores` | object | Probability for each class |
| `processing_time` | float | Time in seconds |

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - No file provided or invalid format
- `413 Payload Too Large` - File too large
- `500 Internal Server Error` - Processing error

**Examples:**

Using curl:
```bash
curl -X POST -F "file=@voice.wav" http://localhost:5000/api/detect
```

Using Python:
```python
import requests

with open('voice.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/detect', files=files)
    result = response.json()
    print(f"{result['classification']}: {result['confidence']*100:.1f}%")
```

Using JavaScript:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/detect', {
    method: 'POST',
    body: formData
})
.then(r => r.json())
.then(data => {
    console.log(`${data.classification}: ${(data.confidence*100).toFixed(1)}%`);
});
```

---

### POST /api/detect-batch - Analyze Multiple Files
Process multiple audio files in one request.

**Request:**
```bash
POST /api/detect-batch
Content-Type: multipart/form-data

files=@audio1.wav
files=@audio2.wav
files=@audio3.wav
```

**Response:**
```json
{
  "total_files": 3,
  "results": [
    {
      "file_name": "audio1.wav",
      "classification": "real",
      "confidence": 0.95,
      "scores": {
        "real": 0.95,
        "deepfake": 0.05
      }
    },
    {
      "file_name": "audio2.wav",
      "classification": "deepfake",
      "confidence": 0.92,
      "scores": {
        "real": 0.08,
        "deepfake": 0.92
      }
    },
    {
      "file_name": "audio3.wav",
      "classification": "real",
      "confidence": 0.87,
      "scores": {
        "real": 0.87,
        "deepfake": 0.13
      }
    }
  ],
  "summary": {
    "real_count": 2,
    "deepfake_count": 1,
    "total_processing_time": 3.45
  }
}
```

**Status Codes:**
- `200 OK` - All files processed
- `207 Multi-Status` - Some files failed (returns partial results)
- `400 Bad Request` - No files provided
- `500 Internal Server Error` - Processing error

**Examples:**

Using curl:
```bash
curl -X POST -F "files=@voice1.wav" -F "files=@voice2.wav" http://localhost:5000/api/detect-batch
```

Using Python:
```python
import requests

files = [
    ('files', open('voice1.wav', 'rb')),
    ('files', open('voice2.wav', 'rb')),
    ('files', open('voice3.wav', 'rb')),
]

response = requests.post('http://localhost:5000/api/detect-batch', files=files)
data = response.json()

for result in data['results']:
    print(f"{result['file_name']}: {result['classification']}")
```

---

## Feedback Endpoints

### POST /api/feedback - Submit Feedback
Record user verification of a prediction.

**Request:**
```bash
POST /api/feedback
Content-Type: application/json

{
  "file_name": "voice.wav",
  "predicted_label": "real",
  "actual_label": "deepfake",
  "confidence": 0.95,
  "is_correct": false,
  "user_comment": "This is clearly synthetic"
}
```

**Request Body Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file_name` | string | Yes | Name of analyzed file |
| `predicted_label` | string | Yes | What model predicted ("real" or "deepfake") |
| `actual_label` | string | Yes | What the actual label is ("real" or "deepfake") |
| `confidence` | float | Yes | Model confidence (0.0-1.0) |
| `is_correct` | boolean | Yes | Whether prediction was correct |
| `user_comment` | string | No | Optional feedback explanation |

**Response:**
```json
{
  "status": "success",
  "feedback": {
    "id": "2026-03-01T10:30:45.123456",
    "file_name": "voice.wav",
    "predicted_label": "real",
    "actual_label": "deepfake",
    "confidence": 0.95,
    "is_correct": false,
    "user_comment": "This is clearly synthetic",
    "timestamp": "2026-03-01T10:30:45.123456"
  }
}
```

**Status Codes:**
- `201 Created` - Feedback saved successfully
- `400 Bad Request` - Missing required fields
- `422 Unprocessable Entity` - Invalid field values
- `500 Internal Server Error` - Database error

**Examples:**

Using curl:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "file_name": "voice.wav",
    "predicted_label": "real",
    "actual_label": "deepfake",
    "confidence": 0.95,
    "is_correct": false,
    "user_comment": "Clearly synthetic"
  }' \
  http://localhost:5000/api/feedback
```

Using Python:
```python
import requests
import json

feedback = {
    "file_name": "voice.wav",
    "predicted_label": "real",
    "actual_label": "deepfake",
    "confidence": 0.95,
    "is_correct": False,
    "user_comment": "Clearly synthetic"
}

response = requests.post(
    'http://localhost:5000/api/feedback',
    json=feedback
)

if response.status_code == 201:
    print("Feedback saved successfully")
else:
    print(f"Error: {response.status_code}")
```

---

### GET /api/feedback - Get Feedback History
Retrieve previously submitted feedback entries.

**Request:**
```bash
GET /api/feedback?limit=50&offset=0
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 100 | Max number of entries to return |
| `offset` | integer | 0 | Skip first N entries (pagination) |

**Response:**
```json
{
  "total": 42,
  "limit": 50,
  "offset": 0,
  "feedback": [
    {
      "id": "2026-03-01T10:30:45.123456",
      "file_name": "voice1.wav",
      "predicted_label": "real",
      "actual_label": "deepfake",
      "confidence": 0.95,
      "is_correct": false,
      "user_comment": "Clearly synthetic",
      "timestamp": "2026-03-01T10:30:45.123456"
    },
    {
      "id": "2026-03-01T10:35:20.654321",
      "file_name": "voice2.wav",
      "predicted_label": "deepfake",
      "actual_label": "deepfake",
      "confidence": 0.92,
      "is_correct": true,
      "user_comment": "",
      "timestamp": "2026-03-01T10:35:20.654321"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Feedback retrieved successfully
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Database error

**Examples:**

Using curl:
```bash
# Get last 50 entries
curl "http://localhost:5000/api/feedback?limit=50"

# Get entries 100-150
curl "http://localhost:5000/api/feedback?limit=50&offset=100"
```

Using Python:
```python
import requests

response = requests.get('http://localhost:5000/api/feedback?limit=50')
data = response.json()

for entry in data['feedback']:
    print(f"{entry['file_name']}: {entry['is_correct']}")

print(f"Total feedback: {data['total']}")
```

---

### GET /api/feedback/stats - Get Statistics
Retrieve aggregated feedback statistics and model accuracy metrics.

**Request:**
```bash
GET /api/feedback/stats
```

**Response:**
```json
{
  "total_feedback": 42,
  "correct_predictions": 38,
  "incorrect_predictions": 4,
  "accuracy": 90.48,
  "last_updated": "2026-03-01T10:35:20.123456"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total_feedback` | integer | Total feedback entries received |
| `correct_predictions` | integer | Count where is_correct=true |
| `incorrect_predictions` | integer | Count where is_correct=false |
| `accuracy` | float | Percentage of correct predictions (0-100) |
| `last_updated` | string | ISO timestamp of last stats update |

**Status Codes:**
- `200 OK` - Statistics retrieved successfully
- `500 Internal Server Error` - Database error

**Examples:**

Using curl:
```bash
curl http://localhost:5000/api/feedback/stats
```

Using Python:
```python
import requests

response = requests.get('http://localhost:5000/api/feedback/stats')
stats = response.json()

print(f"Model Accuracy: {stats['accuracy']:.1f}%")
print(f"Total Verified: {stats['total_feedback']}")
print(f"Correct: {stats['correct_predictions']}")
print(f"Incorrect: {stats['incorrect_predictions']}")
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": "Error description",
  "details": "Additional details (optional)"
}
```

### Common Errors

**400 Bad Request**
```json
{
  "error": "No file provided"
}
```

**413 Payload Too Large**
```json
{
  "error": "File too large. Maximum size is 50MB"
}
```

**415 Unsupported Media Type**
```json
{
  "error": "Unsupported audio format. Supported: wav, mp3, flac, ogg"
}
```

**422 Unprocessable Entity**
```json
{
  "error": "Invalid request body",
  "details": "Field 'confidence' must be between 0 and 1"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "details": "Failed to process audio file"
}
```

---

## Rate Limiting

✅ No rate limiting (local API)
- Process unlimited files
- Submit unlimited feedback
- Query stats freely

---

## Response Headers

All responses include:
```
Content-Type: application/json
Access-Control-Allow-Origin: *
```

---

## Complete Workflow Example

### 1. Analyze a file
```bash
curl -X POST -F "file=@voice.wav" http://localhost:5000/api/detect
# Returns: {"classification": "real", "confidence": 0.95, ...}
```

### 2. Review prediction and submit feedback
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "file_name": "voice.wav",
    "predicted_label": "real",
    "actual_label": "deepfake",
    "confidence": 0.95,
    "is_correct": false,
    "user_comment": "Model was wrong"
  }' \
  http://localhost:5000/api/feedback
# Returns: {"status": "success", "feedback": {...}}
```

### 3. Check updated statistics
```bash
curl http://localhost:5000/api/feedback/stats
# Returns: {"total_feedback": 1, "accuracy": 0.0, ...}
```

### 4. Analyze more files
```bash
curl -X POST -F "files=@voice1.wav" -F "files=@voice2.wav" \
  http://localhost:5000/api/detect-batch
# Returns: {"total_files": 2, "results": [...]}
```

---

## Client Library Recommendations

### Python
```bash
pip install requests
```

### JavaScript
```bash
# Using fetch (built-in)
fetch('/api/detect', {method: 'POST', body: formData})
```

### cURL
```bash
curl -X POST -F "file=@audio.wav" http://localhost:5000/api/detect
```

---

## Versioning

Current Version: **1.0**

No breaking changes planned. All future updates will maintain backward compatibility.

---

## Support & Debugging

### Enable Debug Mode
Edit `api.py`:
```python
app.run(debug=True, port=5000)
```

### Check Logs
Look for output in terminal where `python api.py` is running

### Verify API Health
```bash
curl http://localhost:5000/health
```

### Test Specific Endpoint
```bash
curl -v http://localhost:5000/api/feedback/stats
```

---

Last Updated: 2026-03-01
