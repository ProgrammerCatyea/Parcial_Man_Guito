# Sistema de Gestión de Proyectos – Man_Guito

API REST desarrollada con **FastAPI** y **SQLAlchemy** para la gestión completa de proyectos, empleados y asignaciones.  
Permite registrar miembros, crear proyectos, asignar empleados, generar reportes y mantener la trazabilidad de todos los procesos de una empresa.

---

## Características principales

- **Gestión completa** de miembros, proyectos y asignaciones (crear, listar, actualizar y eliminar).
- **Relaciones uno a muchos (1:N)** entre proyectos y miembros (gerentes).
- **Relaciones muchos a muchos (N:M)** entre proyectos y miembros mediante la tabla *Asignaciones*.
- **Validaciones automáticas** mediante Pydantic para campos, tipos de datos y restricciones.
- **Eliminación lógica** de registros (mantiene historial y evita pérdida de información).
- **Generación de reportes automáticos** en formato `.txt` con las asignaciones activas.
- **Control de errores HTTP** estandarizado (`404`, `400`, `422`, `500`).
- **Filtros avanzados** para buscar miembros por especialidad o estado, y proyectos por presupuesto o estado.

---

## Reglas de negocio integradas

1. Un **miembro que sea gerente** no puede ser eliminado mientras tenga proyectos activos.  
2. Los **proyectos eliminados** se mantienen en la base de datos con estado `"Eliminado"`.  
3. No se permite **asignar un miembro a un proyecto duplicado**.  
4. Solo los **proyectos activos** pueden recibir nuevas asignaciones.  
5. Cada **miembro** puede estar asignado a múltiples proyectos, pero no como gerente en más de uno simultáneamente.  

---

## Tecnologías usadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic

---

## Instalación y ejecución
---
### 1. Clonar el repositorio
git clone https://github.com/tu-usuario/Man_Guito.git
cd Man_Guito
---
2. Crear y activar entorno virtual
python -m venv venv
# Linux/MacOS
source venv/bin/activate
# Windows
venv\Scripts\activate
---
3. Instalar dependencias
pip install -r requirements.txt

---
5. Ejecutar el servidor
bash
Copiar código
uvicorn app.main:app --reload
6. Acceder a la documentación interactiva
Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc

Estructura del proyecto
bash
Copiar código
Man_Guito/
│
├── app/
│   ├── main.py                 # Configuración principal de la app y routers
│   ├── core/
│   │   ├── config.py           # Configuración de entorno
│   │   ├── database.py         # Conexión a la base de datos SQLite
│   ├── models/                 # Modelos SQLAlchemy
│   ├── schemas/                # Modelos Pydantic
│   ├── crud/                   # Lógica de base de datos
│   ├── routes/                 # Endpoints organizados
│
├── frontend/                   # Interfaz HTML + JS
├── reportes_generados/         # Carpeta donde se guardan los reportes .txt
├── requirements.txt            # Dependencias del proyecto
├── parcial_manguito.db         # Base de datos SQLite
└── README.md                   # Documentación del proyecto
Mapa de Endpoints
Miembros
Método	Endpoint	Descripción
GET	/miembros/	Lista todos los miembros con filtros por estado o especialidad
POST	/miembros/	Crea un nuevo miembro
PUT	/miembros/{miembro_id}	Actualiza los datos de un miembro existente
DELETE	/miembros/{miembro_id}	Elimina un miembro (lógica)
GET	/miembros/eliminados	Lista los miembros eliminados

Proyectos
Método	Endpoint	Descripción
GET	/proyectos/	Lista todos los proyectos con filtros por estado o presupuesto
POST	/proyectos/	Crea un nuevo proyecto
PUT	/proyectos/{proyecto_id}	Actualiza un proyecto existente
DELETE	/proyectos/{proyecto_id}	Marca un proyecto como eliminado
GET	/proyectos/eliminados	Lista los proyectos eliminados

Asignaciones
Método	Endpoint	Descripción
GET	/asignaciones/	Lista todas las asignaciones
POST	/asignaciones/	Crea una nueva asignación entre miembro y proyecto
PUT	/asignaciones/{asignacion_id}	Actualiza una asignación existente
DELETE	/asignaciones/{asignacion_id}	Elimina una asignación
GET	/asignaciones/reporte	Genera un reporte .txt con todas las asignaciones activas

Ejemplos de cuerpos JSON
Crear Miembro (POST /miembros)

json
Copiar código
{
  "nombre": "Laura Tovar",
  "especialidad": "Backend",
  "estado": "Activo"
}
Crear Proyecto (POST /proyectos)

json
Copiar código
{
  "nombre": "Sistema de Inventario",
  "descripcion": "Proyecto para controlar existencias de productos",
  "estado": "Activo",
  "presupuesto": 2000000,
  "fecha_inicio": "2025-10-30",
  "fecha_fin": "2026-02-28",
  "id_gerente": 1
}
Crear Asignación (POST /asignaciones)

json
Copiar código
{
  "id_proyecto": 1,
  "id_miembro": 2,
  "rol": "Desarrollador Backend",
  "fecha_asignacion": "2025-10-30"
}
Estado actual
CRUD completo para miembros, proyectos y asignaciones.

Reglas de negocio implementadas.

Filtros activos en endpoints.

Base de datos SQLite funcional y validada.

Documentación automática accesible desde /docs.

Frontend funcional enlazado con los endpoints del backend.

Autor
Nicolás Lozano Díaz
Proyecto desarrollado para el curso de Desarrollo de Software.
Repositorio GitHub: https://github.com/NicolasLozano/Man_Guito


