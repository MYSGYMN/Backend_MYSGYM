from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Usuario, db

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        "id_usuario": u.id_usuario,
        "nombre": u.nombre,
        "email": u.email,
        "telefono": u.telefono,
        "estado": u.estado
    } for u in usuarios]), 200

@usuarios_bp.route('/perfil', methods=['GET'])
@jwt_required()
def get_perfil():
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get(current_user_id)
    
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
        
    return jsonify({
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "estado": usuario.estado,
        "fecha_registro": str(usuario.fecha_registro)
    }), 200

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
        
    data = request.get_json()
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.telefono = data.get('telefono', usuario.telefono)
    usuario.estado = data.get('estado', usuario.estado)
    
    db.session.commit()
    return jsonify({"message": "Usuario actualizado con éxito"}), 200
