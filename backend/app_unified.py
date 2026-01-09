"""
Unified Flask Application - PyTestGenie
Combines Test Code Generation and Test Smell Detection
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

from config.settings import config
from routes.test_generation import test_gen_bp
from routes.smell_detection import smell_detect_bp


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup CORS - Allow all origins in development
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Set environment variables
    os.environ["PYNGUIN_DANGER_AWARE"] = app.config['PYNGUIN_DANGER_AWARE']
    
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(test_gen_bp, url_prefix='/api/test-generator')
    app.register_blueprint(smell_detect_bp, url_prefix='/api/smell-detector')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            "name": "PyTestGenie API",
            "version": "1.0.0",
            "services": {
                "test_generator": "/api/test-generator",
                "smell_detector": "/api/smell-detector"
            },
            "endpoints": {
                "test_generation": {
                    "pynguin": "POST /api/test-generator/generate-tests/pynguin",
                    "ai": "POST /api/test-generator/generate-tests/ai",
                    "stream": "GET /api/test-generator/generate-tests/stream/<task_id>"
                },
                "smell_detection": {
                    "analyze_file": "POST /api/smell-detector/analyze/file",
                    "analyze_code": "POST /api/smell-detector/analyze/code",
                    "analyze_directory": "POST /api/smell-detector/analyze/directory",
                    "analyze_github": "POST /api/smell-detector/analyze/github",
                    "get_report": "GET /api/smell-detector/report"
                }
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
