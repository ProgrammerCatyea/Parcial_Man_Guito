# MAN_GUITO - TU AYUDANTE Y GESTOR

Sistema de **gestión de proyectos y empleados** desarrollado con **FastAPI**, **SQLite** y **SQLAlchemy**, que permite administrar proyectos, miembros, asignaciones y generar reportes automáticos.

---

##  Características Principales

- **Gestión de Miembros (Empleados):**
  - Crear, listar, filtrar, actualizar y eliminar miembros.
  - Filtros por estado y especialidad.
  - Restricción: un gerente activo no puede ser eliminado.

- **Gestión de Proyectos:**
  - Crear, listar, filtrar, actualizar y eliminar proyectos.
  - Filtros por estado y rango de presupuesto.
  - Restricción: un proyecto solo puede tener un gerente asignado.

- **Asignaciones:**
  - Asignar miembros a proyectos (relación N:M).
  - Evita duplicados (no se puede asignar dos veces al mismo proyecto).
  - Permite desasignar miembros fácilmente.

- **Reportes automáticos:**
  - Generación y descarga automática de reportes `.txt` con los proyectos y miembros eliminados.

- **Eliminados visibles:**
  - Los elementos eliminados se conservan y se pueden consultar desde el sistema.

---

## Estructura del Proyecto


