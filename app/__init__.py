from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from . import models

    # Registro de Blueprints
    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.gym import gym_bp
    from app.routes.reservas import reservas_bp
    from app.routes.pagos import pagos_bp
    from app.routes.mantenimiento import mantenimiento_bp
    from app.routes.empleados import empleados_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(gym_bp, url_prefix='/gym')
    app.register_blueprint(reservas_bp, url_prefix='/reservas')
    app.register_blueprint(pagos_bp, url_prefix='/pagos')
    app.register_blueprint(mantenimiento_bp, url_prefix='/mantenimiento')
    app.register_blueprint(empleados_bp, url_prefix='/empleados')

    @app.route('/')
    def index():
        return {
            "status": "success",
            "message": "Bienvenido a la API de MYSGYM",
            "endpoints": {
                "auth": "/auth/register, /auth/login",
                "usuarios": "/usuarios (JWT)",
                "empleados": "/empleados (JWT)",
                "gym": "/gym/actividades, /gym/salas, /gym/horarios",
                "reservas": "/reservas (JWT)",
                "pagos": "/pagos (JWT)",
                "mantenimiento": "/mantenimiento/materiales, /mantenimiento/incidencias"
            }
        }

    return app
