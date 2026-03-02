#!/usr/bin/env python3
"""
Deepfake Voice Detection - Model Training

Trains a GradientBoosting classifier on audio data.
Data structure:
- data/raw/real/ - genuine voice samples
- data/raw/fake/ - deepfake/synthetic voice samples

Usage:
    python train.py
"""

import os
import sys
import numpy as np
import logging
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import soundfile as sf
import librosa

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)




def extract_mfcc_stats(y, sr=22050, n_mfcc=40):
    """Extract MFCC and statistical features."""
    # Extract MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    # Statistics for MFCC
    mfcc_mean = mfcc.mean(axis=1)
    mfcc_std = mfcc.std(axis=1)
    mfcc_min = mfcc.min(axis=1)
    mfcc_max = mfcc.max(axis=1)
    
    # Zero-crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0].mean()
    
    # Energy
    energy = np.mean(y ** 2)
    
    # Concatenate all features
    features = np.concatenate([
        mfcc_mean, mfcc_std, mfcc_min, mfcc_max,
        [zcr], [energy]
    ])
    
    return features


class ModelTrainer:
    """Train deepfake detection model."""
    
    def __init__(self, data_dir='data/raw', model_output_path='models/deepfake_model.pkl'):
        """Initialize trainer."""
        self.data_dir = Path(data_dir)
        self.model_output_path = Path(model_output_path)
        self.model = None
        
        # Ensure output directory exists
        self.model_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load audio files and extract features."""
        logger.info("Loading audio data...")
        
        X = []
        y = []
        
        # Load real voice samples (label=0)
        real_dir = self.data_dir / 'real'
        if real_dir.exists():
            real_files = sorted(real_dir.glob('*.wav'))
            logger.info(f"Found {len(real_files)} real voice samples")
            
            for i, audio_file in enumerate(real_files, 1):
                try:
                    audio_data, sr = sf.read(str(audio_file))
                    
                    # If stereo, convert to mono
                    if len(audio_data.shape) > 1:
                        audio_data = np.mean(audio_data, axis=1)
                    
                    # Resample to 22050 Hz if needed
                    if sr != 22050:
                        audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=22050)
                    
                    # Extract features
                    features = extract_mfcc_stats(audio_data, sr=22050)
                    X.append(features)
                    y.append(0)  # Real voice
                    
                    if i % 5 == 0:
                        logger.info(f"  Processed {i}/{len(real_files)} real samples...")
                        
                except Exception as e:
                    logger.warning(f"Failed to process {audio_file}: {e}")
        
        # Load deepfake samples (label=1)
        fake_dir = self.data_dir / 'fake'
        if fake_dir.exists():
            fake_files = sorted(fake_dir.glob('*.wav'))
            logger.info(f"Found {len(fake_files)} deepfake samples")
            
            for i, audio_file in enumerate(fake_files, 1):
                try:
                    audio_data, sr = sf.read(str(audio_file))
                    
                    # If stereo, convert to mono
                    if len(audio_data.shape) > 1:
                        audio_data = np.mean(audio_data, axis=1)
                    
                    # Resample to 22050 Hz if needed
                    if sr != 22050:
                        audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=22050)
                    
                    # Extract features
                    features = extract_mfcc_stats(audio_data, sr=22050)
                    X.append(features)
                    y.append(1)  # Deepfake
                    
                    if i % 5 == 0:
                        logger.info(f"  Processed {i}/{len(fake_files)} fake samples...")
                        
                except Exception as e:
                    logger.warning(f"Failed to process {audio_file}: {e}")
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"✓ Loaded {len(X)} samples with {X.shape[1]} features each")
        logger.info(f"  Class distribution: Real={np.sum(y==0)}, Deepfake={np.sum(y==1)}")
        
        return X, y
    
    def train(self, X, y):
        """Train the model."""
        logger.info("Training GradientBoostingClassifier...")
        
        # Split data: 80% train, 20% test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Train set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        
        # Create and train model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=2,
            random_state=42,
            verbose=1
        )
        
        self.model.fit(X_train, y_train)
        
        logger.info("✓ Model training completed")
        
        # Evaluate on training set
        y_pred_train = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, y_pred_train)
        logger.info(f"Training Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
        
        # Evaluate on test set
        y_pred_test = self.model.predict(X_test)
        test_acc = accuracy_score(y_test, y_pred_test)
        logger.info(f"Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
        
        # Additional metrics
        precision = precision_score(y_test, y_pred_test, zero_division=0)
        recall = recall_score(y_test, y_pred_test, zero_division=0)
        f1 = f1_score(y_test, y_pred_test, zero_division=0)
        
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall: {recall:.4f}")
        logger.info(f"F1-Score: {f1:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred_test)
        logger.info(f"Confusion Matrix:\n{cm}")
        
        # Classification Report
        logger.info(f"\nDetailed Classification Report:\n{classification_report(y_test, y_pred_test, target_names=['Real', 'Deepfake'])}")
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'total_features': X.shape[1]
        }
    
    def save_model(self):
        """Save trained model to disk."""
        if self.model is None:
            logger.error("No model to save. Train the model first.")
            return False
        
        joblib.dump(self.model, self.model_output_path)
        size_mb = self.model_output_path.stat().st_size / (1024 * 1024)
        logger.info(f"✓ Model saved to: {self.model_output_path}")
        logger.info(f"  File size: {size_mb:.2f} MB")
        
        return True
    
    def run(self):
        """Run complete training pipeline."""
        logger.info("=" * 60)
        logger.info("DEEPFAKE VOICE DETECTION - MODEL TRAINING")
        logger.info("=" * 60)
        
        # Load data
        X, y = self.load_data()
        
        if len(X) == 0:
            logger.error("No audio data found. Check data/raw/ directory.")
            return False
        
        # Train model
        metrics = self.train(X, y)
        
        # Save model
        if not self.save_model():
            return False
        
        # Summary
        logger.info("=" * 60)
        logger.info("TRAINING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Samples: {len(X)}")
        logger.info(f"Features: {metrics['total_features']}")
        logger.info(f"Train/Test Split: {metrics['train_samples']}/{metrics['test_samples']}")
        logger.info(f"Test Accuracy: {metrics['test_accuracy']*100:.2f}%")
        logger.info(f"Model Status: READY FOR DEPLOYMENT")
        logger.info("=" * 60)
        
        return True


if __name__ == '__main__':
    trainer = ModelTrainer()
    success = trainer.run()
    sys.exit(0 if success else 1)
