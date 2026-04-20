from flask import Blueprint, request, jsonify
from app.models import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    """Listar todos los usuarios."""
    try:
        usuarios = Usuario.query.all()
        return jsonify([u.to_dict() for u in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    """Obtener un usuario por ID."""
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    """Crear un nuevo usuario."""
    try:
        data = request.get_json()
        
        # Validación básica
        if not data or not all(k in data for k in ['nombre', 'email']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Verificar email único
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'El email ya existe'}), 409
        
        usuario = Usuario(
            nombre=data.get('nombre'),
            email=data.get('email'),
            password_hash=data.get('password_hash', ''),
            telefono=data.get('telefono'),
            fecha_registro=data.get('fecha_registro'),
            estado=data.get('estado', 'activo')
        )
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    """Actualizar un usuario."""
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.email = data.get('email', usuario.email)
        usuario.telefono = data.get('telefono', usuario.telefono)
        usuario.estado = data.get('estado', usuario.estado)
        
        db.session.commit()
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    """Eliminar un usuario."""
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
