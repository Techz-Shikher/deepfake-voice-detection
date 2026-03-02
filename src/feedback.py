import json
import os
from datetime import datetime
from typing import Dict, List

FEEDBACK_FILE = 'data/feedback.json'
FEEDBACK_STATS_FILE = 'data/feedback_stats.json'

class FeedbackManager:
    """Manage user feedback for model verification and improvement."""
    
    @staticmethod
    def ensure_files_exist():
        """Create feedback files if they don't exist."""
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(FEEDBACK_STATS_FILE):
            with open(FEEDBACK_STATS_FILE, 'w') as f:
                json.dump({
                    'total_feedback': 0,
                    'correct_predictions': 0,
                    'incorrect_predictions': 0,
                    'accuracy': 0.0,
                    'last_updated': None
                }, f)
    
    @staticmethod
    def save_feedback(file_name: str, predicted_label: str, actual_label: str, 
                     confidence: float, is_correct: bool, user_comment: str = '') -> Dict:
        """Save user feedback about a prediction."""
        FeedbackManager.ensure_files_exist()
        
        feedback_entry = {
            'id': datetime.now().isoformat(),
            'file_name': file_name,
            'predicted_label': predicted_label,
            'actual_label': actual_label,
            'confidence': confidence,
            'is_correct': is_correct,
            'user_comment': user_comment,
            'timestamp': datetime.now().isoformat()
        }
        
        # Read existing feedback
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
        
        # Add new feedback
        feedback_data.append(feedback_entry)
        
        # Write back
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        
        # Update statistics
        FeedbackManager.update_stats()
        
        return feedback_entry
    
    @staticmethod
    def update_stats() -> Dict:
        """Update feedback statistics."""
        FeedbackManager.ensure_files_exist()
        
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
        
        total = len(feedback_data)
        correct = sum(1 for f in feedback_data if f['is_correct'])
        incorrect = total - correct
        accuracy = (correct / total * 100) if total > 0 else 0.0
        
        stats = {
            'total_feedback': total,
            'correct_predictions': correct,
            'incorrect_predictions': incorrect,
            'accuracy': round(accuracy, 2),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(FEEDBACK_STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    @staticmethod
    def get_stats() -> Dict:
        """Get feedback statistics."""
        FeedbackManager.ensure_files_exist()
        
        try:
            with open(FEEDBACK_STATS_FILE, 'r') as f:
                return json.load(f)
        except:
            return FeedbackManager.update_stats()
    
    @staticmethod
    def get_feedback(limit: int = None) -> List[Dict]:
        """Get all feedback entries."""
        FeedbackManager.ensure_files_exist()
        
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
        
        if limit:
            return feedback_data[-limit:]
        return feedback_data
    
    @staticmethod
    def get_feedback_for_retraining() -> Dict:
        """Get feedback in format suitable for retraining."""
        feedback_data = FeedbackManager.get_feedback()
        
        real_samples = []
        fake_samples = []
        
        for entry in feedback_data:
            file_info = {
                'file': entry['file_name'],
                'predicted': entry['predicted_label'],
                'actual': entry['actual_label'],
                'is_correct': entry['is_correct'],
                'confidence': entry['confidence']
            }
            
            if entry['actual_label'] == 'real':
                real_samples.append(file_info)
            else:
                fake_samples.append(file_info)
        
        return {
            'real': real_samples,
            'fake': fake_samples,
            'total': len(feedback_data),
            'misclassified': [f for f in feedback_data if not f['is_correct']]
        }
    
    @staticmethod
    def clear_feedback():
        """Clear all feedback data (for testing)."""
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump([], f)
        
        with open(FEEDBACK_STATS_FILE, 'w') as f:
            json.dump({
                'total_feedback': 0,
                'correct_predictions': 0,
                'incorrect_predictions': 0,
                'accuracy': 0.0,
                'last_updated': None
            }, f)
