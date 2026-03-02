import numpy as np
import librosa
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureExtractor:
    """Extract audio features for deepfake detection."""
    
    def __init__(self, sample_rate: int = 16000, n_mfcc: int = 13, n_mels: int = 128):
        """
        Initialize FeatureExtractor.
        
        Args:
            sample_rate: Sample rate of audio
            n_mfcc: Number of MFCC coefficients
            n_mels: Number of Mel frequency bins
        """
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_mels = n_mels
    
    def extract_mfcc(self, y: np.ndarray) -> np.ndarray:
        """
        Extract MFCC (Mel-frequency cepstral coefficients).
        
        Args:
            y: Audio time series
            
        Returns:
            MFCC features (n_mfcc, n_frames)
        """
        mfcc = librosa.feature.mfcc(y=y, sr=self.sample_rate, n_mfcc=self.n_mfcc)
        logger.info(f"Extracted MFCC: {mfcc.shape}")
        return mfcc
    
    def extract_mel_spectrogram(self, y: np.ndarray) -> np.ndarray:
        """
        Extract Mel-spectrogram.
        
        Args:
            y: Audio time series
            
        Returns:
            Mel-spectrogram features (n_mels, n_frames)
        """
        mel_spec = librosa.feature.melspectrogram(y=y, sr=self.sample_rate, n_mels=self.n_mels)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        logger.info(f"Extracted Mel-spectrogram: {mel_spec_db.shape}")
        return mel_spec_db
    
    def extract_statistical_features(self, y: np.ndarray) -> Dict[str, float]:
        """
        Extract statistical features from raw audio.
        
        Args:
            y: Audio time series
            
        Returns:
            Dictionary of statistical features
        """
        features = {
            'mean': np.mean(np.abs(y)),
            'std': np.std(np.abs(y)),
            'min': np.min(np.abs(y)),
            'max': np.max(np.abs(y)),
            'median': np.median(np.abs(y)),
            'rms': np.sqrt(np.mean(y ** 2)),
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y))
        }
        logger.info(f"Extracted statistical features: {list(features.keys())}")
        return features
    
    def extract_spectral_features(self, y: np.ndarray) -> Dict[str, float]:
        """
        Extract spectral features.
        
        Args:
            y: Audio time series
            
        Returns:
            Dictionary of spectral features
        """
        D = librosa.stft(y)
        S = np.abs(D) ** 2
        
        features = {
            'spectral_centroid': np.mean(librosa.feature.spectral_centroid(S=S, sr=self.sample_rate)),
            'spectral_rolloff': np.mean(librosa.feature.spectral_rolloff(S=S, sr=self.sample_rate)),
            'spectral_bandwidth': np.mean(librosa.feature.spectral_bandwidth(S=S, sr=self.sample_rate)),
        }
        logger.info(f"Extracted spectral features: {list(features.keys())}")
        return features
    
    def extract_chroma_features(self, y: np.ndarray) -> np.ndarray:
        """
        Extract chroma features (useful for voice characteristics).
        
        Args:
            y: Audio time series
            
        Returns:
            Chroma features (12, n_frames)
        """
        chroma = librosa.feature.chroma_stft(y=y, sr=self.sample_rate)
        logger.info(f"Extracted chroma features: {chroma.shape}")
        return chroma
    
    def extract_all_features(self, y: np.ndarray) -> Dict:
        """
        Extract all available features.
        
        Args:
            y: Audio time series
            
        Returns:
            Dictionary containing all extracted features
        """
        all_features = {
            'mfcc': self.extract_mfcc(y),
            'mel_spectrogram': self.extract_mel_spectrogram(y),
            'chroma': self.extract_chroma_features(y),
            'statistical': self.extract_statistical_features(y),
            'spectral': self.extract_spectral_features(y),
        }
        logger.info("All features extracted successfully")
        return all_features
    
    def get_feature_vector(self, features: Dict) -> np.ndarray:
        """
        Convert extracted features to a flat feature vector.
        
        Args:
            features: Dictionary of features from extract_all_features()
            
        Returns:
            Flattened feature vector
        """
        vector = []
        
        # Flatten spectrogram-like features
        for key in ['mfcc', 'mel_spectrogram', 'chroma']:
            if key in features:
                vector.extend(features[key].flatten())
        
        # Add statistical features
        if 'statistical' in features:
            vector.extend(features['statistical'].values())
        
        # Add spectral features
        if 'spectral' in features:
            vector.extend(features['spectral'].values())
        
        feature_vector = np.array(vector)
        logger.info(f"Feature vector shape: {feature_vector.shape}")
        return feature_vector
