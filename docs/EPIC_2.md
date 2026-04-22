## EPIC 2 — Backend Flask
# HU-10 — Estructura del proyecto
Feature: Estructura del backend
  Scenario: Crear estructura modular
    Given que se inicia el backend en Flask
    When se crea la estructura del proyecto
    Then deben existir carpetas para routes, models, config y tests
    And debe existir un archivo run.py para iniciar la aplicación
# HU-11 — Configurar SQLAlchemy
Feature: Conexión a MySQL
  Scenario: Configurar SQLAlchemy
    Given que MySQL está instalado y accesible
    When se configura SQLAlchemy en Flask
    Then la aplicación debe conectarse correctamente a la base de datos
    And debe permitir operaciones CRUD desde el ORM
# HU-12 — Modelos ORM
Feature: Modelos SQLAlchemy
  Scenario: Crear modelos ORM
    Given que existe un modelo relacional
    When se implementan los modelos en SQLAlchemy
    Then cada tabla debe tener su clase correspondiente
    And deben definirse relaciones con ForeignKey y relationship
# CRUDs (HU-13 a HU-20)
Feature: CRUD de entidades
  Scenario: Crear un registro
    Given que el usuario tiene un token válido
    When envía una solicitud POST con datos válidos
    Then el sistema debe crear el registro
    And debe devolver un código 201

  Scenario: Consultar registros
    Given que existen registros en la base de datos
    When el usuario envía una solicitud GET
    Then el sistema debe devolver la lista de registros
    And debe responder con código 200

  Scenario: Actualizar un registro
    Given que el usuario tiene permisos
    When envía una solicitud PUT con datos válidos
    Then el sistema debe actualizar el registro
    And debe responder con código 200

  Scenario: Eliminar un registro
    Given que el usuario tiene rol admin
    When envía una solicitud DELETE
    Then el sistema debe eliminar el registro
    And debe responder con código 204

# HU-21 — Implementar JWT
Feature: Autenticación JWT
  Scenario: Login exitoso
    Given que el usuario existe y su contraseña es correcta
    When envía una solicitud POST a /auth/login
    Then el sistema debe generar un token JWT
    And debe devolverlo en formato JSON
# HU-22 — Roles
Feature: Roles de usuario
  Scenario: Validar rol admin
    Given que el usuario tiene rol admin
    When accede a una ruta protegida
    Then el sistema debe permitir el acceso

  Scenario: Denegar acceso por rol insuficiente
    Given que el usuario tiene rol socio
    When intenta acceder a una ruta de administración
    Then el sistema debe responder con código 403
# HU-23 — Proteger rutas
Feature: Protección de rutas
  Scenario: Acceso sin token
    Given que el usuario no envía un token
    When intenta acceder a una ruta protegida
    Then el sistema debe responder con código 401

# HU-24 — Crear colección Postman
Feature: Colección Postman
  Scenario: Crear colección de endpoints
    Given que el backend expone rutas REST
    When se crea una colección en Postman
    Then deben incluirse los endpoints principales del sistema
    And debe poder ejecutarse la demo desde Postman
