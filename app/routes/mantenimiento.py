from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Material, Incidencia, db
from datetime import datetime

mantenimiento_bp = Blueprint('mantenimiento', __name__)

# --- ENDPOINTS PARA MATERIALES ---

@mantenimiento_bp.route('/materiales', methods=['GET'])
def get_materiales():
    materiales = Material.query.all()
    return jsonify([{
        "id_material": m.id_material,
        "nombre": m.nombre,
        "estado": m.estado,
        "sala": m.sala.nombre if m.sala else "General"
    } for m in materiales]), 200

@mantenimiento_bp.route('/materiales', methods=['POST'])
@jwt_required()
def crear_material():
    data = request.get_json()
    nuevo_material = Material(
        nombre=data.get('nombre'),
        estado=data.get('estado', 'Bueno'),
        sala_id=data.get('sala_id')
    )
    db.session.add(nuevo_material)
    db.session.commit()
    return jsonify({"message": "Material registrado con éxito"}), 201

# --- ENDPOINTS PARA INCIDENCIAS ---

@mantenimiento_bp.route('/incidencias', methods=['POST'])
@jwt_required()
def reportar_incidencia():
    current_user_id = get_jwt_identity() # En un sistema real, esto podría ser un empleado
    data = request.get_json()
    
    nueva_incidencia = Incidencia(
        descripcion=data.get('descripcion'),
        material_id=data.get('material_id'),
        empleado_id=data.get('empleado_id'), # Opcional: quién la gestiona
        fecha=datetime.utcnow().date(),
        estado='pendiente'
    )
    
    db.session.add(nueva_incidencia)
    db.session.commit()
    return jsonify({"message": "Incidencia reportada con éxito"}), 201

@mantenimiento_bp.route('/incidencias', methods=['GET'])
def listar_incidencias():
    incidencias = Incidencia.query.all()
    return jsonify([{
        "id_incidencia": i.id_incidencia,
        "descripcion": i.descripcion,
        "material": i.material.nombre if i.material else "Desconocido",
        "estado": i.estado,
        "fecha": str(i.fecha)
    } for i in incidencias]), 200
