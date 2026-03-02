"""
REST API for Deepfake Voice Detection
Provides endpoints for detecting deepfake voice in audio files
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tempfile
from werkzeug.utils import secure_filename
import logging
from src.feedback import FeedbackManager

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg'}
MODEL_PATH = 'models/deepfake_model.pkl'  # Update with your model path

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app with template and static folders
app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static',
            static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize detector (defer to avoid TensorFlow import issues)
detector = None

def init_detector():
    """Initialize detector lazily."""
    global detector
    if detector is None:
        try:
            from src.detector import DeepfakeDetector
            if os.path.exists(MODEL_PATH):
                detector = DeepfakeDetector(model_path=MODEL_PATH, model_type='sklearn')
                logger.info(f"Detector initialized with model from {MODEL_PATH}")
            else:
                detector = DeepfakeDetector(model_type='sklearn')
                logger.info("Detector initialized without pre-trained model")
        except Exception as e:
            logger.warning(f"Could not initialize detector: {e}")
            detector = None
    return detector


def allowed_file(filename: str) -> bool:
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def frontend():
    """Serve the frontend web interface."""
    try:
        return render_template('index.html'), 200
    except Exception as e:
        logger.error(f"Error serving frontend: {e}")
        return jsonify({
            'name': 'Deepfake Voice Detection API',
            'version': '1.0.0',
            'status': 'running',
            'api_info': 'Use /health for server status, /info for API documentation'
        }), 200


@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Deepfake Voice Detection API',
        'version': '1.0.0',
        'status': 'running',
        'documentation': 'Visit /info for API documentation',
        'health': 'Visit /health for server status'
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    det = init_detector()
    return jsonify({
        'status': 'healthy',
        'model_loaded': det is not None and det.model is not None,
        'version': '1.0.0'
    }), 200


@app.route('/detect', methods=['POST'])
def detect_deepfake():
    """
    Detect deepfake in uploaded audio file.
    
    Request:
        - file: Audio file (required)
        - threshold: Detection threshold (optional, default 0.75)
    
    Response:
        - is_deepfake: Boolean result
        - confidence: Confidence score
        - scores: Raw scores
    """
    det = init_detector()
    if det is None or det.model is None:
        return jsonify({'error': 'Model not loaded. Please train a model first.'}), 503
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    # Get threshold from request (optional)
    threshold = request.form.get('threshold', 0.75, type=float)
    if not 0 <= threshold <= 1:
        return jsonify({'error': 'Threshold must be between 0 and 1'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect deepfake
        result = det.detect(filepath, confidence_threshold=threshold)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'file': filename,
            'is_deepfake': result['is_deepfake'],
            'confidence': result['confidence'],
            'scores': result['scores']
        }), 200
    
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        return jsonify({'error': f'Detection failed: {str(e)}'}), 500


@app.route('/detect-batch', methods=['POST'])
def detect_batch():
    """
    Detect deepfake in multiple uploaded audio files.
    
    Request:
        - files: Multiple audio files (required)
        - threshold: Detection threshold (optional, default 0.75)
    
    Response:
        - results: List of detection results
        - summary: Summary statistics
    """
    det = init_detector()
    if det is None or det.model is None:
        return jsonify({'error': 'Model not loaded. Please train a model first.'}), 503
    
    # Check if files are in request
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400
    
    threshold = request.form.get('threshold', 0.75, type=float)
    if not 0 <= threshold <= 1:
        return jsonify({'error': 'Threshold must be between 0 and 1'}), 400
    
    results = []
    deepfake_count = 0
    
    try:
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                continue
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                result = det.detect(filepath, confidence_threshold=threshold)
                results.append({
                    'file': filename,
                    'result': result
                })
                
                if result['is_deepfake']:
                    deepfake_count += 1
            
            except Exception as e:
                results.append({
                    'file': filename,
                    'error': str(e)
                })
            
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        return jsonify({
            'results': results,
            'summary': {
                'total_files': len(results),
                'deepfake_detected': deepfake_count,
                'threshold': threshold
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Batch detection error: {str(e)}")
        return jsonify({'error': f'Batch detection failed: {str(e)}'}), 500


@app.route('/info', methods=['GET'])
def get_info():
    """Get API information."""
    return jsonify({
        'name': 'Deepfake Voice Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'GET - Health check',
            '/detect': 'POST - Detect single file',
            '/detect-batch': 'POST - Detect multiple files',
            '/info': 'GET - API information'
        },
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': 50
    }), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large (max 50MB)'}), 413


# =====================
# FEEDBACK ENDPOINTS
# =====================
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit user feedback about prediction accuracy.
    
    Request body:
        - file_name: Name of analyzed file
        - predicted_label: Model's prediction (real/deepfake)
        - actual_label: User's assessment (real/deepfake)
        - confidence: Model's confidence score
        - is_correct: Whether prediction was correct
        - user_comment: Optional user comment
    
    Response:
        - feedback entry with timestamp
    """
    try:
        data = request.get_json()
        
        feedback = FeedbackManager.save_feedback(
            file_name=data.get('file_name'),
            predicted_label=data.get('predicted_label'),
            actual_label=data.get('actual_label'),
            confidence=data.get('confidence'),
            is_correct=data.get('is_correct'),
            user_comment=data.get('user_comment', '')
        )
        
        logger.info(f"Feedback saved for {data.get('file_name')}")
        return jsonify({
            'status': 'success',
            'feedback': feedback
        }), 201
        
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        return jsonify({'error': f'Failed to save feedback: {str(e)}'}), 500


@app.route('/api/feedback/stats', methods=['GET'])
def get_feedback_stats():
    """
    Get feedback statistics for model verification.
    
    Response:
        - total_feedback: Total feedback entries
        - correct_predictions: Number of correct predictions
        - incorrect_predictions: Number of incorrect predictions
        - accuracy: Overall accuracy percentage
        - last_updated: Last update timestamp
    """
    try:
        stats = FeedbackManager.get_stats()
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Failed to get stats'}), 500


@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """
    Get all feedback entries (limited to last 100 for performance).
    
    Query parameters:
        - limit: Number of entries to return (default: 100)
    
    Response:
        - List of feedback entries
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        feedback_data = FeedbackManager.get_feedback(limit=limit)
        
        return jsonify({
            'total': len(feedback_data),
            'feedback': feedback_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving feedback: {str(e)}")
        return jsonify({'error': 'Failed to retrieve feedback'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle not found error."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    logger.info("Starting Deepfake Voice Detection API...")
    logger.info(f"Debug mode: {debug_mode}, Port: {port}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
