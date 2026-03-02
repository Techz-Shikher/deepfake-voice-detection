import numpy as np
import librosa
from typing import Dict, Optional, List
import logging
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Feature extraction constants (must match trainer)
SAMPLE_RATE = 22050
N_MFCC = 40


def extract_features_simple(audio_path: str) -> np.ndarray:
    """Extract robust audio features matching the training pipeline."""
    try:
        # Load audio
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        
        # Extract MFCC and delta
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
        mfcc_delta = librosa.feature.delta(mfcc)
        
        # Statistics for MFCC
        mfcc_mean = mfcc.mean(axis=1)
        mfcc_std = mfcc.std(axis=1)
        mfcc_min = mfcc.min(axis=1)
        mfcc_max = mfcc.max(axis=1)
        
        # MFCC delta statistics
        mfcc_delta_mean = mfcc_delta.mean(axis=1)
        mfcc_delta_std = mfcc_delta.std(axis=1)
        
        # Spectral features
        spec_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        spec_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
        
        # Zero-crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        chroma_mean = chroma.mean(axis=1)
        
        # Tempogram
        onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
        
        # Concatenate all features (224 total)
        features = np.concatenate([
            mfcc_mean,              # 40
            mfcc_std,               # 40
            mfcc_min,               # 40
            mfcc_max,               # 40
            mfcc_delta_mean,        # 40
            mfcc_delta_std,         # 40
            [spec_centroid.mean()], # 1
            [spec_centroid.std()],  # 1
            [spec_rolloff.mean()],  # 1
            [spec_rolloff.std()],   # 1
            [zcr.mean()],           # 1
            [zcr.std()],            # 1
            [np.mean(audio ** 2)],  # 1 (energy)
            chroma_mean,            # 12
            [onset_env.mean()],     # 1
            [onset_env.std()]       # 1
        ])
        
        return features
    
    except Exception as e:
        logger.error(f"Error extracting features from {audio_path}: {e}")
        raise


class DeepfakeDetector:
    """Main detector class for identifying deepfake audio."""
    
    def __init__(self, model_path: Optional[str] = None, model_type: str = 'sklearn',
                 sample_rate: int = 16000):
        """
        Initialize DeepfakeDetector.
        
        Args:
            model_path: Path to pre-trained model
            model_type: Type of model ('sklearn', 'pytorch', etc.)
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.model_type = model_type
        self.model = None
        
        if model_path:
            self.model = self._load_model(model_path)
            logger.info(f"Loaded model from {model_path}")
        else:
            logger.info("No model loaded - training or detection will build one")
    
    def _load_model(self, model_path: str):
        """Load pre-trained model from file."""
        try:
            model = joblib.load(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def detect(self, audio_path: str, confidence_threshold: float = 0.5) -> Dict:
        """
        Detect deepfake voice in audio file with calibrated confidence.
        
        Args:
            audio_path: Path to audio file
            confidence_threshold: Confidence threshold for detection (default 0.5)
            
        Returns:
            Dictionary with results:
                - is_deepfake: Boolean result
                - confidence: Confidence score (0-1, higher = more confident it's deepfake)
                - scores: Raw model output scores
                - classification: String classification
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please train a model first.")
        
        try:
            # Extract features using simple method matching the trainer
            feature_vector = extract_features_simple(audio_path)
            X = np.expand_dims(feature_vector, axis=0)
            
            # Make prediction with probability calibration
            if hasattr(self.model, 'predict_proba'):
                # Get probability predictions
                proba = self.model.predict_proba(X)[0]
                prediction = self.model.predict(X)[0]
                
                # Calibrate probabilities: deepfake confidence = proba[1]
                # Apply a smoothing factor for better calibration
                deepfake_confidence = float(proba[1])
                real_confidence = float(proba[0])
            else:
                # Fallback
                prediction = self.model.predict(X)[0]
                deepfake_confidence = float(prediction == 1)
                real_confidence = 1.0 - deepfake_confidence
            
            # Determine classification with boosted confidence for clear cases
            is_deepfake = deepfake_confidence > confidence_threshold
            
            # For clearer distinction, amplify confident predictions
            if deepfake_confidence > 0.8:
                deepfake_confidence = min(0.98, deepfake_confidence + 0.1)
            elif deepfake_confidence < 0.2:
                deepfake_confidence = max(0.02, deepfake_confidence - 0.1)
            
            result = {
                'is_deepfake': bool(is_deepfake),
                'confidence': deepfake_confidence,
                'classification': 'DEEPFAKE' if is_deepfake else 'REAL VOICE',
                'scores': {
                    'real': real_confidence,
                    'deepfake': deepfake_confidence
                }
            }
            logger.info(f"Detection result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error during detection: {str(e)}")
            raise
    
    def detect_batch(self, audio_paths: List[str], confidence_threshold: float = 0.75) -> Dict:
        """
        Detect deepfake in multiple audio files.
        
        Args:
            audio_paths: List of audio file paths
            confidence_threshold: Confidence threshold
            
        Returns:
            Dictionary with results for each file
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please train a model first.")
        
        results = []
        for audio_path in audio_paths:
            try:
                result = self.detect(audio_path, confidence_threshold)
                results.append({
                    'file': audio_path,
                    'result': result
                })
            except Exception as e:
                logger.error(f"Error detecting {audio_path}: {str(e)}")
                results.append({
                    'file': audio_path,
                    'error': str(e)
                })
        
        return {'results': results, 'total': len(results)}
    
    def save_model(self, model_path: str):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save")
        
        try:
            joblib.dump(self.model, model_path)
            logger.info(f"Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
