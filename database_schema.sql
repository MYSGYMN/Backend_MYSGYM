-- Script SQL Completo para MYSGYM
-- Generado para el proyecto de gestión de gimnasio

CREATE DATABASE IF NOT EXISTS gimnasio;
USE gimnasio;

-- 1. Tabla de Usuarios (Socios)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro DATE DEFAULT (CURRENT_DATE),
    estado ENUM('activo', 'inactivo', 'suspendido') DEFAULT 'activo',
    INDEX (email),
    INDEX (nombre)
) ENGINE=InnoDB;

-- 2. Tabla de Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_contratacion DATE DEFAULT (CURRENT_DATE),
    INDEX (email)
) ENGINE=InnoDB;

-- 3. Tabla de Salas
CREATE TABLE IF NOT EXISTS salas (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL
) ENGINE=InnoDB;

-- 4. Tabla de Horarios
CREATE TABLE IF NOT EXISTS horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
) ENGINE=InnoDB;

-- 5. Tabla de Actividades
CREATE TABLE IF NOT EXISTS actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    monitor_id INT,
    sala_id INT,
    horario_id INT,
    aforo_maximo INT,
    FOREIGN KEY (monitor_id) REFERENCES empleados(id_empleado) ON DELETE SET NULL,
    FOREIGN KEY (sala_id) REFERENCES salas(id_sala) ON DELETE SET NULL,
    FOREIGN KEY (horario_id) REFERENCES horarios(id_horario) ON DELETE SET NULL,
    INDEX (nombre)
) ENGINE=InnoDB;

-- 6. Tabla de Reservas
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    actividad_id INT NOT NULL,
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('confirmada', 'cancelada', 'asistida') DEFAULT 'confirmada',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (actividad_id) REFERENCES actividades(id_actividad) ON DELETE CASCADE,
    INDEX (fecha_reserva)
) ENGINE=InnoDB;

-- 7. Tabla de Pagos
CREATE TABLE IF NOT EXISTS pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_pago DATE DEFAULT (CURRENT_DATE),
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Completado',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    INDEX (fecha_pago)
) ENGINE=InnoDB;

-- 8. Tabla de Materiales
CREATE TABLE IF NOT EXISTS materiales (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado ENUM('nuevo', 'bueno', 'desgastado', 'averiado') DEFAULT 'nuevo',
    sala_id INT,
    FOREIGN KEY (sala_id) REFERENCES salas(id_sala) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 9. Tabla de Incidencias
CREATE TABLE IF NOT EXISTS incidencias (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha DATE DEFAULT (CURRENT_DATE),
    empleado_id INT,
    material_id INT,
    estado ENUM('pendiente', 'en proceso', 'resuelta') DEFAULT 'pendiente',
    FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado) ON DELETE SET NULL,
    FOREIGN KEY (material_id) REFERENCES materiales(id_material) ON DELETE SET NULL,
    INDEX (fecha),
    INDEX (estado)
) ENGINE=InnoDB;

-- Permisos
-- Crear un usuario específico para la aplicación si no existe
CREATE USER IF NOT EXISTS 'gym_app'@'localhost' IDENTIFIED BY 'gym_password_2024';
GRANT SELECT, INSERT, UPDATE, DELETE ON gimnasio.* TO 'gym_app'@'localhost';
FLUSH PRIVILEGES;
