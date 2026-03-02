import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelBuilder:
    """Build machine learning models for deepfake detection using scikit-learn."""
    
    @staticmethod
    def build_random_forest(n_estimators: int = 100, random_state: int = 42):
        """Build Random Forest classifier."""
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            verbose=1
        )
        logger.info(f"Random Forest model built with {n_estimators} estimators")
        return model
    
    @staticmethod
    def build_gradient_boosting(n_estimators: int = 100, learning_rate: float = 0.1):
        """Build Gradient Boosting classifier."""
        model = GradientBoostingClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42,
            verbose=1
        )
        logger.info(f"Gradient Boosting model built with {n_estimators} estimators")
        return model
    
    @staticmethod
    def build_mlp(hidden_layer_sizes: tuple = (256, 128, 64), 
                   learning_rate: float = 0.001, max_iter: int = 500):
        """Build Multi-Layer Perceptron classifier."""
        model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            learning_rate_init=learning_rate,
            max_iter=max_iter,
            random_state=42,
            verbose=1,
            early_stopping=True,
            validation_fraction=0.2
        )
        logger.info(f"MLP model built with hidden layers {hidden_layer_sizes}")
        return model
    
    @staticmethod
    def build_cnn_model(input_shape: tuple, num_classes: int = 2):
        """Deprecated: Use build_random_forest, build_gradient_boosting, or build_mlp instead."""
        logger.warning("CNN model not available. Using Random Forest instead.")
        return ModelBuilder.build_random_forest()
    
    @staticmethod
    def build_lstm_model(input_shape: tuple, num_classes: int = 2):
        """Deprecated: Use build_random_forest, build_gradient_boosting, or build_mlp instead."""
        logger.warning("LSTM model not available. Using Gradient Boosting instead.")
        return ModelBuilder.build_gradient_boosting()
    
    @staticmethod
    def build_ensemble_model(input_shape: tuple, num_classes: int = 2):
        """Deprecated: Use build_random_forest, build_gradient_boosting, or build_mlp instead."""
        logger.warning("Ensemble model not available. Using MLP instead.")
        return ModelBuilder.build_mlp()
    
    @staticmethod
    def build_simple_model(input_shape: int, num_classes: int = 2):
        """Build simple MLP model for feature vectors."""
        return ModelBuilder.build_mlp(hidden_layer_sizes=(512, 256, 128, 64))
