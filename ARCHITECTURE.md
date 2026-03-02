# Project Implementation Guide

## System Architecture

The Deepfake Voice Detection system is built with a modular architecture:

```
┌─────────────────────────────────────┐
│     Audio Input (WAV, MP3, etc)     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     AudioProcessor                   │
│  - Load & normalize audio            │
│  - Noise reduction                   │
│  - Silence removal                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     FeatureExtractor                 │
│  - MFCC extraction                   │
│  - Mel-spectrogram                   │
│  - Spectral features                 │
│  - Statistical features              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Feature Vector / Spectrogram     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Neural Network Model             │
│  - CNN / LSTM / Ensemble             │
│  - Classification layer              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Detection Result                 │
│  - is_deepfake (boolean)             │
│  - confidence (0-1)                  │
│  - scores (real vs fake)             │
└─────────────────────────────────────┘
```

## Core Components

### 1. AudioProcessor (audio_processor.py)
- **Purpose**: Handle audio file operations
- **Key Methods**:
  - `load_audio()`: Load with sample rate conversion
  - `normalize_audio()`: Normalize to [-1, 1]
  - `reduce_noise()`: Apply spectral gating
  - `remove_silence()`: Trim silent segments
  - `preprocess()`: Complete pipeline
  - `get_spectrogram()`: Generate STFT spectrogram

### 2. FeatureExtractor (feature_extractor.py)
- **Purpose**: Extract discriminative audio features
- **Key Methods**:
  - `extract_mfcc()`: 13 MFCC coefficients
  - `extract_mel_spectrogram()`: 128-bin Mel-scale spectrum
  - `extract_statistical_features()`: Mean, std, RMS, ZCR
  - `extract_spectral_features()`: Centroid, rolloff, bandwidth
  - `extract_chroma_features()`: 12-bin chroma representation
  - `get_feature_vector()`: Flatten all features

### 3. ModelBuilder (model_builder.py)
- **Purpose**: Define neural network architectures
- **Models**:
  - `build_cnn_model()`: 3-layer CNN for 2D spectrograms
  - `build_lstm_model()`: 3-layer LSTM for sequences
  - `build_ensemble_model()`: Combined architecture
  - `build_simple_model()`: 4-layer Dense network

### 4. DeepfakeDetector (detector.py)
- **Purpose**: Main detection interface
- **Key Methods**:
  - `detect()`: Single audio detection
  - `detect_batch()`: Multiple audio files
  - `build_and_train()`: Train new model
  - `save_model()`: Serialize model
  - `evaluate()`: Test set evaluation

### 5. API Server (api.py)
- **Purpose**: REST API for web services
- **Endpoints**:
  - `POST /detect`: Single file detection
  - `POST /detect-batch`: Batch processing
  - `GET /health`: Health check
  - `GET /info`: API information

## Data Flow

### Training Flow
```
Raw Audio Files (real + fake)
    ↓
Audio Processing (norm, noise reduction)
    ↓
Feature Extraction (MFCC, Mel-spec)
    ↓
Train/Val/Test Split (70/15/15)
    ↓
Model Training (50 epochs)
    ↓
Evaluation & Metrics
    ↓
Save Model (H5/PKL)
```

### Inference Flow
```
Input Audio File
    ↓
AudioProcessor.preprocess()
    ↓
FeatureExtractor.extract_all_features()
    ↓
Format Features (batch + channel dims)
    ↓
Model.predict()
    ↓
Apply Threshold (0.75)
    ↓
Return Result (is_deepfake, confidence)
```

## Feature Engineering

### Extracted Features

| Feature | Dimension | Purpose |
|---------|-----------|---------|
| MFCC | 13 | Vocal characteristics |
| Mel-spectrogram | 128×T | Time-frequency representation |
| Chroma | 12×T | Pitch distribution |
| Zero-crossing rate | 1 | Voice activity indicator |
| RMS Energy | 1 | Power level |
| Spectral centroid | 1 | Brightness of sound |
| Spectral rolloff | 1 | High-frequency content |
| Spectral bandwidth | 1 | Frequency spread |

## Model Architecture

### CNN Model (3 conv blocks)
```
Input (128, 129, 1)
  ↓
Conv2D(32) → BN → maxpool → dropout
  ↓
Conv2D(64) → BN → maxpool → dropout
  ↓
Conv2D(128) → BN → maxpool → dropout
  ↓
GlobalAvgPool → Dense(256) → Dense(128) → Dense(2)
```

### LSTM Model (3 LSTM layers)
```
Input (timesteps, features)
  ↓
LSTM(128, return_seq) → dropout
  ↓
LSTM(64, return_seq) → dropout
  ↓
LSTM(32) → dropout
  ↓
Dense(128) → Dense(64) → Dense(2)
```

## Configuration System

Edit `configs/config.yaml` to control:
- **Audio parameters**: Sample rate, FFT size, hop length
- **Feature parameters**: MFCC count, Mel bins
- **Model parameters**: Layer sizes, dropout rates
- **Training parameters**: Learning rate, batch size, epochs

## Deployment Options

### 1. Command Line
```bash
python main.py --audio test.wav --model models/cnn_model.h5
```

### 2. Python API
```python
from src.detector import DeepfakeDetector
detector = DeepfakeDetector(model_path='models/cnn_model.h5')
result = detector.detect('audio.wav')
```

### 3. REST API
```bash
python api.py  # Runs on http://localhost:5000
curl -F "file=@audio.wav" http://localhost:5000/detect
```

### 4. Docker
```bash
docker-compose up
# API available at http://localhost:5000
```

## Performance Optimization

### Inference Speed
- **Single file**: ~0.5-1 second
- **Batch processing**: 10+ files/minute
- **Model size**: ~50-100 MB

### Memory Usage
- **Model loading**: 500 MB RAM
- **Per-file processing**: 100-200 MB
- **Batch processing**: Linear with batch size

### GPU Acceleration
- Enable in config.yaml: `use_gpu: true`
- Requires CUDA 11.8+ and cuDNN 8.6+
- ~2-3x speedup for inference

## Quality Assurance

### Testing Coverage
- Unit tests for each module
- Integration tests for pipelines
- Performance benchmarks

### Evaluation Metrics
- **Accuracy**: Overall correctness
- **Precision**: True positive rate
- **Recall**: Detection rate
- **F1-Score**: Harmonic mean
- **AUC-ROC**: Threshold robustness

## Troubleshooting Guide

### Audio Loading Issues
- **Problem**: "Audio file not found"
- **Solution**: Verify absolute paths, check file permissions

### Memory Errors
- **Problem**: "Out of memory during batch processing"
- **Solution**: Reduce batch_size in config, process serially

### Model Loading Fails
- **Problem**: "Model file corrupt or incompatible"
- **Solution**: Reinstall TensorFlow, verify model format

### Poor Detection Accuracy
- **Problem**: "Detection confidence very low"
- **Solution**: Check training data quality, retrain with new data

## Future Enhancements

1. **Multi-language Support**: Extend to non-English voices
2. **Real-time Streaming**: Live call monitoring
3. **Transfer Learning**: Pre-trained models
4. **Explainability**: LIME/SHAP feature importance
5. **Edge Deployment**: TensorFlow Lite for mobile

## References

- LibROSA: https://librosa.org/doc/latest/index.html
- TensorFlow: https://www.tensorflow.org/api_docs
- Audio Signal Processing: https://en.wikipedia.org/wiki/Audio_signal_processing
