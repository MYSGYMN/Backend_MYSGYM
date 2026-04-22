## EPIC 4 — Documentación y Demo

# HU-30 — Diccionario de datos
Feature: Diccionario de datos
  Scenario: Documentar tablas
    Given que las tablas están definidas
    When se redacta el diccionario de datos
    Then cada atributo debe tener nombre, tipo y descripción

# HU-31 — Manual de instalación
Feature: Manual técnico
  Scenario: Crear manual de instalación
    Given que el sistema requiere MySQL y Flask
    When se redacta el manual
    Then debe incluir pasos claros para instalar y ejecutar el proyecto
# HU-32 — README profesional
Feature: Documentación del repositorio
  Scenario: Crear README
    Given que el proyecto está en GitHub
    When se redacta el README
    Then debe incluir instalación, ejecución y estructura del proyecto
# HU-33 — Preparar presentación final
Feature: Presentación final
  Scenario: Preparar presentación
    Given que el Sprint está finalizando
    When se prepara la presentación
    Then debe incluir arquitectura, demo y conclusiones
# HU-34 — Ensayo de demo
Feature: Ensayo de demo
  Scenario: Practicar la demo
    Given que la presentación está lista
    When el equipo realiza un ensayo
    Then debe verificarse que la demo funciona sin errores
