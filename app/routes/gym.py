from flask import Blueprint, jsonify, request
from app.models import Actividad, Sala, Horario, db

gym_bp = Blueprint('gym', __name__)

# --- ENDPOINTS PARA ACTIVIDADES ---

@gym_bp.route('/actividades', methods=['GET'])
def get_actividades():
    actividades = Actividad.query.all()
    return jsonify([{
        "id_actividad": a.id_actividad,
        "nombre": a.nombre,
        "descripcion": a.descripcion,
        "aforo_maximo": a.aforo_maximo,
        "sala": a.sala.nombre if a.sala else None,
        "monitor": a.monitor.nombre if a.monitor else None,
        "horario": f"{a.horario.dia_semana} {a.horario.hora_inicio}-{a.horario.hora_fin}" if a.horario else None
    } for a in actividades]), 200

# --- ENDPOINTS PARA SALAS ---

@gym_bp.route('/salas', methods=['GET'])
def get_salas():
    salas = Sala.query.all()
    return jsonify([{
        "id_sala": s.id_sala,
        "nombre": s.nombre,
        "capacidad": s.capacidad
    } for s in salas]), 200

@gym_bp.route('/salas', methods=['POST'])
def create_sala():
    data = request.get_json()
    nueva_sala = Sala(
        nombre=data.get('nombre'),
        capacidad=data.get('capacidad')
    )
    db.session.add(nueva_sala)
    db.session.commit()
    return jsonify({"message": "Sala creada con éxito"}), 201
