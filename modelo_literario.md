# Historias de Usuario, Buyer Persona y Modelo Literario – Proyecto MYSGYM

Este documento recoge de forma unificada:

- Buyer Persona principal y secundario  
- Modelo literario del sistema MYSGYM  
- Historias de Usuario organizadas por EPIC  
- Criterios de aceptación en formato Gherkin (Given–When–Then)  

Es un entregable oficial del Sprint de 2 semanas del proyecto MYSGYM.

---

## 1. Buyer Persona

### 1.1 Buyer Persona principal: Recepcionista / Administrativa del Gimnasio

**Perfil**

- Mujer u hombre mayor de edad  
- Nivel de alfabetización digital: básico a medio  
- Maneja tareas administrativas del gimnasio  
- No es programador/a  
- Necesita herramientas simples, rápidas y claras  

**Objetivos**

- Registrar socios sin errores  
- Gestionar pagos y cuotas  
- Controlar reservas y asistencia  
- Consultar incidencias y materiales  
- Coordinar horarios y clases con monitores  

**Frustraciones**

- Sistemas complicados  
- Formularios largos o confusos  
- Información duplicada o desactualizada  
- Tener que usar varias herramientas distintas  

**Necesidades**

- Interfaz intuitiva  
- Acceso rápido a datos  
- Automatización de tareas repetitivas  
- Seguridad (roles, permisos)  
- Información clara y centralizada  

---

### 1.2 Buyer Persona secundario: Monitor / Entrenador

**Objetivos**

- Ver sus clases asignadas  
- Consultar reservas  
- Registrar incidencias  
- Controlar asistencia  

**Necesidades**

- Acceso rápido desde móvil o tablet  
- Información clara y en tiempo real  

---

## 2. Modelo literario del proyecto

El modelo literario define la estructura conceptual del sistema MYSGYM, estableciendo los actores, procesos, objetivos y requisitos necesarios para construir una solución robusta, escalable y alineada con las necesidades reales de un gimnasio moderno.  
Este documento sirve como base para el diseño del modelo E/R y el desarrollo del backend.

---

### 2.1 Contexto general del negocio

MYSGYM es un gimnasio de tamaño medio que ofrece servicios de entrenamiento, clases dirigidas, uso de salas especializadas y acceso a material deportivo.  
El negocio requiere un sistema digital que permita gestionar de forma centralizada la información relacionada con socios, empleados, clases, reservas, pagos, incidencias y recursos internos.

El objetivo principal es disponer de una plataforma que facilite la operación diaria del gimnasio, mejore la experiencia del usuario y permita un control eficiente de las actividades internas.

---

### 2.2 Necesidad del sistema

Actualmente, la gestión del gimnasio se realiza mediante herramientas dispersas (hojas de cálculo, registros manuales y aplicaciones no integradas). Esto genera:

- Duplicidad de datos  
- Errores en reservas y pagos  
- Falta de trazabilidad  
- Dificultad para controlar horarios, incidencias y disponibilidad de salas  

El sistema MYSGYM busca resolver estos problemas mediante una base de datos estructurada y un backend profesional que permita automatizar procesos clave.

---

### 2.3 Objetivo del sistema

El sistema MYSGYM debe permitir:

- Registrar y gestionar socios y empleados  
- Administrar clases, horarios y salas  
- Controlar reservas de clases  
- Registrar pagos y cuotas  
- Gestionar materiales deportivos  
- Registrar incidencias internas  
- Garantizar seguridad mediante autenticación y roles  
- Proveer información actualizada y consistente para la toma de decisiones  

---

### 2.4 Descripción de los actores

**Socios**  
Personas inscritas en el gimnasio. Pueden reservar clases, pagar cuotas y acceder a servicios.

**Empleados**  
Incluye monitores, recepcionistas y personal administrativo.  
Tienen permisos diferenciados según su rol.

**Administración**  
Encargados de gestionar:

- Altas y bajas de socios  
- Gestión de empleados  
- Control de pagos  
- Gestión de incidencias  
- Configuración de clases y horarios  

---

### 2.5 Procesos principales del negocio

**5.1 Gestión de Socios**

- Registro de nuevos socios  
- Actualización de datos personales  
- Consulta de historial de reservas y pagos  
- Control de fecha de alta y estado del socio  

**5.2 Gestión de Empleados**

- Registro de empleados  
- Asignación de roles (monitor, recepcionista, admin)  
- Asignación de clases a monitores  

**5.3 Gestión de Clases**

- Creación de clases con actividad, monitor, sala y horario  
- Definición de capacidad máxima  
- Control de asistencia  

**5.4 Gestión de Reservas**

- Un socio puede reservar una clase disponible  
- Validación de aforo  
- Cancelación de reservas  
- Registro de asistencia  

**5.5 Gestión de Pagos y Cuotas**

- Registro de cuotas (mensual, trimestral, anual)  
- Registro de pagos puntuales  
- Control del estado de pago del socio  
- Generación de historial de pagos  

**5.6 Gestión de Materiales**

- Registro de materiales disponibles en el gimnasio  
- Control de estado (nuevo, usado, averiado)  
- Asignación a salas o actividades  

**5.7 Gestión de Incidencias**

- Registro de incidencias (averías, quejas, problemas internos)  
- Asignación a empleados responsables  
- Seguimiento del estado (pendiente, en proceso, resuelta)  

**5.8 Gestión de Horarios**

- Definición de horarios de apertura  
- Gestión de franjas horarias para clases  
- Control de disponibilidad de salas  

---

### 2.6 Requisitos funcionales

El sistema debe:

1. Permitir registrar, modificar y consultar socios.  
2. Permitir gestionar empleados y roles.  
3. Permitir crear y administrar clases.  
4. Permitir que los socios reserven clases disponibles.  
5. Controlar el aforo de cada clase.  
6. Registrar pagos y cuotas.  
7. Permitir registrar y gestionar incidencias.  
8. Gestionar materiales deportivos y su estado.  
9. Permitir autenticación mediante JWT.  
10. Diferenciar permisos según el rol del usuario.  

---

### 2.7 Requisitos no funcionales

- **Seguridad:** Autenticación JWT, roles y permisos.  
- **Disponibilidad:** El sistema debe estar operativo durante el horario del gimnasio.  
- **Escalabilidad:** La base de datos debe permitir crecimiento en número de socios y clases.  
- **Integridad:** Uso de claves foráneas y motor InnoDB para garantizar consistencia.  
- **Usabilidad:** API clara y documentada para facilitar integración futura con frontend.  

---

### 2.8 Alcance del proyecto

El proyecto MYSGYM incluye:

- Diseño completo de la base de datos  
- Implementación del backend en Flask  
- CRUDs completos para todas las entidades  
- Autenticación y autorización  
- Pruebas unitarias con Pytest  
- Documentación técnica  
- Presentación final con demo  

No incluye:

- Integración con sistemas de pago externos  
- Aplicación móvil  

---

## 3. Historias de Usuario y Criterios de Aceptación

---

## EPIC 1 — Diseño de Base de Datos

### HU-01 — Modelo literario

```gherkin
Feature: Modelo literario del sistema MYSGYM
  Scenario: Redacción del modelo literario
    Given que el equipo necesita documentar el funcionamiento del gimnasio
    When el Product Owner redacta el modelo literario
    Then el documento debe describir actores, procesos y objetivos del sistema
    And debe estar aprobado por el equipo
