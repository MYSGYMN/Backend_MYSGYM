from app import create_app, db
from app.models import Sala, Empleado, Horario, Actividad, Usuario, Material, Incidencia, Reserva, Pago
from datetime import time
from werkzeug.security import generate_password_hash

app = create_app()

def seed():
    with app.app_context():
        # Get existing records
        salas = Sala.query.all()
        empleados = Empleado.query.all()
        horarios = Horario.query.all()
        actividades = Actividad.query.all()
        usuarios = Usuario.query.all()
        
        print(f"Estado inicial:")
        print(f"  Salas: {len(salas)}")
        print(f"  Empleados: {len(empleados)}")
        print(f"  Horarios: {len(horarios)}")
        print(f"  Actividades: {len(actividades)}")
        print(f"  Usuarios: {len(usuarios)}")
        
        # Add Usuarios if none exist
        if len(usuarios) == 0:
            usuario1 = Usuario(nombre="Juan Cliente", email="juan@mysgym.com", password_hash=generate_password_hash("juan123"), telefono="1234567890")
            usuario2 = Usuario(nombre="Maria Cliente", email="maria@mysgym.com", password_hash=generate_password_hash("maria123"), telefono="0987654321")
            usuario3 = Usuario(nombre="Luis Cliente", email="luis@mysgym.com", password_hash=generate_password_hash("luis123"), telefono="5555555555")
            db.session.add_all([usuario1, usuario2, usuario3])
            db.session.commit()
            usuarios = Usuario.query.all()
            print(f"  Usuarios agregados: 3")
        
        # Add Material if less than 3
        if Material.query.count() < 3:
            material1 = Material(nombre="Bicicleta Estatica 1", estado="nuevo", sala_id=salas[0].id_sala if salas else None)
            material2 = Material(nombre="Bicicleta Estatica 2", estado="bueno", sala_id=salas[0].id_sala if salas else None)
            material3 = Material(nombre="Mancuernas 5kg", estado="desgastado", sala_id=salas[2].id_sala if len(salas) > 2 else None)
            db.session.add_all([material1, material2, material3])
            db.session.commit()
            print(f"  Materiales agregados: 3")
        
        materiales = Material.query.all()
        
        # Add Incidencias if less than 3
        if Incidencia.query.count() < 3 and len(materiales) > 0 and len(empleados) > 0:
            incid1 = Incidencia(descripcion="Bicicleta con ruido", material_id=materiales[0].id_material, empleado_id=empleados[0].id_empleado, estado="pendiente")
            incid2 = Incidencia(descripcion="Mancuerna desgaste", material_id=materiales[2].id_material, empleado_id=empleados[1].id_empleado, estado="resuelta")
            incid3 = Incidencia(descripcion="Pedido repuestos", material_id=materiales[1].id_material, empleado_id=empleados[0].id_empleado, estado="en proceso")
            db.session.add_all([incid1, incid2, incid3])
            db.session.commit()
            print(f"  Incidencias agregadas: 3")
        
        from datetime import datetime
        actividades = Actividad.query.all()
        
        # Add Reservas if less than 3
        if Reserva.query.count() < 3 and len(usuarios) > 0 and len(actividades) > 0:
            res1 = Reserva(usuario_id=usuarios[0].id_usuario, actividad_id=actividades[0].id_actividad, estado="confirmada")
            res2 = Reserva(usuario_id=usuarios[1].id_usuario, actividad_id=actividades[1].id_actividad, estado="cancelada")
            res3 = Reserva(usuario_id=usuarios[0].id_usuario, actividad_id=actividades[2].id_actividad, estado="confirmada")
            db.session.add_all([res1, res2, res3])
            db.session.commit()
            print(f"  Reservas agregadas: 3")
        
        # Add Pagos if less than 3
        if Pago.query.count() < 3 and len(usuarios) > 0:
            pago1 = Pago(usuario_id=usuarios[0].id_usuario, monto=50.00, metodo_pago="efectivo", estado="Completado")
            pago2 = Pago(usuario_id=usuarios[1].id_usuario, monto=75.00, metodo_pago="tarjeta", estado="Completado")
            usuario3_id = usuarios[2].id_usuario if len(usuarios) > 2 else usuarios[0].id_usuario
            pago3 = Pago(usuario_id=usuario3_id, monto=50.00, metodo_pago="transferencia", estado="Pendiente")
            db.session.add_all([pago1, pago2, pago3])
            db.session.commit()
            print(f"  Pagos agregados: 3")
        
        print(f"\nEstado final:")
        print(f"  Salas: {Sala.query.count()}")
        print(f"  Empleados: {Empleado.query.count()}")
        print(f"  Horarios: {Horario.query.count()}")
        print(f"  Actividades: {Actividad.query.count()}")
        print(f"  Usuarios: {Usuario.query.count()}")
        print(f"  Materiales: {Material.query.count()}")
        print(f"  Incidencias: {Incidencia.query.count()}")
        print(f"  Reservas: {Reserva.query.count()}")
        print(f"  Pagos: {Pago.query.count()}")

if __name__ == "__main__":
    seed()