import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handle audio loading, preprocessing, and normalization."""
    
    def __init__(self, sample_rate: int = 16000, n_fft: int = 2048, 
                 hop_length: int = 512):
        """
        Initialize AudioProcessor.
        
        Args:
            sample_rate: Target sample rate for audio
            n_fft: FFT window size
            hop_length: Hop length for STFT
        """
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length
    
    def load_audio(self, file_path: str, duration: Optional[float] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file with specified sample rate.
        
        Args:
            file_path: Path to audio file
            duration: Duration in seconds to load
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            y, sr = librosa.load(file_path, sr=self.sample_rate, duration=duration)
            logger.info(f"Loaded audio from {file_path}: {len(y)} samples")
            return y, sr
        except Exception as e:
            logger.error(f"Error loading audio file {file_path}: {str(e)}")
            raise
    
    def normalize_audio(self, y: np.ndarray) -> np.ndarray:
        """
        Normalize audio to range [-1, 1].
        
        Args:
            y: Audio time series
            
        Returns:
            Normalized audio
        """
        max_val = np.max(np.abs(y))
        if max_val > 0:
            y = y / max_val
        return y
    
    def reduce_noise(self, y: np.ndarray, sr: int, stationary: bool = True) -> np.ndarray:
        """
        Apply noise reduction using spectral gating.
        
        Args:
            y: Audio time series
            sr: Sample rate
            stationary: Whether to use stationary noise reduction
            
        Returns:
            Noise-reduced audio
        """
        try:
            from noisereduce import reduce_noise
            reduced = reduce_noise(y=y, sr=sr, stationary=stationary)
            logger.info("Noise reduction applied")
            return reduced
        except ImportError:
            logger.warning("noisereduce not installed, skipping noise reduction")
            return y
    
    def remove_silence(self, y: np.ndarray, sr: int, top_db: float = 20) -> np.ndarray:
        """
        Remove silent segments from audio.
        
        Args:
            y: Audio time series
            sr: Sample rate
            top_db: Threshold in dB below reference
            
        Returns:
            Audio with silence removed
        """
        y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)
        logger.info(f"Trimmed silence: {len(y)} -> {len(y_trimmed)} samples")
        return y_trimmed
    
    def preprocess(self, file_path: str, normalize: bool = True, 
                   reduce_noise: bool = True, remove_silence: bool = True) -> np.ndarray:
        """
        Complete preprocessing pipeline.
        
        Args:
            file_path: Path to audio file
            normalize: Whether to normalize audio
            reduce_noise: Whether to apply noise reduction
            remove_silence: Whether to remove silence
            
        Returns:
            Preprocessed audio
        """
        y, sr = self.load_audio(file_path)
        
        if remove_silence:
            y = self.remove_silence(y, sr)
        
        if reduce_noise:
            y = self.reduce_noise(y, sr)
        
        if normalize:
            y = self.normalize_audio(y)
        
        logger.info("Preprocessing completed")
        return y
    
    def get_spectrogram(self, y: np.ndarray) -> np.ndarray:
        """
        Compute magnitude spectrogram.
        
        Args:
            y: Audio time series
            
        Returns:
            Magnitude spectrogram (dB scale)
        """
        D = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)
        S_db = librosa.power_to_db(np.abs(D) ** 2, ref=np.max)
        return S_db
    
    def save_audio(self, y: np.ndarray, file_path: str, sr: int) -> None:
        """
        Save audio to file.
        
        Args:
            y: Audio time series
            file_path: Output file path
            sr: Sample rate
        """
        sf.write(file_path, y, sr)
        logger.info(f"Audio saved to {file_path}")
