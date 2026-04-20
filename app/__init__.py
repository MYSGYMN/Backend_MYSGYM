import logging
import os
from flask import Flask
from flask_cors import CORS
from config import config
from app.models import db

def create_app(config_name=None):
    """Factory pattern para crear la app Flask."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    from app.routes import usuarios_bp, empleados_bp, actividades_bp
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(empleados_bp)
    app.register_blueprint(actividades_bp)
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'Backend MYSGYM está operativo'}, 200
    
    # Context para crear tablas
    with app.app_context():
        db.create_all()
    
    return app

def setup_logging(app):
    """Configurar logging de la aplicación."""
    handler = logging.StreamHandler()
    handler.setLevel(app.config.get('LOG_LEVEL', 'INFO'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config.get('LOG_LEVEL', 'INFO'))
