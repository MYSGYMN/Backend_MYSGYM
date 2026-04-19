## EPIC 3 — Pruebas y Calidad

# HU-25 — Configurar Pytest
Feature: Configuración de pruebas
  Scenario: Inicializar Pytest
    Given que el backend está configurado
    When se ejecuta pytest
    Then debe detectar los tests correctamente

# HU-26 — BD temporal
Feature: Base de datos de pruebas
  Scenario: Crear base de datos temporal
    Given que Pytest está configurado
    When se ejecutan los tests
    Then debe crearse una base de datos temporal
    And debe eliminarse al finalizar las pruebas
# HU-27 — Tests de autenticación
Feature: Pruebas de autenticación
  Scenario: Login con credenciales válidas
    Given que existe un usuario registrado
    When se envía un login válido
    Then debe devolverse un token JWT

  Scenario: Login con credenciales inválidas
    Given que el usuario no existe
    When se envía un login incorrecto
    Then debe devolverse un código 401
# HU-28 — Tests CRUD
Feature: Pruebas CRUD
  Scenario: Crear registro
    Given que el endpoint está disponible
    When se envía un POST válido
    Then debe crearse el registro
# HU-29 — Validación de errores
Feature: Manejo de errores
  Scenario: Solicitud inválida
    Given que el usuario envía datos incompletos
    When el sistema valida la solicitud
    Then debe responder con código 400

