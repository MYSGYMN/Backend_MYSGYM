SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE incidencias;
TRUNCATE TABLE material;
TRUNCATE TABLE pagos;
TRUNCATE TABLE reservas;
TRUNCATE TABLE actividades;
TRUNCATE TABLE horarios;
TRUNCATE TABLE salas;
TRUNCATE TABLE empleados;
TRUNCATE TABLE usuarios;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO usuarios (id_usuario, nombre, email, password_hash, telefono, fecha_registro, estado) VALUES
(1, 'Ana Lopez', 'ana.lopez@example.com', 'hash_ana_001', '600111222', '2026-01-10', 'activo'),
(2, 'Carlos Perez', 'carlos.perez@example.com', 'hash_carlos_001', '600222333', '2026-01-15', 'activo'),
(3, 'Lucia Martin', 'lucia.martin@example.com', 'hash_lucia_001', '600333444', '2026-02-01', 'activo'),
(4, 'Diego Ruiz', 'diego.ruiz@example.com', 'hash_diego_001', '600444555', '2026-02-20', 'inactivo'),
(5, 'Maria Gomez', 'maria.gomez@example.com', 'hash_maria_001', '600555666', '2026-03-03', 'activo');

INSERT INTO empleados (id_empleado, nombre, email, rol, fecha_contratacion) VALUES
(1, 'Sergio Trainer', 'sergio.trainer@example.com', 'monitor', '2025-10-01'),
(2, 'Elena Frontdesk', 'elena.frontdesk@example.com', 'recepcionista', '2025-11-12'),
(3, 'Raul Admin', 'raul.admin@example.com', 'admin', '2025-09-20');

INSERT INTO salas (id_sala, nombre, capacidad) VALUES
(1, 'Sala Funcional', 20),
(2, 'Sala Ciclo', 18),
(3, 'Sala Yoga', 25);

INSERT INTO horarios (id_horario, dia_semana, hora_inicio, hora_fin) VALUES
(1, 'Lunes', '08:00:00', '09:00:00'),
(2, 'Miercoles', '19:00:00', '20:00:00'),
(3, 'Viernes', '18:00:00', '19:00:00');

INSERT INTO actividades (id_actividad, nombre, descripcion, monitor_id, sala_id, horario_id, aforo_maximo) VALUES
(1, 'Entrenamiento Funcional', 'Circuito de fuerza y cardio para nivel intermedio.', 1, 1, 1, 20),
(2, 'Ciclo Indoor', 'Sesion de ciclismo de alta intensidad.', 1, 2, 2, 18),
(3, 'Yoga Flow', 'Clase de movilidad y respiracion.', 1, 3, 3, 25);

INSERT INTO reservas (id_reserva, usuario_id, actividad_id, fecha_reserva, estado) VALUES
(1, 1, 1, '2026-04-18 10:12:00', 'confirmada'),
(2, 2, 2, '2026-04-18 11:03:00', 'confirmada'),
(3, 3, 3, '2026-04-18 12:40:00', 'pendiente'),
(4, 5, 1, '2026-04-19 09:30:00', 'cancelada');

INSERT INTO pagos (id_pago, usuario_id, fecha_pago, monto, metodo_pago) VALUES
(1, 1, '2026-04-01', 39.90, 'tarjeta'),
(2, 2, '2026-04-01', 39.90, 'tarjeta'),
(3, 3, '2026-04-02', 29.90, 'transferencia'),
(4, 5, '2026-04-03', 39.90, 'efectivo');

INSERT INTO material (id_material, nombre, estado, sala_id) VALUES
(1, 'Mancuernas 10kg', 'disponible', 1),
(2, 'Bicicleta Spinning #07', 'mantenimiento', 2),
(3, 'Esterillas Yoga', 'disponible', 3);

INSERT INTO incidencias (id_incidencia, descripcion, fecha, empleado_id, material_id, estado) VALUES
(1, 'Ruido en el eje de bicicleta #07.', '2026-04-10', 2, 2, 'abierta'),
(2, 'Reposicion de esterillas por desgaste.', '2026-04-12', 1, 3, 'resuelta');

ALTER TABLE usuarios AUTO_INCREMENT = 6;
ALTER TABLE empleados AUTO_INCREMENT = 4;
ALTER TABLE salas AUTO_INCREMENT = 4;
ALTER TABLE horarios AUTO_INCREMENT = 4;
ALTER TABLE actividades AUTO_INCREMENT = 4;
ALTER TABLE reservas AUTO_INCREMENT = 5;
ALTER TABLE pagos AUTO_INCREMENT = 5;
ALTER TABLE material AUTO_INCREMENT = 4;
ALTER TABLE incidencias AUTO_INCREMENT = 3;
