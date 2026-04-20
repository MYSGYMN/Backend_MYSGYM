from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.Date)
    estado = db.Column(db.String(20))
    
    reservas = db.relationship('Reserva', back_populates='usuario')
    pagos = db.relationship('Pago', back_populates='usuario')
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'estado': self.estado
        }

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(120))
    rol = db.Column(db.String(50))
    fecha_contratacion = db.Column(db.Date)
    
    actividades = db.relationship('Actividad', back_populates='monitor')
    incidencias = db.relationship('Incidencia', back_populates='empleado')
    
    def to_dict(self):
        return {
            'id_empleado': self.id_empleado,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'fecha_contratacion': self.fecha_contratacion.isoformat() if self.fecha_contratacion else None
        }

class Sala(db.Model):
    __tablename__ = 'salas'
    
    id_sala = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    capacidad = db.Column(db.Integer)
    
    actividades = db.relationship('Actividad', back_populates='sala')
    material = db.relationship('Material', back_populates='sala')
    
    def to_dict(self):
        return {
            'id_sala': self.id_sala,
            'nombre': self.nombre,
            'capacidad': self.capacidad
        }

class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id_horario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dia_semana = db.Column(db.String(20))
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    
    actividades = db.relationship('Actividad', back_populates='horario')
    
    def to_dict(self):
        return {
            'id_horario': self.id_horario,
            'dia_semana': self.dia_semana,
            'hora_inicio': self.hora_inicio.isoformat() if self.hora_inicio else None,
            'hora_fin': self.hora_fin.isoformat() if self.hora_fin else None
        }

class Actividad(db.Model):
    __tablename__ = 'actividades'
    
    id_actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    monitor_id = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'))
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id_sala'))
    horario_id = db.Column(db.Integer, db.ForeignKey('horarios.id_horario'))
    aforo_maximo = db.Column(db.Integer)
    
    monitor = db.relationship('Empleado', back_populates='actividades')
    sala = db.relationship('Sala', back_populates='actividades')
    horario = db.relationship('Horario', back_populates='actividades')
    reservas = db.relationship('Reserva', back_populates='actividad')
    
    def to_dict(self):
        return {
            'id_actividad': self.id_actividad,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'monitor_id': self.monitor_id,
            'sala_id': self.sala_id,
            'horario_id': self.horario_id,
            'aforo_maximo': self.aforo_maximo,
            'monitor': self.monitor.to_dict() if self.monitor else None,
            'sala': self.sala.to_dict() if self.sala else None,
            'horario': self.horario.to_dict() if self.horario else None
        }

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id_reserva = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades.id_actividad'))
    fecha_reserva = db.Column(db.DateTime)
    estado = db.Column(db.String(20))
    
    usuario = db.relationship('Usuario', back_populates='reservas')
    actividad = db.relationship('Actividad', back_populates='reservas')
    
    def to_dict(self):
        return {
            'id_reserva': self.id_reserva,
            'usuario_id': self.usuario_id,
            'actividad_id': self.actividad_id,
            'fecha_reserva': self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            'estado': self.estado,
            'usuario': self.usuario.to_dict() if self.usuario else None,
            'actividad': self.actividad.to_dict() if self.actividad else None
        }

class Pago(db.Model):
    __tablename__ = 'pagos'
    
    id_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    fecha_pago = db.Column(db.Date)
    monto = db.Column(db.Numeric(10, 2))
    metodo_pago = db.Column(db.String(50))
    
    usuario = db.relationship('Usuario', back_populates='pagos')
    
    def to_dict(self):
        return {
            'id_pago': self.id_pago,
            'usuario_id': self.usuario_id,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'monto': float(self.monto) if self.monto else 0,
            'metodo_pago': self.metodo_pago,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }

class Material(db.Model):
    __tablename__ = 'material'
    
    id_material = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id_sala'))
    
    sala = db.relationship('Sala', back_populates='material')
    incidencias = db.relationship('Incidencia', back_populates='material')
    
    def to_dict(self):
        return {
            'id_material': self.id_material,
            'nombre': self.nombre,
            'estado': self.estado,
            'sala_id': self.sala_id,
            'sala': self.sala.to_dict() if self.sala else None
        }

class Incidencia(db.Model):
    __tablename__ = 'incidencias'
    
    id_incidencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id_material'))
    estado = db.Column(db.String(20))
    
    empleado = db.relationship('Empleado', back_populates='incidencias')
    material = db.relationship('Material', back_populates='incidencias')
    
    def to_dict(self):
        return {
            'id_incidencia': self.id_incidencia,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'empleado_id': self.empleado_id,
            'material_id': self.material_id,
            'estado': self.estado,
            'empleado': self.empleado.to_dict() if self.empleado else None,
            'material': self.material.to_dict() if self.material else None
        }
