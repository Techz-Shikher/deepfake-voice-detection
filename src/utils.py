import numpy as np
import os
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_audio_files(directory: str, extensions: List[str] = ['.wav', '.mp3', '.flac']) -> List[str]:
    """
    Recursively find audio files in directory.
    
    Args:
        directory: Root directory to search
        extensions: List of audio file extensions to look for
        
    Returns:
        List of audio file paths
    """
    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                audio_files.append(os.path.join(root, file))
    
    logger.info(f"Found {len(audio_files)} audio files in {directory}")
    return audio_files


def create_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    logger.info(f"Directory ensured: {path}")


def print_model_summary(model) -> None:
    """Print detailed model architecture."""
    print("\n" + "="*80)
    print("MODEL ARCHITECTURE")
    print("="*80)
    model.summary()
    print("="*80 + "\n")


def normalize_predictions(predictions: np.ndarray) -> np.ndarray:
    """Ensure predictions are in valid range [0, 1]."""
    predictions = np.clip(predictions, 0, 1)
    return predictions


def get_metrics_from_predictions(y_true: np.ndarray, y_pred: np.ndarray,
                                  threshold: float = 0.5) -> dict:
    """
    Calculate classification metrics.
    
    Args:
        y_true: True labels (binary)
        y_pred: Predicted probabilities
        threshold: Classification threshold
        
    Returns:
        Dictionary of metrics
    """
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    
    y_pred_binary = (y_pred >= threshold).astype(int)
    
    metrics = {
        'accuracy': float(accuracy_score(y_true, y_pred_binary)),
        'precision': float(precision_score(y_true, y_pred_binary, zero_division=0)),
        'recall': float(recall_score(y_true, y_pred_binary, zero_division=0)),
        'f1': float(f1_score(y_true, y_pred_binary, zero_division=0))
    }
    
    return metrics


def augment_audio_batch(audio_batch: np.ndarray, factor: float = 1.2) -> np.ndarray:
    """
    Simple audio augmentation by adding noise.
    
    Args:
        audio_batch: Batch of audio samples
        factor: Noise intensity factor
        
    Returns:
        Augmented audio batch
    """
    noise = np.random.normal(0, 0.001 * factor, audio_batch.shape)
    augmented = audio_batch + noise
    return np.clip(augmented, -1, 1)


def split_data(X: np.ndarray, y: np.ndarray, train_ratio: float = 0.7,
               val_ratio: float = 0.15, seed: int = 42) -> Tuple:
    """
    Split data into train, validation, and test sets.
    
    Args:
        X: Features
        y: Labels
        train_ratio: Training set ratio
        val_ratio: Validation set ratio
        seed: Random seed
        
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    np.random.seed(seed)
    indices = np.random.permutation(len(X))
    
    train_idx = int(len(X) * train_ratio)
    val_idx = int(len(X) * (train_ratio + val_ratio))
    
    X_train, y_train = X[indices[:train_idx]], y[indices[:train_idx]]
    X_val, y_val = X[indices[train_idx:val_idx]], y[indices[train_idx:val_idx]]
    X_test, y_test = X[indices[val_idx:]], y[indices[val_idx:]]
    
    logger.info(f"Data split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test
