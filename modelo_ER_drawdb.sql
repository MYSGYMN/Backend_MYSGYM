CREATE TABLE IF NOT EXISTS `usuarios` (
	`id_usuario` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(100),
	`email` VARCHAR(120) UNIQUE,
	`password_hash` VARCHAR(255),
	`telefono` VARCHAR(20),
	`fecha_registro` DATE,
	`estado` VARCHAR(20),
	PRIMARY KEY(`id_usuario`)
);


CREATE TABLE IF NOT EXISTS `empleados` (
	`id_empleado` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(100),
	`email` VARCHAR(120),
	`rol` VARCHAR(50) COMMENT 'monitor, recepcionista, admin',
	`fecha_contratacion` DATE,
	PRIMARY KEY(`id_empleado`)
);


CREATE TABLE IF NOT EXISTS `salas` (
	`id_sala` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(100),
	`capacidad` INT,
	PRIMARY KEY(`id_sala`)
);


CREATE TABLE IF NOT EXISTS `horarios` (
	`id_horario` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`dia_semana` VARCHAR(20),
	`hora_inicio` TIME,
	`hora_fin` TIME,
	PRIMARY KEY(`id_horario`)
);


CREATE TABLE IF NOT EXISTS `actividades` (
	`id_actividad` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(100),
	`descripcion` TEXT,
	`monitor_id` INT,
	`sala_id` INT,
	`horario_id` INT,
	`aforo_maximo` INT,
	PRIMARY KEY(`id_actividad`)
);


CREATE TABLE IF NOT EXISTS `reservas` (
	`id_reserva` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`usuario_id` INT,
	`actividad_id` INT,
	`fecha_reserva` DATETIME,
	`estado` VARCHAR(20),
	PRIMARY KEY(`id_reserva`)
);


CREATE TABLE IF NOT EXISTS `pagos` (
	`id_pago` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`usuario_id` INT,
	`fecha_pago` DATE,
	`monto` DECIMAL(10,2),
	`metodo_pago` VARCHAR(50),
	PRIMARY KEY(`id_pago`)
);


CREATE TABLE IF NOT EXISTS `material` (
	`id_material` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`nombre` VARCHAR(100),
	`estado` VARCHAR(50),
	`sala_id` INT,
	PRIMARY KEY(`id_material`)
);


CREATE TABLE IF NOT EXISTS `incidencias` (
	`id_incidencia` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` TEXT,
	`fecha` DATE,
	`empleado_id` INT,
	`material_id` INT,
	`estado` VARCHAR(20),
	PRIMARY KEY(`id_incidencia`)
);


ALTER TABLE `actividades`
ADD FOREIGN KEY(`monitor_id`) REFERENCES `empleados`(`id_empleado`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `actividades`
ADD FOREIGN KEY(`sala_id`) REFERENCES `salas`(`id_sala`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `actividades`
ADD FOREIGN KEY(`horario_id`) REFERENCES `horarios`(`id_horario`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `reservas`
ADD FOREIGN KEY(`usuario_id`) REFERENCES `usuarios`(`id_usuario`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `reservas`
ADD FOREIGN KEY(`actividad_id`) REFERENCES `actividades`(`id_actividad`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `pagos`
ADD FOREIGN KEY(`usuario_id`) REFERENCES `usuarios`(`id_usuario`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `material`
ADD FOREIGN KEY(`sala_id`) REFERENCES `salas`(`id_sala`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `incidencias`
ADD FOREIGN KEY(`empleado_id`) REFERENCES `empleados`(`id_empleado`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `incidencias`
ADD FOREIGN KEY(`material_id`) REFERENCES `material`(`id_material`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
