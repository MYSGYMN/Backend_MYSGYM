import sys
import os
from datetime import datetime, time

# Add the Backend path to sys.path so we can import the app
sys.path.append('/home/penascalf5/Escritorio/Backend_MYSGYM')

from app import create_app, db
from app.models import Sala, Horario, Empleado, Usuario, Actividad, Material
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Iniciando la inserción de datos base didácticos...")

    # 1. Crear Salas
    sala1 = db.session.get(Sala, 1)
    if not sala1:
        sala1 = Sala(id_sala=1, nombre="Sala de Yoga", capacidad=10)
        db.session.add(sala1)
    
    sala2 = db.session.get(Sala, 2)
    if not sala2:
        sala2 = Sala(id_sala=2, nombre="Zona Musculación", capacidad=8)
        db.session.add(sala2)

    # 2. Crear Horarios
    horario1 = db.session.get(Horario, 1)
    if not horario1:
        horario1 = Horario(id_horario=1, dia_semana="Lunes", hora_inicio=time(9, 0), hora_fin=time(10, 0))
        db.session.add(horario1)

    horario2 = db.session.get(Horario, 2)
    if not horario2:
        horario2 = Horario(id_horario=2, dia_semana="Miercoles", hora_inicio=time(18, 30), hora_fin=time(19, 30))
        db.session.add(horario2)

    # 3. Crear Empleados (Monitores)
    empleado1 = db.session.get(Empleado, 1)
    if not empleado1:
        empleado1 = Empleado(id_empleado=1, nombre="Monitor Yoga", email="yoga@gym.com", rol="monitor", password_hash=generate_password_hash("1234"))
        db.session.add(empleado1)

    empleado2 = db.session.get(Empleado, 2)
    if not empleado2:
        empleado2 = Empleado(id_empleado=2, nombre="Monitor Spinning", email="spinning@gym.com", rol="monitor", password_hash=generate_password_hash("1234"))
        db.session.add(empleado2)

    # 4. Crear Usuario Cliente
    usuario1 = db.session.get(Usuario, 1)
    if not usuario1:
        usuario1 = Usuario(id_usuario=1, nombre="Cliente Ejemplo", email="cliente@gym.com", password_hash=generate_password_hash("1234"), telefono="600123456")
        db.session.add(usuario1)

    # 5. Crear Material
    material1 = db.session.get(Material, 1)
    if not material1:
        material1 = Material(id_material=1, nombre="Mancuernas 5kg", estado="bueno", sala_id=1)
        db.session.add(material1)

    # 6. Crear Actividad Base (opcional)
    actividad1 = db.session.get(Actividad, 1)
    if not actividad1:
        actividad1 = Actividad(id_actividad=1, nombre="Yoga Flow", descripcion="Clase relajante", monitor_id=1, sala_id=1, horario_id=1, aforo_maximo=10)
        db.session.add(actividad1)

    # Guardar todos los cambios
    db.session.commit()
    print("¡Datos base insertados correctamente!")
