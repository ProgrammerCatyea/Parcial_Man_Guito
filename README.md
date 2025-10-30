 # Man_Guito – Sistema de Gestión de Proyectos y Asignaciones

API REST desarrollada con **FastAPI** y **SQLAlchemy** para la gestión integral de proyectos, miembros y asignaciones dentro de una organización.  
El sistema permite registrar empleados, crear proyectos, asignar roles, generar reportes y mantener un control eficiente del trabajo en equipo.

---

## Características principales

- Gestión completa de **miembros**, **proyectos** y **asignaciones** (crear, listar, actualizar, eliminar).  
- Relaciones entre entidades:
  - **1:N** entre miembros y proyectos (un gerente puede gestionar varios proyectos).
  - **N:M** entre miembros y proyectos mediante la tabla intermedia `Asignaciones`.
- **Validaciones automáticas** con Pydantic (formatos, tipos de datos, campos obligatorios).  
- **Eliminación lógica** mediante cambio de estado a “Eliminado”.  
- **Reportes automáticos** en formato `.txt` con las asignaciones activas.  
- **Filtros personalizados**:
  - Miembros por estado o especialidad.
  - Proyectos por estado o presupuesto mínimo.  
- **Control de errores HTTP** estandarizado (404, 400, 422, 500).  

---

## Tecnologías utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pydantic

---

## Instalación y ejecución

### 1. Clonar el repositorio
```
git clone https://github.com/NicolasLozano/Man_Guito.git
cd Man_Guito
```

### 2. Crear y activar entorno virtual
```
python -m venv venv
```

#### En Linux / macOS
```
source venv/bin/activate
```

#### En Windows
```
venv\Scripts\activate
```

### 3. Instalar dependencias
```
pip install -r requirements.txt
```

### 4. Ejecutar el servidor
```
uvicorn app.main:app --reload
```

### 5. Acceder a la documentación interactiva

Swagger UI → http://127.0.0.1:8000/docs  
Redoc → http://127.0.0.1:8000/redoc  

---

## Estructura del proyecto
```
Parcial_Man_Guito/
│
├── app/
│   ├── main.py                # Configuración principal y registro de rutas
│   ├── core/
│   │   ├── config.py          # Variables de entorno y configuración global
│   │   ├── database.py        # Conexión y sesión de base de datos SQLite
│   ├── models/                # Modelos SQLAlchemy
│   ├── schemas/               # Modelos Pydantic
│   ├── crud/                  # Lógica CRUD
│   ├── routes/                # Endpoints (Miembros, Proyectos, Asignaciones)
│
├── frontend/                  # Archivos HTML, CSS y JS conectados al backend
├── reportes/                  # Reportes generados en formato .txt
├── parcial_manguito.db        # Base de datos SQLite
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación
```

---

## Mapa de Endpoints

### Miembros
| Método | Endpoint | Descripción |
| :------ | :-------- | :------------ |
| `GET` | `/miembros/` | Lista todos los miembros (filtro por estado o especialidad). |
| `POST` | `/miembros/` | Crea un nuevo miembro. |
| `PUT` | `/miembros/{miembro_id}` | Actualiza los datos de un miembro. |
| `DELETE` | `/miembros/{miembro_id}` | Elimina un miembro (lógica, no física). |
| `GET` | `/miembros/eliminados` | Lista los miembros eliminados. |

---

### Proyectos
| Método | Endpoint | Descripción |
| :------ | :-------- | :------------ |
| `GET` | `/proyectos/` | Lista los proyectos activos (filtro por estado o presupuesto). |
| `POST` | `/proyectos/` | Crea un nuevo proyecto. |
| `PUT` | `/proyectos/{proyecto_id}` | Actualiza los datos de un proyecto. |
| `DELETE` | `/proyectos/{proyecto_id}` | Marca un proyecto como eliminado. |
| `GET` | `/proyectos/eliminados` | Lista los proyectos eliminados. |

---

### Asignaciones
| Método | Endpoint | Descripción |
| :------ | :-------- | :------------ |
| `GET` | `/asignaciones/` | Lista todas las asignaciones activas. |
| `POST` | `/asignaciones/` | Crea una nueva asignación entre miembro y proyecto. |
| `PUT` | `/asignaciones/{asignacion_id}` | Actualiza una asignación existente. |
| `DELETE` | `/asignaciones/{asignacion_id}` | Elimina una asignación. |
| `GET` | `/asignaciones/reporte` | Genera y descarga un archivo `.txt` con todas las asignaciones. |

---

## Ejemplos de cuerpos JSON

### Crear Miembro (POST /miembros)
```
{
  "nombre": "Laura Tovar",
  "especialidad": "Backend",
  "estado": "Activo"
}
```

### Crear Proyecto (POST /proyectos)
```
{
  "nombre": "Sistema de Inventario",
  "descripcion": "Proyecto para gestionar inventarios empresariales",
  "estado": "Activo",
  "presupuesto": 2500000,
  "fecha_inicio": "2025-10-30",
  "fecha_fin": "2026-02-28",
  "id_gerente": 1
}
```

### Crear Asignación (POST /asignaciones)
```
{
  "id_proyecto": 1,
  "id_miembro": 2,
  "rol": "Desarrollador Backend",
  "fecha_asignacion": "2025-10-30"
}
```

---

## Estado actual

- CRUD completo y funcional para miembros, proyectos y asignaciones.  
- Reglas de negocio implementadas.  
- Filtros activos y operativos en endpoints.  
- Base de datos funcional y validada.  
- Frontend conectado correctamente al backend.  
- Documentación automática disponible en `/docs`.  

---

## Autor

**Nicolás Lozano Díaz**  
Proyecto académico desarrollado para la materia **Desarrollo de Software**.  
Repositorio GitHub: [https://github.com/ProgrammerCatyea/Parcial_Man_Guito.git](https://github.com/ProgrammerCatyea/Parcial_Man_Guito.git)




