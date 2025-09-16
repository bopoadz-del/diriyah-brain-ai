"""
Main Flask application file for Diriyah Brain AI with RBAC
"""
import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from diriyah_brain_ai.config import BASE_DIR, STATIC_DIR, INDEX_HTML, UPLOAD_DIR
from diriyah_brain_ai.routers.ai import ai_router
from diriyah_brain_ai.routers.auth import auth_router
from diriyah_brain_ai.routers.documents import documents_router
from diriyah_brain_ai.routers.admin import admin_router
from diriyah_brain_ai.routers.analytics import analytics_router
from diriyah_brain_ai.routers.bim import bim_router

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'diriyah_brain_ai_secret_2024')

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(ai_router, url_prefix='/api')
app.register_blueprint(auth_router, url_prefix='/api/auth')
app.register_blueprint(documents_router, url_prefix='/api/documents')
app.register_blueprint(admin_router, url_prefix='/api/admin')
app.register_blueprint(analytics_router, url_prefix='/api/analytics')
app.register_blueprint(bim_router, url_prefix='/api/bim')

@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        return send_from_directory(STATIC_DIR, path)
    except FileNotFoundError:
        # If file not found, serve index.html for SPA routing
        return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Diriyah Brain AI',
        'version': '2.0.0',
        'features': ['RBAC', 'Multilingual', 'Role-aware AI']
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving index.html for SPA"""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )

