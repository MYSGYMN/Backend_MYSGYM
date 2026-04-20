from flask import Blueprint, request, jsonify
from app.models import db, Actividad

actividades_bp = Blueprint('actividades', __name__, url_prefix='/api/actividades')

@actividades_bp.route('/', methods=['GET'])
def listar_actividades():
    """Listar todas las actividades."""
    try:
        actividades = Actividad.query.all()
        return jsonify([a.to_dict() for a in actividades]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/<int:id>', methods=['GET'])
def obtener_actividad(id):
    """Obtener una actividad por ID."""
    try:
        actividad = Actividad.query.get(id)
        if not actividad:
            return jsonify({'error': 'Actividad no encontrada'}), 404
        return jsonify(actividad.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/', methods=['POST'])
def crear_actividad():
    """Crear una nueva actividad."""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['nombre', 'monitor_id', 'sala_id', 'horario_id']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        actividad = Actividad(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            monitor_id=data.get('monitor_id'),
            sala_id=data.get('sala_id'),
            horario_id=data.get('horario_id'),
            aforo_maximo=data.get('aforo_maximo')
        )
        
        db.session.add(actividad)
        db.session.commit()
        
        return jsonify(actividad.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/<int:id>', methods=['PUT'])
def actualizar_actividad(id):
    """Actualizar una actividad."""
    try:
        actividad = Actividad.query.get(id)
        if not actividad:
            return jsonify({'error': 'Actividad no encontrada'}), 404
        
        data = request.get_json()
        actividad.nombre = data.get('nombre', actividad.nombre)
        actividad.descripcion = data.get('descripcion', actividad.descripcion)
        actividad.aforo_maximo = data.get('aforo_maximo', actividad.aforo_maximo)
        
        db.session.commit()
        return jsonify(actividad.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@actividades_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_actividad(id):
    """Eliminar una actividad."""
    try:
        actividad = Actividad.query.get(id)
        if not actividad:
            return jsonify({'error': 'Actividad no encontrada'}), 404
        
        db.session.delete(actividad)
        db.session.commit()
        return jsonify({'message': 'Actividad eliminada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
