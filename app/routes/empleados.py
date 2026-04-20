from flask import Blueprint, request, jsonify
from app.models import db, Empleado

empleados_bp = Blueprint('empleados', __name__, url_prefix='/api/empleados')

@empleados_bp.route('/', methods=['GET'])
def listar_empleados():
    """Listar todos los empleados."""
    try:
        empleados = Empleado.query.all()
        return jsonify([e.to_dict() for e in empleados]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:id>', methods=['GET'])
def obtener_empleado(id):
    """Obtener un empleado por ID."""
    try:
        empleado = Empleado.query.get(id)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify(empleado.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/', methods=['POST'])
def crear_empleado():
    """Crear un nuevo empleado."""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['nombre', 'email', 'rol']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        empleado = Empleado(
            nombre=data.get('nombre'),
            email=data.get('email'),
            rol=data.get('rol'),
            fecha_contratacion=data.get('fecha_contratacion')
        )
        
        db.session.add(empleado)
        db.session.commit()
        
        return jsonify(empleado.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    """Actualizar un empleado."""
    try:
        empleado = Empleado.query.get(id)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        
        data = request.get_json()
        empleado.nombre = data.get('nombre', empleado.nombre)
        empleado.email = data.get('email', empleado.email)
        empleado.rol = data.get('rol', empleado.rol)
        
        db.session.commit()
        return jsonify(empleado.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    """Eliminar un empleado."""
    try:
        empleado = Empleado.query.get(id)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({'message': 'Empleado eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
