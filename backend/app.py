import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes.products import products_bp
from routes.customers import customers_bp
from routes.invoices import invoices_bp

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(customers_bp, url_prefix='/api')
    app.register_blueprint(invoices_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Home route
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Inventory Management API',
            'version': '1.0.0',
            'endpoints': {
                'products': '/api/products',
                'customers': '/api/customers',
                'invoices': '/api/invoices'
            }
        })
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
