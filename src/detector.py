import numpy as np
import librosa
from typing import Dict, Optional, List
import logging
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Feature extraction constants (must match trainer)
SAMPLE_RATE = 16000
N_MFCC = 40


def extract_features_simple(audio_path: str) -> np.ndarray:
    """Extract features matching the training pipeline."""
    try:
        audio, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        
        # Extract MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
        
        # Extract additional features
        zcr = librosa.feature.zero_crossing_rate(audio)
        energy = np.sqrt(np.sum(audio**2))
        
        # Compute statistics
        features = []
        
        # MFCC statistics
        features.extend(np.mean(mfcc, axis=1).tolist())
        features.extend(np.std(mfcc, axis=1).tolist())
        features.extend(np.min(mfcc, axis=1).tolist())
        features.extend(np.max(mfcc, axis=1).tolist())
        
        # Zero-crossing rate (mean and std across frames)
        features.append(float(np.mean(zcr)))
        features.append(float(np.std(zcr)))
        
        # Energy
        features.append(float(energy))
        
        return np.array(features)
    
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
    
    def detect(self, audio_path: str, confidence_threshold: float = 0.75) -> Dict:
        """
        Detect deepfake voice in audio file.
        
        Args:
            audio_path: Path to audio file
            confidence_threshold: Confidence threshold for detection
            
        Returns:
            Dictionary with results:
                - is_deepfake: Boolean result
                - confidence: Confidence score
                - scores: Raw model output scores
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please train a model first.")
        
        try:
            # Extract features using simple method matching the trainer
            feature_vector = extract_features_simple(audio_path)
            X = np.expand_dims(feature_vector, axis=0)
            
            # Make prediction
            if hasattr(self.model, 'predict_proba'):
                # Use probability predictions if available
                scores = self.model.predict_proba(X)[0]
                prediction = self.model.predict(X)[0]
            else:
                # Fallback for models without predict_proba
                prediction = self.model.predict(X)[0]
                scores = np.array([1 - prediction, prediction]) if isinstance(prediction, (int, float)) else prediction
            
            # Determine if deepfake (class 1) or real (class 0)
            is_deepfake = prediction == 1
            confidence = scores[1] if len(scores) > 1 else scores[0]
            
            result = {
                'is_deepfake': bool(is_deepfake),
                'confidence': float(confidence),
                'scores': {
                    'real': float(scores[0]),
                    'deepfake': float(scores[1]) if len(scores) > 1 else float(scores[0])
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
