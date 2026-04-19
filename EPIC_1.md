## EPIC 1 — Diseño de Base de Datos

# HU-01 — Modelo literario
Feature: Modelo literario del sistema MYSGYM
  Scenario: Redacción del modelo literario
    Given que el equipo necesita documentar el funcionamiento del gimnasio
    When el Product Owner redacta el modelo literario
    Then el documento debe describir actores, procesos y objetivos del sistema
    And debe estar aprobado por el equipo
# HU-02 — Definir entidades y atributos
Feature: Definición de entidades
  Scenario: Identificación de entidades y atributos
    Given que el sistema requiere una base de datos estructurada
    When se definen las 12 entidades con sus atributos
    Then cada entidad debe tener clave primaria
    And deben identificarse las claves foráneas necesarias
# HU-03 — Crear diagrama E/R
Feature: Diagrama entidad-relación
  Scenario: Construcción del E/R
    Given que las entidades están definidas
    When se crea el diagrama E/R
    Then debe incluir todas las entidades y relaciones
    And debe mostrar cardinalidades correctas
# HU-04 — Modelo relacional
Feature: Modelo relacional
  Scenario: Transformación del E/R en modelo relacional
    Given que existe un diagrama E/R validado
    When se genera el modelo relacional
    Then deben definirse todas las tablas con sus claves
    And deben reflejarse todas las relaciones del E/R
# HU-05 — Normalización
Feature: Normalización de la base de datos
  Scenario: Normalización hasta 3FN
    Given que el modelo relacional está definido
    When se aplica normalización
    Then no debe haber datos redundantes
    And cada tabla debe cumplir 1FN, 2FN y 3FN
# HU-06 — Script SQL CREATE
Feature: Script SQL de creación
  Scenario: Crear tablas en MySQL
    Given que el modelo relacional está aprobado
    When se genera el script SQL
    Then debe incluir las 12 tablas del sistema
    And debe usar ENGINE=InnoDB
    And debe incluir claves foráneas correctas
# HU-07 — Script SQL INSERTS
Feature: Datos de ejemplo
  Scenario: Insertar datos iniciales
    Given que las tablas están creadas
    When se generan los inserts
    Then cada tabla debe tener entre 5 y 10 registros
    And los datos deben ser coherentes entre sí
# HU-08 — Crear usuarios MySQL
Feature: Usuarios MySQL
  Scenario: Crear usuarios con permisos diferenciados
    Given que el servidor MySQL está operativo
    When se crean los usuarios admin y app_user
    Then admin debe tener todos los privilegios sobre la base de datos
    And app_user debe tener permisos limitados (SELECT, INSERT, UPDATE)
# HU-09 — Exportar dump
Feature: Exportación de la base de datos
  Scenario: Generar dump SQL
    Given que la base de datos está completa
    When se ejecuta mysqldump
    Then debe generarse un archivo gimnasio_backup.sql
    And debe permitir recrear la base de datos en otro entorno
