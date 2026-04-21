from app import create_app, db
from app.models import Sala, Empleado, Horario, Actividad
from datetime import time

app = create_app()

with app.app_context():
    # 1. Crear Sala
    sala1 = Sala(nombre="Sala Principal", capacidad=20)
    db.session.add(sala1)
    
    # 2. Crear Empleado (Monitor)
    monitor1 = Empleado(nombre="Carlos Monitor", rol="Instructor", email="carlos@mysgym.com")
    db.session.add(monitor1)
    
    # 3. Crear Horario
    horario1 = Horario(dia_semana="Lunes", hora_inicio=time(10, 0), hora_fin=time(11, 0))
    db.session.add(horario1)
    
    db.session.commit() # Guardamos para obtener IDs
    
    # 4. Crear Actividad
    actividad1 = Actividad(
        nombre="Yoga Zen",
        descripcion="Clase de yoga para todos los niveles",
        aforo_maximo=15,
        sala_id=sala1.id_sala,
        monitor_id=monitor1.id_empleado,
        horario_id=horario1.id_horario
    )
    db.session.add(actividad1)
    db.session.commit()
    
    print("¡Datos de prueba insertados con éxito!")
