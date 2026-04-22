# MYSGYM - Descripción de la rama Yeremi

Este documento resume el proyecto del backend MYSGYM para que cualquier miembro del equipo pueda entender rápidamente qué hace, cómo está organizado y qué cubre cada módulo.

## 1. Objetivo del proyecto

MYSGYM es una API backend para la gestión integral de un gimnasio. Su finalidad es centralizar en un solo sistema la administración de usuarios, empleados, actividades, salas, horarios, reservas, pagos, materiales e incidencias de mantenimiento.

La aplicación está construida con Flask, SQLAlchemy y MySQL, y utiliza JWT para controlar el acceso a las rutas protegidas según el rol del usuario.

## 2. Alcance funcional

El sistema cubre estos procesos principales:

- Registro e inicio de sesión de clientes.
- Registro e inicio de sesión de empleados, con roles como monitor o admin.
- Gestión de usuarios del gimnasio.
- Gestión de empleados.
- Administración de actividades, salas y horarios.
- Reserva de actividades por parte de usuarios autenticados.
- Registro y consulta del historial de pagos.
- Control de materiales del gimnasio.
- Reporte y seguimiento de incidencias de mantenimiento.

## 3. Arquitectura general

El backend sigue una estructura modular basada en Blueprints, lo que permite separar la lógica por dominios funcionales y mantener el código organizado.

La aplicación principal se crea mediante una factory en [app/__init__.py](app/__init__.py), donde se inicializan los servicios base:

- SQLAlchemy para el acceso a datos.
- Flask-Migrate para migraciones.
- Flask-JWT-Extended para autenticación por tokens.

El punto de entrada del proyecto es [run.py](run.py), que arranca la API en modo desarrollo.

## 4. Estructura de carpetas

La organización del proyecto es la siguiente:

- [app/](app/) contiene la lógica principal.
- [app/models.py](app/models.py) define las entidades ORM.
- [app/routes/](app/routes/) agrupa los endpoints REST por módulo.
- [app/utils.py](app/utils.py) incluye utilidades de seguridad y autorización.
- [migrations/](migrations/) almacena las migraciones de base de datos.
- [scripts/](scripts/) contiene utilidades de apoyo, como carga de datos.
- [tests/](tests/) reúne las pruebas del proyecto.
- [docs/](docs/) centraliza la documentación funcional y técnica.

## 5. Modelo de datos

El modelo de datos refleja las entidades clave del dominio del gimnasio:

- Usuario: clientes registrados en el sistema.
- Empleado: personal interno, con rol asociado.
- Sala: espacios donde se realizan actividades.
- Horario: franjas horarias para la planificación.
- Actividad: clases o servicios del gimnasio.
- Reserva: inscripción de un usuario a una actividad.
- Pago: registro de cobros realizados por los usuarios.
- Material: inventario o equipamiento asignado a salas.
- Incidencia: reporte de fallos o problemas relacionados con materiales o mantenimiento.

Relaciones principales:

- Un usuario puede tener muchas reservas y muchos pagos.
- Un empleado puede monitorizar muchas actividades.
- Una sala puede contener muchas actividades y materiales.
- Un horario puede asociarse a varias actividades.
- Una actividad puede recibir muchas reservas.
- Un material puede tener incidencias asociadas.

## 6. Módulos del backend

### 6.1 Autenticación

El módulo [app/routes/auth.py](app/routes/auth.py) gestiona el acceso al sistema.

Funciones principales:

- Registro de usuarios en `/auth/register`.
- Login de usuarios en `/auth/login`.
- Registro de empleados en `/auth/register-empleado`.
- Login de empleados en `/auth/login-empleado`.

En los logins se genera un token JWT con el rol incluido en los claims, lo que permite aplicar control de acceso en las rutas protegidas.

### 6.2 Usuarios

El módulo [app/routes/usuarios.py](app/routes/usuarios.py) permite administrar los clientes del gimnasio.

Funciones principales:

- Listado de usuarios, restringido a admin.
- Consulta del perfil propio.
- Actualización de datos del usuario.
- Eliminación de usuarios, restringida a admin.

### 6.3 Empleados

El módulo [app/routes/empleados.py](app/routes/empleados.py) administra el personal interno.

Funciones principales:

- Listar empleados.
- Crear empleados.
- Actualizar empleados.
- Eliminar empleados.

Estas operaciones están protegidas y requieren rol admin.

### 6.4 Gimnasio

El módulo [app/routes/gym.py](app/routes/gym.py) agrupa la gestión de actividades, salas y horarios.

Funciones principales:

- Consultar actividades, salas y horarios de forma pública.
- Crear, actualizar y eliminar actividades.
- Crear, actualizar y eliminar salas.
- Crear horarios.

Las operaciones de escritura están protegidas y suelen quedar reservadas a admin.

### 6.5 Reservas

El módulo [app/routes/reservas.py](app/routes/reservas.py) controla el flujo de inscripción a actividades.

Funciones principales:

- Crear una reserva autenticada.
- Consultar las reservas del usuario actual.
- Cancelar una reserva propia.
- Actualizar el estado de una reserva.

La reserva valida que la actividad exista y que no se supere el aforo máximo.

### 6.6 Pagos

El módulo [app/routes/pagos.py](app/routes/pagos.py) registra y consulta pagos de usuarios.

Funciones principales:

- Registrar un pago.
- Consultar historial de pagos del usuario autenticado.
- Actualizar un pago.
- Eliminar un pago.

### 6.7 Mantenimiento

El módulo [app/routes/mantenimiento.py](app/routes/mantenimiento.py) cubre inventario e incidencias.

Funciones principales:

- Listar materiales.
- Crear, actualizar y eliminar materiales.
- Reportar incidencias.
- Listar incidencias.
- Actualizar incidencias.

Los reportes de incidencias pueden ser generados por usuarios autenticados, mientras que la consulta global y la administración quedan restringidas a admin.

## 7. Seguridad y control de acceso

La seguridad del proyecto se apoya en JWT y en decoradores de autorización. El sistema distingue, al menos, estos roles:

- cliente.
- monitor.
- admin.

En [app/utils.py](app/utils.py) se implementan las validaciones de rol para proteger las rutas que no deben estar disponibles para cualquier usuario.

Reglas generales:

- Las rutas públicas permiten consultar información general como actividades, salas y horarios.
- Las rutas protegidas requieren token JWT.
- Las rutas administrativas exigen rol admin.
- Algunas acciones permiten monitor o admin, según el caso de uso.

## 8. Base de datos y persistencia

El proyecto usa MySQL como motor de persistencia. La conexión se configura desde [config.py](config.py) mediante variables de entorno, lo que permite adaptar el entorno local, Docker o producción sin cambiar el código.

También existen migraciones en [migrations/](migrations/) para evolucionar el esquema de forma controlada.

## 9. Ejecución local

Flujo básico para levantar el proyecto:

1. Arrancar MySQL con Docker.
2. Configurar las variables de entorno en `.env`.
3. Activar el entorno virtual de Python.
4. Ejecutar [run.py](run.py).

La documentación principal del proyecto está resumida en [README.md](README.md), pero este archivo sirve como explicación rápida de la rama Yeremi para el resto del equipo.

## 10. Valor de la rama Yeremi

Esta rama deja preparado el backend con una base funcional para el trabajo colaborativo: entidades principales, endpoints REST, autenticación JWT, protección por roles y una estructura modular que facilita seguir desarrollando el sistema sin mezclar responsabilidades.

En resumen, el proyecto ya cubre la operativa esencial de un gimnasio moderno y sirve como base para seguir ampliando funciones, endurecer la seguridad, añadir pruebas y pulir la documentación técnica.

## 11. Endpoints principales por módulo

Para facilitar la lectura del proyecto por parte del equipo, esta sección resume las rutas más importantes y el tipo de acceso que requieren.

### 11.1 Autenticación

- `POST /auth/register`: registra un usuario cliente.
- `POST /auth/login`: inicia sesión de un usuario cliente y devuelve un JWT.
- `POST /auth/register-empleado`: registra un empleado.
- `POST /auth/login-empleado`: inicia sesión de un empleado y devuelve un JWT con su rol.

Uso esperado:

- El cliente se registra primero y luego inicia sesión para obtener su token.
- El personal interno usa el flujo de empleado para acceder como monitor o admin.

### 11.2 Usuarios

- `GET /usuarios/`: lista usuarios, solo admin.
- `GET /usuarios/perfil`: devuelve el perfil del usuario autenticado.
- `PUT /usuarios/<id>`: actualiza un perfil; el propio usuario puede editarse y un monitor o admin puede intervenir según el caso.
- `DELETE /usuarios/<id>`: elimina un usuario, solo admin.

### 11.3 Empleados

- `GET /empleados/`: lista empleados, solo admin.
- `POST /empleados/`: crea un empleado, solo admin.
- `PUT /empleados/<id>`: actualiza un empleado, solo admin.
- `DELETE /empleados/<id>`: elimina un empleado, solo admin.

### 11.4 Gimnasio

- `GET /gym/actividades`: lista actividades públicas.
- `POST /gym/actividades`: crea una actividad, solo admin.
- `PUT /gym/actividades/<id>`: actualiza una actividad, solo admin.
- `DELETE /gym/actividades/<id>`: elimina una actividad, solo admin.
- `GET /gym/salas`: lista salas públicas.
- `POST /gym/salas`: crea una sala, solo admin.
- `PUT /gym/salas/<id>`: actualiza una sala, solo admin.
- `DELETE /gym/salas/<id>`: elimina una sala, solo admin.
- `GET /gym/horarios`: lista horarios públicos.
- `POST /gym/horarios`: crea un horario, solo admin.

### 11.5 Reservas

- `POST /reservas/`: crea una reserva para el usuario autenticado.
- `GET /reservas/mis-reservas`: muestra las reservas del usuario autenticado.
- `DELETE /reservas/<id>`: cancela una reserva propia.
- `PUT /reservas/<id>`: actualiza el estado de una reserva.

Regla importante:

- Antes de reservar, el sistema verifica que exista la actividad y que no se haya superado el aforo máximo.

### 11.6 Pagos

- `POST /pagos/`: registra un pago del usuario autenticado.
- `GET /pagos/historial`: muestra el historial de pagos del usuario autenticado.
- `PUT /pagos/<id>`: actualiza un pago.
- `DELETE /pagos/<id>`: elimina un pago.

### 11.7 Mantenimiento

- `GET /mantenimiento/materiales`: lista materiales públicos.
- `POST /mantenimiento/materiales`: crea un material, solo admin.
- `PUT /mantenimiento/materiales/<id>`: actualiza un material, solo admin.
- `DELETE /mantenimiento/materiales/<id>`: elimina un material, solo admin.
- `POST /mantenimiento/incidencias`: reporta una incidencia con usuario autenticado.
- `GET /mantenimiento/incidencias`: lista incidencias, solo admin.
- `PUT /mantenimiento/incidencias/<id>`: actualiza una incidencia, solo admin.

## 12. Flujo de uso recomendado

Un flujo normal de trabajo dentro del sistema sería este:

1. Se registra un usuario cliente o un empleado.
2. El usuario inicia sesión y obtiene su token JWT.
3. El usuario consulta actividades, salas y horarios disponibles.
4. El usuario crea una reserva sobre una actividad disponible.
5. El usuario registra un pago o consulta su historial.
6. Si detecta un problema, reporta una incidencia de mantenimiento.
7. El admin revisa usuarios, empleados, reservas, pagos, materiales e incidencias desde las rutas protegidas.

## 13. Observaciones para el equipo

Hay algunos puntos importantes que conviene tener presentes al continuar desarrollando la rama:

- Los listados públicos sirven para mostrar información general sin obligar a autenticación.
- Las rutas con escritura deben mantenerse protegidas para evitar modificaciones no autorizadas.
- Las validaciones de aforo en reservas son importantes para no sobrepasar la capacidad de una actividad.
- El sistema ya está preparado para crecer hacia una capa más completa de administración, pero todavía puede ampliarse con validaciones, paginación, pruebas y control más fino de permisos.

Con esta información, cualquier miembro del equipo puede entender la función de la rama Yeremi tanto a nivel conceptual como a nivel de uso real de la API.
