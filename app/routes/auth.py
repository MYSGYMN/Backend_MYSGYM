from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import Usuario, db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email y contraseña son obligatorios"}), 400
        
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({"message": "El usuario ya existe"}), 400
        
    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        email=data.get('email'),
        password_hash=generate_password_hash(data.get('password')),
        telefono=data.get('telefono'),
        fecha_registro=datetime.utcnow().date()
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({"message": "Usuario registrado con éxito"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email y contraseña son obligatorios"}), 400
        
    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    
    if not usuario or not check_password_hash(usuario.password_hash, data.get('password')):
        return jsonify({"message": "Credenciales inválidas"}), 401
        
    access_token = create_access_token(identity=str(usuario.id_usuario))
    return jsonify(access_token=access_token), 200
