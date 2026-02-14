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
from routes.auth import auth_bp
from routes.admin import admin_bp


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
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
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
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            "name": "PyTestGenie API",
            "version": "1.0.0",
            "services": {
                "test_generator": "/api/test-generator",
                "smell_detector": "/api/smell-detector",
                "authentication": "/api/auth",
                "admin": "/api/admin"
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    # use_reloader=False prevents Windows socket errors
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
