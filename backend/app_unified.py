"""
Unified Flask Application - PyTestGenie
Combines Test Code Generation and Test Smell Detection
"""

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os

from config.settings import config
from routes.test_generation import test_gen_bp
from routes.smell_detection import smell_detect_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.refactoring import refactoring_bp
from routes.projects import projects_bp


def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup CORS - allow all origins unconditionally (JWT token auth, no cookies)
    CORS(app, supports_credentials=False)

    # Bulletproof CORS: explicit after_request handler covers every route
    # including error responses and routes Flask-CORS might miss
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return response

    # Handle OPTIONS preflight for all routes explicitly
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            resp = make_response()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            resp.headers['Access-Control-Max-Age'] = '86400'
            return resp, 200
    
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
    app.register_blueprint(refactoring_bp, url_prefix='/api/refactoring')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    
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
                "admin": "/api/admin",
                "refactoring": "/api/refactoring",
                "projects": "/api/projects"
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})
    
    return app


# Module-level app instance for production WSGI servers (gunicorn)
app = create_app(os.getenv('FLASK_ENV', 'production'))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') != 'production'
    # use_reloader=False prevents Windows socket errors
    app.run(debug=debug, host='0.0.0.0', port=port, use_reloader=False)
