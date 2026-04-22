CREATE DATABASE IF NOT EXISTS gimnasio;
USE gimnasio;

-- Crear usuario de la aplicación si no existe
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'segura123';
GRANT SELECT, INSERT, UPDATE ON gimnasio.* TO 'app_user'@'localhost';

-- Crear usuario administrador si no existe
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'adminpass';
GRANT ALL PRIVILEGES ON gimnasio.* TO 'admin'@'localhost';

FLUSH PRIVILEGES;
