from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Pago, Usuario, db
from datetime import datetime

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/', methods=['POST'])
@jwt_required()
def registrar_pago():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    nuevo_pago = Pago(
        usuario_id=current_user_id,
        monto=data.get('monto'),
        fecha_pago=datetime.utcnow(),
        metodo_pago=data.get('metodo_pago', 'Tarjeta'),
        estado='Completado'
    )
    
    db.session.add(nuevo_pago)
    db.session.commit()
    
    return jsonify({"message": "Pago registrado correctamente"}), 201

@pagos_bp.route('/historial', methods=['GET'])
@jwt_required()
def historial_pagos():
    current_user_id = get_jwt_identity()
    pagos = Pago.query.filter_by(usuario_id=current_user_id).all()
    
    return jsonify([{
        "id_pago": p.id_pago,
        "monto": float(p.monto),
        "fecha": str(p.fecha_pago),
        "metodo": p.metodo_pago,
        "estado": p.estado
    } for p in pagos]), 200
