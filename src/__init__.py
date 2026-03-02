"""Deepfake Voice Detection Package"""

__version__ = "1.0.0"
__author__ = "Deepfake Detection Team"

from src.audio_processor import AudioProcessor
from src.feature_extractor import FeatureExtractor
from src.model_builder import ModelBuilder
from src.detector import DeepfakeDetector
from src import utils

__all__ = [
    'AudioProcessor',
    'FeatureExtractor',
    'ModelBuilder',
    'DeepfakeDetector',
    'utils'
]
