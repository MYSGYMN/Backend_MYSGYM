from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Reserva, Actividad, db

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('', methods=['POST'])
@reservas_bp.route('/', methods=['POST'])
@jwt_required()
def crear_reserva():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    actividad_id = data.get('actividad_id')
    if not actividad_id:
        return jsonify({"message": "ID de actividad es obligatorio"}), 400

    actividad = db.session.get(Actividad, actividad_id)
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
        fecha_reserva=datetime.now(timezone.utc)
    )

    db.session.add(nueva_reserva)
    db.session.commit()

    return jsonify({"message": "Reserva realizada con éxito"}), 201

@reservas_bp.route('', methods=['GET'])
@reservas_bp.route('/', methods=['GET'])
@jwt_required()
def listar_reservas():
    current_user_id = get_jwt_identity()
    role = get_jwt().get("role")

    if role in {"admin", "monitor"}:
        reservas = Reserva.query.all()
    else:
        reservas = Reserva.query.filter_by(usuario_id=current_user_id).all()

    return jsonify([{
        "id_reserva": r.id_reserva,
        "usuario": r.usuario.nombre if r.usuario else None,
        "actividad": r.actividad.nombre if r.actividad else None,
        "fecha": str(r.fecha_reserva),
        "estado": r.estado,
    } for r in reservas]), 200

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

@reservas_bp.route('/<int:reserva_id>', methods=['DELETE'])
@jwt_required()
def cancelar_reserva(reserva_id):
    current_user_id = get_jwt_identity()
    role = get_jwt().get("role")
    reserva = db.session.get(Reserva, reserva_id)

    if not reserva:
        return jsonify({"message": "Reserva no encontrada"}), 404

    if role not in {"admin", "monitor"} and str(reserva.usuario_id) != str(current_user_id):
        return jsonify({"message": "No tienes permiso para cancelar esta reserva"}), 403

    db.session.delete(reserva)
    db.session.commit()

    return jsonify({"message": "Reserva cancelada con éxito"}), 200

@reservas_bp.route('/<int:reserva_id>', methods=['PUT'])
@jwt_required()
def actualizar_estado_reserva(reserva_id):
    current_user_id = get_jwt_identity()
    role = get_jwt().get("role")
    reserva = db.session.get(Reserva, reserva_id)
    if not reserva:
        return jsonify({"message": "Reserva no encontrada"}), 404

    if role not in {"admin", "monitor"} and str(reserva.usuario_id) != str(current_user_id):
        return jsonify({"message": "No tienes permiso para actualizar esta reserva"}), 403

    data = request.get_json()
    reserva.estado = data.get('estado', reserva.estado)
    db.session.commit()

    return jsonify({"message": "Estado de reserva actualizado"}), 200
