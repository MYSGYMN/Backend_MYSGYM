# Documentación del Diseño de Base de Datos — MYSGYM

Este documento describe el diseño relacional, la estructura de las entidades y el proceso de normalización aplicado a la base de datos del sistema MYSGYM.

## 1. Modelo Relacional y Entidades

El sistema se compone de 9 entidades principales interconectadas para cubrir toda la operativa del gimnasio.

### Entidades Nucleares:
- **Usuarios (Socios):** Registra a las personas que utilizan el gimnasio.
- **Empleados:** Gestiona al personal (monitores, recepcionistas, administradores).
- **Salas:** Define los espacios físicos disponibles.

### Entidades de Operación:
- **Actividades:** Relaciona una actividad con un monitor, una sala y un horario.
- **Horarios:** Define las franjas temporales para las actividades.
- **Reservas:** Vincula a los usuarios con las actividades en las que se inscriben.

### Entidades de Soporte y Control:
- **Pagos:** Registro financiero de las cuotas de los socios.
- **Materiales:** Inventario de equipo deportivo.
- **Incidencias:** Control de averías o problemas reportados por el personal.

---

## 2. Normalización

Se ha aplicado el proceso de normalización hasta la **Tercera Forma Normal (3FN)** para garantizar la integridad de los datos y evitar redundancias.

### Primera Forma Normal (1FN)
- Todas las tablas tienen una **Clave Primaria (PK)** única (`id_...`).
- Los atributos son atómicos (por ejemplo, el `nombre` no contiene listas de valores).
- No hay grupos repetitivos.

### Segunda Forma Normal (2FN)
- El sistema cumple con la 1FN.
- Todos los atributos que no forman parte de la clave primaria dependen funcionalmente de la clave completa. 
- *Ejemplo:* En la tabla `actividades`, el nombre de la actividad depende del `id_actividad`, no de una parte de la clave.

### Tercera Forma Normal (3FN)
- El sistema cumple con la 2FN.
- No existen dependencias transitivas. Los atributos no clave dependen únicamente de la clave primaria.
- *Ejemplo:* En lugar de guardar el nombre de la sala dentro de la tabla `actividades`, guardamos el `sala_id`. Así, si el nombre de una sala cambia, solo se actualiza en la tabla `salas`, manteniendo la integridad.

---

## 3. Integridad y Seguridad

### Claves Foráneas (FK)
Se han implementado restricciones de integridad referencial:
- **ON DELETE CASCADE:** Aplicado en `reservas` y `pagos`. Si un usuario es eliminado, sus registros asociados desaparecen para evitar datos huérfanos.
- **ON DELETE SET NULL:** Aplicado en `actividades` e `incidencias`. Si un monitor o un material se elimina, la actividad o incidencia permanece pero el campo queda vacío para mantener el historial.

### Índices
Se han creado índices en columnas de búsqueda frecuente para mejorar el rendimiento de la API:
- `usuarios.email`
- `empleados.email`
- `actividades.nombre`
- `reservas.fecha_reserva`

### Permisos
Se ha definido un usuario de base de datos (`gym_app`) con permisos restringidos (DML: SELECT, INSERT, UPDATE, DELETE) para evitar que la aplicación web pueda realizar cambios estructurales (DDL) de forma accidental o malintencionada.
