from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Reserva, Actividad, Usuario, db
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/', methods=['POST'])
@jwt_required()
def crear_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    actividad_id = data.get('actividad_id')
    if not actividad_id:
        return jsonify({"message": "ID de actividad es obligatorio"}), 400
        
    actividad = Actividad.query.get(actividad_id)
    if not actividad:
        return jsonify({"message": "Actividad no encontrada"}), 404
        
    # Comprobar aforo
    reservas_actuales = Reserva.query.filter_by(actividad_id=actividad_id).count()
    if reservas_actuales >= actividad.aforo_maximo:
        return jsonify({"message": "La actividad está llena"}), 400
        
    # Crear la reserva
    nueva_reserva = Reserva(
        usuario_id=current_user_id,
        actividad_id=actividad_id,
        fecha_reserva=datetime.utcnow()
    )
    
    db.session.add(nueva_reserva)
    db.session.commit()
    
    return jsonify({"message": "Reserva realizada con éxito"}), 201

@reservas_bp.route('/mis-reservas', methods=['GET'])
@jwt_required()
def listar_mis_reservas():
    current_user_id = get_jwt_identity()
    reservas = Reserva.query.filter_by(usuario_id=current_user_id).all()
    
    return jsonify([{
        "id_reserva": r.id_reserva,
        "actividad": r.actividad.nombre,
        "fecha": str(r.fecha_reserva),
        "estado": r.estado
    } for r in reservas]), 200
