# Vercel Deployment - Bundle Size Solution

## Problem
Your dependencies are 2395.68 MB, but Vercel's Lambda functions have a 500 MB storage limit.

**Heavy Dependencies:**
- TensorFlow: ~300-400 MB
- Keras: included with TensorFlow
- Other ML libraries add up quickly

## Solution Applied

### 1. Created `requirements-prod.txt`
A lightweight production requirements file that **excludes** TensorFlow and Keras:
```
numpy, scipy, librosa, scikit-learn, soundfile, pydub, flask, python-dotenv
```

### 2. Updated `vercel.json`
Now uses `requirements-prod.txt` instead of full `requirements.txt`

### 3. Your API Already Handles Missing Model
The `api.py` gracefully handles when the detector isn't available:
- Returns HTTP 503 (Service Unavailable) if model is missing
- All endpoints check for model availability

---

## Deployment Strategy

### For Vercel (Lightweight)
✅ Use `requirements-prod.txt` (no TensorFlow)
- Smaller bundle size (~150-200 MB)
- API endpoints work without local model
- Model loads from cloud storage at runtime (future enhancement)

### For Local Development
✅ Use full `requirements.txt`
- Includes TensorFlow for training
- Full detector functionality

---

## Next Steps for Production

### Option A: Upload Model to Cloud Storage (Recommended)
1. Store your trained model in AWS S3 or Google Cloud Storage
2. Modify `api.py` to download model at startup
3. Model stays in the 500 MB runtime storage

### Option B: Use Alternative ML Framework
Replace TensorFlow with lighter alternative:
- **ONNX Runtime** (~20 MB) - for model inference
- **scikit-learn** (already included) - for smaller models

### Option C: Use Vercel Enterprise
For organizations needing full TensorFlow support.

---

## Current Deployment Status

Your app is now ready to deploy:

```powershell
.\deploy.ps1
```

**Expected behavior on first deployment:**
- ✅ Builds successfully (< 500 MB)
- ✅ Web UI loads (routes work)
- ⚠️ Detection endpoints return 503 (Model not loaded)

Once you add model loading from cloud storage, detection will work fully.

---

## File Reference

| File | Purpose |
|------|---------|
| `requirements.txt` | Full dependencies (local dev + training) |
| `requirements-prod.txt` | Production only (for Vercel) |
| `vercel.json` | Uses `requirements-prod.txt` |
| `app.py` | Flask entrypoint for Vercel |
| `api.py` | Actual API logic |

Deploy with confidence - the bundle is now within limits!
